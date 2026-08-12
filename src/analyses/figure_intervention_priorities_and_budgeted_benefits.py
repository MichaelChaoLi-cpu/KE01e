#!/usr/bin/env python3
"""Intervention Priorities and Budgeted Benefits.

Plan: Identify priority roads and communities and show protected population under
budget and cost-effect sensitivity assumptions.
Framework: Section 5 decision estimands; Section 6 action-appropriate closure
propensity reduction, avoided isolation, protected population, and assigned-action
priority score; Section 7 consequence-aware screening against a planning-unit budget.

All priorities are emergency-screening outputs. Costs are relative planning units,
effects are assumptions, and results do not replace field engineering assessment.
"""
from __future__ import annotations

import os
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import resvg_py
from rasterio.transform import from_bounds
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import seaborn as sns
import shapely

import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure
from cache_fingerprint import cache_matches, content_signature


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
ROAD_PATH = PROCESSED / "road_sections_preprocessed.parquet"
EDGE_PATH = PROCESSED / "road_edges_preprocessed.parquet"
NODE_PATH = PROCESSED / "road_nodes_preprocessed.parquet"
SVG_OUT = ROOT / "data/results/figures/Figure_intervention_priorities_and_budgeted_benefits.svg"
OUT = ROOT / "data/results/figures/Figure_intervention_priorities_and_budgeted_benefits.png"

DISPLAY_WIDTH = 950
TOP_ROADS_TO_MAP = 50
TOP_COMMUNITIES_TO_MAP = 30
SINGLE_CLOSE_SCREEN_COUNT = 1000
PORTFOLIO_CANDIDATE_COUNT = 150
PORTFOLIO_BUDGET_COUNT = 7

ACTION_EFFECT = {
    "Temporary reinforcement": {"Conservative": 0.25, "Central": 0.45, "Optimistic": 0.60},
    "Clearance pre-positioning": {"Conservative": 0.10, "Central": 0.20, "Optimistic": 0.30},
    "Alternative-route protection": {"Conservative": 0.20, "Central": 0.35, "Optimistic": 0.50},
}
COST_MULTIPLIER = {"Conservative": 1.20, "Central": 1.00, "Optimistic": 0.80}
SETTING_COLORS = {
    "Conservative": "#3A86FF",
    "Central": "#E76F51",
    "Optimistic": "#2A9D8F",
}
COMPARATOR_COLORS = {
    "Hazard only": "#6B7280",
    "Emergency route only": "#8B5CF6",
    "Road class only": "#A16207",
    "Equal-cost consequence": "#111827",
}
COMPARATOR_CACHE = ROOT / "data/exp/analysis_cache/intervention_comparators_v5.npz"
INTERVENTION_CACHE_DIR = (
    ROOT / "data/results/intermediate/intervention_event_idw_v5"
)
SINGLE_CLOSE_CACHE = INTERVENTION_CACHE_DIR / "single_section_consequence.npz"
# Retained for compatibility with scripts that identify the primary replicate;
# final intervention comparisons use all seeds in ``isolation.REPLICATE_SEEDS``.
INTERVENTION_RANDOM_SEED = isolation.RANDOM_SEED


def quiet_isolation_frequency(
    candidate_u: np.ndarray,
    candidate_v: np.ndarray,
    candidate_edge_section: np.ndarray,
    section_propensity: np.ndarray,
    root_count: int,
    target_roots: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
    seed: int,
) -> np.ndarray:
    """Run the accepted connectivity simulation without progress messages."""
    random = np.random.default_rng(seed)
    isolated_count = np.zeros(community_count, dtype="int32")
    for _ in range(isolation.MONTE_CARLO_DRAWS):
        section_open = random.random(len(section_propensity)) >= section_propensity
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
        component_count, labels = connected_components(graph, directed=False, return_labels=True)
        target_component = np.zeros(component_count, dtype=bool)
        target_component[labels[target_roots]] = True
        root_accessible = target_component[labels]
        community_accessible = np.zeros(community_count, dtype="uint8")
        np.maximum.at(
            community_accessible,
            attachment_community,
            root_accessible[attachment_root].astype("uint8"),
        )
        isolated_count += community_accessible == 0
    return isolated_count.astype("float32") / isolation.MONTE_CARLO_DRAWS


def cached_intervention_frequency(
    cache_name: str,
    *args: object,
) -> np.ndarray:
    """Cache one deterministic intervention simulation for resumable generation."""
    if len(args) < 10:
        raise ValueError(
            "cached_intervention_frequency requires the complete simulation argument set."
        )
    signature = content_signature(
        "intervention-frequency-v5",
        files=(Path(__file__),),
        arrays={
            "candidate_u": np.asarray(args[0]),
            "candidate_v": np.asarray(args[1]),
            "candidate_edge_section": np.asarray(args[2]),
            "section_propensity": np.asarray(args[3]),
            "target_roots": np.asarray(args[5]),
            "attachment_community": np.asarray(args[6]),
            "attachment_root": np.asarray(args[7]),
        },
        parameters={
            "root_count": int(args[4]),
            "community_count": int(args[8]),
            "seed": int(args[9]),
            "draws": isolation.MONTE_CARLO_DRAWS,
        },
    )
    path = INTERVENTION_CACHE_DIR / f"{cache_name}.npz"
    if path.exists():
        cached = np.load(path, allow_pickle=False)
        if cache_matches(cached, signature):
            print(f"  loaded intervention cache: {cache_name}", flush=True)
            return cached["frequency"].astype("float32")
    frequency = quiet_isolation_frequency(*args)
    INTERVENTION_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        signature=np.asarray(signature),
        frequency=frequency.astype("float32"),
    )
    print(f"  cached intervention simulation: {cache_name}", flush=True)
    return frequency


def single_close_signature(
    screen_positions: np.ndarray,
    candidate_u: np.ndarray,
    candidate_v: np.ndarray,
    candidate_edge_section: np.ndarray,
    root_count: int,
    target_roots: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_population: np.ndarray,
) -> str:
    """Return the complete cache signature for single-section consequence checks."""
    return content_signature(
        "single-section-consequence-v5",
        files=(Path(__file__),),
        arrays={
            "screen_positions": screen_positions,
            "candidate_u": candidate_u,
            "candidate_v": candidate_v,
            "candidate_edge_section": candidate_edge_section,
            "target_roots": target_roots,
            "attachment_community": attachment_community,
            "attachment_root": attachment_root,
            "community_population": community_population,
        },
        parameters={"root_count": root_count},
    )


def single_section_closed_population(
    section_position: int,
    candidate_u: np.ndarray,
    candidate_v: np.ndarray,
    candidate_edge_section: np.ndarray,
    root_count: int,
    target_roots: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_population: np.ndarray,
) -> float:
    """Return population disconnected when only one candidate section is closed."""
    edge_open = candidate_edge_section != section_position
    u = candidate_u[edge_open]
    v = candidate_v[edge_open]
    graph = coo_matrix(
        (
            np.ones(len(u) * 2, dtype="uint8"),
            (np.concatenate([u, v]), np.concatenate([v, u])),
        ),
        shape=(root_count, root_count),
    ).tocsr()
    component_count, labels = connected_components(graph, directed=False, return_labels=True)
    target_component = np.zeros(component_count, dtype=bool)
    target_component[labels[target_roots]] = True
    root_accessible = target_component[labels]
    community_accessible = np.zeros(len(community_population), dtype="uint8")
    np.maximum.at(
        community_accessible,
        attachment_community,
        root_accessible[attachment_root].astype("uint8"),
    )
    return float(community_population[community_accessible == 0].sum())


def action_assignment(
    emergency_membership: pd.Series,
    road_score: np.ndarray,
    high_score_cutoff: float,
    alternative_scarcity: np.ndarray,
) -> np.ndarray:
    """Assign a declared screening action by road role and exposure."""
    action = np.full(len(road_score), "Clearance pre-positioning", dtype=object)
    emergency = emergency_membership.astype("string").ne("None").to_numpy()
    positive_scarcity = alternative_scarcity[alternative_scarcity > 0]
    scarcity_cutoff = (
        float(np.quantile(positive_scarcity, 0.90)) if len(positive_scarcity) else np.inf
    )
    scarce = (alternative_scarcity > 0) & (alternative_scarcity >= scarcity_cutoff)
    alternative = emergency | scarce
    action[alternative] = "Alternative-route protection"
    action[(road_score >= high_score_cutoff) & ~alternative] = "Temporary reinforcement"
    return action


def select_under_budget(
    order: np.ndarray,
    costs: np.ndarray,
    budget: float,
) -> tuple[np.ndarray, float]:
    """Greedily select an ordered screening portfolio under the stated budget."""
    selected: list[int] = []
    spent = 0.0
    for position in order:
        cost = float(costs[position])
        if spent + cost <= budget + 1e-9:
            selected.append(int(position))
            spent += cost
    return np.asarray(selected, dtype="int32"), spent


def section_burden_from_frequency(
    baseline_frequency: np.ndarray,
    community_population: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    candidate_u: np.ndarray,
    candidate_v: np.ndarray,
    candidate_edge_section: np.ndarray,
    root_count: int,
    section_count: int,
) -> np.ndarray:
    """Allocate simulation-conditional community burden to adjacent road sections."""
    attachment_count = np.bincount(
        attachment_community,
        minlength=len(community_population),
    ).astype(float)
    attachment_share_burden = (
        community_population * baseline_frequency / np.maximum(attachment_count, 1.0)
    )
    root_burden = np.zeros(root_count, dtype="float64")
    np.add.at(root_burden, attachment_root, attachment_share_burden[attachment_community])
    section_burden = np.zeros(section_count, dtype="float64")
    edge_burden = root_burden[candidate_u] + root_burden[candidate_v]
    np.maximum.at(section_burden, candidate_edge_section, edge_burden)
    return section_burden


def assigned_action_priority_score(
    consequence_proxy: np.ndarray,
    actions: np.ndarray,
    base_cost: np.ndarray,
) -> np.ndarray:
    """Return the declared assigned-action median score across cost-effect settings."""
    setting_scores: list[np.ndarray] = []
    for setting in ("Conservative", "Central", "Optimistic"):
        effect = np.asarray([ACTION_EFFECT[str(action)][setting] for action in actions])
        cost = base_cost * COST_MULTIPLIER[setting]
        setting_scores.append(consequence_proxy * effect / np.maximum(cost, 1e-6))
    return np.median(np.vstack(setting_scores), axis=0)


def comparator_orders(
    candidate_score: np.ndarray,
    emergency_candidate: np.ndarray,
    road_category: pd.Series,
    consequence_proxy: np.ndarray,
    actions: np.ndarray,
    base_cost: np.ndarray,
    setting: str,
) -> dict[str, np.ndarray]:
    """Return comparators under the same cost-effect setting as the focal ranking."""
    class_weight = road_category.astype("string").map(
        {
            "National Expressway or Equivalent": 4.0,
            "National Highway": 3.0,
            "Prefectural Road": 2.0,
            "Municipal Road or Equivalent": 1.0,
            "Other": 0.0,
        }
    ).fillna(0.0).to_numpy(dtype=float)
    setting_effect = np.asarray(
        [ACTION_EFFECT[str(action)][setting] for action in actions],
        dtype=float,
    )
    setting_cost = base_cost * COST_MULTIPLIER[setting]
    return {
        "Hazard only": np.argsort(candidate_score)[::-1],
        "Emergency route only": np.argsort(
            emergency_candidate.astype(float) * 10.0 + candidate_score
        )[::-1],
        "Road class only": np.argsort(class_weight * 10.0 + candidate_score)[::-1],
        "Equal-cost consequence": np.argsort(
            consequence_proxy * setting_effect / np.maximum(setting_cost, 1e-6)
        )[::-1],
    }


def evaluate_comparator_portfolios(
    budgets: np.ndarray,
    base_cost: np.ndarray,
    actions: np.ndarray,
    candidate_score: np.ndarray,
    emergency_candidate: np.ndarray,
    road_category: pd.Series,
    consequence_proxy: np.ndarray,
    section_propensity: np.ndarray,
    baseline_frequencies: dict[int, np.ndarray],
    community_population: np.ndarray,
    community_older: np.ndarray,
    candidate_u: np.ndarray,
    candidate_v: np.ndarray,
    candidate_edge_section: np.ndarray,
    root_count: int,
    target_roots: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
) -> pd.DataFrame:
    """Evaluate setting-matched comparators across independent simulation seeds."""
    seeds = tuple(sorted(baseline_frequencies))
    signature = content_signature(
        "intervention-comparators-v5",
        files=(Path(__file__),),
        arrays={
            "budgets": budgets,
            "base_cost": base_cost,
            "actions": np.asarray(actions, dtype="U40"),
            "candidate_score": candidate_score,
            "emergency_candidate": emergency_candidate,
            "road_category": road_category.astype("string").fillna("").to_numpy(dtype="U40"),
            "consequence_proxy": consequence_proxy,
            "section_propensity": section_propensity,
            "community_population": community_population,
            "community_older": community_older,
            "candidate_u": candidate_u,
            "candidate_v": candidate_v,
            "candidate_edge_section": candidate_edge_section,
            "target_roots": target_roots,
            "attachment_community": attachment_community,
            "attachment_root": attachment_root,
            **{f"baseline_seed_{seed}": baseline_frequencies[seed] for seed in seeds},
        },
        parameters={
            "root_count": root_count,
            "seeds": seeds,
            "draws": isolation.MONTE_CARLO_DRAWS,
            "action_effect": ACTION_EFFECT,
            "cost_multiplier": COST_MULTIPLIER,
        },
    )
    if COMPARATOR_CACHE.exists():
        cached = np.load(COMPARATOR_CACHE, allow_pickle=False)
        if cache_matches(cached, signature):
            return pd.DataFrame(
                {
                    "Comparator": cached["comparator"].astype(str),
                    "Setting": cached["setting"].astype(str),
                    "Budget (Planning Units)": cached["budget"],
                    "Selected Road Count": cached["selected_count"].astype(int),
                    "Realized Portfolio Cost": cached["spent"],
                    "Protected Population": cached["protected"],
                    "Protected Population Low": cached["protected_low"],
                    "Protected Population High": cached["protected_high"],
                    "Protected Population Age 65+": cached["protected_older"],
                    "Protected Population Age 65+ Low": cached["protected_older_low"],
                    "Protected Population Age 65+ High": cached["protected_older_high"],
                }
            )

    rows: list[dict[str, object]] = []
    for setting in ("Conservative", "Central", "Optimistic"):
        setting_effect = np.asarray(
            [ACTION_EFFECT[str(action)][setting] for action in actions],
            dtype=float,
        )
        setting_cost = base_cost * COST_MULTIPLIER[setting]
        orders = comparator_orders(
            candidate_score,
            emergency_candidate,
            road_category,
            consequence_proxy,
            actions,
            base_cost,
            setting,
        )
        for name, order in orders.items():
            safe_name = name.lower().replace(" ", "_").replace("-", "_")
            for budget_index, budget in enumerate(budgets):
                selected, spent = select_under_budget(order, setting_cost, float(budget))
                adjusted = section_propensity.copy()
                if selected.size:
                    adjusted[selected] *= 1.0 - setting_effect[selected]
                protected_by_seed: list[float] = []
                protected_older_by_seed: list[float] = []
                for seed in seeds:
                    frequency = cached_intervention_frequency(
                        f"comparator_{setting.lower()}_{safe_name}_b{budget_index}_seed_{seed}",
                        candidate_u,
                        candidate_v,
                        candidate_edge_section,
                        adjusted,
                        root_count,
                        target_roots,
                        attachment_community,
                        attachment_root,
                        len(community_population),
                        seed,
                    ).astype(float)
                    reduction = np.maximum(
                        baseline_frequencies[seed].astype(float) - frequency,
                        0.0,
                    )
                    protected_by_seed.append(float(np.sum(community_population * reduction)))
                    protected_older_by_seed.append(float(np.sum(community_older * reduction)))
                rows.append(
                    {
                        "Comparator": name,
                        "Setting": setting,
                        "Budget (Planning Units)": float(budget),
                        "Selected Road Count": int(selected.size),
                        "Realized Portfolio Cost": float(spent),
                        "Protected Population": float(np.mean(protected_by_seed)),
                        "Protected Population Low": float(np.min(protected_by_seed)),
                        "Protected Population High": float(np.max(protected_by_seed)),
                        "Protected Population Age 65+": float(np.mean(protected_older_by_seed)),
                        "Protected Population Age 65+ Low": float(np.min(protected_older_by_seed)),
                        "Protected Population Age 65+ High": float(np.max(protected_older_by_seed)),
                    }
                )
    table = pd.DataFrame(rows)
    COMPARATOR_CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        COMPARATOR_CACHE,
        signature=np.asarray(signature),
        comparator=table["Comparator"].to_numpy(dtype="U32"),
        setting=table["Setting"].to_numpy(dtype="U16"),
        budget=table["Budget (Planning Units)"].to_numpy(dtype=float),
        selected_count=table["Selected Road Count"].to_numpy(dtype=int),
        spent=table["Realized Portfolio Cost"].to_numpy(dtype=float),
        protected=table["Protected Population"].to_numpy(dtype=float),
        protected_low=table["Protected Population Low"].to_numpy(dtype=float),
        protected_high=table["Protected Population High"].to_numpy(dtype=float),
        protected_older=table["Protected Population Age 65+"].to_numpy(dtype=float),
        protected_older_low=table["Protected Population Age 65+ Low"].to_numpy(dtype=float),
        protected_older_high=table["Protected Population Age 65+ High"].to_numpy(dtype=float),
    )
    if not any(
        np.sum(community_population * value) > 0
        for value in baseline_frequencies.values()
    ):
        raise RuntimeError("Comparator evaluation requires positive baseline isolation.")
    return table


def main() -> None:
    sns.set_theme(style="white", context="paper")

    admin = pd.read_parquet(ADMIN_PATH, columns=["Municipality Name", "Geometry"])
    municipality_names = admin["Municipality Name"].astype(str).to_numpy()
    admin_geometry = road_exposure.decode_geometry(admin.pop("Geometry"))
    admin_union = shapely.union_all(admin_geometry)
    min_x, min_y, max_x, max_y = shapely.bounds(admin_union)
    pad_x = (max_x - min_x) * 0.025
    pad_y = (max_y - min_y) * 0.025
    extent = (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)
    west, east, south, north = extent
    display_height = max(650, round(DISPLAY_WIDTH * (north - south) / (east - west)))
    display_shape = (display_height, DISPLAY_WIDTH)
    display_transform = from_bounds(west, south, east, north, DISPLAY_WIDTH, display_height)

    terrain_scores, _, model_mode, elevation_grid = road_exposure.load_or_build_landslide_scores(
        admin,
        admin_geometry,
        admin_union,
        extent,
        display_shape,
        display_transform,
    )
    roads = pd.read_parquet(
        ROAD_PATH,
        columns=[
            "Road Section ID",
            "Road Section Length (m)",
            "Road Category",
            "Emergency Route Membership",
            "Network Analysis Eligible",
            "Geometry",
        ],
    )
    roads = roads.loc[roads["Network Analysis Eligible"]].reset_index(drop=True)
    road_geometry = road_exposure.decode_geometry(roads.pop("Geometry"))
    road_scores = road_exposure.load_or_build_road_scores(
        road_geometry,
        terrain_scores,
        extent,
        elevation_grid,
    )
    heavy_lower = isolation.positive_score_quantile(
        road_scores["Heavy"], isolation.CANDIDATE_QUANTILE
    )
    heavy_upper = isolation.positive_score_quantile(
        road_scores["Heavy"], isolation.UPPER_MAPPING_QUANTILE
    )
    candidate = np.isfinite(road_scores["Heavy"]) & (road_scores["Heavy"] >= heavy_lower)
    candidate_ids = roads.loc[candidate, "Road Section ID"].reset_index(drop=True)
    candidate_position = pd.Series(
        np.arange(len(candidate_ids), dtype="int32"),
        index=candidate_ids,
    )
    candidate_road_index = roads.index[candidate].to_numpy(dtype="int32")
    candidate_score = road_scores["Heavy"][candidate]
    section_propensity = isolation.closure_propensity(
        candidate_score,
        heavy_lower,
        heavy_upper,
    )

    nodes = pd.read_parquet(
        NODE_PATH,
        columns=["Network Node ID", "Network Component ID", "Geometry"],
    )
    node_geometry = road_exposure.decode_geometry(nodes.pop("Geometry"))
    node_index = pd.Index(nodes["Network Node ID"])
    edges = pd.read_parquet(
        EDGE_PATH,
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
        raise RuntimeError("Road edges reference missing network nodes.")
    edge_candidate = edges["Road Section ID"].isin(candidate_ids).to_numpy()

    stable_u = edge_u[~edge_candidate]
    stable_v = edge_v[~edge_candidate]
    stable_graph = coo_matrix(
        (
            np.ones(len(stable_u) * 2, dtype="uint8"),
            (np.concatenate([stable_u, stable_v]), np.concatenate([stable_v, stable_u])),
        ),
        shape=(len(nodes), len(nodes)),
    ).tocsr()
    root_count, stable_labels = connected_components(
        stable_graph,
        directed=False,
        return_labels=True,
    )
    stable_labels = stable_labels.astype("int32")
    candidate_u = stable_labels[edge_u[edge_candidate]]
    candidate_v = stable_labels[edge_v[edge_candidate]]
    candidate_edge_section = (
        edges.loc[edge_candidate, "Road Section ID"].map(candidate_position).to_numpy(dtype="int32")
    )
    between_root = candidate_u != candidate_v
    candidate_u = candidate_u[between_root]
    candidate_v = candidate_v[between_root]
    candidate_edge_section = candidate_edge_section[between_root]

    target_definitions, target_network_components = isolation.external_target_definitions(
        nodes,
        node_geometry,
        stable_labels,
        edges,
        edge_u,
        edge_v,
        admin_union,
    )
    target_roots = target_definitions["Primary boundary gateways"]
    (
        community,
        attachment_community,
        attachment_root,
        _,
        _,
        _,
    ) = isolation.build_baseline_communities(
        nodes,
        node_geometry,
        stable_labels,
        target_network_components,
    )
    community_population = community["Total_Population"].to_numpy(dtype=float)
    community_older = community["Population_Age_65"].to_numpy(dtype=float)
    print("Loading five independently seeded Heavy baselines for intervention screening")
    baseline_frequencies = {
        seed: isolation.cached_isolation(
            f"central_heavy_seed_{seed}_m1000",
            candidate_u,
            candidate_v,
            candidate_edge_section,
            section_propensity,
            root_count,
            target_roots,
            attachment_community,
            attachment_root,
            len(community),
            seed,
        ).astype(float)
        for seed in isolation.REPLICATE_SEEDS
    }
    baseline_frequency = np.mean(
        np.vstack(list(baseline_frequencies.values())),
        axis=0,
    )
    baseline_expected_by_seed = np.asarray(
        [
            np.sum(community_population * baseline_frequencies[seed])
            for seed in isolation.REPLICATE_SEEDS
        ],
        dtype=float,
    )
    baseline_expected_isolated = float(np.mean(baseline_expected_by_seed))

    root_degree = np.bincount(
        np.concatenate([candidate_u, candidate_v]),
        minlength=root_count,
    ).astype(float)

    section_burden = section_burden_from_frequency(
        baseline_frequency,
        community_population,
        attachment_community,
        attachment_root,
        candidate_u,
        candidate_v,
        candidate_edge_section,
        root_count,
        len(candidate_ids),
    )
    section_scarcity = np.zeros(len(candidate_ids), dtype="float64")
    edge_scarcity = 1.0 / np.sqrt(
        np.maximum(np.minimum(root_degree[candidate_u], root_degree[candidate_v]), 1.0)
    )
    np.maximum.at(section_scarcity, candidate_edge_section, edge_scarcity)
    emergency_candidate = (
        roads.loc[candidate_road_index, "Emergency Route Membership"]
        .astype("string")
        .ne("None")
        .to_numpy()
    )
    candidate_road_category = roads.loc[candidate_road_index, "Road Category"].reset_index(drop=True)
    preliminary_score = (
        candidate_score
        * np.log1p(section_burden)
        * (1.0 + section_scarcity)
        * np.where(emergency_candidate, 1.20, 1.0)
    )

    screen_positions = np.argsort(preliminary_score)[-SINGLE_CLOSE_SCREEN_COUNT:]
    single_signature = single_close_signature(
        screen_positions,
        candidate_u,
        candidate_v,
        candidate_edge_section,
        root_count,
        target_roots,
        attachment_community,
        attachment_root,
        community_population,
    )
    if SINGLE_CLOSE_CACHE.exists():
        cached_single = np.load(SINGLE_CLOSE_CACHE, allow_pickle=False)
    else:
        cached_single = None
    if (
        cached_single is not None
        and cache_matches(cached_single, single_signature)
    ):
        single_close_population = cached_single["single_close_population"].astype("float64")
        print("Loaded cached single-road consequence checks.", flush=True)
    else:
        single_close_population = np.zeros(len(candidate_ids), dtype="float64")
        for count, position in enumerate(screen_positions, start=1):
            single_close_population[position] = single_section_closed_population(
                int(position),
                candidate_u,
                candidate_v,
                candidate_edge_section,
                root_count,
                target_roots,
                attachment_community,
                attachment_root,
                community_population,
            )
            if count % 250 == 0:
                print(
                    f"  completed {count:,}/{len(screen_positions):,} "
                    "single-road consequence checks"
                )
        SINGLE_CLOSE_CACHE.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            SINGLE_CLOSE_CACHE,
            signature=np.asarray(single_signature),
            single_close_population=single_close_population,
        )

    consequence_proxy = single_close_population + 0.15 * section_burden
    candidate_length_km = (
        roads.loc[candidate_road_index, "Road Section Length (m)"].to_numpy(dtype=float) / 1000.0
    )
    actions = action_assignment(
        roads.loc[candidate_road_index, "Emergency Route Membership"],
        candidate_score,
        heavy_upper,
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

    priority_score = assigned_action_priority_score(consequence_proxy, actions, base_cost)
    seed_priority_scores: list[np.ndarray] = []
    for seed in isolation.REPLICATE_SEEDS:
        seed_burden = section_burden_from_frequency(
            baseline_frequencies[seed],
            community_population,
            attachment_community,
            attachment_root,
            candidate_u,
            candidate_v,
            candidate_edge_section,
            root_count,
            len(candidate_ids),
        )
        seed_priority_scores.append(
            assigned_action_priority_score(
                single_close_population + 0.15 * seed_burden,
                actions,
                base_cost,
            )
        )
    priority_order = np.argsort(priority_score)[::-1]
    top_priority_set = set(priority_order[:PORTFOLIO_CANDIDATE_COUNT])
    priority_rank_correlations = np.asarray(
        [pd.Series(priority_score).corr(pd.Series(score), method="spearman") for score in seed_priority_scores],
        dtype=float,
    )
    priority_top_overlap = np.asarray(
        [
            len(top_priority_set & set(np.argsort(score)[::-1][:PORTFOLIO_CANDIDATE_COUNT]))
            / PORTFOLIO_CANDIDATE_COUNT
            for score in seed_priority_scores
        ],
        dtype=float,
    )
    portfolio_positions = priority_order[:PORTFOLIO_CANDIDATE_COUNT]
    top_road_positions = priority_order[:TOP_ROADS_TO_MAP]

    max_budget = float(base_cost[portfolio_positions[:100]].sum())
    budgets = np.linspace(0.0, max_budget, PORTFOLIO_BUDGET_COUNT)
    protected_population: dict[str, list[float]] = {
        setting: [] for setting in ("Conservative", "Central", "Optimistic")
    }
    protected_population_low: dict[str, list[float]] = {
        setting: [] for setting in ("Conservative", "Central", "Optimistic")
    }
    protected_population_high: dict[str, list[float]] = {
        setting: [] for setting in ("Conservative", "Central", "Optimistic")
    }
    selected_counts: dict[str, list[int]] = {
        setting: [] for setting in ("Conservative", "Central", "Optimistic")
    }
    for setting in ("Conservative", "Central", "Optimistic"):
        setting_cost = base_cost * COST_MULTIPLIER[setting]
        setting_effect = np.array([ACTION_EFFECT[action][setting] for action in actions])
        for budget_index, budget in enumerate(budgets):
            selected_array, spent = select_under_budget(
                portfolio_positions,
                setting_cost,
                float(budget),
            )
            adjusted_propensity = section_propensity.copy()
            if selected_array.size:
                adjusted_propensity[selected_array] *= 1.0 - setting_effect[selected_array]
            protected_by_seed: list[float] = []
            for seed in isolation.REPLICATE_SEEDS:
                frequency = cached_intervention_frequency(
                    f"assigned_{setting.lower()}_b{budget_index}_seed_{seed}",
                    candidate_u,
                    candidate_v,
                    candidate_edge_section,
                    adjusted_propensity,
                    root_count,
                    target_roots,
                    attachment_community,
                    attachment_root,
                    len(community),
                    seed,
                ).astype(float)
                reduction = np.maximum(baseline_frequencies[seed] - frequency, 0.0)
                protected_by_seed.append(float(np.sum(community_population * reduction)))
            protected_population[setting].append(float(np.mean(protected_by_seed)))
            protected_population_low[setting].append(float(np.min(protected_by_seed)))
            protected_population_high[setting].append(float(np.max(protected_by_seed)))
            selected_counts[setting].append(len(selected_array))

    comparator_table = evaluate_comparator_portfolios(
        budgets,
        base_cost,
        actions,
        candidate_score,
        emergency_candidate,
        candidate_road_category,
        consequence_proxy,
        section_propensity,
        baseline_frequencies,
        community_population,
        community_older,
        candidate_u,
        candidate_v,
        candidate_edge_section,
        root_count,
        target_roots,
        attachment_community,
        attachment_root,
    )

    community_burden = baseline_frequency * community_population
    community_older_burden = baseline_frequency * community_older
    community_order = np.lexsort((-community_older_burden, -community_burden))
    top_community = community_order[:TOP_COMMUNITIES_TO_MAP]
    community_points = shapely.points(
        community["Longitude"].to_numpy(),
        community["Latitude"].to_numpy(),
    )
    older_share = np.divide(
        community_older,
        community_population,
        out=np.zeros_like(community_older),
        where=community_population > 0,
    )
    vulnerability_class = np.where(
        older_share < 0.25,
        "Under 25% age 65+",
        np.where(older_share < 0.40, "25–40% age 65+", "Over 40% age 65+"),
    )
    vulnerability_colors = {
        "Under 25% age 65+": "#3A86FF",
        "25–40% age 65+": "#FFB703",
        "Over 40% age 65+": "#D62828",
    }
    top_burden = community_burden[top_community]
    burden_reference = max(float(np.quantile(top_burden, 0.90)), 1.0)
    community_sizes = np.clip(30 + 150 * np.sqrt(top_burden / burden_reference), 30, 200)

    figure = plt.figure(figsize=(14.5, 11.0), constrained_layout=True)
    grid = figure.add_gridspec(
        2,
        2,
        width_ratios=[1.0, 1.0],
        height_ratios=[1.0, 0.78],
        wspace=0.08,
        hspace=0.10,
    )
    axes = np.array(
        [
            figure.add_subplot(grid[0, 0]),
            figure.add_subplot(grid[0, 1]),
            figure.add_subplot(grid[1, 0]),
            figure.add_subplot(grid[1, 1]),
        ]
    )
    boundary_segments = road_exposure.line_segments(shapely.boundary(admin_geometry))
    emergency_segments = road_exposure.line_segments(
        road_geometry[roads["Emergency Route Membership"].astype("string").ne("None").to_numpy()]
    )

    for axis in axes[:2]:
        axis.set_facecolor("#F8FAFC")
        axis.add_collection(
            LineCollection(
                emergency_segments,
                colors="#CBD5E1",
                linewidths=0.42,
                alpha=0.82,
                zorder=2,
            )
        )
        axis.add_collection(
            LineCollection(
                boundary_segments,
                colors="#667085",
                linewidths=0.50,
                alpha=0.88,
                zorder=4,
            )
        )
        road_exposure.style_map_axis(axis, extent)

    top_geometry = road_geometry[candidate_road_index[top_road_positions]]
    rank_groups = [
        (slice(0, 10), "Top 10 priority roads", "#D62828", 2.2, 25),
        (slice(10, 30), "Priority ranks 11–30", "#F77F00", 1.6, 17),
        (slice(30, 50), "Priority ranks 31–50", "#FCBF49", 1.2, 11),
    ]
    road_handles: list[Line2D] = []
    for rank_slice, label, color, width, marker_area in rank_groups:
        selected_geometry = top_geometry[rank_slice]
        segments = road_exposure.line_segments(selected_geometry)
        axes[0].add_collection(
            LineCollection(
                segments,
                colors=color,
                linewidths=width,
                alpha=0.96,
                zorder=10,
            )
        )
        centers = shapely.get_coordinates(shapely.centroid(selected_geometry))[:, :2]
        axes[0].scatter(
            centers[:, 0],
            centers[:, 1],
            s=marker_area,
            c=color,
            edgecolors="white",
            linewidths=0.45,
            alpha=0.96,
            zorder=11,
        )
        road_handles.append(
            Line2D(
                [0],
                [0],
                color=color,
                linewidth=width,
                marker="o",
                markerfacecolor=color,
                markeredgecolor="white",
                markersize=np.sqrt(marker_area),
                label=label,
            )
        )
    axes[0].legend(
        handles=road_handles,
        loc="lower left",
        fontsize=7.2,
        frameon=True,
        framealpha=0.94,
    )
    axes[0].text(
        0.018,
        0.982,
        "Road-access intervention priorities\nHeavy rainfall screening",
        transform=axes[0].transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        fontweight="bold",
        color="#172033",
        bbox={"boxstyle": "round,pad=0.30", "facecolor": "white", "edgecolor": "#D0D5DD", "alpha": 0.94},
        zorder=20,
    )

    for vulnerability, color in vulnerability_colors.items():
        selected = vulnerability_class[top_community] == vulnerability
        axes[1].scatter(
            community.loc[top_community[selected], "Longitude"],
            community.loc[top_community[selected], "Latitude"],
            s=community_sizes[selected],
            c=color,
            edgecolors="white",
            linewidths=0.65,
            alpha=0.90,
            label=vulnerability,
            zorder=10,
        )
    axes[1].legend(
        loc="lower left",
        fontsize=7.0,
        frameon=True,
        framealpha=0.94,
    )
    axes[1].text(
        0.018,
        0.982,
        "Community pre-positioning priorities\nMarker size: isolation burden",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        fontweight="bold",
        color="#172033",
        bbox={"boxstyle": "round,pad=0.30", "facecolor": "white", "edgecolor": "#D0D5DD", "alpha": 0.94},
        zorder=20,
    )

    for setting in ("Conservative", "Central", "Optimistic"):
        axes[2].fill_between(
            budgets,
            protected_population_low[setting],
            protected_population_high[setting],
            color=SETTING_COLORS[setting],
            alpha=0.12,
            linewidth=0,
            zorder=2,
        )
        axes[2].plot(
            budgets,
            protected_population[setting],
            color=SETTING_COLORS[setting],
            marker="o",
            markersize=4.8,
            linewidth=1.8,
            label=f"Assigned-action: {setting}",
            zorder=5,
        )
        matched = comparator_table.loc[
            (comparator_table["Comparator"] == "Equal-cost consequence")
            & (comparator_table["Setting"] == setting)
        ].sort_values("Budget (Planning Units)")
        axes[2].plot(
            matched["Budget (Planning Units)"],
            matched["Protected Population"],
            color=SETTING_COLORS[setting],
            linestyle=(0, (4, 3)),
            linewidth=1.35,
            alpha=0.90,
            label=f"Equal-cost audit: {setting}",
            zorder=4,
        )
        axes[2].fill_between(
            matched["Budget (Planning Units)"],
            matched["Protected Population Low"],
            matched["Protected Population High"],
            color=SETTING_COLORS[setting],
            alpha=0.07,
            linewidth=0,
            zorder=1,
        )
    axes[2].set_xlabel("Planning budget units", fontsize=9)
    axes[2].set_ylabel("Expected population protected", fontsize=9)
    axes[2].tick_params(axis="both", labelsize=8)
    axes[2].grid(True, color="#D0D5DD", linewidth=0.60, linestyle=(0, (3, 3)))
    axes[2].set_axisbelow(True)
    axes[2].legend(
        loc="upper left",
        fontsize=6.3,
        ncol=1,
        frameon=True,
        framealpha=0.94,
    )
    axes[2].text(
        0.98,
        0.075,
        (
            f"Heavy baseline mean: {baseline_expected_isolated:,.0f} "
            f"({baseline_expected_by_seed.min():,.0f}–{baseline_expected_by_seed.max():,.0f})\n"
            f"Five seeds; maximum portfolio: {max(selected_counts['Central']):,} roads\n"
            f"Priority stability: ρ ≥ {np.nanmin(priority_rank_correlations):.3f}; "
            f"top-{PORTFOLIO_CANDIDATE_COUNT} overlap ≥ {priority_top_overlap.min():.1%}"
        ),
        transform=axes[2].transAxes,
        ha="right",
        va="bottom",
        fontsize=7.7,
        color="#344054",
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "#D0D5DD", "alpha": 0.94},
    )
    for spine in axes[2].spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.85)
        spine.set_color("#344054")

    central_comparators = (
        comparator_table.loc[comparator_table["Setting"] == "Central"]
        .sort_values("Budget (Planning Units)")
        .groupby("Comparator", sort=False)
        .tail(1)
        .set_index("Comparator")
    )
    comparison_labels = [
        "Assigned-action screening",
        "Equal-cost consequence",
        "Hazard only",
        "Emergency route only",
        "Road class only",
    ]
    comparison_values = np.asarray(
        [protected_population["Central"][-1]]
        + [
            float(central_comparators.loc[label, "Protected Population"])
            for label in comparison_labels[1:]
        ],
        dtype=float,
    )
    comparison_colors = [SETTING_COLORS["Central"]] + [
        COMPARATOR_COLORS[label] for label in comparison_labels[1:]
    ]
    comparison_low = np.asarray(
        [protected_population_low["Central"][-1]]
        + [
            float(central_comparators.loc[label, "Protected Population Low"])
            for label in comparison_labels[1:]
        ],
        dtype=float,
    )
    comparison_high = np.asarray(
        [protected_population_high["Central"][-1]]
        + [
            float(central_comparators.loc[label, "Protected Population High"])
            for label in comparison_labels[1:]
        ],
        dtype=float,
    )
    comparison_y = np.arange(len(comparison_labels))
    axes[3].barh(
        comparison_y,
        comparison_values,
        color=comparison_colors,
        height=0.62,
        alpha=0.90,
        zorder=3,
    )
    axes[3].errorbar(
        comparison_values,
        comparison_y,
        xerr=np.vstack(
            [comparison_values - comparison_low, comparison_high - comparison_values]
        ),
        fmt="none",
        ecolor="#344054",
        elinewidth=0.9,
        capsize=2.5,
        zorder=5,
    )
    axes[3].set_yticks(comparison_y, labels=comparison_labels)
    axes[3].invert_yaxis()
    axes[3].set_xlabel("Expected population protected at maximum budget", fontsize=9)
    axes[3].tick_params(axis="both", labelsize=7.6)
    axes[3].grid(axis="x", color="#D0D5DD", linewidth=0.60, linestyle=(0, (3, 3)))
    axes[3].set_axisbelow(True)
    value_reference = max(float(comparison_values.max()), 1.0)
    axes[3].set_xlim(0, value_reference * 1.18)
    for y_position, value in enumerate(comparison_values):
        axes[3].text(
            value + value_reference * 0.018,
            y_position,
            f"{value:,.0f}",
            va="center",
            ha="left",
            fontsize=7.7,
            fontweight="bold",
            color="#172033",
        )
    equal_cost_value = comparison_values[1]
    incremental = comparison_values[0] - equal_cost_value
    incremental_percent = 100.0 * incremental / max(equal_cost_value, 1e-6)
    axes[3].text(
        0.98,
        0.04,
        (
            "Central setting; identical costs and effects\n"
            f"Assigned-action minus equal-cost audit: {incremental:+,.0f} "
            f"({incremental_percent:+.1f}%)"
        ),
        transform=axes[3].transAxes,
        ha="right",
        va="bottom",
        fontsize=7.4,
        color="#344054",
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "#D0D5DD"},
        zorder=10,
    )
    axes[2].text(
        0.02,
        0.02,
        "Central modeled cost at 1 km: reinforcement 5.0 | clearance 2.0 | "
        "alternative-route 3.7 units",
        transform=axes[2].transAxes,
        ha="left",
        va="bottom",
        fontsize=6.8,
        color="#475467",
        bbox={
            "boxstyle": "round,pad=0.24",
            "facecolor": "white",
            "edgecolor": "#D0D5DD",
            "alpha": 0.94,
        },
        zorder=10,
    )
    for spine in axes[3].spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.85)
        spine.set_color("#344054")

    for label, axis in zip("abcd", axes):
        road_exposure.add_panel_label(axis, label)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(SVG_OUT, format="svg", bbox_inches="tight", facecolor="white")
    plt.close(figure)
    OUT.write_bytes(
        resvg_py.svg_to_bytes(
            svg_path=str(SVG_OUT),
            dpi=300.0,
            background="white",
        )
    )

    top_action_counts = pd.Series(actions[top_road_positions]).value_counts()
    print(f"Saved SVG: {SVG_OUT.relative_to(ROOT)}")
    print(f"Converted PNG (300 dpi): {OUT.relative_to(ROOT)}")
    print(f"Terrain-score construction: {model_mode}")
    print(
        "Heavy baseline expected isolated population across five seeds: "
        f"mean={baseline_expected_isolated:,.1f}; "
        f"range={baseline_expected_by_seed.min():,.1f}–{baseline_expected_by_seed.max():,.1f}"
    )
    print(f"Candidate road sections: {len(candidate_ids):,}")
    print(f"Single-road consequence checks: {len(screen_positions):,}")
    print("Top-50 assigned intervention types:")
    for action, count in top_action_counts.items():
        print(f"  {action}: {count:,}")
    for setting in ("Conservative", "Central", "Optimistic"):
        print(
            f"{setting}: protected at maximum budget="
            f"{protected_population[setting][-1]:,.1f} "
            f"({protected_population_low[setting][-1]:,.1f}–"
            f"{protected_population_high[setting][-1]:,.1f}); "
            f"selected roads={selected_counts[setting][-1]:,}"
        )
    print(
        "Central maximum-budget comparison: assigned-action="
        f"{comparison_values[0]:,.1f}; equal-cost consequence={equal_cost_value:,.1f}; "
        f"increment={incremental:+,.1f} ({incremental_percent:+.1f}%)"
    )
    print(
        "Priority stability across baseline seeds: minimum Spearman rho="
        f"{np.nanmin(priority_rank_correlations):.4f}; minimum top-"
        f"{PORTFOLIO_CANDIDATE_COUNT} overlap={priority_top_overlap.min():.1%}"
    )
    print("Interpretation: screening priorities under relative costs and assumed effects")


if __name__ == "__main__":
    main()
