#!/usr/bin/env python3
"""Predeclared rainfall-weight and gamma sensitivity for Reviewer 2 Comment 4."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.special import expit, logit
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score
import shapely

import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_official_threshold_adjusted_landslide_disruption_score as terrain_score
import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "Rev/docs/analysis-spec-reviewer-2-comment-4.md"
SCENARIO_PATH = ROOT / "data/processed/jma_rainfall_scenario_quantiles_preprocessed.parquet"
EVENT_PATH = ROOT / "data/processed/jma_rainfall_event_maxima_preprocessed.parquet"
THRESHOLD_PATH = ROOT / "data/processed/official_threshold_factors_preprocessed.parquet"
COMPATIBILITY_EVENTS = ROOT / (
    "data/exp/revision/reviewer-2-comment-2/event_indicator_comparison.csv"
)
OUT = ROOT / "data/exp/revision/reviewer-2-comment-4"

WEIGHT_SCHEMES: dict[str, tuple[float, float, float, float]] = {
    "equal": (0.25, 0.25, 0.25, 0.25),
    "short_gradient": (0.40, 0.30, 0.20, 0.10),
    "long_gradient": (0.10, 0.20, 0.30, 0.40),
    "one_hour_only": (1.00, 0.00, 0.00, 0.00),
    "seventy_two_hour_only": (0.00, 0.00, 0.00, 1.00),
}
GAMMAS = (0.50, 1.00, 2.00)
NETWORK_SETTINGS = (
    ("equal", 1.00),
    ("short_gradient", 0.50),
    ("short_gradient", 2.00),
    ("long_gradient", 0.50),
    ("long_gradient", 2.00),
)
SCENARIOS = ("Moderate", "Heavy", "Extreme")
WINDOWS = (1, 3, 24, 72)
CENTRAL_KEY = "equal__g1.00"
MATCH_BOOTSTRAP_SEED = 20260812
MATCH_BOOTSTRAP_REPLICATES = 2_000


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def setting_key(scheme: str, gamma: float) -> str:
    return f"{scheme}__g{gamma:.2f}"


def safe_spearman(x: np.ndarray, y: np.ndarray) -> float:
    valid = np.isfinite(x) & np.isfinite(y)
    if valid.sum() < 3 or np.unique(x[valid]).size < 2 or np.unique(y[valid]).size < 2:
        return np.nan
    return float(spearmanr(x[valid], y[valid]).statistic)


def top_overlap(reference: np.ndarray, candidate: np.ndarray, quantile: float = 0.99) -> float:
    valid = np.isfinite(reference) & np.isfinite(candidate) & ((reference > 0) | (candidate > 0))
    ref = reference[valid]
    alt = candidate[valid]
    if len(ref) < 100:
        return np.nan
    ref_top = ref >= np.quantile(ref, quantile)
    alt_top = alt >= np.quantile(alt, quantile)
    denominator = min(int(ref_top.sum()), int(alt_top.sum()))
    return float(np.sum(ref_top & alt_top) / denominator) if denominator else np.nan


def window_surfaces(
    scenario_values: pd.DataFrame,
    extent: tuple[float, float, float, float],
    shape: tuple[int, int],
) -> tuple[dict[str, dict[int, np.ndarray]], dict[int, float]]:
    central = scenario_values.loc[
        scenario_values["Support Specification"].eq(terrain_score.CENTRAL_SUPPORT)
    ].copy()
    stations = (
        central[["Station ID", "Station Latitude", "Station Longitude"]]
        .drop_duplicates()
        .sort_values("Station ID")
        .reset_index(drop=True)
    )
    if len(stations) != 7:
        raise RuntimeError("The frozen central support requires seven stations")
    west, east, south, north = extent
    rows, columns = shape
    longitude = west + (np.arange(columns) + 0.5) / columns * (east - west)
    latitude = north - (np.arange(rows) + 0.5) / rows * (north - south)
    longitude_grid, latitude_grid = np.meshgrid(longitude, latitude)
    station_longitude = stations["Station Longitude"].to_numpy(dtype=float)
    station_latitude = stations["Station Latitude"].to_numpy(dtype=float)
    cosine = np.cos(np.deg2rad(latitude_grid))[..., None]
    distance_squared = (
        ((longitude_grid[..., None] - station_longitude) * cosine) ** 2
        + (latitude_grid[..., None] - station_latitude) ** 2
        + terrain_score.DISTANCE_STABILIZER_DEGREES**2
    )
    inverse_distance = 1.0 / distance_squared
    station_weights = inverse_distance / inverse_distance.sum(axis=2, keepdims=True)
    heavy = central.loc[central["Rainfall Scenario"].eq("Heavy")]
    references = {
        window: float(heavy[f"Scenario {window} h Rainfall"].median()) for window in WINDOWS
    }
    surfaces: dict[str, dict[int, np.ndarray]] = {}
    for scenario in SCENARIOS:
        subset = (
            central.loc[central["Rainfall Scenario"].eq(scenario)]
            .set_index("Station ID")
            .reindex(stations["Station ID"])
        )
        surfaces[scenario] = {}
        for window in WINDOWS:
            ratio = subset[f"Scenario {window} h Rainfall"].to_numpy(dtype=float) / references[window]
            surfaces[scenario][window] = np.sum(
                station_weights * ratio[None, None, :], axis=2
            ).astype("float32")
    return surfaces, references


def build_factor_grid(
    admin: pd.DataFrame,
    admin_geometry: np.ndarray,
    shape: tuple[int, int],
    transform: object,
    admin_mask: np.ndarray,
) -> np.ndarray:
    threshold = pd.read_parquet(THRESHOLD_PATH)
    factors, mixed = terrain_score.threshold_categories(admin, threshold)
    factors[mixed] = 0.75
    grid = rasterize(
        ((geometry, float(factor)) for geometry, factor in zip(admin_geometry, factors, strict=True)),
        out_shape=shape,
        transform=transform,
        fill=1.0,
        all_touched=True,
        dtype="float32",
    )
    grid[~admin_mask] = np.nan
    return grid


def derive_terrain_logit(
    central_scores: dict[str, np.ndarray],
    central_loads: dict[str, np.ndarray],
    factor_grid: np.ndarray,
) -> tuple[np.ndarray, float]:
    estimates: list[np.ndarray] = []
    for scenario in SCENARIOS:
        score = central_scores[scenario].astype(float)
        loading = central_loads[scenario].astype(float) / factor_grid
        estimate = logit(np.clip(score, 1e-7, 1 - 1e-7)) - np.log(np.clip(loading, 1e-7, None))
        estimate[~np.isfinite(score)] = np.nan
        estimates.append(estimate)
    context = np.nanmedian(np.stack(estimates), axis=0).astype("float32")
    reconstructed = expit(context + np.log(np.clip(central_loads["Heavy"] / factor_grid, 1e-7, None)))
    valid = np.isfinite(central_scores["Heavy"]) & np.isfinite(reconstructed)
    error = float(np.max(np.abs(reconstructed[valid] - central_scores["Heavy"][valid])))
    return context, error


def event_weight_compatibility(references: dict[int, float]) -> pd.DataFrame:
    events = pd.read_parquet(EVENT_PATH)
    events = events.loc[events["Support Specification"].eq(terrain_score.CENTRAL_SUPPORT)].copy()
    comparator = pd.read_csv(COMPATIBILITY_EVENTS)
    comparator = comparator[["rainfall_event_id", "jma_temporary_utilization_max"]]
    events = events.merge(
        comparator,
        left_on="Rainfall Event ID",
        right_on="rainfall_event_id",
        how="inner",
        validate="one_to_one",
    )
    factor_lookup = (
        pd.read_csv(ROOT / "data/exp/revision/reviewer-2-comment-2/event_indicator_comparison.csv")
        .drop_duplicates("rainfall_event_id")
        .set_index("rainfall_event_id")["nominal_retention_factor"]
    )
    events["factor"] = events["Rainfall Event ID"].map(factor_lookup)
    rows: list[dict[str, object]] = []
    for scheme, weights in WEIGHT_SCHEMES.items():
        score = np.zeros(len(events), dtype=float)
        valid = np.ones(len(events), dtype=bool)
        for weight, window in zip(weights, WINDOWS, strict=True):
            values = events[f"Event Maximum {window} h Rainfall"].to_numpy(dtype=float)
            if weight > 0:
                valid &= np.isfinite(values)
                score += weight * values / references[window]
        score = score / events["factor"].to_numpy(dtype=float)
        official = events["jma_temporary_utilization_max"].to_numpy(dtype=float)
        valid &= np.isfinite(score) & np.isfinite(official)
        pooled = safe_spearman(score[valid], official[valid])
        station_rhos = []
        overlaps = []
        target_all: list[np.ndarray] = []
        score_all: list[np.ndarray] = []
        for _, station in events.loc[valid].assign(weighted_score=score[valid]).groupby("Station Slug"):
            station_score = station["weighted_score"].to_numpy(dtype=float)
            station_official = station["jma_temporary_utilization_max"].to_numpy(dtype=float)
            station_rhos.append(safe_spearman(station_score, station_official))
            official_top = station_official >= np.quantile(station_official, 0.90)
            score_top = station_score >= np.quantile(station_score, 0.90)
            denominator = min(int(official_top.sum()), int(score_top.sum()))
            overlaps.append(float(np.sum(official_top & score_top) / denominator))
            target_all.append(official_top.astype(int))
            score_all.append(station_score)
        rows.append(
            {
                "weight_scheme": scheme,
                "eligible_events": int(valid.sum()),
                "pooled_spearman_rho": pooled,
                "median_station_spearman_rho": float(np.median(station_rhos)),
                "minimum_station_spearman_rho": float(np.min(station_rhos)),
                "top_decile_roc_auc": float(roc_auc_score(np.concatenate(target_all), np.concatenate(score_all))),
                "median_station_top_decile_overlap": float(np.median(overlaps)),
            }
        )
    return pd.DataFrame(rows)


def evidence_sections() -> pd.Series:
    matches = pd.read_parquet(
        road_exposure.MATCH_PATH,
        columns=[
            "Restriction Observation ID",
            "Snapshot Time",
            "Restriction Reason",
            "Matched Road Edge ID",
            "Road Edge Match Distance (m)",
            "Road Edge Match Status",
        ],
    )
    reliable = (
        matches["Restriction Reason"].astype("string").str.contains(
            road_exposure.LANDSLIDE_REASON_PATTERN, na=False
        )
        & matches["Road Edge Match Status"].eq("matched_primary")
        & matches["Road Edge Match Distance (m)"].le(50)
    )
    evidence = matches.loc[reliable].drop_duplicates(
        ["Restriction Observation ID", "Snapshot Time", "Matched Road Edge ID"]
    )
    edges = pd.read_parquet(
        road_exposure.EDGE_PATH, columns=["Road Edge ID", "Road Section ID"]
    )
    linked = evidence.merge(
        edges,
        left_on="Matched Road Edge ID",
        right_on="Road Edge ID",
        how="inner",
        validate="many_to_one",
    )
    return linked["Road Section ID"].drop_duplicates()


def matched_control_design(
    roads: pd.DataFrame,
    road_geometry: np.ndarray,
    evidence_section_ids: pd.Series,
    admin_geometry: np.ndarray,
    shape: tuple[int, int],
    transform: object,
    extent: tuple[float, float, float, float],
) -> tuple[np.ndarray, list[np.ndarray], np.ndarray]:
    municipality_grid = rasterize(
        ((geometry, index + 1) for index, geometry in enumerate(admin_geometry)),
        out_shape=shape,
        transform=transform,
        fill=0,
        all_touched=True,
        dtype="int16",
    )
    midpoints = shapely.line_interpolate_point(road_geometry, 0.5, normalized=True)
    municipality = road_exposure.sample_grid(
        municipality_grid.astype("float32"), shapely.get_coordinates(midpoints)[:, :2], extent
    ).astype(int)
    length_decile = pd.qcut(
        roads["Road Section Length (m)"].rank(method="first"), q=10, labels=False, duplicates="drop"
    ).to_numpy(dtype=int)
    category = roads["Road Category"].fillna("Unknown").astype(str).to_numpy()
    emergency = roads["Emergency Route Membership"].fillna("None").astype(str).to_numpy()
    lookup = pd.Series(np.arange(len(roads), dtype=int), index=roads["Road Section ID"].astype(str))
    cases = evidence_section_ids.astype(str).drop_duplicates().map(lookup).dropna().astype(int).to_numpy()
    case_set = set(cases.tolist())
    rng = np.random.default_rng(MATCH_BOOTSTRAP_SEED)
    retained_cases: list[int] = []
    controls: list[np.ndarray] = []
    for case in cases:
        eligible = (
            (municipality == municipality[case])
            & (category == category[case])
            & (emergency == emergency[case])
            & (length_decile == length_decile[case])
        )
        candidates = np.array(
            [position for position in np.flatnonzero(eligible) if position not in case_set], dtype=int
        )
        if candidates.size:
            retained_cases.append(int(case))
            controls.append(rng.choice(candidates, size=min(10, candidates.size), replace=False))
    bootstrap_indices = rng.integers(
        0, len(retained_cases), size=(MATCH_BOOTSTRAP_REPLICATES, len(retained_cases))
    )
    return np.asarray(retained_cases, dtype=int), controls, bootstrap_indices


def concordance(
    score: np.ndarray, cases: np.ndarray, controls: list[np.ndarray], bootstrap: np.ndarray
) -> tuple[float, float, float]:
    case_values = []
    for case, case_controls in zip(cases, controls, strict=True):
        difference = score[case] - score[case_controls]
        case_values.append(float(np.mean((difference > 0) + 0.5 * (difference == 0))))
    values = np.asarray(case_values, dtype=float)
    boot = values[bootstrap].mean(axis=1)
    return float(values.mean()), float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))


def setup_network(
    roads: pd.DataFrame,
    central_heavy: np.ndarray,
    admin_union: object,
) -> dict[str, object]:
    lower = isolation.positive_score_quantile(central_heavy, isolation.CANDIDATE_QUANTILE)
    upper = isolation.positive_score_quantile(central_heavy, isolation.UPPER_MAPPING_QUANTILE)
    candidate = np.isfinite(central_heavy) & (central_heavy >= lower)
    candidate_ids = roads.loc[candidate, "Road Section ID"].reset_index(drop=True)
    candidate_position = pd.Series(np.arange(len(candidate_ids), dtype="int32"), index=candidate_ids)
    nodes = pd.read_parquet(
        isolation.NODE_PATH, columns=["Network Node ID", "Network Component ID", "Geometry"]
    )
    node_geometry = road_exposure.decode_geometry(nodes.pop("Geometry"))
    node_index = pd.Index(nodes["Network Node ID"])
    edges = pd.read_parquet(
        isolation.EDGE_PATH,
        columns=[
            "Road Section ID",
            "From Node ID",
            "To Node ID",
            "Network Component ID",
            "Emergency Route Membership",
            "Network Analysis Eligible",
        ],
    )
    edges = edges.loc[edges["Network Analysis Eligible"]].reset_index(drop=True)
    edge_u = node_index.get_indexer(edges["From Node ID"])
    edge_v = node_index.get_indexer(edges["To Node ID"])
    if np.any(edge_u < 0) or np.any(edge_v < 0):
        raise RuntimeError("Road edges reference missing network nodes")
    edge_candidate = edges["Road Section ID"].isin(candidate_ids).to_numpy()
    stable_u, stable_v = edge_u[~edge_candidate], edge_v[~edge_candidate]
    stable_graph = coo_matrix(
        (
            np.ones(len(stable_u) * 2, dtype="uint8"),
            (np.concatenate([stable_u, stable_v]), np.concatenate([stable_v, stable_u])),
        ),
        shape=(len(nodes), len(nodes)),
    ).tocsr()
    root_count, stable_labels = connected_components(stable_graph, directed=False, return_labels=True)
    stable_labels = stable_labels.astype("int32")
    candidate_u = stable_labels[edge_u[edge_candidate]]
    candidate_v = stable_labels[edge_v[edge_candidate]]
    candidate_edge_section = (
        edges.loc[edge_candidate, "Road Section ID"].map(candidate_position).to_numpy(dtype="int32")
    )
    between = candidate_u != candidate_v
    candidate_u, candidate_v = candidate_u[between], candidate_v[between]
    candidate_edge_section = candidate_edge_section[between]
    targets, target_components = isolation.external_target_definitions(
        nodes, node_geometry, stable_labels, edges, edge_u, edge_v, admin_union
    )
    community, attachment_community, attachment_root, diagnostics, _, _ = (
        isolation.build_baseline_communities(
            nodes, node_geometry, stable_labels, target_components
        )
    )
    return {
        "lower": lower,
        "upper": upper,
        "candidate_ids": candidate_ids,
        "candidate_u": candidate_u,
        "candidate_v": candidate_v,
        "candidate_edge_section": candidate_edge_section,
        "root_count": root_count,
        "target_roots": targets["Primary boundary gateways"],
        "attachment_community": attachment_community,
        "attachment_root": attachment_root,
        "community": community,
        "diagnostics": diagnostics,
    }


def main() -> None:
    for scheme, weights in WEIGHT_SCHEMES.items():
        if not math.isclose(sum(weights), 1.0):
            raise RuntimeError(f"Weights do not sum to one: {scheme}")
    required = [
        SPEC,
        SCENARIO_PATH,
        EVENT_PATH,
        THRESHOLD_PATH,
        COMPATIBILITY_EVENTS,
        terrain_score.DEM_PATH,
        terrain_score.WARNING_PATH,
        terrain_score.LANDSLIDE_PATH,
        road_exposure.ADMIN_PATH,
        road_exposure.ROAD_PATH,
        road_exposure.EDGE_PATH,
        road_exposure.MATCH_PATH,
        isolation.NODE_PATH,
        isolation.MESH_PATH,
        isolation.GROUP_PATH,
        Path(terrain_score.__file__),
        Path(road_exposure.__file__),
        Path(isolation.__file__),
        Path(__file__),
    ]
    required = list(dict.fromkeys(required))
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing frozen inputs: {missing}")

    admin = pd.read_parquet(road_exposure.ADMIN_PATH, columns=["Municipality Name", "Geometry"])
    admin_geometry = road_exposure.decode_geometry(admin.pop("Geometry"))
    admin_union = shapely.union_all(admin_geometry)
    min_x, min_y, max_x, max_y = shapely.bounds(admin_union)
    pad_x, pad_y = (max_x - min_x) * 0.025, (max_y - min_y) * 0.025
    extent = (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)
    west, east, south, north = extent
    height = max(650, round(road_exposure.DISPLAY_WIDTH * (north - south) / (east - west)))
    shape = (height, road_exposure.DISPLAY_WIDTH)
    transform = from_bounds(west, south, east, north, shape[1], shape[0])
    admin_mask = rasterize(
        [(admin_union, 1)], out_shape=shape, transform=transform, fill=0, all_touched=True, dtype="uint8"
    ).astype(bool)

    central_scores, central_loads, model_mode, elevation = road_exposure.load_or_build_landslide_scores(
        admin, admin_geometry, admin_union, extent, shape, transform
    )
    factor_grid = build_factor_grid(admin, admin_geometry, shape, transform, admin_mask)
    context, reconstruction_error = derive_terrain_logit(central_scores, central_loads, factor_grid)
    surfaces, references = window_surfaces(pd.read_parquet(SCENARIO_PATH), extent, shape)
    equal_check = {
        scenario: float(
            np.nanmax(
                np.abs(
                    np.mean(np.stack([surfaces[scenario][window] for window in WINDOWS]), axis=0)
                    - central_loads[scenario]
                )
            )
        )
        for scenario in SCENARIOS
    }

    grid_scores: dict[str, np.ndarray] = {}
    slope_rows: list[dict[str, object]] = []
    for scheme, weights in WEIGHT_SCHEMES.items():
        for gamma in GAMMAS:
            key = setting_key(scheme, gamma)
            for scenario in SCENARIOS:
                loading = np.zeros(shape, dtype="float32")
                for weight, window in zip(weights, WINDOWS, strict=True):
                    loading += np.float32(weight) * surfaces[scenario][window]
                adjusted = loading / factor_grid
                score = expit(context + gamma * np.log(np.clip(adjusted, 1e-7, None))).astype("float32")
                score[~np.isfinite(context)] = np.nan
                grid_scores[f"{key}__{scenario}"] = score
                values = score[np.isfinite(score)]
                slope_rows.append(
                    {
                        "weight_scheme": scheme,
                        "gamma": gamma,
                        "scenario": scenario,
                        "score_p50": float(np.quantile(values, 0.50)),
                        "score_p90": float(np.quantile(values, 0.90)),
                        "score_p99": float(np.quantile(values, 0.99)),
                    }
                )

    roads = pd.read_parquet(
        road_exposure.ROAD_PATH,
        columns=[
            "Road Section ID",
            "Road Category",
            "Road Section Length (m)",
            "Emergency Route Membership",
            "Network Analysis Eligible",
            "Geometry",
        ],
    )
    roads = roads.loc[roads["Network Analysis Eligible"]].reset_index(drop=True)
    road_geometry = road_exposure.decode_geometry(roads.pop("Geometry"))
    road_scores = road_exposure.road_scores(road_geometry, grid_scores, extent, elevation)
    del grid_scores

    cases, controls, bootstrap = matched_control_design(
        roads, road_geometry, evidence_sections(), admin_geometry, shape, transform, extent
    )
    road_rows: list[dict[str, object]] = []
    setting_rows: list[dict[str, object]] = []
    central_by_scenario = {
        scenario: road_scores[f"{CENTRAL_KEY}__{scenario}"] for scenario in SCENARIOS
    }
    for scheme in WEIGHT_SCHEMES:
        for gamma in GAMMAS:
            key = setting_key(scheme, gamma)
            setting_scenario_scores = [road_scores[f"{key}__{scenario}"] for scenario in SCENARIOS]
            supported = np.any(np.vstack([values > 0 for values in setting_scenario_scores]), axis=0)
            monotone = (
                (setting_scenario_scores[0] <= setting_scenario_scores[1] + 1e-7)
                & (setting_scenario_scores[1] <= setting_scenario_scores[2] + 1e-7)
            )
            concord, ci_low, ci_high = concordance(
                setting_scenario_scores[1], cases, controls, bootstrap
            )
            setting_rows.append(
                {
                    "weight_scheme": scheme,
                    "gamma": gamma,
                    "road_scenario_order_fraction": float(monotone[supported].mean()),
                    "matched_concordance": concord,
                    "matched_concordance_ci_low": ci_low,
                    "matched_concordance_ci_high": ci_high,
                    "matched_evidence_sections": int(len(cases)),
                }
            )
            for scenario, values in zip(SCENARIOS, setting_scenario_scores, strict=True):
                positive = values[np.isfinite(values) & (values > 0)]
                reference = central_by_scenario[scenario]
                rank_support = (
                    np.isfinite(reference)
                    & np.isfinite(values)
                    & ((reference > 0) | (values > 0))
                )
                road_rows.append(
                    {
                        "weight_scheme": scheme,
                        "gamma": gamma,
                        "scenario": scenario,
                        "positive_road_sections": int(len(positive)),
                        "score_p50": float(np.quantile(positive, 0.50)),
                        "score_p90": float(np.quantile(positive, 0.90)),
                        "score_p99": float(np.quantile(positive, 0.99)),
                        "central_rank_spearman_rho": safe_spearman(
                            reference[rank_support], values[rank_support]
                        ),
                        "central_top1_overlap": top_overlap(reference, values),
                    }
                )

    network = setup_network(roads, central_by_scenario["Heavy"], admin_union)
    id_to_position = pd.Series(
        np.arange(len(roads), dtype=int), index=roads["Road Section ID"]
    )
    candidate_positions = network["candidate_ids"].map(id_to_position).to_numpy(dtype=int)
    population = network["community"]["Total_Population"].to_numpy(dtype=float)
    older = network["community"]["Population_Age_65"].to_numpy(dtype=float)
    network_rows: list[dict[str, object]] = []
    for scheme, gamma in NETWORK_SETTINGS:
        key = setting_key(scheme, gamma)
        candidate_score = road_scores[f"{key}__Heavy"][candidate_positions]
        propensity = isolation.closure_propensity(
            candidate_score, float(network["lower"]), float(network["upper"])
        )
        totals, older_totals = [], []
        for seed in isolation.REPLICATE_SEEDS:
            frequency = isolation.cached_isolation(
                f"revision_r2c4_{scheme}_g{gamma:.2f}_heavy_seed_{seed}_m1000",
                network["candidate_u"],
                network["candidate_v"],
                network["candidate_edge_section"],
                propensity,
                network["root_count"],
                network["target_roots"],
                network["attachment_community"],
                network["attachment_root"],
                len(network["community"]),
                seed,
                draws=1_000,
                report_progress=False,
            )
            totals.append(float(np.sum(population * frequency)))
            older_totals.append(float(np.sum(older * frequency)))
        network_rows.append(
            {
                "weight_scheme": scheme,
                "gamma": gamma,
                "expected_isolated_population_mean": float(np.mean(totals)),
                "expected_isolated_population_min": float(np.min(totals)),
                "expected_isolated_population_max": float(np.max(totals)),
                "expected_isolated_population_sd": float(np.std(totals, ddof=1)),
                "expected_isolated_population_age65_mean": float(np.mean(older_totals)),
                "candidate_road_sections": int(len(candidate_positions)),
            }
        )
    network_frame = pd.DataFrame(network_rows)
    central_population = float(
        network_frame.loc[
            network_frame["weight_scheme"].eq("equal") & network_frame["gamma"].eq(1.0),
            "expected_isolated_population_mean",
        ].iloc[0]
    )
    network_frame["ratio_to_central"] = (
        network_frame["expected_isolated_population_mean"] / central_population
    )

    road_frame = pd.DataFrame(road_rows)
    setting_frame = pd.DataFrame(setting_rows)
    slope_frame = pd.DataFrame(slope_rows)
    compatibility_frame = event_weight_compatibility(references)
    noncentral_road = road_frame.loc[
        ~(
            road_frame["weight_scheme"].eq("equal")
            & road_frame["gamma"].eq(1.0)
        )
    ]
    minimum_rho = float(noncentral_road["central_rank_spearman_rho"].min())
    minimum_overlap = float(noncentral_road["central_top1_overlap"].min())
    if minimum_rho >= 0.90 and minimum_overlap >= 0.60:
        road_stability = "high"
    elif minimum_rho >= 0.75 and minimum_overlap >= 0.40:
        road_stability = "moderate"
    else:
        road_stability = "sensitive"
    maximum_network_deviation = float(np.max(np.abs(network_frame["ratio_to_central"] - 1.0)))
    if maximum_network_deviation <= 0.25:
        network_stability = "high"
    elif maximum_network_deviation <= 0.50:
        network_stability = "moderate"
    else:
        network_stability = "sensitive"
    scenario_order_stable = bool(np.allclose(setting_frame["road_scenario_order_fraction"], 1.0))

    OUT.mkdir(parents=True, exist_ok=True)
    slope_frame.to_csv(OUT / "slope_score_sensitivity.csv", index=False)
    road_frame.to_csv(OUT / "road_score_sensitivity.csv", index=False)
    setting_frame.to_csv(OUT / "matched_validation_and_ordering.csv", index=False)
    compatibility_frame.to_csv(OUT / "weight_scheme_jma_compatibility.csv", index=False)
    network_frame.to_csv(OUT / "community_isolation_parameter_sensitivity.csv", index=False)
    np.savez_compressed(
        OUT / "road_scores_15x3_scenarios.npz",
        **{key: value.astype("float32") for key, value in road_scores.items()},
    )
    input_hashes = pd.DataFrame(
        [
            {"path": str(path.relative_to(ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in required
        ]
    )
    input_hashes.to_csv(OUT / "input_hashes.csv", index=False)
    decision = {
        "decision_record": "KILA-D-20260903-002",
        "spec_sha256": sha256(SPEC),
        "model_mode": model_mode,
        "weights": WEIGHT_SCHEMES,
        "gammas": GAMMAS,
        "network_settings": NETWORK_SETTINGS,
        "terrain_reconstruction_max_abs_error": reconstruction_error,
        "equal_load_max_abs_errors": equal_check,
        "matched_evidence_sections": int(len(cases)),
        "road_stability": road_stability,
        "minimum_central_rank_spearman_rho": minimum_rho,
        "minimum_central_top1_overlap": minimum_overlap,
        "scenario_order_stable": scenario_order_stable,
        "network_stability": network_stability,
        "maximum_network_relative_deviation": maximum_network_deviation,
        "corrected_central_expected_isolated_population": central_population,
        "community_diagnostics": network["diagnostics"],
    }
    (OUT / "decision.json").write_text(
        json.dumps(decision, ensure_ascii=False, indent=2, default=float) + "\n", encoding="utf-8"
    )
    report = [
        "# Rainfall-parameter Sensitivity Report",
        "",
        "- Reviewer unit: `reviewer-2/comment-4`",
        "- Decision record: `KILA-D-20260903-002`",
        f"- Frozen specification SHA-256: `{sha256(SPEC)}`",
        f"- Central terrain reconstruction maximum absolute error: {reconstruction_error:.8f}",
        f"- Road-priority stability classification: **{road_stability}**",
        f"- Minimum road-rank Spearman correlation: {minimum_rho:.4f}",
        f"- Minimum top-1% road overlap: {minimum_overlap:.4f}",
        f"- Scenario ordering stable in all 15 combinations: {'yes' if scenario_order_stable else 'no'}",
        f"- Community-consequence stability classification: **{network_stability}**",
        f"- Maximum boundary-setting deviation from central: {maximum_network_deviation:.1%}",
        f"- Corrected central Heavy expected isolated population: {central_population:.1f}",
        "",
        "## JMA-type compatibility by weight scheme",
        "",
        compatibility_frame.to_markdown(index=False),
        "",
        "## Matched validation and ordering",
        "",
        setting_frame.to_markdown(index=False),
        "",
        "## Preselected Heavy community-isolation settings",
        "",
        network_frame.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "The equal-weight, gamma=1.00 model remains a transparent central reference rather than an empirically estimated optimum. Single-window specifications are stress tests. Sensitivity classifications follow the frozen thresholds and do not select a model by favorable validation performance.",
        "",
    ]
    (OUT / "sensitivity_report.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps(decision, ensure_ascii=False, indent=2, default=float))


if __name__ == "__main__":
    main()
