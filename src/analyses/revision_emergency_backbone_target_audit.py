#!/usr/bin/env python3
"""Audit and validate the Reviewer 3 Comment 6 isolation-target revision."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.stats import spearmanr
import shapely

from cache_fingerprint import cache_matches, content_signature
import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure
import revision_spatially_correlated_closure_sensitivity as network_inputs


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "Rev/docs/analysis-spec-reviewer-3-comment-6.md"
OUT = ROOT / "data/exp/revision/reviewer-3-comment-6"
CACHE = OUT / "cache"
SCENARIOS = ("Moderate", "Heavy", "Extreme")
TARGETS = (
    isolation.PRIMARY_TARGET_NAME,
    isolation.BROADER_TARGET_NAME,
    isolation.LEGACY_TARGET_NAME,
)
SIMULATION_TARGETS = (
    isolation.PRIMARY_TARGET_NAME,
    isolation.BROADER_TARGET_NAME,
)
DRAWS = 1_000
DECISION_RECORD = "KILA-D-20260904-006"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def slug(value: str) -> str:
    return value.lower().replace(" ", "_").replace("-", "_")


def safe_spearman(left: np.ndarray, right: np.ndarray) -> float:
    valid = np.isfinite(left) & np.isfinite(right)
    if valid.sum() < 3 or np.unique(left[valid]).size < 2 or np.unique(right[valid]).size < 2:
        return float("nan")
    return float(spearmanr(left[valid], right[valid]).statistic)


def top_n_overlap(left: np.ndarray, right: np.ndarray, n: int = 30) -> float:
    count = min(n, len(left), len(right))
    left_order = np.argsort(-left, kind="stable")[:count]
    right_order = np.argsort(-right, kind="stable")[:count]
    return float(len(set(left_order.tolist()) & set(right_order.tolist())) / count)


def simulate_targets(
    *,
    candidate_u: np.ndarray,
    candidate_v: np.ndarray,
    candidate_edge_section: np.ndarray,
    propensity: np.ndarray,
    root_count: int,
    target_definitions: dict[str, np.ndarray],
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
    seed: int,
    draws: int,
) -> dict[str, np.ndarray]:
    """Evaluate multiple fixed target sets from the same closure draws."""
    random = np.random.default_rng(seed)
    isolated_counts = {
        name: np.zeros(community_count, dtype="int32") for name in target_definitions
    }
    for _ in range(draws):
        section_open = random.random(len(propensity)) >= propensity
        edge_open = section_open[candidate_edge_section]
        u = candidate_u[edge_open]
        v = candidate_v[edge_open]
        graph = coo_matrix(
            (
                np.ones(len(u) * 2, dtype="uint8"),
                (np.concatenate([u, v]), np.concatenate([v, u])),
            ),
            shape=(root_count, root_count),
        ).tocsr()
        component_count, labels = connected_components(
            graph, directed=False, return_labels=True
        )
        for name, target_roots in target_definitions.items():
            target_component = np.zeros(component_count, dtype=bool)
            target_component[labels[target_roots]] = True
            root_accessible = target_component[labels]
            community_accessible = np.zeros(community_count, dtype="uint8")
            np.maximum.at(
                community_accessible,
                attachment_community,
                root_accessible[attachment_root].astype("uint8"),
            )
            isolated_counts[name] += community_accessible == 0
    return {
        name: counts.astype("float32") / draws
        for name, counts in isolated_counts.items()
    }


def cached_targets(
    scenario: str,
    seed: int,
    inputs: dict[str, object],
) -> dict[str, np.ndarray]:
    propensity = np.asarray(inputs["propensities"][scenario], dtype="float32")
    target_definitions = {
        name: np.asarray(inputs["target_definitions"][name], dtype="int32")
        for name in SIMULATION_TARGETS
    }
    signature = content_signature(
        "reviewer-3-comment-6-emergency-backbone-target-v1",
        files=(Path(__file__), SPEC, Path(isolation.__file__)),
        arrays={
            "candidate_u": np.asarray(inputs["candidate_u"]),
            "candidate_v": np.asarray(inputs["candidate_v"]),
            "candidate_edge_section": np.asarray(inputs["candidate_edge_section"]),
            "propensity": propensity,
            "attachment_community": np.asarray(inputs["attachment_community"]),
            "attachment_root": np.asarray(inputs["attachment_root"]),
            **{
                f"target_{slug(name)}": roots
                for name, roots in target_definitions.items()
            },
        },
        parameters={
            "scenario": scenario,
            "seed": seed,
            "draws": DRAWS,
            "root_count": int(inputs["root_count"]),
            "community_count": len(inputs["community"]),
        },
    )
    path = CACHE / f"{scenario.lower()}_seed_{seed}.npz"
    if path.exists():
        cached = np.load(path, allow_pickle=False)
        if cache_matches(cached, signature):
            return {
                name: cached[f"frequency_{slug(name)}"] for name in SIMULATION_TARGETS
            }
    result = simulate_targets(
        candidate_u=np.asarray(inputs["candidate_u"]),
        candidate_v=np.asarray(inputs["candidate_v"]),
        candidate_edge_section=np.asarray(inputs["candidate_edge_section"]),
        propensity=propensity,
        root_count=int(inputs["root_count"]),
        target_definitions=target_definitions,
        attachment_community=np.asarray(inputs["attachment_community"]),
        attachment_root=np.asarray(inputs["attachment_root"]),
        community_count=len(inputs["community"]),
        seed=seed,
        draws=DRAWS,
    )
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        signature=np.asarray(signature),
        **{f"frequency_{slug(name)}": value for name, value in result.items()},
    )
    return result


def cached_legacy_target(
    scenario: str,
    seed: int,
    inputs: dict[str, object],
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
) -> np.ndarray:
    propensity = np.asarray(inputs["propensities"][scenario], dtype="float32")
    roots = np.asarray(
        inputs["target_definitions"][isolation.LEGACY_TARGET_NAME], dtype="int32"
    )
    signature = content_signature(
        "reviewer-3-comment-6-legacy-boundary-pipeline-v1",
        files=(Path(__file__), SPEC, Path(isolation.__file__)),
        arrays={
            "candidate_u": np.asarray(inputs["candidate_u"]),
            "candidate_v": np.asarray(inputs["candidate_v"]),
            "candidate_edge_section": np.asarray(inputs["candidate_edge_section"]),
            "propensity": propensity,
            "target_roots": roots,
            "attachment_community": attachment_community,
            "attachment_root": attachment_root,
        },
        parameters={
            "scenario": scenario,
            "seed": seed,
            "draws": DRAWS,
            "root_count": int(inputs["root_count"]),
            "community_count": community_count,
        },
    )
    path = CACHE / f"legacy_{scenario.lower()}_seed_{seed}.npz"
    if path.exists():
        cached = np.load(path, allow_pickle=False)
        if cache_matches(cached, signature):
            return cached["frequency"].astype("float32")
    frequency = isolation.simulate_isolation(
        np.asarray(inputs["candidate_u"]),
        np.asarray(inputs["candidate_v"]),
        np.asarray(inputs["candidate_edge_section"]),
        propensity,
        int(inputs["root_count"]),
        roots,
        attachment_community,
        attachment_root,
        community_count,
        seed,
        draws=DRAWS,
        report_progress=False,
    )
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, signature=np.asarray(signature), frequency=frequency)
    return frequency


def main() -> None:
    required = [
        SPEC,
        isolation.ADMIN_PATH,
        isolation.ROAD_PATH,
        isolation.EDGE_PATH,
        isolation.NODE_PATH,
        isolation.MESH_PATH,
        isolation.GROUP_PATH,
        Path(isolation.__file__),
        Path(road_exposure.__file__),
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing frozen inputs: {missing}")
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = network_inputs.prepare_inputs()
    target_definitions = {
        name: np.asarray(inputs["target_definitions"][name], dtype="int32")
        for name in TARGETS
    }
    if not set(target_definitions[isolation.LEGACY_TARGET_NAME]).issubset(
        set(target_definitions[isolation.PRIMARY_TARGET_NAME])
    ):
        raise RuntimeError("Legacy target roots are not nested in the primary backbone roots")
    if not set(target_definitions[isolation.PRIMARY_TARGET_NAME]).issubset(
        set(target_definitions[isolation.BROADER_TARGET_NAME])
    ):
        raise RuntimeError("Primary target roots are not nested in the broader backbone roots")

    membership = inputs["edges"]["Emergency Route Membership"].astype("string")
    primary_edge = membership.eq("Primary Emergency Road").to_numpy()
    primary_nodes = np.unique(
        np.concatenate(
            [
                np.asarray(inputs["edge_u"])[primary_edge],
                np.asarray(inputs["edge_v"])[primary_edge],
            ]
        )
    )
    boundary = shapely.boundary(inputs["admin_union"])
    legacy_boundary_nodes = primary_nodes[
        shapely.distance(np.asarray(inputs["node_geometry"])[primary_nodes], boundary)
        <= 0.02
    ]
    legacy_components = set(
        inputs["nodes"]
        .iloc[legacy_boundary_nodes]["Network Component ID"]
        .astype(str)
        .unique()
    )
    (
        legacy_community,
        legacy_attachment_community,
        legacy_attachment_root,
        legacy_diagnostics,
        _,
        _,
    ) = isolation.build_baseline_communities(
        inputs["nodes"],
        np.asarray(inputs["node_geometry"]),
        np.asarray(inputs["stable_labels"]),
        legacy_components,
    )

    blocks: dict[tuple[str, int], dict[str, np.ndarray]] = {}
    for scenario in SCENARIOS:
        for seed in isolation.REPLICATE_SEEDS:
            print(f"Simulating {scenario} / seed {seed} ({DRAWS:,} common draws)", flush=True)
            blocks[(scenario, seed)] = cached_targets(scenario, seed, inputs)
    legacy_blocks: dict[tuple[str, int], np.ndarray] = {}
    for scenario in SCENARIOS:
        for seed in isolation.REPLICATE_SEEDS:
            print(
                f"Reproducing legacy {scenario} / seed {seed} ({DRAWS:,} draws)",
                flush=True,
            )
            legacy_blocks[(scenario, seed)] = cached_legacy_target(
                scenario,
                seed,
                inputs,
                legacy_attachment_community,
                legacy_attachment_root,
                len(legacy_community),
            )

    short_multi = simulate_targets(
        candidate_u=np.asarray(inputs["candidate_u"]),
        candidate_v=np.asarray(inputs["candidate_v"]),
        candidate_edge_section=np.asarray(inputs["candidate_edge_section"]),
        propensity=np.asarray(inputs["propensities"]["Heavy"]),
        root_count=int(inputs["root_count"]),
        target_definitions={
            isolation.PRIMARY_TARGET_NAME: target_definitions[isolation.PRIMARY_TARGET_NAME]
        },
        attachment_community=np.asarray(inputs["attachment_community"]),
        attachment_root=np.asarray(inputs["attachment_root"]),
        community_count=len(inputs["community"]),
        seed=isolation.REPLICATE_SEEDS[0],
        draws=50,
    )[isolation.PRIMARY_TARGET_NAME]
    short_reference = isolation.simulate_isolation(
        np.asarray(inputs["candidate_u"]),
        np.asarray(inputs["candidate_v"]),
        np.asarray(inputs["candidate_edge_section"]),
        np.asarray(inputs["propensities"]["Heavy"]),
        int(inputs["root_count"]),
        target_definitions[isolation.PRIMARY_TARGET_NAME],
        np.asarray(inputs["attachment_community"]),
        np.asarray(inputs["attachment_root"]),
        len(inputs["community"]),
        isolation.REPLICATE_SEEDS[0],
        draws=50,
        report_progress=False,
    )
    exact_short_reproduction = bool(np.array_equal(short_multi, short_reference))
    if not exact_short_reproduction:
        raise RuntimeError("Multi-target implementation does not reproduce production isolation")

    primary_community = inputs["community"].copy()
    cohorts = {
        isolation.PRIMARY_TARGET_NAME: primary_community,
        isolation.BROADER_TARGET_NAME: primary_community,
        isolation.LEGACY_TARGET_NAME: legacy_community,
    }
    summary_rows: list[dict[str, object]] = []
    community_rows: list[dict[str, object]] = []
    monotone_pass = True
    mean_frequencies: dict[tuple[str, str], np.ndarray] = {}
    for target in TARGETS:
        for scenario in SCENARIOS:
            matrix = np.vstack(
                [
                    legacy_blocks[(scenario, seed)]
                    if target == isolation.LEGACY_TARGET_NAME
                    else blocks[(scenario, seed)][target]
                    for seed in isolation.REPLICATE_SEEDS
                ]
            )
            mean_frequency = matrix.mean(axis=0)
            mean_frequencies[(target, scenario)] = mean_frequency

    for target in TARGETS:
        for lower, upper in zip(SCENARIOS[:-1], SCENARIOS[1:]):
            if np.any(
                mean_frequencies[(target, lower)]
                > mean_frequencies[(target, upper)] + 1e-7
            ):
                monotone_pass = False
    if not monotone_pass:
        raise RuntimeError("Scenario monotonicity failed for at least one target")

    for scenario in SCENARIOS:
        primary_frequency = mean_frequencies[(isolation.PRIMARY_TARGET_NAME, scenario)]
        primary_population = primary_community["Total_Population"].to_numpy(dtype=float)
        primary_burden = primary_population * primary_frequency
        for target in TARGETS:
            community = cohorts[target]
            population = community["Total_Population"].to_numpy(dtype=float)
            older = community["Population_Age_65"].to_numpy(dtype=float)
            matrix = np.vstack(
                [
                    legacy_blocks[(scenario, seed)]
                    if target == isolation.LEGACY_TARGET_NAME
                    else blocks[(scenario, seed)][target]
                    for seed in isolation.REPLICATE_SEEDS
                ]
            )
            mean_frequency = mean_frequencies[(target, scenario)]
            population_by_seed = matrix @ population
            older_by_seed = matrix @ older
            burden = population * mean_frequency
            summary_rows.append(
                {
                    "target_definition": target,
                    "scenario": scenario,
                    "target_root_count": len(target_definitions[target]),
                    "eligible_community_count": len(community),
                    "eligible_mesh_count": int(
                        legacy_diagnostics["Baseline-Eligible Meshes"]
                        if target == isolation.LEGACY_TARGET_NAME
                        else inputs["diagnostics"]["Baseline-Eligible Meshes"]
                    ),
                    "eligible_population": float(
                        legacy_diagnostics["Eligible Population"]
                        if target == isolation.LEGACY_TARGET_NAME
                        else inputs["diagnostics"]["Eligible Population"]
                    ),
                    "seed_count": len(isolation.REPLICATE_SEEDS),
                    "draws_per_seed": DRAWS,
                    "expected_isolated_population_mean": float(population_by_seed.mean()),
                    "expected_isolated_population_min": float(population_by_seed.min()),
                    "expected_isolated_population_max": float(population_by_seed.max()),
                    "expected_isolated_population_sd": float(population_by_seed.std(ddof=1)),
                    "expected_isolated_age65_mean": float(older_by_seed.mean()),
                    "expected_isolated_age65_min": float(older_by_seed.min()),
                    "expected_isolated_age65_max": float(older_by_seed.max()),
                    "expected_isolated_age65_sd": float(older_by_seed.std(ddof=1)),
                    "positive_frequency_communities": int(np.count_nonzero(mean_frequency > 0)),
                    "frequency_spearman_vs_primary": (
                        float("nan")
                        if target == isolation.LEGACY_TARGET_NAME
                        else safe_spearman(mean_frequency, primary_frequency)
                    ),
                    "top30_population_burden_overlap_vs_primary": (
                        float("nan")
                        if target == isolation.LEGACY_TARGET_NAME
                        else top_n_overlap(burden, primary_burden)
                    ),
                }
            )
            for row_index, row in community.iterrows():
                community_rows.append(
                    {
                        "target_definition": target,
                        "scenario": scenario,
                        "community_id": row["Community ID"],
                        "longitude": float(row["Longitude"]),
                        "latitude": float(row["Latitude"]),
                        "total_population": float(row["Total_Population"]),
                        "population_age65": float(row["Population_Age_65"]),
                        "mean_isolation_frequency": float(mean_frequency[row_index]),
                        "expected_isolated_population": float(burden[row_index]),
                    }
                )

    summary = pd.DataFrame(summary_rows)
    community_output = pd.DataFrame(community_rows)
    target_summary = pd.DataFrame(
        [
            {
                "target_definition": name,
                "role": (
                    "primary operational estimand"
                    if name == isolation.PRIMARY_TARGET_NAME
                    else "broader robustness comparator"
                    if name == isolation.BROADER_TARGET_NAME
                    else "audit-only superseded proxy"
                ),
                "target_root_count": len(target_definitions[name]),
                "is_primary_subset": bool(
                    set(target_definitions[name]).issubset(
                        set(target_definitions[isolation.PRIMARY_TARGET_NAME])
                    )
                ),
                "primary_is_subset": bool(
                    set(target_definitions[isolation.PRIMARY_TARGET_NAME]).issubset(
                        set(target_definitions[name])
                    )
                ),
            }
            for name in TARGETS
        ]
    )
    summary_path = OUT / "isolation_target_sensitivity_summary.csv"
    community_path = OUT / "isolation_target_sensitivity_community.csv"
    target_path = OUT / "target_definition_audit.csv"
    summary.to_csv(summary_path, index=False, float_format="%.10g")
    community_output.to_csv(community_path, index=False, float_format="%.10g")
    target_summary.to_csv(target_path, index=False)

    decision = {
        "decision_record": DECISION_RECORD,
        "primary_target": isolation.PRIMARY_TARGET_NAME,
        "broader_comparator": isolation.BROADER_TARGET_NAME,
        "legacy_audit_target": isolation.LEGACY_TARGET_NAME,
        "community_count": int(len(primary_community)),
        "eligible_mesh_count": int(inputs["diagnostics"]["Baseline-Eligible Meshes"]),
        "eligible_population": float(inputs["diagnostics"]["Eligible Population"]),
        "exact_short_production_reproduction": exact_short_reproduction,
        "scenario_monotonicity_pass": monotone_pass,
        "target_nesting_pass": True,
        "legacy_pipeline_community_count": int(len(legacy_community)),
        "legacy_pipeline_eligible_population": float(
            legacy_diagnostics["Eligible Population"]
        ),
        "baseline_ineligible_excluded": True,
        "status": "pass",
    }
    decision_path = OUT / "decision.json"
    decision_path.write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")

    input_rows = []
    for path in required:
        input_rows.append(
            {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
        )
    input_rows.extend(
        {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
        for path in (
            ROOT / "data/results/intermediate/road_disruption_scores_normalized_v4_y075.npz",
            Path(network_inputs.__file__),
        )
        if path.exists()
    )
    input_path = OUT / "input_hashes.csv"
    pd.DataFrame(input_rows).drop_duplicates("path").to_csv(input_path, index=False)

    report_lines = [
        "# Reviewer 3 Comment 6 Target Audit",
        "",
        f"- Decision record: `{DECISION_RECORD}`",
        f"- Status: **{decision['status']}**",
        f"- Primary target: {isolation.PRIMARY_TARGET_NAME}",
        f"- Broader comparator: {isolation.BROADER_TARGET_NAME}",
        f"- Audit-only legacy target: {isolation.LEGACY_TARGET_NAME}",
        f"- Eligible communities: {len(primary_community):,}",
        f"- Eligible meshes: {int(inputs['diagnostics']['Baseline-Eligible Meshes']):,}",
        f"- Eligible population: {float(inputs['diagnostics']['Eligible Population']):,.1f}",
        f"- Production reproduction check: {exact_short_reproduction}",
        f"- Scenario monotonicity: {monotone_pass}",
        f"- Target nesting: legacy subset primary subset broader = True",
        f"- Legacy pipeline cohort: {len(legacy_community):,} communities and "
        f"{float(legacy_diagnostics['Eligible Population']):,.1f} residents",
        "",
        "## Five-seed results",
        "",
    ]
    for row in summary.itertuples(index=False):
        report_lines.append(
            f"- {row.target_definition}; {row.scenario}: expected isolated population "
            f"{row.expected_isolated_population_mean:,.1f} "
            f"({row.expected_isolated_population_min:,.1f}–"
            f"{row.expected_isolated_population_max:,.1f}); age 65+ "
            f"{row.expected_isolated_age65_mean:,.1f}; Spearman vs primary "
            f"{row.frequency_spearman_vs_primary:.3f}; top-30 overlap "
            f"{row.top30_population_burden_overlap_vs_primary:.1%}."
        )
    report_path = OUT / "audit_report.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Saved {summary_path.relative_to(ROOT)}")
    print(f"Saved {community_path.relative_to(ROOT)}")
    print(f"Saved {target_path.relative_to(ROOT)}")
    print(f"Saved {decision_path.relative_to(ROOT)}")
    print(f"Saved {input_path.relative_to(ROOT)}")
    print(f"Saved {report_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
