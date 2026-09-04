#!/usr/bin/env python3
"""Reviewer 4 Comment 5 emergency-water missing-location sensitivity.

The analysis treats hypothetical locations as a sensitivity assumption only. It
does not impute the production data, overwrite production outputs, or modify any
manuscript artifact.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.stats import spearmanr

import figure_basic_service_reachability_loss as service
import figure_community_isolation_frequency_and_exposed_population as isolation
import revision_service_destination_rerouting_audit as rerouting
import table_municipality_isolation_and_service_loss_summary as municipality_table


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/exp/revision/reviewer-4-comment-5"
WATER_INPUT = ROOT / "data/processed/emergency_water_points_preprocessed.parquet"
ADMIN_INPUT = ROOT / "data/processed/administrative_areas_preprocessed.parquet"
CACHE_DIR = ROOT / "data/results/intermediate/service_reachability_five_seed_v4"

PLACEMENT_REPLICATES = 50
DRAWS_PER_NETWORK_SEED = 250
PLACEMENT_SEED_BASE = 2026090450
MISSING_BY_CODE = {"43202": 18, "43213": 6, "43468": 2}
NON_WATER_CLASSES = ("Shelter", "Fire service", "Municipal facility")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def array_sha256(array: np.ndarray) -> str:
    values = np.ascontiguousarray(array)
    return hashlib.sha256(values.view(np.uint8)).hexdigest()


def stable_top(values: np.ndarray, n: int = 30) -> np.ndarray:
    score = np.where(np.isfinite(values), values, -np.inf)
    return np.argsort(-score, kind="stable")[: min(n, np.count_nonzero(np.isfinite(values)))]


def rank_metrics(
    observed: np.ndarray,
    hypothetical: np.ndarray,
    population: np.ndarray,
) -> tuple[float, float, int]:
    common = np.isfinite(observed) & np.isfinite(hypothetical)
    if np.count_nonzero(common) < 2:
        return np.nan, np.nan, int(np.count_nonzero(common))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        correlation = float(spearmanr(observed[common], hypothetical[common]).statistic)
    observed_burden = np.where(np.isfinite(observed), observed * population, np.nan)
    hypothetical_burden = np.where(
        np.isfinite(hypothetical), hypothetical * population, np.nan
    )
    observed_top = set(stable_top(observed_burden).tolist())
    hypothetical_top = set(stable_top(hypothetical_burden).tolist())
    overlap = len(observed_top & hypothetical_top) / max(len(observed_top), 1)
    return correlation, float(overlap), int(np.count_nonzero(common))


def canonical_mean(service_name: str) -> np.ndarray:
    arrays = []
    for seed in isolation.REPLICATE_SEEDS:
        path = CACHE_DIR / f"central_seed_{seed}.npz"
        with np.load(path, allow_pickle=False) as cached:
            arrays.append(cached[f"loss_{service_name}"].astype("float32"))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        return np.nanmean(np.stack(arrays), axis=0).astype("float32")


def placement_roots(context: dict[str, object]) -> tuple[list[np.ndarray], pd.DataFrame]:
    selected = context["selected_mesh"].copy().reset_index(drop=True)
    admin = context["admin"].reset_index(drop=True)
    admin_position = municipality_table.administrative_positions(
        context["selected_mesh_geometry"], context["admin_geometry"]
    )
    selected["Admin Position"] = admin_position
    code_to_position = {
        str(code): int(position)
        for position, code in enumerate(admin["Municipality Code"].astype(str))
    }
    observed_roots = np.asarray(
        context["service_roots"]["Emergency water"], dtype="int32"
    )
    placements: list[np.ndarray] = []
    rows: list[dict[str, object]] = []
    for replicate in range(PLACEMENT_REPLICATES):
        rng = np.random.default_rng(PLACEMENT_SEED_BASE + replicate)
        sampled_roots: list[np.ndarray] = []
        record: dict[str, object] = {
            "Placement Replicate": replicate + 1,
            "Placement Seed": PLACEMENT_SEED_BASE + replicate,
        }
        for code, count in MISSING_BY_CODE.items():
            position = code_to_position[code]
            pool = np.flatnonzero(selected["Admin Position"].to_numpy() == position)
            if len(pool) < count:
                raise RuntimeError(f"Insufficient eligible meshes for municipality {code}.")
            chosen = rng.choice(pool, size=count, replace=False)
            roots = selected.loc[chosen, "Stable Root"].to_numpy(dtype="int32")
            sampled_roots.append(roots)
            record[f"{code} Sampled Meshes"] = int(count)
            record[f"{code} Unique Added Roots"] = int(np.unique(roots).size)
        combined = np.unique(np.concatenate([observed_roots, *sampled_roots])).astype(
            "int32"
        )
        placements.append(combined)
        record["Observed Roots"] = int(observed_roots.size)
        record["Combined Unique Roots"] = int(combined.size)
        rows.append(record)
    return placements, pd.DataFrame(rows)


def baseline_eligible(
    roots: np.ndarray,
    baseline_graph: object,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
) -> np.ndarray:
    root_distance = dijkstra(
        baseline_graph, directed=False, indices=roots, min_only=True
    )
    community_distance = service.community_distance(
        root_distance, attachment_community, attachment_root, community_count
    )
    return np.isfinite(community_distance)


def reachable(
    labels: np.ndarray,
    roots: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
) -> np.ndarray:
    target_components = np.unique(labels[roots])
    attachment_reachable = np.isin(
        labels[attachment_root], target_components, assume_unique=False
    )
    community_reachable = np.zeros(community_count, dtype=bool)
    np.logical_or.at(
        community_reachable, attachment_community, attachment_reachable
    )
    return community_reachable


def simulate_common_draws(
    context: dict[str, object], placements: list[np.ndarray]
) -> tuple[np.ndarray, np.ndarray, list[np.ndarray], np.ndarray]:
    original_roots = np.asarray(
        context["service_roots"]["Emergency water"], dtype="int32"
    )
    community_count = len(context["community"])
    all_open = np.ones(len(context["section_propensity"]), dtype=bool)
    baseline_graph = service.weighted_draw_graph(
        all_open, context["pair_reduction"], context["root_count"]
    )
    original_eligible = baseline_eligible(
        original_roots,
        baseline_graph,
        context["attachment_community"],
        context["attachment_root"],
        community_count,
    )
    placement_eligible = [
        baseline_eligible(
            roots,
            baseline_graph,
            context["attachment_community"],
            context["attachment_root"],
            community_count,
        )
        for roots in placements
    ]
    original_count = np.zeros(community_count, dtype="int32")
    placement_count = np.zeros(
        (len(placements), community_count), dtype="int32"
    )
    total_draws = 0
    for seed in isolation.REPLICATE_SEEDS:
        random = np.random.default_rng(seed)
        for _ in range(DRAWS_PER_NETWORK_SEED):
            section_open = (
                random.random(len(context["section_propensity"]))
                >= context["section_propensity"]
            )
            graph = service.weighted_draw_graph(
                section_open, context["pair_reduction"], context["root_count"]
            )
            _, labels = connected_components(
                graph, directed=False, return_labels=True
            )
            labels = labels.astype("int32", copy=False)
            original_reachable = reachable(
                labels,
                original_roots,
                context["attachment_community"],
                context["attachment_root"],
                community_count,
            )
            original_count += original_eligible & ~original_reachable
            for position, roots in enumerate(placements):
                placement_reachable = reachable(
                    labels,
                    roots,
                    context["attachment_community"],
                    context["attachment_root"],
                    community_count,
                )
                placement_count[position] += (
                    placement_eligible[position] & ~placement_reachable
                )
            total_draws += 1
        print(
            f"Completed seed {seed}: {DRAWS_PER_NETWORK_SEED} common closure draws",
            flush=True,
        )
    original_frequency = np.full(community_count, np.nan, dtype="float32")
    original_frequency[original_eligible] = (
        original_count[original_eligible] / total_draws
    ).astype("float32")
    placement_frequency: list[np.ndarray] = []
    for position, eligible in enumerate(placement_eligible):
        frequency = np.full(community_count, np.nan, dtype="float32")
        frequency[eligible] = (
            placement_count[position, eligible] / total_draws
        ).astype("float32")
        placement_frequency.append(frequency)
    return original_frequency, original_eligible, placement_frequency, np.asarray(
        placement_eligible
    )


def cross_class_invariance(
    context: dict[str, object], counterfactual_water_roots: np.ndarray
) -> dict[str, bool]:
    original_roots = {
        name: np.asarray(roots, dtype="int32").copy()
        for name, roots in context["service_roots"].items()
    }
    counterfactual_roots = {
        name: roots.copy() for name, roots in original_roots.items()
    }
    counterfactual_roots["Emergency water"] = counterfactual_water_roots.copy()
    original_draws = isolation.MONTE_CARLO_DRAWS
    isolation.MONTE_CARLO_DRAWS = 50
    try:
        reference = service.simulate_service_loss(
            context["section_propensity"],
            context["pair_reduction"],
            context["root_count"],
            original_roots,
            context["attachment_community"],
            context["attachment_root"],
            len(context["community"]),
            isolation.REPLICATE_SEEDS[0],
        )
        counterfactual = service.simulate_service_loss(
            context["section_propensity"],
            context["pair_reduction"],
            context["root_count"],
            counterfactual_roots,
            context["attachment_community"],
            context["attachment_root"],
            len(context["community"]),
            isolation.REPLICATE_SEEDS[0],
        )
    finally:
        isolation.MONTE_CARLO_DRAWS = original_draws
    checks: dict[str, bool] = {}
    for output_name, reference_output, counterfactual_output in zip(
        ("loss", "excess", "baseline"), reference, counterfactual, strict=True
    ):
        for service_name in NON_WATER_CLASSES:
            checks[f"{service_name}_{output_name}_exact"] = bool(
                np.array_equal(
                    reference_output[service_name],
                    counterfactual_output[service_name],
                    equal_nan=True,
                )
            )
    return checks


def quantiles(values: pd.Series) -> tuple[float, float, float]:
    return tuple(float(values.quantile(q)) for q in (0.05, 0.50, 0.95))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    context = rerouting.build_context()
    placements, placement_table = placement_roots(context)
    (
        original_frequency,
        original_eligible,
        placement_frequencies,
        placement_eligible,
    ) = simulate_common_draws(context, placements)
    population = context["community"]["Total_Population"].to_numpy(dtype="float64")
    canonical_water = canonical_mean("Emergency water")
    canonical_fire = canonical_mean("Fire service")
    canonical_municipal = canonical_mean("Municipal facility")

    original_expected = float(
        np.nansum(original_frequency * population)
    )
    canonical_expected = float(np.nansum(canonical_water * population))
    placement_rows: list[dict[str, object]] = []
    for position, (frequency, eligible) in enumerate(
        zip(placement_frequencies, placement_eligible, strict=True)
    ):
        correlation, overlap, common_count = rank_metrics(
            original_frequency, frequency, population
        )
        placement_rows.append(
            {
                **placement_table.iloc[position].to_dict(),
                "Baseline-Eligible Communities": int(np.count_nonzero(eligible)),
                "Baseline-Eligible Population": float(population[eligible].sum()),
                "Newly Eligible Communities": int(
                    np.count_nonzero(eligible & ~original_eligible)
                ),
                "Newly Eligible Population": float(
                    population[eligible & ~original_eligible].sum()
                ),
                "Expected Affected Population": float(
                    np.nansum(frequency * population)
                ),
                "Common-Eligible Communities": common_count,
                "Frequency Spearman vs Observed-Only": correlation,
                "Top-30 Burden Overlap vs Observed-Only": overlap,
            }
        )
    placement_result = pd.DataFrame(placement_rows)
    invariance = cross_class_invariance(context, placements[0])
    if not all(invariance.values()):
        failed = [key for key, value in invariance.items() if not value]
        raise RuntimeError(f"Cross-service invariance failed: {failed}")

    expected_q = quantiles(placement_result["Expected Affected Population"])
    eligible_q = quantiles(placement_result["Baseline-Eligible Population"])
    new_population_q = quantiles(placement_result["Newly Eligible Population"])
    correlation_q = quantiles(
        placement_result["Frequency Spearman vs Observed-Only"]
    )
    overlap_q = quantiles(
        placement_result["Top-30 Burden Overlap vs Observed-Only"]
    )
    summary = pd.DataFrame(
        [
            {
                "Metric": "Observed-only expected affected population (1,250 common draws)",
                "Observed / Central": original_expected,
                "Placement P05": np.nan,
                "Placement Median": np.nan,
                "Placement P95": np.nan,
            },
            {
                "Metric": "Observed-only canonical expected affected population (5 x 1,000)",
                "Observed / Central": canonical_expected,
                "Placement P05": np.nan,
                "Placement Median": np.nan,
                "Placement P95": np.nan,
            },
            {
                "Metric": "Uniform-mesh expected affected population",
                "Observed / Central": np.nan,
                "Placement P05": expected_q[0],
                "Placement Median": expected_q[1],
                "Placement P95": expected_q[2],
            },
            {
                "Metric": "Uniform-mesh baseline-eligible population",
                "Observed / Central": float(population[original_eligible].sum()),
                "Placement P05": eligible_q[0],
                "Placement Median": eligible_q[1],
                "Placement P95": eligible_q[2],
            },
            {
                "Metric": "Uniform-mesh newly eligible population",
                "Observed / Central": 0.0,
                "Placement P05": new_population_q[0],
                "Placement Median": new_population_q[1],
                "Placement P95": new_population_q[2],
            },
            {
                "Metric": "Emergency-water frequency Spearman vs observed-only",
                "Observed / Central": 1.0,
                "Placement P05": correlation_q[0],
                "Placement Median": correlation_q[1],
                "Placement P95": correlation_q[2],
            },
            {
                "Metric": "Emergency-water Top-30 burden overlap vs observed-only",
                "Observed / Central": 1.0,
                "Placement P05": overlap_q[0],
                "Placement Median": overlap_q[1],
                "Placement P95": overlap_q[2],
            },
        ]
    )
    placement_result.to_csv(
        OUT / "placement_sensitivity.csv",
        index=False,
        float_format="%.10g",
        lineterminator="\n",
    )
    summary.to_csv(
        OUT / "summary.csv", index=False, float_format="%.10g", lineterminator="\n"
    )
    input_paths = [
        WATER_INPUT,
        ADMIN_INPUT,
        Path(rerouting.__file__).resolve(),
        Path(service.__file__).resolve(),
        *[CACHE_DIR / f"central_seed_{seed}.npz" for seed in isolation.REPLICATE_SEEDS],
    ]
    pd.DataFrame(
        [
            {"Path": str(path.relative_to(ROOT)), "SHA-256": sha256(path)}
            for path in input_paths
        ]
    ).to_csv(OUT / "input_hashes.csv", index=False, lineterminator="\n")

    canonical_hashes = {
        "fire_mean_array": array_sha256(canonical_fire),
        "municipal_mean_array": array_sha256(canonical_municipal),
    }
    decision = {
        "reviewer_id": "reviewer-4",
        "comment_id": "comment-5",
        "identifiable_missingness": {
            "municipality_and_name_class_concentration": True,
            "urban_rural_missingness_identifiable": False,
            "uniform_or_random_missingness_supported": False,
        },
        "sensitivity_design": {
            "assumption": "uniform without replacement over eligible populated 125 m meshes within each source municipality",
            "placement_replicates": PLACEMENT_REPLICATES,
            "network_seeds": list(isolation.REPLICATE_SEEDS),
            "draws_per_network_seed": DRAWS_PER_NETWORK_SEED,
            "total_common_draws_per_placement": int(
                len(isolation.REPLICATE_SEEDS) * DRAWS_PER_NETWORK_SEED
            ),
            "missing_counts_by_municipality_code": MISSING_BY_CODE,
        },
        "results": {
            "observed_only_expected_affected_population_diagnostic": original_expected,
            "observed_only_expected_affected_population_canonical": canonical_expected,
            "uniform_mesh_expected_affected_population_p05_median_p95": expected_q,
            "uniform_mesh_baseline_eligible_population_p05_median_p95": eligible_q,
            "uniform_mesh_newly_eligible_population_p05_median_p95": new_population_q,
            "emergency_water_frequency_spearman_p05_median_p95": correlation_q,
            "emergency_water_top30_overlap_p05_median_p95": overlap_q,
        },
        "cross_service_invariance": invariance,
        "canonical_non_water_array_hashes": canonical_hashes,
        "interpretation": {
            "emergency_water_magnitude_and_ranking_sensitive_to_hypothetical_locations": True,
            "fire_and_municipal_rankings_change_when_only_water_locations_change": False,
            "reason": "service classes are evaluated separately and no cross-service composite is calculated",
            "production_imputation_authorized": False,
        },
    }
    (OUT / "decision.json").write_text(
        json.dumps(decision, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report = f"""# Reviewer 4 Comment 5 emergency-water missingness sensitivity

## Identifiable missingness

The 26 unresolved announcements are concentrated by municipality and facility-name class, so uniform or random missingness is not supported by the observed metadata. Urban–rural missingness cannot be identified because the unresolved records have no coordinates.

## Uniform-over-eligible-mesh sensitivity

The hypothetical analysis retains the ten observed destinations and places the 18 Yatsushiro, six Uki, and two Hikawa unresolved records uniformly over eligible populated 125 m meshes within their source municipality. This is a declared sensitivity assumption, not recovered location data. Across {PLACEMENT_REPLICATES} placement replicates and {len(isolation.REPLICATE_SEEDS)} × {DRAWS_PER_NETWORK_SEED} common Heavy-scenario closure draws per placement:

- expected emergency-water affected population has a 5th–median–95th percentile range of {expected_q[0]:,.1f}–{expected_q[1]:,.1f}–{expected_q[2]:,.1f};
- baseline-eligible population has a range of {eligible_q[0]:,.1f}–{eligible_q[1]:,.1f}–{eligible_q[2]:,.1f};
- newly eligible population has a range of {new_population_q[0]:,.1f}–{new_population_q[1]:,.1f}–{new_population_q[2]:,.1f};
- common-eligible emergency-water frequency correlation with the observed-only branch has a range of {correlation_q[0]:.3f}–{correlation_q[1]:.3f}–{correlation_q[2]:.3f}; and
- Top-30 emergency-water population-burden overlap has a range of {overlap_q[0]:.1%}–{overlap_q[1]:.1%}–{overlap_q[2]:.1%}.

The observed-only diagnostic gives {original_expected:,.1f} affected residents using the same 1,250 common draws, compared with the canonical five-seed × 1,000-draw result of {canonical_expected:,.1f}.

## Cross-service consequence

Changing only the emergency-water destination roots leaves shelter, fire-service, and municipal-facility loss, excess-time, and baseline arrays exactly identical in the same-seed sentinel test ({sum(invariance.values())}/{len(invariance)} gates passed). Fire-service and municipal-facility rankings therefore cannot change under this hypothetical because each service class is evaluated separately and the analysis contains no cross-service composite.

## Interpretation boundary

The sensitivity demonstrates that the emergency-water result itself depends on unobserved location support. It does not locate the missing announcements, identify urban–rural bias, or justify replacing the production data with synthetic destinations. The conditional emergency-water result should remain separate from the three primary service classes.
"""
    (OUT / "audit_report.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"Saved outputs to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
