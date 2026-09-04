#!/usr/bin/env python3
"""Validate the Reviewer 1 Comment 2 Yatsushiro midpoint sensitivity."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import warnings

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from cache_fingerprint import cache_matches, content_signature
import figure_basic_service_reachability_loss as service
import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_intervention_priorities_and_budgeted_benefits as intervention
import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure
import revision_spatially_correlated_closure_sensitivity as network_inputs


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "Rev/docs/analysis-spec-reviewer-1-comment-2.md"
OUT = ROOT / "data/exp/revision/reviewer-1-comment-2"
CACHE = OUT / "cache"
FACTORS = (0.70, 0.75, 0.80)
SEEDS = isolation.REPLICATE_SEEDS
SERVICES = service.SERVICE_CLASSES
MAGNITUDE_LIMIT = 0.10
RANK_LIMIT = 0.95
TOP_OVERLAP_LIMIT = 0.80
CANDIDATE_OVERLAP_LIMIT = 0.95


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def factor_tag(factor: float) -> str:
    return f"{int(round(factor * 100)):02d}"


def safe_spearman(left: np.ndarray, right: np.ndarray) -> float:
    valid = np.isfinite(left) & np.isfinite(right)
    if valid.sum() < 3:
        return float("nan")
    if np.unique(left[valid]).size < 2 or np.unique(right[valid]).size < 2:
        return float("nan")
    return float(spearmanr(left[valid], right[valid]).statistic)


def top_overlap(left: np.ndarray, right: np.ndarray, count: int) -> float:
    count = min(count, len(left), len(right))
    left_values = np.nan_to_num(left, nan=-np.inf)
    right_values = np.nan_to_num(right, nan=-np.inf)
    left_top = set(np.argsort(left_values, kind="stable")[-count:].tolist())
    right_top = set(np.argsort(right_values, kind="stable")[-count:].tolist())
    return float(len(left_top & right_top) / count)


def relative_change(value: float, reference: float) -> float:
    return float(value / reference - 1.0)


def load_npz(path: Path) -> np.lib.npyio.NpzFile:
    cached = np.load(path, allow_pickle=False)
    if "signature" not in cached.files:
        raise RuntimeError(f"Cache lacks a signature: {path}")
    return cached


def isolation_cache_path(factor: float, seed: int) -> Path:
    prefix = "central" if factor == 0.75 else f"yatsushiro_{factor_tag(factor)}"
    return (
        isolation.SIMULATION_CACHE_DIR
        / f"{prefix}_heavy_seed_{seed}_m{isolation.MONTE_CARLO_DRAWS}.npz"
    )


def service_cache_path(factor: float, seed: int) -> Path:
    prefix = "central" if factor == 0.75 else f"yatsushiro_{factor_tag(factor)}"
    return service.SERVICE_LOSS_CACHE_DIR / f"{prefix}_seed_{seed}.npz"


def expected_isolation_signature(
    inputs: dict[str, object], propensity: np.ndarray, seed: int
) -> str:
    return content_signature(
        "community-isolation-event-idw-v3",
        files=(Path(isolation.__file__),),
        arrays={
            "candidate_u": np.asarray(inputs["candidate_u"]),
            "candidate_v": np.asarray(inputs["candidate_v"]),
            "candidate_edge_section": np.asarray(inputs["candidate_edge_section"]),
            "section_propensity": propensity,
            "target_roots": np.asarray(inputs["target_roots"]),
            "attachment_community": np.asarray(inputs["attachment_community"]),
            "attachment_root": np.asarray(inputs["attachment_root"]),
        },
        parameters={
            "root_count": int(inputs["root_count"]),
            "community_count": len(inputs["community"]),
            "seed": int(seed),
            "draws": isolation.MONTE_CARLO_DRAWS,
        },
    )


def expected_service_signature(
    *,
    inputs: dict[str, object],
    propensity: np.ndarray,
    pair_reduction: dict[str, np.ndarray],
    service_roots: dict[str, np.ndarray],
    seed: int,
    cache_tag: str,
) -> str:
    return content_signature(
        "service-reachability-event-idw-v3",
        files=(Path(service.__file__),),
        arrays={
            "section_propensity": propensity,
            "pair_order": pair_reduction["order"],
            "pair_start": pair_reduction["start"],
            "pair_u": pair_reduction["pair_u"],
            "pair_v": pair_reduction["pair_v"],
            "pair_edge_section": pair_reduction["edge_section"],
            "pair_edge_time": pair_reduction["edge_time"],
            "attachment_community": np.asarray(inputs["attachment_community"]),
            "attachment_root": np.asarray(inputs["attachment_root"]),
            **{f"service_roots_{name}": service_roots[name] for name in SERVICES},
        },
        parameters={
            "root_count": int(inputs["root_count"]),
            "community_count": len(inputs["community"]),
            "draws": isolation.MONTE_CARLO_DRAWS,
            "seed": int(seed),
            "cache_tag": cache_tag,
        },
    )


def cached_intervention_frequency(
    *,
    factor: float,
    seed: int,
    propensity: np.ndarray,
    inputs: dict[str, object],
) -> np.ndarray:
    signature = content_signature(
        "reviewer-1-comment-2-yatsushiro-intervention-v1",
        files=(Path(__file__), SPEC, Path(isolation.__file__)),
        arrays={
            "candidate_u": np.asarray(inputs["candidate_u"]),
            "candidate_v": np.asarray(inputs["candidate_v"]),
            "candidate_edge_section": np.asarray(inputs["candidate_edge_section"]),
            "section_propensity": propensity,
            "target_roots": np.asarray(inputs["target_roots"]),
            "attachment_community": np.asarray(inputs["attachment_community"]),
            "attachment_root": np.asarray(inputs["attachment_root"]),
        },
        parameters={
            "factor": factor,
            "seed": int(seed),
            "draws": isolation.MONTE_CARLO_DRAWS,
            "root_count": int(inputs["root_count"]),
            "community_count": len(inputs["community"]),
        },
    )
    path = CACHE / f"intervention_y{factor_tag(factor)}_seed_{seed}.npz"
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
        np.asarray(inputs["target_roots"]),
        np.asarray(inputs["attachment_community"]),
        np.asarray(inputs["attachment_root"]),
        len(inputs["community"]),
        seed,
        draws=isolation.MONTE_CARLO_DRAWS,
        report_progress=False,
    )
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, signature=np.asarray(signature), frequency=frequency)
    return frequency


def main() -> None:
    terrain_paths = {
        factor: road_exposure.INTERMEDIATE
        / f"landslide_score_grids_event_idw_v4_y{int(round(factor * 100)):03d}.npz"
        for factor in FACTORS
    }
    road_paths = {
        factor: road_exposure.INTERMEDIATE
        / f"road_disruption_scores_normalized_v4_y{int(round(factor * 100)):03d}.npz"
        for factor in FACTORS
    }
    production_paths = [*terrain_paths.values(), *road_paths.values()]
    production_paths.extend(
        isolation_cache_path(factor, seed) for factor in FACTORS for seed in SEEDS
    )
    production_paths.extend(
        service_cache_path(factor, seed) for factor in FACTORS for seed in SEEDS
    )
    production_paths.append(intervention.SINGLE_CLOSE_CACHE)
    required = [SPEC, *production_paths]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing frozen inputs: {missing}")
    before_hashes = {path: sha256(path) for path in production_paths}

    inputs = network_inputs.prepare_inputs()
    community = inputs["community"]
    population = community["Total_Population"].to_numpy(dtype=float)
    older = community["Population_Age_65"].to_numpy(dtype=float)
    if len(community) != 4_346:
        raise RuntimeError("The current Primary Emergency Road cohort is not 4,346 communities")

    roads = pd.read_parquet(
        isolation.ROAD_PATH,
        columns=[
            "Road Section ID",
            "Road Section Length (m)",
            "Road Category",
            "Emergency Route Membership",
            "Network Analysis Eligible",
        ],
    )
    roads = roads.loc[roads["Network Analysis Eligible"]].reset_index(drop=True)
    terrain_scores = {
        factor: {
            scenario: load_npz(terrain_paths[factor])[f"score_{scenario}"].astype("float32")
            for scenario in ("Moderate", "Heavy", "Extreme")
        }
        for factor in FACTORS
    }
    road_scores = {
        factor: {
            scenario: load_npz(road_paths[factor])[f"score_{scenario}"].astype("float32")
            for scenario in ("Moderate", "Heavy", "Extreme")
        }
        for factor in FACTORS
    }
    central_heavy = road_scores[0.75]["Heavy"]
    central_candidate_mask = np.isfinite(central_heavy) & (
        central_heavy >= float(inputs["heavy_lower"])
    )
    central_candidate_ids = roads.loc[central_candidate_mask, "Road Section ID"].reset_index(
        drop=True
    )
    if not central_candidate_ids.equals(inputs["candidate_ids"]):
        raise RuntimeError("Central candidate IDs do not reproduce the current network inputs")
    candidate_index = roads.index[central_candidate_mask].to_numpy(dtype="int32")

    propensities = {
        factor: isolation.closure_propensity(
            road_scores[factor]["Heavy"][central_candidate_mask],
            float(inputs["heavy_lower"]),
            float(inputs["heavy_upper"]),
        )
        for factor in FACTORS
    }

    edge_frame = pd.read_parquet(
        isolation.EDGE_PATH,
        columns=[
            "Road Section ID",
            "Baseline Edge Travel Time (min)",
            "Network Analysis Eligible",
        ],
    )
    edge_frame = edge_frame.loc[edge_frame["Network Analysis Eligible"]].reset_index(drop=True)
    edge_candidate = edge_frame["Road Section ID"].isin(central_candidate_ids).to_numpy()
    candidate_position = pd.Series(
        np.arange(len(central_candidate_ids), dtype="int32"), index=central_candidate_ids
    )
    edge_section = (
        edge_frame.loc[edge_candidate, "Road Section ID"]
        .map(candidate_position)
        .to_numpy(dtype="int32")
    )
    edge_time = edge_frame.loc[
        edge_candidate, "Baseline Edge Travel Time (min)"
    ].to_numpy(dtype="float64")
    raw_u = np.asarray(inputs["stable_labels"])[np.asarray(inputs["edge_u"])[edge_candidate]]
    raw_v = np.asarray(inputs["stable_labels"])[np.asarray(inputs["edge_v"])[edge_candidate]]
    between = raw_u != raw_v
    if not np.array_equal(raw_u[between], np.asarray(inputs["candidate_u"])):
        raise RuntimeError("Contracted candidate-u reconstruction failed")
    if not np.array_equal(raw_v[between], np.asarray(inputs["candidate_v"])):
        raise RuntimeError("Contracted candidate-v reconstruction failed")
    if not np.array_equal(edge_section[between], np.asarray(inputs["candidate_edge_section"])):
        raise RuntimeError("Contracted candidate-section reconstruction failed")
    pair_reduction = service.prepare_pair_reduction(
        raw_u[between], raw_v[between], edge_section[between], edge_time[between], int(inputs["root_count"])
    )
    service_geometry, _ = service.service_geometries()
    service_roots, _, _ = service.attach_services_to_roots(
        service_geometry,
        np.asarray(inputs["node_geometry"]),
        np.asarray(inputs["stable_labels"]),
    )

    isolation_seed_frequency: dict[float, list[np.ndarray]] = {}
    isolation_signature_pass = True
    for factor in FACTORS:
        isolation_seed_frequency[factor] = []
        for seed in SEEDS:
            path = isolation_cache_path(factor, seed)
            cached = load_npz(path)
            expected = expected_isolation_signature(inputs, propensities[factor], seed)
            isolation_signature_pass &= cache_matches(cached, expected)
            isolation_seed_frequency[factor].append(cached["frequency"].astype("float32"))
    if not isolation_signature_pass:
        raise RuntimeError("At least one Yatsushiro isolation cache is stale")

    service_seed_loss: dict[float, dict[str, list[np.ndarray]]] = {
        factor: {name: [] for name in SERVICES} for factor in FACTORS
    }
    service_signature_pass = True
    for factor in FACTORS:
        cache_tag = "central" if factor == 0.75 else f"yatsushiro_{factor_tag(factor)}"
        for seed in SEEDS:
            cached = load_npz(service_cache_path(factor, seed))
            expected = expected_service_signature(
                inputs=inputs,
                propensity=propensities[factor],
                pair_reduction=pair_reduction,
                service_roots=service_roots,
                seed=seed,
                cache_tag=cache_tag,
            )
            service_signature_pass &= cache_matches(cached, expected)
            for name in SERVICES:
                service_seed_loss[factor][name].append(
                    cached[f"loss_{name}"].astype("float32")
                )
    if not service_signature_pass:
        raise RuntimeError("At least one Yatsushiro service cache is stale")

    isolation_mean = {
        factor: np.mean(np.vstack(isolation_seed_frequency[factor]), axis=0)
        for factor in FACTORS
    }
    isolation_rows: list[dict[str, object]] = []
    central_burden = population * isolation_mean[0.75]
    central_total = float(np.sum(central_burden))
    central_older = float(np.sum(older * isolation_mean[0.75]))
    for factor in FACTORS:
        mean_frequency = isolation_mean[factor]
        totals = np.asarray(
            [np.sum(population * values) for values in isolation_seed_frequency[factor]],
            dtype=float,
        )
        older_totals = np.asarray(
            [np.sum(older * values) for values in isolation_seed_frequency[factor]],
            dtype=float,
        )
        isolation_rows.append(
            {
                "yatsushiro_factor": factor,
                "expected_disconnected_population": float(totals.mean()),
                "seed_min": float(totals.min()),
                "seed_max": float(totals.max()),
                "seed_sd": float(totals.std(ddof=1)),
                "relative_change_vs_midpoint": relative_change(float(totals.mean()), central_total),
                "expected_disconnected_age65": float(older_totals.mean()),
                "age65_relative_change_vs_midpoint": relative_change(
                    float(older_totals.mean()), central_older
                ),
                "community_frequency_spearman_vs_midpoint": safe_spearman(
                    mean_frequency, isolation_mean[0.75]
                ),
                "top30_population_burden_overlap_vs_midpoint": top_overlap(
                    population * mean_frequency, central_burden, 30
                ),
                "maximum_community_frequency_change": float(
                    np.max(np.abs(mean_frequency - isolation_mean[0.75]))
                ),
            }
        )
    isolation_summary = pd.DataFrame(isolation_rows)

    service_rows: list[dict[str, object]] = []
    for name in SERVICES:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            central_frequency = np.nanmean(
                np.stack(service_seed_loss[0.75][name]), axis=0
            )
        central_service_total = float(np.nansum(population * central_frequency))
        central_service_burden = population * central_frequency
        for factor in FACTORS:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                mean_frequency = np.nanmean(
                    np.stack(service_seed_loss[factor][name]), axis=0
                )
            totals = np.asarray(
                [np.nansum(population * values) for values in service_seed_loss[factor][name]],
                dtype=float,
            )
            service_rows.append(
                {
                    "service_class": name,
                    "yatsushiro_factor": factor,
                    "expected_affected_population": float(totals.mean()),
                    "seed_min": float(totals.min()),
                    "seed_max": float(totals.max()),
                    "seed_sd": float(totals.std(ddof=1)),
                    "relative_change_vs_midpoint": relative_change(
                        float(totals.mean()), central_service_total
                    ),
                    "frequency_spearman_vs_midpoint": safe_spearman(
                        mean_frequency, central_frequency
                    ),
                    "top30_population_burden_overlap_vs_midpoint": top_overlap(
                        population * mean_frequency, central_service_burden, 30
                    ),
                    "maximum_community_frequency_change": float(
                        np.nanmax(np.abs(mean_frequency - central_frequency))
                    ),
                    "interpretation": (
                        "conditional on 10/36 geolocated destinations"
                        if name == "Emergency water"
                        else "primary service consequence"
                    ),
                }
            )
    service_summary = pd.DataFrame(service_rows)

    score_rows: list[dict[str, object]] = []
    for level, scores in (("Slope", terrain_scores), ("Road", road_scores)):
        for scenario in ("Moderate", "Heavy", "Extreme"):
            central = scores[0.75][scenario].astype(float)
            for factor in (0.70, 0.80):
                bound = scores[factor][scenario].astype(float)
                valid = np.isfinite(central) & np.isfinite(bound)
                if level == "Road":
                    valid &= (central > 0) & (bound > 0)
                changed = valid & (np.abs(bound - central) > 1e-12)
                row: dict[str, object] = {
                    "level": level,
                    "scenario": scenario,
                    "yatsushiro_factor": factor,
                    "valid_units": int(valid.sum()),
                    "changed_units": int(changed.sum()),
                    "spearman_vs_midpoint": safe_spearman(central[valid], bound[valid]),
                    "maximum_absolute_score_change": float(
                        np.max(np.abs(bound[valid] - central[valid]))
                    ),
                    "midpoint_mean_on_changed_support": float(np.mean(central[changed])),
                    "bound_mean_on_changed_support": float(np.mean(bound[changed])),
                }
                if level == "Road":
                    supported_positions = np.flatnonzero(valid)
                    top_count = max(1, int(np.ceil(len(supported_positions) * 0.01)))
                    row["top1pct_overlap_vs_midpoint"] = top_overlap(
                        central[supported_positions], bound[supported_positions], top_count
                    )
                    bound_positive = bound[np.isfinite(bound) & (bound > 0)]
                    bound_candidate = np.isfinite(bound) & (
                        bound >= np.quantile(bound_positive, isolation.CANDIDATE_QUANTILE)
                    )
                    intersection = int(np.count_nonzero(central_candidate_mask & bound_candidate))
                    row["central_candidate_overlap"] = float(
                        intersection / np.count_nonzero(central_candidate_mask)
                    )
                    row["candidate_jaccard"] = float(
                        intersection / np.count_nonzero(central_candidate_mask | bound_candidate)
                    )
                else:
                    row["top1pct_overlap_vs_midpoint"] = np.nan
                    row["central_candidate_overlap"] = np.nan
                    row["candidate_jaccard"] = np.nan
                score_rows.append(row)
    score_summary = pd.DataFrame(score_rows)

    root_degree = np.bincount(
        np.concatenate([np.asarray(inputs["candidate_u"]), np.asarray(inputs["candidate_v"])]),
        minlength=int(inputs["root_count"]),
    ).astype(float)
    section_scarcity = np.zeros(len(central_candidate_ids), dtype="float64")
    edge_scarcity = 1.0 / np.sqrt(
        np.maximum(
            np.minimum(
                root_degree[np.asarray(inputs["candidate_u"])],
                root_degree[np.asarray(inputs["candidate_v"])],
            ),
            1.0,
        )
    )
    np.maximum.at(
        section_scarcity, np.asarray(inputs["candidate_edge_section"]), edge_scarcity
    )
    emergency_candidate = (
        roads.loc[candidate_index, "Emergency Route Membership"]
        .astype("string")
        .ne("None")
        .to_numpy()
    )
    candidate_length_km = (
        roads.loc[candidate_index, "Road Section Length (m)"].to_numpy(dtype=float) / 1000.0
    )
    candidate_category = roads.loc[candidate_index, "Road Category"].reset_index(drop=True)

    central_section_burden = intervention.section_burden_from_frequency(
        isolation_mean[0.75],
        population,
        np.asarray(inputs["attachment_community"]),
        np.asarray(inputs["attachment_root"]),
        np.asarray(inputs["candidate_u"]),
        np.asarray(inputs["candidate_v"]),
        np.asarray(inputs["candidate_edge_section"]),
        int(inputs["root_count"]),
        len(central_candidate_ids),
    )
    preliminary = (
        road_scores[0.75]["Heavy"][central_candidate_mask]
        * np.log1p(central_section_burden)
        * (1.0 + section_scarcity)
        * np.where(emergency_candidate, 1.20, 1.0)
    )
    screen_positions = np.argsort(preliminary)[-intervention.SINGLE_CLOSE_SCREEN_COUNT :]
    expected_single_signature = intervention.single_close_signature(
        screen_positions,
        np.asarray(inputs["candidate_u"]),
        np.asarray(inputs["candidate_v"]),
        np.asarray(inputs["candidate_edge_section"]),
        int(inputs["root_count"]),
        np.asarray(inputs["target_roots"]),
        np.asarray(inputs["attachment_community"]),
        np.asarray(inputs["attachment_root"]),
        population,
    )
    single_cache = load_npz(intervention.SINGLE_CLOSE_CACHE)
    single_signature_pass = cache_matches(single_cache, expected_single_signature)
    if not single_signature_pass:
        raise RuntimeError("Single-section intervention cache is stale")
    single_close = single_cache["single_close_population"].astype("float64")

    priority_scores: dict[float, np.ndarray] = {}
    priority_orders: dict[float, np.ndarray] = {}
    actions_by_factor: dict[float, np.ndarray] = {}
    costs_by_factor: dict[float, np.ndarray] = {}
    for factor in FACTORS:
        section_burden = intervention.section_burden_from_frequency(
            isolation_mean[factor],
            population,
            np.asarray(inputs["attachment_community"]),
            np.asarray(inputs["attachment_root"]),
            np.asarray(inputs["candidate_u"]),
            np.asarray(inputs["candidate_v"]),
            np.asarray(inputs["candidate_edge_section"]),
            int(inputs["root_count"]),
            len(central_candidate_ids),
        )
        consequence = single_close + 0.15 * section_burden
        candidate_score = road_scores[factor]["Heavy"][central_candidate_mask]
        actions = intervention.action_assignment(
            roads.loc[candidate_index, "Emergency Route Membership"],
            candidate_score,
            float(inputs["heavy_upper"]),
            section_scarcity,
        )
        base_cost = np.select(
            [
                actions == "Temporary reinforcement",
                actions == "Alternative-route protection",
            ],
            [3.0 + 2.0 * candidate_length_km, 2.5 + 1.2 * candidate_length_km],
            default=1.5 + 0.5 * candidate_length_km,
        ).astype("float64")
        score = intervention.assigned_action_priority_score(consequence, actions, base_cost)
        priority_scores[factor] = score
        priority_orders[factor] = np.argsort(score)[::-1]
        actions_by_factor[factor] = actions
        costs_by_factor[factor] = base_cost

    central_portfolio = priority_orders[0.75][: intervention.PORTFOLIO_CANDIDATE_COUNT]
    budget = float(costs_by_factor[0.75][central_portfolio[:100]].sum())
    intervention_rows: list[dict[str, object]] = []
    protected_means: dict[float, float] = {}
    for factor in FACTORS:
        factor_portfolio = priority_orders[factor][: intervention.PORTFOLIO_CANDIDATE_COUNT]
        selected, spent = intervention.select_under_budget(
            factor_portfolio, costs_by_factor[factor], budget
        )
        effects = np.asarray(
            [
                intervention.ACTION_EFFECT[str(action)]["Central"]
                for action in actions_by_factor[factor]
            ],
            dtype=float,
        )
        adjusted = propensities[factor].copy()
        adjusted[selected] *= 1.0 - effects[selected]
        protected = []
        for seed, baseline in zip(SEEDS, isolation_seed_frequency[factor]):
            revised = cached_intervention_frequency(
                factor=factor,
                seed=seed,
                propensity=adjusted,
                inputs=inputs,
            )
            protected.append(
                float(np.sum(population * np.maximum(baseline - revised, 0.0)))
            )
        protected_means[factor] = float(np.mean(protected))
        intervention_rows.append(
            {
                "yatsushiro_factor": factor,
                "fixed_budget_planning_units": budget,
                "spent_planning_units": spent,
                "selected_road_count": len(selected),
                "priority_spearman_vs_midpoint": safe_spearman(
                    priority_scores[factor], priority_scores[0.75]
                ),
                "top150_priority_overlap_vs_midpoint": top_overlap(
                    priority_scores[factor],
                    priority_scores[0.75],
                    intervention.PORTFOLIO_CANDIDATE_COUNT,
                ),
                "protected_population_mean": float(np.mean(protected)),
                "protected_population_min": float(np.min(protected)),
                "protected_population_max": float(np.max(protected)),
                "protected_population_sd": float(np.std(protected, ddof=1)),
                "action_changes_vs_midpoint": int(
                    np.count_nonzero(actions_by_factor[factor] != actions_by_factor[0.75])
                ),
            }
        )
    intervention_summary = pd.DataFrame(intervention_rows)
    intervention_summary["protected_population_relative_change_vs_midpoint"] = (
        intervention_summary["protected_population_mean"] / protected_means[0.75] - 1.0
    )

    bound_isolation = isolation_summary[isolation_summary["yatsushiro_factor"] != 0.75]
    bound_services = service_summary[service_summary["yatsushiro_factor"] != 0.75]
    bound_roads = score_summary[
        (score_summary["level"] == "Road") & (score_summary["scenario"] == "Heavy")
    ]
    bound_intervention = intervention_summary[
        intervention_summary["yatsushiro_factor"] != 0.75
    ]
    gates = {
        "production_cache_hashes_unchanged": True,
        "isolation_cache_signatures_current": bool(isolation_signature_pass),
        "service_cache_signatures_current": bool(service_signature_pass),
        "single_close_cache_signature_current": bool(single_signature_pass),
        "isolation_magnitude_within_10pct": bool(
            bound_isolation["relative_change_vs_midpoint"].abs().max() <= MAGNITUDE_LIMIT
            and bound_isolation["age65_relative_change_vs_midpoint"].abs().max()
            <= MAGNITUDE_LIMIT
        ),
        "isolation_rank_stable": bool(
            bound_isolation["community_frequency_spearman_vs_midpoint"].min() >= RANK_LIMIT
            and bound_isolation["top30_population_burden_overlap_vs_midpoint"].min()
            >= TOP_OVERLAP_LIMIT
        ),
        "service_magnitude_within_10pct": bool(
            bound_services["relative_change_vs_midpoint"].abs().max() <= MAGNITUDE_LIMIT
        ),
        "service_rank_stable": bool(
            bound_services["frequency_spearman_vs_midpoint"].min() >= RANK_LIMIT
            and bound_services["top30_population_burden_overlap_vs_midpoint"].min()
            >= TOP_OVERLAP_LIMIT
        ),
        "road_rank_and_candidate_stable": bool(
            bound_roads["spearman_vs_midpoint"].min() >= RANK_LIMIT
            and bound_roads["top1pct_overlap_vs_midpoint"].min() >= TOP_OVERLAP_LIMIT
            and bound_roads["central_candidate_overlap"].min() >= CANDIDATE_OVERLAP_LIMIT
        ),
        "intervention_stable": bool(
            bound_intervention["priority_spearman_vs_midpoint"].min() >= RANK_LIMIT
            and bound_intervention["top150_priority_overlap_vs_midpoint"].min()
            >= TOP_OVERLAP_LIMIT
            and bound_intervention[
                "protected_population_relative_change_vs_midpoint"
            ].abs().max()
            <= MAGNITUDE_LIMIT
        ),
    }

    after_hashes = {path: sha256(path) for path in production_paths}
    gates["production_cache_hashes_unchanged"] = before_hashes == after_hashes
    status = "pass" if all(gates.values()) else "review_required"
    OUT.mkdir(parents=True, exist_ok=True)
    isolation_path = OUT / "isolation_sensitivity.csv"
    service_path = OUT / "service_sensitivity.csv"
    score_path = OUT / "slope_road_sensitivity.csv"
    intervention_path = OUT / "intervention_sensitivity.csv"
    isolation_summary.to_csv(isolation_path, index=False, float_format="%.10g")
    service_summary.to_csv(service_path, index=False, float_format="%.10g")
    score_summary.to_csv(score_path, index=False, float_format="%.10g")
    intervention_summary.to_csv(intervention_path, index=False, float_format="%.10g")
    pd.DataFrame(
        [
            {"path": str(path.relative_to(ROOT)), "sha256": after_hashes[path]}
            for path in production_paths
        ]
    ).to_csv(OUT / "input_hashes.csv", index=False)

    decision = {
        "reviewer_id": "reviewer-1",
        "comment_id": "comment-2",
        "central_yatsushiro_factor": 0.75,
        "bounding_factors": [0.70, 0.80],
        "community_count": len(community),
        "eligible_population": float(population.sum()),
        "fixed_intervention_budget_planning_units": budget,
        "gates": gates,
        "status": status,
        "interpretation": (
            "The downstream Heavy-scenario results are not highly sensitive to the "
            "municipality-wide Yatsushiro midpoint within the tested 0.70-0.80 bounds."
            if status == "pass"
            else "At least one prespecified sensitivity gate failed."
        ),
    }
    (OUT / "decision.json").write_text(
        json.dumps(decision, indent=2) + "\n", encoding="utf-8"
    )

    report = [
        "# Reviewer 1 Comment 2 Yatsushiro Midpoint Sensitivity",
        "",
        f"- Status: **{status}**",
        f"- Eligible cohort: {len(community):,} communities and {population.sum():,.0f} residents",
        f"- Production caches unchanged: {gates['production_cache_hashes_unchanged']}",
        f"- Isolation and service cache signatures current: "
        f"{isolation_signature_pass} / {service_signature_pass}",
        "",
        "## Heavy connectivity consequences",
        "",
    ]
    for row in isolation_summary.itertuples(index=False):
        report.append(
            f"- f={row.yatsushiro_factor:.2f}: disconnected population "
            f"{row.expected_disconnected_population:,.1f} "
            f"({row.seed_min:,.1f}-{row.seed_max:,.1f}); age 65+ "
            f"{row.expected_disconnected_age65:,.1f}; change versus midpoint "
            f"{row.relative_change_vs_midpoint:+.1%}; Spearman "
            f"{row.community_frequency_spearman_vs_midpoint:.3f}; Top-30 overlap "
            f"{row.top30_population_burden_overlap_vs_midpoint:.1%}."
        )
    report.extend(["", "## Service consequences", ""])
    for name in SERVICES:
        rows = service_summary[service_summary["service_class"] == name]
        values = "; ".join(
            f"f={row.yatsushiro_factor:.2f}: {row.expected_affected_population:,.1f} "
            f"({row.relative_change_vs_midpoint:+.1%})"
            for row in rows.itertuples(index=False)
        )
        report.append(f"- {name}: {values}.")
    report.extend(["", "## Intervention trigger check", ""])
    for row in intervention_summary.itertuples(index=False):
        report.append(
            f"- f={row.yatsushiro_factor:.2f}: protected population "
            f"{row.protected_population_mean:,.1f}; priority Spearman "
            f"{row.priority_spearman_vs_midpoint:.3f}; Top-150 overlap "
            f"{row.top150_priority_overlap_vs_midpoint:.1%}; action changes "
            f"{row.action_changes_vs_midpoint}."
        )
    report.extend(["", "## Gates", ""])
    report.extend(f"- {name}: {value}" for name, value in gates.items())
    (OUT / "audit_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Status: {status}")
    print(isolation_summary.to_string(index=False))
    print(service_summary.to_string(index=False))
    print(intervention_summary.to_string(index=False))
    print(json.dumps(gates, indent=2))
    print(f"Saved outputs under {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
