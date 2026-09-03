#!/usr/bin/env python3
"""Predeclared compatibility test for Reviewer 2, Comment 2.

The frozen design is documented in
Rev/docs/analysis-spec-reviewer-2-comment-2.md. This script compares the
current event rainfall-loading index with a JMA-type Level-4 criterion
utilization ratio and writes auditable revision-only outputs. It does not
modify manuscript or publication figure/table files.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "Rev/docs/analysis-spec-reviewer-2-comment-2.md"
HOURLY = ROOT / "data/processed/jma_hourly_rainfall_preprocessed.parquet"
EVENTS = ROOT / "data/processed/jma_rainfall_event_maxima_preprocessed.parquet"
SCENARIOS = ROOT / "data/processed/jma_rainfall_scenario_quantiles_preprocessed.parquet"
FACTORS = ROOT / "data/exp/acquisition-audit/official_threshold_factors.csv"
NORMAL = ROOT / (
    "data/raw/official_reference/2026_event/jma_thresholds/"
    "jma_kumamoto_level4_landslide_normal_20260903.csv"
)
TEMPORARY = ROOT / (
    "data/raw/official_reference/2026_event/jma_thresholds/"
    "jma_kumamoto_level4_landslide_temporary_20260903.csv"
)
SECOND_REPORT = ROOT / (
    "data/raw/official_reference/2026_event/"
    "mlit_jma_temporary_landslide_warning_thresholds_second_report_20260730.pdf"
)
SOIL_INDEX_SOURCE = ROOT / (
    "data/raw/official_reference/2026_event/jma_thresholds/"
    "jma_soil_water_index_definition_20260903.html"
)
OUT = ROOT / "data/exp/revision/reviewer-2-comment-2"

CENTRAL_SUPPORT = "Central: 7 stations, 2016-2020"
WINDOWS = (1, 3, 24, 72)
SCENARIO_QUANTILES = {"Moderate": 0.75, "Heavy": 0.90, "Extreme": 0.99}
BOOTSTRAP_SEED = 20260903
BOOTSTRAP_REPLICATES = 2_000

# Explicit station-to-warning-area assignment. Yatsushiro station is in the
# western subarea. These labels match the official criterion CSV.
STATION_AREAS = {
    "kikuchi": "菊池市",
    "kosa": "甲佐町",
    "kumamoto": "熊本市",
    "matsushima": "上天草市",
    "misumi": "宇城市",
    "takamori": "高森町",
    "yatsushiro": "八代市西部",
}

# JMA national three-tank parameters. Units are mm and 1/hour; calculation
# step is 10 minutes (1/6 hour).
L1, L2, L3, L4 = 15.0, 60.0, 15.0, 15.0
A1, A2, A3, A4 = 0.10, 0.15, 0.05, 0.01
B1, B2, B3 = 0.12, 0.05, 0.01
DT_HOURS = 1.0 / 6.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_criterion(path: Path) -> tuple[str, pd.DataFrame]:
    metadata = path.read_text(encoding="cp932").splitlines()[0]
    frame = pd.read_csv(path, encoding="cp932", skiprows=1, dtype={"格子番号": "string"})
    rainfall_columns: dict[str, int] = {}
    for column in frame.columns:
        label = str(column)
        if label.startswith("60分雨量") and label.endswith("ミリの時の土壌雨量指数"):
            rainfall_columns[column] = int(label.removeprefix("60分雨量").removesuffix("ミリの時の土壌雨量指数"))
    if sorted(rainfall_columns.values()) != list(range(151)):
        raise RuntimeError(f"Unexpected rainfall columns in {path}")
    frame = frame.rename(
        columns={
            "二次細分区域コ－ド": "area_code",
            "市町村等": "area_name",
            "格子番号": "mesh_code",
            **{column: f"threshold_{rainfall}" for column, rainfall in rainfall_columns.items()},
        }
    )
    for rainfall in range(151):
        column = f"threshold_{rainfall}"
        frame[column] = pd.to_numeric(frame[column].replace("－", np.nan), errors="coerce")
    frame["mesh_code"] = frame["mesh_code"].astype("string").str.zfill(8)
    return metadata, frame


def mesh_center(code: str) -> tuple[float, float]:
    """Decode an 8-digit Japanese third-level mesh code to its cell centre."""
    if len(code) != 8 or not code.isdigit():
        return np.nan, np.nan
    p, q = int(code[:2]), int(code[2:4])
    r, s, t, u = (int(code[index]) for index in range(4, 8))
    south = p / 1.5 + r * (5.0 / 60.0) + t * (30.0 / 3600.0)
    west = 100.0 + q + s * (7.5 / 60.0) + u * (45.0 / 3600.0)
    return south + 15.0 / 3600.0, west + 22.5 / 3600.0


def criterion_curves(frame: pd.DataFrame) -> dict[str, np.ndarray]:
    columns = [f"threshold_{rainfall}" for rainfall in range(151)]
    return {
        str(mesh): values.astype(float, copy=False)
        for mesh, values in zip(
            frame["mesh_code"].astype(str), frame[columns].to_numpy(dtype=float), strict=True
        )
    }


def station_grid_matches(
    stations: pd.DataFrame, normal: pd.DataFrame, temporary: pd.DataFrame
) -> pd.DataFrame:
    joined = normal[["area_name", "mesh_code", *[f"threshold_{r}" for r in range(151)]]].merge(
        temporary[["mesh_code", *[f"threshold_{r}" for r in range(151)]]],
        on="mesh_code",
        how="inner",
        suffixes=("_normal", "_temporary"),
        validate="one_to_one",
    )
    joined = joined.copy()
    centres = joined["mesh_code"].astype(str).map(mesh_center)
    joined["grid_latitude"] = [value[0] for value in centres]
    joined["grid_longitude"] = [value[1] for value in centres]
    threshold_columns = [f"threshold_{r}_normal" for r in range(151)]
    joined["valid_count"] = joined[threshold_columns].notna().sum(axis=1)

    rows: list[dict[str, object]] = []
    for slug_value, station_name, station_latitude, station_longitude in stations.itertuples(
        index=False, name=None
    ):
        slug = str(slug_value)
        area_name = STATION_AREAS[slug]
        candidates = joined.loc[joined["area_name"].eq(area_name) & joined["valid_count"].gt(0)].copy()
        if candidates.empty:
            raise RuntimeError(f"No valid criterion grid for station {slug} in {area_name}")
        cosine = math.cos(math.radians(float(station_latitude)))
        candidates["distance_degrees"] = np.sqrt(
            ((candidates["grid_longitude"] - float(station_longitude)) * cosine) ** 2
            + (candidates["grid_latitude"] - float(station_latitude)) ** 2
        )
        best = candidates.sort_values(["distance_degrees", "mesh_code"]).iloc[0]
        rows.append(
            {
                "station_slug": slug,
                "station_name_japanese": str(station_name),
                "official_area_name": area_name,
                "station_latitude": float(station_latitude),
                "station_longitude": float(station_longitude),
                "mesh_code": str(best["mesh_code"]),
                "grid_latitude": float(best["grid_latitude"]),
                "grid_longitude": float(best["grid_longitude"]),
                "distance_km_approx": float(best["distance_degrees"] * 111.0),
                "valid_rainfall_columns": int(best["valid_count"]),
            }
        )
    return pd.DataFrame(rows)


def soil_water_index(hourly_rainfall: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Calculate end-of-hour soil-water index from hourly rainfall."""
    result = np.full(len(hourly_rainfall), np.nan, dtype=float)
    eligible = np.zeros(len(hourly_rainfall), dtype=bool)
    s1 = s2 = s3 = 0.0
    valid_streak = 0
    for index, hourly_value in enumerate(hourly_rainfall):
        if not np.isfinite(hourly_value):
            s1 = s2 = s3 = 0.0
            valid_streak = 0
            continue
        valid_streak += 1
        rain_step = max(float(hourly_value), 0.0) / 6.0
        for _ in range(6):
            q1 = A1 * max(s1 - L1, 0.0) + A2 * max(s1 - L2, 0.0)
            q2 = A3 * max(s2 - L3, 0.0)
            q3 = A4 * max(s3 - L4, 0.0)
            old1, old2, old3 = s1, s2, s3
            s1 = (1.0 - B1 * DT_HOURS) * old1 - q1 * DT_HOURS + rain_step
            s2 = (1.0 - B2 * DT_HOURS) * old2 - q2 * DT_HOURS + B1 * old1 * DT_HOURS
            s3 = (1.0 - B3 * DT_HOURS) * old3 - q3 * DT_HOURS + B2 * old2 * DT_HOURS
            s1, s2, s3 = max(s1, 0.0), max(s2, 0.0), max(s3, 0.0)
        result[index] = s1 + s2 + s3
        eligible[index] = valid_streak >= 72
    result[~eligible] = np.nan
    return result, eligible


def interpolate_threshold(curve: np.ndarray, rainfall: np.ndarray) -> np.ndarray:
    valid = np.isfinite(curve)
    output = np.full(len(rainfall), np.nan, dtype=float)
    if valid.sum() < 2:
        return output
    x = np.arange(151, dtype=float)[valid]
    y = curve[valid]
    finite = np.isfinite(rainfall)
    output[finite] = np.interp(np.clip(rainfall[finite], x.min(), x.max()), x, y)
    output[output <= 0] = np.nan
    return output


def nominal_station_factors() -> dict[str, float]:
    factors = pd.read_csv(FACTORS)
    mapping = dict(zip(factors["municipality_or_subarea"], factors["baseline_fraction"], strict=False))
    result = {slug: float(mapping.get(area, 1.0)) for slug, area in STATION_AREAS.items()}
    if not np.isclose(result["kosa"], 0.80):
        raise RuntimeError("Kosa Town must use the official 30 July 2026 factor of 0.80")
    return result


def hourly_official_indices(
    hourly: pd.DataFrame,
    matches: pd.DataFrame,
    normal_curves: dict[str, np.ndarray],
    temporary_curves: dict[str, np.ndarray],
) -> dict[str, pd.DataFrame]:
    output: dict[str, pd.DataFrame] = {}
    mesh_by_station = dict(zip(matches["station_slug"], matches["mesh_code"], strict=True))
    for slug, frame in hourly.groupby("Station Slug", sort=True):
        frame = frame.sort_values("Observation Time").drop_duplicates("Observation Time", keep="last")
        index = pd.date_range(frame["Observation Time"].min(), frame["Observation Time"].max(), freq="h")
        indexed = frame.set_index("Observation Time")
        rain = indexed["Hourly Rainfall"].where(indexed["Quality Flag"].eq(8)).reindex(index).to_numpy(dtype=float)
        swi, eligible = soil_water_index(rain)
        mesh = str(mesh_by_station[str(slug)])
        normal_threshold = interpolate_threshold(normal_curves[mesh], rain)
        temporary_threshold = interpolate_threshold(temporary_curves[mesh], rain)
        output[str(slug)] = pd.DataFrame(
            {
                "rainfall_60min_mm": rain,
                "soil_water_index": swi,
                "eligible_after_72h": eligible,
                "normal_threshold_swi": normal_threshold,
                "temporary_threshold_swi": temporary_threshold,
                "normal_utilization_ratio": swi / normal_threshold,
                "temporary_utilization_ratio": swi / temporary_threshold,
            },
            index=index,
        )
    return output


def event_comparison(
    events: pd.DataFrame,
    scenarios: pd.DataFrame,
    official: dict[str, pd.DataFrame],
    factors: dict[str, float],
) -> pd.DataFrame:
    central_scenarios = scenarios.loc[scenarios["Support Specification"].eq(CENTRAL_SUPPORT)]
    heavy = central_scenarios.loc[central_scenarios["Rainfall Scenario"].eq("Heavy")]
    references = {
        window: float(heavy[f"Scenario {window} h Rainfall"].median()) for window in WINDOWS
    }
    central_events = events.loc[events["Support Specification"].eq(CENTRAL_SUPPORT)].copy()
    rows: list[dict[str, object]] = []
    for _, event in central_events.iterrows():
        slug = str(event["Station Slug"])
        current_components = np.array(
            [float(event[f"Event Maximum {window} h Rainfall"]) / references[window] for window in WINDOWS],
            dtype=float,
        )
        current_baseline = float(np.mean(current_components)) if np.isfinite(current_components).all() else np.nan
        current_adjusted = current_baseline / factors[slug] if np.isfinite(current_baseline) else np.nan
        station_hourly = official[slug]
        start = event["Event Start"]
        end = event["Event End"]
        primary = station_hourly.loc[start:end]
        sensitivity = station_hourly.loc[start : end + pd.Timedelta(hours=6)]
        rows.append(
            {
                "rainfall_event_id": str(event["Rainfall Event ID"]),
                "station_slug": slug,
                "station_name_japanese": str(event["Station Name (Japanese)"]),
                "event_start": start,
                "event_end": end,
                "event_wet_hour_count": int(event["Event Wet Hour Count"]),
                "nominal_retention_factor": factors[slug],
                "current_index_baseline": current_baseline,
                "current_index_adjusted": current_adjusted,
                "jma_normal_utilization_max": primary["normal_utilization_ratio"].max(skipna=True),
                "jma_temporary_utilization_max": primary["temporary_utilization_ratio"].max(skipna=True),
                "jma_temporary_utilization_max_plus6h": sensitivity["temporary_utilization_ratio"].max(skipna=True),
                "eligible_official_hours": int(primary["temporary_utilization_ratio"].notna().sum()),
            }
        )
    result = pd.DataFrame(rows)
    for column in [
        "jma_normal_utilization_max",
        "jma_temporary_utilization_max",
        "jma_temporary_utilization_max_plus6h",
    ]:
        result.loc[~np.isfinite(result[column]), column] = np.nan
    return result


def safe_spearman(x: pd.Series, y: pd.Series) -> float:
    valid = x.notna() & y.notna()
    if valid.sum() < 3 or x[valid].nunique() < 2 or y[valid].nunique() < 2:
        return np.nan
    return float(spearmanr(x[valid], y[valid]).statistic)


def top_decile_metrics(frame: pd.DataFrame, comparator: str) -> tuple[float, float, pd.DataFrame]:
    working = frame.dropna(subset=["current_index_adjusted", comparator]).copy()
    station_rows: list[dict[str, object]] = []
    targets = pd.Series(False, index=working.index)
    predicted_top = pd.Series(False, index=working.index)
    for slug, station in working.groupby("station_slug", sort=True):
        official_cut = station[comparator].quantile(0.90)
        current_cut = station["current_index_adjusted"].quantile(0.90)
        official_top = station[comparator].ge(official_cut)
        current_top = station["current_index_adjusted"].ge(current_cut)
        targets.loc[station.index] = official_top
        predicted_top.loc[station.index] = current_top
        denominator = min(int(official_top.sum()), int(current_top.sum()))
        overlap = int((official_top & current_top).sum()) / denominator if denominator else np.nan
        station_rows.append(
            {
                "station_slug": slug,
                "eligible_events": len(station),
                "official_top_decile_events": int(official_top.sum()),
                "current_top_decile_events": int(current_top.sum()),
                "top_decile_overlap_coefficient": overlap,
            }
        )
    auc = float(roc_auc_score(targets.astype(int), working["current_index_adjusted"]))
    station_summary = pd.DataFrame(station_rows)
    return auc, float(station_summary["top_decile_overlap_coefficient"].median()), station_summary


def cluster_bootstrap_spearman(frame: pd.DataFrame, comparator: str) -> tuple[float, float, float]:
    working = frame.dropna(subset=["current_index_adjusted", comparator]).copy()
    stations = np.array(sorted(working["station_slug"].unique()))
    observed = safe_spearman(working["current_index_adjusted"], working[comparator])
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    values: list[float] = []
    groups = {slug: working.loc[working["station_slug"].eq(slug)] for slug in stations}
    for _ in range(BOOTSTRAP_REPLICATES):
        sample = rng.choice(stations, size=len(stations), replace=True)
        resampled = pd.concat([groups[str(slug)] for slug in sample], ignore_index=True)
        value = safe_spearman(resampled["current_index_adjusted"], resampled[comparator])
        if np.isfinite(value):
            values.append(value)
    lower, upper = np.quantile(values, [0.025, 0.975])
    return observed, float(lower), float(upper)


def scenario_comparison(events: pd.DataFrame, comparator: str) -> tuple[pd.DataFrame, float, int]:
    eligible = events.dropna(subset=["current_index_adjusted", comparator]).copy()
    rows: list[dict[str, object]] = []
    for slug, station in eligible.groupby("station_slug", sort=True):
        for scenario, quantile in SCENARIO_QUANTILES.items():
            rows.append(
                {
                    "station_slug": slug,
                    "scenario": scenario,
                    "quantile": quantile,
                    "current_index_quantile": float(station["current_index_adjusted"].quantile(quantile)),
                    "jma_type_quantile": float(station[comparator].quantile(quantile)),
                }
            )
    result = pd.DataFrame(rows)
    rho = safe_spearman(result["current_index_quantile"], result["jma_type_quantile"])
    inversions = 0
    ordered_names = list(SCENARIO_QUANTILES)
    for _, station in result.groupby("station_slug", sort=True):
        station = station.set_index("scenario").reindex(ordered_names)
        for column in ["current_index_quantile", "jma_type_quantile"]:
            if not np.all(np.diff(station[column].to_numpy(dtype=float)) > 0):
                inversions += 1
    return result, rho, inversions


def transformation_fidelity(
    normal: pd.DataFrame, temporary: pd.DataFrame, factors: pd.DataFrame
) -> tuple[pd.DataFrame, dict[str, float]]:
    factor_map = dict(zip(factors["municipality_or_subarea"], factors["baseline_fraction"], strict=False))
    merged = normal.merge(temporary, on=["area_name", "mesh_code"], suffixes=("_normal", "_temporary"))
    rows: list[pd.DataFrame] = []
    for area, frame in merged.groupby("area_name", sort=True):
        factor = factor_map.get(area)
        if factor is None or float(factor) >= 1.0:
            continue
        pieces: list[pd.DataFrame] = []
        for rainfall in range(151):
            normal_values = frame[f"threshold_{rainfall}_normal"]
            temporary_values = frame[f"threshold_{rainfall}_temporary"]
            valid = normal_values.notna() & temporary_values.notna() & temporary_values.gt(0)
            if valid.any():
                multiplier = normal_values[valid] / temporary_values[valid]
                expected = 1.0 / float(factor)
                pieces.append(
                    pd.DataFrame(
                        {
                            "area_name": area,
                            "rainfall_60min_mm": rainfall,
                            "mesh_code": frame.loc[valid, "mesh_code"].astype(str).to_numpy(),
                            "retention_factor": float(factor),
                            "observed_multiplier": multiplier.to_numpy(dtype=float),
                            "expected_multiplier": expected,
                            "absolute_relative_error": np.abs(multiplier.to_numpy(dtype=float) / expected - 1.0),
                        }
                    )
                )
        if pieces:
            rows.append(pd.concat(pieces, ignore_index=True))
    detail = pd.concat(rows, ignore_index=True)
    summary = {
        "fidelity_median_absolute_relative_error": float(detail["absolute_relative_error"].median()),
        "fidelity_p95_absolute_relative_error": float(detail["absolute_relative_error"].quantile(0.95)),
        "fidelity_valid_grid_rainfall_cells": int(len(detail)),
    }
    return detail, summary


def main() -> None:
    required = [SPEC, HOURLY, EVENTS, SCENARIOS, FACTORS, NORMAL, TEMPORARY, SECOND_REPORT, SOIL_INDEX_SOURCE]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing frozen inputs: {missing}")

    normal_metadata, normal = read_criterion(NORMAL)
    temporary_metadata, temporary = read_criterion(TEMPORARY)
    factors_frame = pd.read_csv(FACTORS)
    factors = nominal_station_factors()
    hourly = pd.read_parquet(HOURLY)
    events = pd.read_parquet(EVENTS)
    scenarios = pd.read_parquet(SCENARIOS)
    hourly = hourly.loc[hourly["Observation Time"].dt.year.between(2016, 2020)].copy()
    stations = (
        hourly[["Station Slug", "Station Name (Japanese)", "Station Latitude", "Station Longitude"]]
        .drop_duplicates()
        .sort_values("Station Slug")
    )
    if set(stations["Station Slug"]) != set(STATION_AREAS):
        raise RuntimeError("Central station inventory differs from the frozen seven-station specification")

    matches = station_grid_matches(stations, normal, temporary)
    normal_curves = criterion_curves(normal)
    temporary_curves = criterion_curves(temporary)
    official_hourly = hourly_official_indices(hourly, matches, normal_curves, temporary_curves)
    comparisons = event_comparison(events, scenarios, official_hourly, factors)
    eligible = comparisons.dropna(subset=["current_index_adjusted", "jma_temporary_utilization_max"]).copy()

    pooled_rho, bootstrap_lower, bootstrap_upper = cluster_bootstrap_spearman(
        eligible, "jma_temporary_utilization_max"
    )
    within_station = (
        eligible.groupby("station_slug", sort=True)
        .apply(
            lambda frame: pd.Series(
                {
                    "eligible_events": len(frame),
                    "spearman_rho": safe_spearman(
                        frame["current_index_adjusted"], frame["jma_temporary_utilization_max"]
                    ),
                }
            ),
            include_groups=False,
        )
        .reset_index()
    )
    auc, median_overlap, overlap_rows = top_decile_metrics(
        eligible, "jma_temporary_utilization_max"
    )
    within_station = within_station.merge(overlap_rows, on=["station_slug", "eligible_events"], how="left")
    scenario_rows, scenario_rho, inversions = scenario_comparison(
        eligible, "jma_temporary_utilization_max"
    )
    plus6_rho = safe_spearman(
        comparisons["current_index_adjusted"], comparisons["jma_temporary_utilization_max_plus6h"]
    )
    fidelity_detail, fidelity = transformation_fidelity(normal, temporary, factors_frame)

    metrics = {
        **fidelity,
        "events_total_central": int(len(comparisons)),
        "events_eligible": int(len(eligible)),
        "events_excluded": int(len(comparisons) - len(eligible)),
        "event_pooled_spearman_rho": pooled_rho,
        "event_cluster_bootstrap_lower_95": bootstrap_lower,
        "event_cluster_bootstrap_upper_95": bootstrap_upper,
        "within_station_median_spearman_rho": float(within_station["spearman_rho"].median()),
        "within_station_minimum_spearman_rho": float(within_station["spearman_rho"].min()),
        "top_decile_roc_auc": auc,
        "within_station_median_top_decile_overlap": median_overlap,
        "scenario_pooled_spearman_rho": scenario_rho,
        "scenario_order_inversions": int(inversions),
        "plus6h_sensitivity_spearman_rho": plus6_rho,
    }
    tests = [
        ("fidelity_median_error", metrics["fidelity_median_absolute_relative_error"] <= 0.02),
        ("fidelity_p95_error", metrics["fidelity_p95_absolute_relative_error"] <= 0.05),
        ("event_pooled_spearman", metrics["event_pooled_spearman_rho"] >= 0.80),
        ("event_bootstrap_lower", metrics["event_cluster_bootstrap_lower_95"] >= 0.75),
        ("station_median_spearman", metrics["within_station_median_spearman_rho"] >= 0.80),
        ("station_minimum_spearman", metrics["within_station_minimum_spearman_rho"] >= 0.60),
        ("top_decile_auc", metrics["top_decile_roc_auc"] >= 0.90),
        ("top_decile_overlap", metrics["within_station_median_top_decile_overlap"] >= 0.70),
        ("scenario_spearman", metrics["scenario_pooled_spearman_rho"] >= 0.80),
        ("scenario_order", metrics["scenario_order_inversions"] == 0),
    ]
    decision = "retain_equation_4" if all(passed for _, passed in tests) else "official_indicator_fallback"

    OUT.mkdir(parents=True, exist_ok=True)
    comparisons.to_csv(OUT / "event_indicator_comparison.csv", index=False)
    within_station.to_csv(OUT / "station_compatibility_summary.csv", index=False)
    scenario_rows.to_csv(OUT / "scenario_indicator_comparison.csv", index=False)
    matches.to_csv(OUT / "station_official_grid_matches.csv", index=False)
    fidelity_detail.to_csv(OUT / "official_factor_transformation_fidelity.csv", index=False)
    pd.DataFrame([{"metric": key, "value": value} for key, value in metrics.items()]).to_csv(
        OUT / "compatibility_metrics.csv", index=False
    )
    pd.DataFrame([{"criterion": name, "passed": passed} for name, passed in tests]).to_csv(
        OUT / "compatibility_decision_tests.csv", index=False
    )
    input_hashes = pd.DataFrame(
        [
            {"path": str(path.relative_to(ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in required
        ]
    )
    input_hashes.to_csv(OUT / "input_hashes.csv", index=False)
    decision_payload = {
        "decision_record": "KILA-D-20260903-001",
        "predeclared_spec_sha256": sha256(SPEC),
        "normal_csv_metadata": normal_metadata,
        "temporary_csv_metadata": temporary_metadata,
        "automatic_branch": decision,
        "all_primary_criteria_passed": bool(all(passed for _, passed in tests)),
        "criteria": {name: bool(passed) for name, passed in tests},
        "metrics": metrics,
    }
    (OUT / "decision.json").write_text(
        json.dumps(decision_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    report_lines = [
        "# Threshold-indicator Compatibility Report",
        "",
        "- Reviewer unit: `reviewer-2/comment-2`",
        "- Decision record: `KILA-D-20260903-001`",
        f"- Frozen specification SHA-256: `{sha256(SPEC)}`",
        f"- Normal criterion metadata: {normal_metadata}",
        f"- Temporary criterion metadata: {temporary_metadata}",
        f"- Eligible events: {len(eligible):,}/{len(comparisons):,}",
        f"- Automatic branch selected: **{decision}**",
        "",
        "## Primary metrics",
        "",
        "| Metric | Result |",
        "|---|---:|",
    ]
    for key, value in metrics.items():
        if isinstance(value, float):
            report_lines.append(f"| `{key}` | {value:.6f} |")
        else:
            report_lines.append(f"| `{key}` | {value} |")
    report_lines.extend(["", "## Decision tests", "", "| Criterion | Passed |", "|---|---:|"])
    report_lines.extend(f"| `{name}` | {'yes' if passed else 'no'} |" for name, passed in tests)
    report_lines.extend(
        [
            "",
            "## Station-grid audit",
            "",
            matches.to_markdown(index=False),
            "",
            "## Within-station audit",
            "",
            within_station.to_markdown(index=False),
            "",
            "## Interpretation boundary",
            "",
            "The comparator reproduces the published JMA tank equations and Level-4 grid curves, but distributes each archived hourly total uniformly over six 10-minute steps. It is therefore a JMA-type reconstruction for indicator compatibility, not a reconstruction of operational JMA analyzed-rainfall products.",
            "",
        ]
    )
    (OUT / "compatibility_report.md").write_text("\n".join(report_lines), encoding="utf-8")
    print(json.dumps(decision_payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
