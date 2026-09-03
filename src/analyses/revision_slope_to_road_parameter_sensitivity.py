#!/usr/bin/env python3
"""Predeclared slope-to-road transfer sensitivity for Reviewer 2 Comment 5.

This script writes revision-only evidence. It deliberately does not update the
accepted road-score caches or any manuscript, figure, or table output.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from dataclasses import asdict, dataclass
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import numpy as np
import pandas as pd
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from scipy.stats import spearmanr
import shapely

import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure
import revision_rainfall_parameter_sensitivity as rainfall_sensitivity


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "Rev/docs/analysis-spec-reviewer-2-comment-5.md"
OUT = ROOT / "data/exp/revision/reviewer-2-comment-5"
SCENARIOS = ("Moderate", "Heavy", "Extreme")
DECISION_RECORD = "KILA-D-20260903-013"
TOP_FRACTION = 0.01
CANDIDATE_QUANTILE = 0.85


@dataclass(frozen=True)
class TransferSpecification:
    key: str
    label: str
    radius_cells: int = 3
    minimum_relief_m: float = 10.0
    minimum_alignment_cosine: float = 0.20
    distance_efold_cells: float = 2.5
    relief_scale_m: float = 100.0
    sample_fractions: tuple[float, ...] = (0.20, 0.50, 0.80)
    design: str = "one-at-a-time"


SPECIFICATIONS = (
    TransferSpecification("central", "Central", design="central"),
    TransferSpecification("radius_2", "Neighborhood half-width: 2 cells", radius_cells=2),
    TransferSpecification("radius_4", "Neighborhood half-width: 4 cells", radius_cells=4),
    TransferSpecification("relief_5", "Minimum relief: 5 m", minimum_relief_m=5.0),
    TransferSpecification("relief_20", "Minimum relief: 20 m", minimum_relief_m=20.0),
    TransferSpecification("alignment_0", "Minimum alignment cosine: 0.00", minimum_alignment_cosine=0.0),
    TransferSpecification("alignment_05", "Minimum alignment cosine: 0.50", minimum_alignment_cosine=0.5),
    TransferSpecification("decay_15", "Distance e-folding length: 1.5 cells", distance_efold_cells=1.5),
    TransferSpecification("decay_40", "Distance e-folding length: 4.0 cells", distance_efold_cells=4.0),
    TransferSpecification("relief_scale_50", "Relief scaling height: 50 m", relief_scale_m=50.0),
    TransferSpecification("relief_scale_150", "Relief scaling height: 150 m", relief_scale_m=150.0),
    TransferSpecification("midpoint", "Road sampling: midpoint only", sample_fractions=(0.50,)),
    TransferSpecification(
        "five_points",
        "Road sampling: five points",
        sample_fractions=(0.10, 0.30, 0.50, 0.70, 0.90),
    ),
    TransferSpecification(
        "strict_joint",
        "Strict joint boundary",
        radius_cells=2,
        minimum_relief_m=20.0,
        minimum_alignment_cosine=0.5,
        distance_efold_cells=1.5,
        relief_scale_m=50.0,
        sample_fractions=(0.10, 0.30, 0.50, 0.70, 0.90),
        design="joint-boundary",
    ),
    TransferSpecification(
        "permissive_joint",
        "Permissive joint boundary",
        radius_cells=4,
        minimum_relief_m=5.0,
        minimum_alignment_cosine=0.0,
        distance_efold_cells=4.0,
        relief_scale_m=150.0,
        sample_fractions=(0.10, 0.30, 0.50, 0.70, 0.90),
        design="joint-boundary",
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_spearman(x: np.ndarray, y: np.ndarray) -> float:
    valid = np.isfinite(x) & np.isfinite(y)
    if valid.sum() < 3 or np.unique(x[valid]).size < 2 or np.unique(y[valid]).size < 2:
        return math.nan
    return float(spearmanr(x[valid], y[valid]).statistic)


def top_indices(values: np.ndarray, fraction: float) -> np.ndarray:
    valid = np.flatnonzero(np.isfinite(values))
    count = max(1, int(math.ceil(fraction * len(valid))))
    local = np.argpartition(values[valid], -count)[-count:]
    return valid[local]


def overlap(reference: np.ndarray, candidate: np.ndarray) -> float:
    if not len(reference) or not len(candidate):
        return math.nan
    return float(len(np.intersect1d(reference, candidate)) / min(len(reference), len(candidate)))


def candidate_indices(values: np.ndarray) -> np.ndarray:
    positive = values[np.isfinite(values) & (values > 0)]
    if not len(positive):
        return np.asarray([], dtype=int)
    threshold = float(np.quantile(positive, CANDIDATE_QUANTILE))
    return np.flatnonzero(np.isfinite(values) & (values >= threshold))


def parameterized_road_scores(
    geometry: np.ndarray,
    terrain_scores: dict[str, np.ndarray],
    extent: tuple[float, float, float, float],
    elevation_grid: np.ndarray,
    specification: TransferSpecification,
) -> tuple[dict[str, np.ndarray], np.ndarray]:
    """Reproduce Equation 7 while exposing only the predeclared parameters."""
    parts, parent_index = shapely.get_parts(geometry, return_index=True)
    sampled_points = [
        shapely.line_interpolate_point(parts, fraction, normalized=True)
        for fraction in specification.sample_fractions
    ]
    rows, columns = elevation_grid.shape
    west, east, south, north = extent
    filled_elevation = np.where(
        np.isfinite(elevation_grid), elevation_grid, float(np.nanmedian(elevation_grid))
    )
    gradient_y, gradient_x = np.gradient(filled_elevation.astype("float64"))
    part_weighted = {
        scenario: np.zeros(len(parts), dtype="float64") for scenario in terrain_scores
    }
    part_weight = np.zeros(len(parts), dtype="float64")
    radius = specification.radius_cells
    offsets = [
        (dy, dx)
        for dy in range(-radius, radius + 1)
        for dx in range(-radius, radius + 1)
        if dx or dy
    ]
    for sample_number, points in enumerate(sampled_points, start=1):
        coordinates = shapely.get_coordinates(points)[:, :2]
        column = np.floor((coordinates[:, 0] - west) / (east - west) * columns).astype(int)
        row = np.floor((north - coordinates[:, 1]) / (north - south) * rows).astype(int)
        point_inside = (row >= 0) & (row < rows) & (column >= 0) & (column < columns)
        road_elevation = np.full(len(parts), np.nan, dtype="float64")
        road_elevation[point_inside] = elevation_grid[row[point_inside], column[point_inside]]
        for dy, dx in offsets:
            neighbour_row, neighbour_column = row + dy, column + dx
            inside = (
                point_inside
                & (neighbour_row >= 0)
                & (neighbour_row < rows)
                & (neighbour_column >= 0)
                & (neighbour_column < columns)
            )
            if not inside.any():
                continue
            positions = np.flatnonzero(inside)
            rr, cc = neighbour_row[positions], neighbour_column[positions]
            neighbour_elevation = elevation_grid[rr, cc]
            relief = neighbour_elevation - road_elevation[positions]
            gx, gy = gradient_x[rr, cc], gradient_y[rr, cc]
            distance = float(np.hypot(dx, dy))
            alignment = (gx * dx + gy * dy) / np.maximum(
                np.hypot(gx, gy) * distance, 1e-6
            )
            plausible = (
                np.isfinite(neighbour_elevation)
                & np.isfinite(relief)
                & (relief >= specification.minimum_relief_m)
                & (alignment >= specification.minimum_alignment_cosine)
            )
            if not plausible.any():
                continue
            selected, rr, cc = positions[plausible], rr[plausible], cc[plausible]
            q_ie = (
                np.exp(-distance / specification.distance_efold_cells)
                * np.clip(alignment[plausible], 0.0, 1.0)
                * np.clip(relief[plausible] / specification.relief_scale_m, 0.20, 1.0)
            )
            np.add.at(part_weight, selected, q_ie)
            for scenario, score_grid in terrain_scores.items():
                np.add.at(
                    part_weighted[scenario],
                    selected,
                    np.nan_to_num(score_grid[rr, cc], nan=0.0) * q_ie,
                )
        print(
            f"{specification.key}: road sample {sample_number}/{len(sampled_points)} complete",
            flush=True,
        )

    road_weight = np.zeros(len(geometry), dtype="float64")
    np.add.at(road_weight, parent_index, part_weight)
    supported = road_weight > 0
    results: dict[str, np.ndarray] = {}
    for scenario, part_numerator in part_weighted.items():
        numerator = np.zeros(len(geometry), dtype="float64")
        np.add.at(numerator, parent_index, part_numerator)
        result = np.zeros(len(geometry), dtype="float32")
        result[supported] = (numerator[supported] / road_weight[supported]).astype("float32")
        results[scenario] = result
    return results, road_weight.astype("float32")


def main() -> None:
    if len(SPECIFICATIONS) != 15 or len({item.key for item in SPECIFICATIONS}) != 15:
        raise RuntimeError("The frozen design must contain 15 unique specifications.")
    required = [
        SPEC,
        road_exposure.ADMIN_PATH,
        road_exposure.ROAD_PATH,
        road_exposure.EDGE_PATH,
        road_exposure.MATCH_PATH,
        road_exposure.SCENARIO_PATH,
        road_exposure.THRESHOLD_PATH,
        road_exposure.WARNING_PATH,
        road_exposure.LANDSLIDE_PATH,
        Path(road_exposure.__file__),
        Path(rainfall_sensitivity.__file__),
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
    terrain_scores, _, model_mode, elevation = road_exposure.load_or_build_landslide_scores(
        admin, admin_geometry, admin_union, extent, shape, transform
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
    central_cached = road_exposure.load_or_build_road_scores(
        road_geometry, terrain_scores, extent, elevation
    )
    evidence = rainfall_sensitivity.evidence_sections()
    cases, controls, bootstrap = rainfall_sensitivity.matched_control_design(
        roads, road_geometry, evidence, admin_geometry, shape, transform, extent
    )
    if len(cases) == 0 or bootstrap.shape != (2_000, len(cases)):
        raise RuntimeError("The frozen matched-control design could not be constructed.")

    all_scores: dict[str, dict[str, np.ndarray]] = {}
    all_weights: dict[str, np.ndarray] = {}
    for number, specification in enumerate(SPECIFICATIONS, start=1):
        print(f"Running specification {number}/15: {specification.key}", flush=True)
        scenarios = terrain_scores if specification.key in {
            "central", "strict_joint", "permissive_joint"
        } else {"Heavy": terrain_scores["Heavy"]}
        scores, weights = parameterized_road_scores(
            road_geometry, scenarios, extent, elevation, specification
        )
        all_scores[specification.key] = scores
        all_weights[specification.key] = weights

    central_error = max(
        float(np.max(np.abs(all_scores["central"][scenario] - central_cached[scenario])))
        for scenario in SCENARIOS
    )
    central_nonzero_mask_equal = bool(
        all(
            np.array_equal(
                all_scores["central"][scenario] > 0,
                central_cached[scenario] > 0,
            )
            for scenario in SCENARIOS
        )
    )
    if central_error > 1e-7 or not central_nonzero_mask_equal:
        raise RuntimeError(
            f"Central-equivalence gate failed: max error={central_error}, "
            f"nonzero_mask_equal={central_nonzero_mask_equal}"
        )

    central = all_scores["central"]["Heavy"]
    central_top = top_indices(central, TOP_FRACTION)
    central_candidate = candidate_indices(central)
    sensitivity_rows: list[dict[str, object]] = []
    validation_rows: list[dict[str, object]] = []
    for specification in SPECIFICATIONS:
        score = all_scores[specification.key]["Heavy"]
        weight = all_weights[specification.key]
        positive = score[np.isfinite(score) & (score > 0)]
        union_supported = (central > 0) | (score > 0)
        top = top_indices(score, TOP_FRACTION)
        candidate = candidate_indices(score)
        sensitivity_rows.append(
            {
                "specification": specification.key,
                "label": specification.label,
                "supported_road_sections": int(np.sum(weight > 0)),
                "support_fraction": float(np.mean(weight > 0)),
                "nonzero_score_sections": int(len(positive)),
                "nonzero_score_fraction": float(len(positive) / len(score)),
                "score_p50_positive": float(np.quantile(positive, 0.50)),
                "score_p90_positive": float(np.quantile(positive, 0.90)),
                "score_p99_positive": float(np.quantile(positive, 0.99)),
                "spearman_all_roads": safe_spearman(central, score),
                "spearman_union_supported": safe_spearman(
                    central[union_supported], score[union_supported]
                ),
                "top1_count": int(len(top)),
                "top1_overlap_with_central": overlap(central_top, top),
                "official_heavy_candidate_count": int(len(candidate)),
                "official_heavy_candidate_overlap_with_central": overlap(
                    central_candidate, candidate
                ),
            }
        )
        concordance, ci_low, ci_high = rainfall_sensitivity.concordance(
            score, cases, controls, bootstrap
        )
        validation_rows.append(
            {
                "specification": specification.key,
                "matched_evidence_sections": int(len(cases)),
                "matched_controls": int(sum(len(item) for item in controls)),
                "matched_concordance": concordance,
                "bootstrap_ci_low": ci_low,
                "bootstrap_ci_high": ci_high,
                "bootstrap_replicates": int(len(bootstrap)),
            }
        )

    ordering_rows: list[dict[str, object]] = []
    for key in ("central", "strict_joint", "permissive_joint"):
        moderate, heavy, extreme = (all_scores[key][scenario] for scenario in SCENARIOS)
        supported = all_weights[key] > 0
        ordered = (moderate <= heavy + 1e-7) & (heavy <= extreme + 1e-7)
        ordering_rows.append(
            {
                "specification": key,
                "supported_road_sections": int(np.sum(supported)),
                "ordered_road_sections": int(np.sum(ordered & supported)),
                "ordering_fraction_supported": float(np.mean(ordered[supported])),
                "maximum_moderate_minus_heavy": float(np.max(moderate[supported] - heavy[supported])),
                "maximum_heavy_minus_extreme": float(np.max(heavy[supported] - extreme[supported])),
            }
        )

    parameter_frame = pd.DataFrame(
        [
            {
                **asdict(item),
                "sample_fractions": ",".join(f"{value:.2f}" for value in item.sample_fractions),
            }
            for item in SPECIFICATIONS
        ]
    )
    sensitivity_frame = pd.DataFrame(sensitivity_rows)
    validation_frame = pd.DataFrame(validation_rows)
    ordering_frame = pd.DataFrame(ordering_rows)
    noncentral = sensitivity_frame.loc[sensitivity_frame["specification"].ne("central")]
    noncentral_validation = validation_frame.loc[validation_frame["specification"].ne("central")]
    minimum_rho = float(noncentral["spearman_union_supported"].min())
    minimum_top_overlap = float(noncentral["top1_overlap_with_central"].min())
    minimum_concordance = float(noncentral_validation["matched_concordance"].min())
    high = (
        minimum_rho >= 0.95
        and minimum_top_overlap >= 0.80
        and minimum_concordance > 0.50
    )
    material = (
        minimum_rho < 0.90
        or minimum_top_overlap < 0.60
        or minimum_concordance <= 0.50
    )
    classification = "high" if high else "material" if material else "moderate"
    ordering_valid = bool(np.allclose(ordering_frame["ordering_fraction_supported"], 1.0))
    if not ordering_valid:
        raise RuntimeError("Scenario-ordering validation failed.")

    OUT.mkdir(parents=True, exist_ok=True)
    parameter_frame.to_csv(OUT / "parameter_specifications.csv", index=False)
    sensitivity_frame.to_csv(OUT / "road_score_sensitivity.csv", index=False)
    validation_frame.to_csv(OUT / "matched_validation_sensitivity.csv", index=False)
    ordering_frame.to_csv(OUT / "scenario_ordering_checks.csv", index=False)
    np.savez_compressed(
        OUT / "heavy_road_scores_15_specifications.npz",
        **{key: values["Heavy"].astype("float32") for key, values in all_scores.items()},
    )
    np.savez_compressed(
        OUT / "joint_boundary_scenario_scores.npz",
        **{
            f"{key}__{scenario}": all_scores[key][scenario].astype("float32")
            for key in ("central", "strict_joint", "permissive_joint")
            for scenario in SCENARIOS
        },
    )
    np.savez_compressed(
        OUT / "fixed_matched_control_design.npz",
        cases=cases,
        control_offsets=np.cumsum([0] + [len(item) for item in controls]),
        controls=np.concatenate(controls),
        bootstrap_indices=bootstrap,
    )
    input_hashes = pd.DataFrame(
        [
            {"path": str(path.relative_to(ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in required
        ]
    )
    input_hashes.to_csv(OUT / "input_hashes.csv", index=False)
    decision = {
        "reviewer_unit": "reviewer-2/comment-5",
        "decision_record": DECISION_RECORD,
        "spec_sha256": sha256(SPEC),
        "model_mode": model_mode,
        "eligible_road_sections": int(len(roads)),
        "matched_evidence_sections": int(len(cases)),
        "matched_controls": int(sum(len(item) for item in controls)),
        "central_equivalence_max_abs_error": central_error,
        "central_nonzero_score_masks_equal": central_nonzero_mask_equal,
        "classification": classification,
        "minimum_supported_road_spearman": minimum_rho,
        "minimum_top1_overlap": minimum_top_overlap,
        "minimum_matched_concordance": minimum_concordance,
        "scenario_ordering_valid": ordering_valid,
        "propagate_joint_boundaries_downstream": classification == "material",
        "candidate_definition": (
            "Road scores at or above the 0.85 quantile among positive scores, "
            "matching the canonical official-Heavy candidate rule."
        ),
        "interpretation_boundary": (
            "Regional directional screening; not physical runout validation or local "
            "engineering calibration."
        ),
    }
    (OUT / "decision.json").write_text(
        json.dumps(decision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    report = [
        "# Slope-to-road transfer sensitivity report",
        "",
        f"- Reviewer unit: `reviewer-2/comment-5`",
        f"- Decision record: `{DECISION_RECORD}`",
        f"- Frozen specification SHA-256: `{sha256(SPEC)}`",
        f"- Central equivalence maximum absolute error: {central_error:.3g}",
        f"- Central nonzero-score masks identical to canonical implementation: {'yes' if central_nonzero_mask_equal else 'no'}",
        f"- Stability classification: **{classification}**",
        f"- Minimum supported-road Spearman correlation: {minimum_rho:.4f}",
        f"- Minimum top-1% overlap: {minimum_top_overlap:.4f}",
        f"- Minimum matched concordance: {minimum_concordance:.4f}",
        f"- Moderate <= Heavy <= Extreme for all supported roads in the central and joint settings: {'yes' if ordering_valid else 'no'}",
        "",
        "## Road-score sensitivity",
        "",
        sensitivity_frame.to_markdown(index=False),
        "",
        "## Matched validation",
        "",
        validation_frame.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        (
            "The classification follows the frozen thresholds and does not reselect the central "
            "specification using restriction evidence. The transfer remains a regional directional-"
            "screening rule rather than a physical runout or road-failure model."
        ),
        "",
    ]
    (OUT / "sensitivity_report.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps(decision, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
