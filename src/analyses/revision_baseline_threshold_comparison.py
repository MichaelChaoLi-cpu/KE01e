#!/usr/bin/env python3
"""All-area f=1.00 versus corrected official-threshold comparison for R2C3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.special import expit, logit
from scipy.stats import spearmanr
import shapely

import figure_basic_service_reachability_loss as service
import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_intervention_priorities_and_budgeted_benefits as intervention
import figure_official_threshold_adjusted_landslide_disruption_score as terrain_score
import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure
import revision_rainfall_parameter_sensitivity as parameter_sensitivity


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "Rev/docs/analysis-spec-reviewer-2-comment-3.md"
OUT = ROOT / "data/exp/revision/reviewer-2-comment-3"
SCENARIOS = ("Moderate", "Heavy", "Extreme")
THRESHOLDS = ("Baseline f=1.00", "Official geography")
TOLERANCE = 1e-7


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_spearman(x: np.ndarray, y: np.ndarray) -> float:
    valid = np.isfinite(x) & np.isfinite(y)
    if valid.sum() < 3 or np.unique(x[valid]).size < 2 or np.unique(y[valid]).size < 2:
        return np.nan
    return float(spearmanr(x[valid], y[valid]).statistic)


def top_overlap(reference: np.ndarray, candidate: np.ndarray, quantile: float = 0.99) -> float:
    valid = np.isfinite(reference) & np.isfinite(candidate)
    ref, alt = reference[valid], candidate[valid]
    if len(ref) < 100:
        return np.nan
    ref_top = ref >= np.quantile(ref, quantile)
    alt_top = alt >= np.quantile(alt, quantile)
    denominator = min(int(ref_top.sum()), int(alt_top.sum()))
    return float(np.sum(ref_top & alt_top) / denominator) if denominator else np.nan


def score_comparison_row(
    level: str,
    scenario: str,
    baseline: np.ndarray,
    official: np.ndarray,
    positive_only: bool,
) -> dict[str, object]:
    support = np.isfinite(baseline) & np.isfinite(official)
    if positive_only:
        support &= (baseline > 0) | (official > 0)
    base, adjusted = baseline[support].astype(float), official[support].astype(float)
    difference = adjusted - base
    return {
        "analysis_level": level,
        "scenario": scenario,
        "supported_units": int(len(base)),
        "baseline_score_p50": float(np.quantile(base, 0.50)),
        "baseline_score_p90": float(np.quantile(base, 0.90)),
        "baseline_score_p99": float(np.quantile(base, 0.99)),
        "official_score_p50": float(np.quantile(adjusted, 0.50)),
        "official_score_p90": float(np.quantile(adjusted, 0.90)),
        "official_score_p99": float(np.quantile(adjusted, 0.99)),
        "mean_official_minus_baseline": float(np.mean(difference)),
        "spearman_rho": safe_spearman(base, adjusted),
        "top1_overlap": top_overlap(base, adjusted),
        "official_ge_baseline_fraction": float(np.mean(adjusted + TOLERANCE >= base)),
    }


def setup_downstream(
    roads: pd.DataFrame,
    official_heavy: np.ndarray,
    admin_union: object,
) -> dict[str, object]:
    lower = isolation.positive_score_quantile(official_heavy, isolation.CANDIDATE_QUANTILE)
    upper = isolation.positive_score_quantile(official_heavy, isolation.UPPER_MAPPING_QUANTILE)
    candidate = np.isfinite(official_heavy) & (official_heavy >= lower)
    candidate_ids = roads.loc[candidate, "Road Section ID"].reset_index(drop=True)
    candidate_position = pd.Series(
        np.arange(len(candidate_ids), dtype="int32"), index=candidate_ids
    )
    candidate_road_index = roads.index[candidate].to_numpy(dtype="int32")

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
            "Baseline Edge Travel Time (min)",
            "Network Analysis Eligible",
        ],
    )
    edges = edges.loc[edges["Network Analysis Eligible"]].reset_index(drop=True)
    edge_u = node_index.get_indexer(edges["From Node ID"])
    edge_v = node_index.get_indexer(edges["To Node ID"])
    if np.any(edge_u < 0) or np.any(edge_v < 0):
        raise RuntimeError("Road edges reference missing network nodes")
    edge_candidate = edges["Road Section ID"].isin(candidate_ids).to_numpy()
    edge_candidate_position_full = (
        edges["Road Section ID"].map(candidate_position).fillna(-1).to_numpy(dtype="int32")
    )

    stable_u, stable_v = edge_u[~edge_candidate], edge_v[~edge_candidate]
    stable_graph = coo_matrix(
        (
            np.ones(len(stable_u) * 2, dtype="uint8"),
            (np.concatenate([stable_u, stable_v]), np.concatenate([stable_v, stable_u])),
        ),
        shape=(len(nodes), len(nodes)),
    ).tocsr()
    root_count, stable_labels = connected_components(
        stable_graph, directed=False, return_labels=True
    )
    stable_labels = stable_labels.astype("int32")
    candidate_u = stable_labels[edge_u[edge_candidate]]
    candidate_v = stable_labels[edge_v[edge_candidate]]
    candidate_edge_section = (
        edges.loc[edge_candidate, "Road Section ID"]
        .map(candidate_position)
        .to_numpy(dtype="int32")
    )
    candidate_edge_time = edges.loc[
        edge_candidate, "Baseline Edge Travel Time (min)"
    ].to_numpy(dtype="float64")
    between = candidate_u != candidate_v
    candidate_u, candidate_v = candidate_u[between], candidate_v[between]
    candidate_edge_section = candidate_edge_section[between]
    candidate_edge_time = candidate_edge_time[between]
    pair_reduction = service.prepare_pair_reduction(
        candidate_u,
        candidate_v,
        candidate_edge_section,
        candidate_edge_time,
        root_count,
    )

    targets, target_components = isolation.external_target_definitions(
        nodes, node_geometry, stable_labels, edges, edge_u, edge_v, admin_union
    )
    community, attachment_community, attachment_root, diagnostics, selected_mesh, _ = (
        isolation.build_baseline_communities(
            nodes, node_geometry, stable_labels, target_components
        )
    )
    service_geometry, service_source_counts = service.service_geometries()
    service_roots, _, service_attached_counts = service.attach_services_to_roots(
        service_geometry, node_geometry, stable_labels
    )
    if any(len(service_roots[name]) == 0 for name in service.SERVICE_CLASSES):
        raise RuntimeError("At least one service class has no attached road root")
    return {
        "lower": lower,
        "upper": upper,
        "candidate_ids": candidate_ids,
        "candidate_road_index": candidate_road_index,
        "candidate_u": candidate_u,
        "candidate_v": candidate_v,
        "candidate_edge_section": candidate_edge_section,
        "root_count": root_count,
        "target_roots": targets[isolation.PRIMARY_TARGET_NAME],
        "attachment_community": attachment_community,
        "attachment_root": attachment_root,
        "community": community,
        "diagnostics": diagnostics,
        "pair_reduction": pair_reduction,
        "service_roots": service_roots,
        "service_source_counts": service_source_counts,
        "service_attached_counts": service_attached_counts,
        "selected_mesh": selected_mesh,
        "edge_u": edge_u,
        "edge_v": edge_v,
        "edge_candidate_position_full": edge_candidate_position_full,
        "node_count": len(nodes),
    }


def isolation_results(
    road_scores: dict[str, dict[str, np.ndarray]],
    roads: pd.DataFrame,
    network: dict[str, object],
) -> tuple[pd.DataFrame, dict[str, dict[str, list[np.ndarray]]], dict[str, np.ndarray]]:
    id_to_position = pd.Series(np.arange(len(roads), dtype=int), index=roads["Road Section ID"])
    candidate_positions = network["candidate_ids"].map(id_to_position).to_numpy(dtype=int)
    population = network["community"]["Total_Population"].to_numpy(dtype=float)
    older = network["community"]["Population_Age_65"].to_numpy(dtype=float)
    replicate: dict[str, dict[str, list[np.ndarray]]] = {}
    propensities: dict[str, np.ndarray] = {}
    rows: list[dict[str, object]] = []
    for threshold_name, threshold_slug in (
        ("Baseline f=1.00", "baseline"),
        ("Official geography", "official"),
    ):
        replicate[threshold_name] = {}
        for scenario in SCENARIOS:
            candidate_score = road_scores[threshold_name][scenario][candidate_positions]
            propensity = isolation.closure_propensity(
                candidate_score, float(network["lower"]), float(network["upper"])
            )
            if scenario == "Heavy":
                propensities[threshold_name] = propensity
            frequencies: list[np.ndarray] = []
            for seed in isolation.REPLICATE_SEEDS:
                frequencies.append(
                    isolation.cached_isolation(
                        f"revision_r2c3_{threshold_slug}_{scenario.lower()}_seed_{seed}_m1000",
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
                )
            replicate[threshold_name][scenario] = frequencies
            totals = np.asarray([np.sum(population * item) for item in frequencies], dtype=float)
            older_totals = np.asarray([np.sum(older * item) for item in frequencies], dtype=float)
            rows.append(
                {
                    "threshold_geography": threshold_name,
                    "scenario": scenario,
                    "expected_isolated_population_mean": float(totals.mean()),
                    "expected_isolated_population_min": float(totals.min()),
                    "expected_isolated_population_max": float(totals.max()),
                    "expected_isolated_population_sd": float(totals.std(ddof=1)),
                    "expected_isolated_population_age65_mean": float(older_totals.mean()),
                    "candidate_road_sections": int(len(candidate_positions)),
                    "seed_count": int(len(frequencies)),
                    "draws_per_seed": 1_000,
                }
            )
    frame = pd.DataFrame(rows)
    for scenario in SCENARIOS:
        base = frame.loc[
            frame["threshold_geography"].eq("Baseline f=1.00")
            & frame["scenario"].eq(scenario),
            "expected_isolated_population_mean",
        ].iloc[0]
        official = frame.loc[
            frame["threshold_geography"].eq("Official geography")
            & frame["scenario"].eq(scenario),
            "expected_isolated_population_mean",
        ].iloc[0]
        mask = frame["scenario"].eq(scenario)
        frame.loc[mask, "official_minus_baseline_population"] = official - base
        frame.loc[mask, "official_to_baseline_ratio"] = official / base if base else np.inf
    return frame, replicate, propensities


def service_results(
    network: dict[str, object],
    propensities: dict[str, np.ndarray],
) -> pd.DataFrame:
    population = network["community"]["Total_Population"].to_numpy(dtype=float)
    rows: list[dict[str, object]] = []
    totals_by_threshold: dict[str, dict[str, float]] = {}
    for threshold_name, threshold_slug in (
        ("Baseline f=1.00", "baseline"),
        ("Official geography", "official"),
    ):
        seed_results = [
            service._cached_service_loss_seed(
                propensities[threshold_name],
                network["pair_reduction"],
                network["root_count"],
                network["service_roots"],
                network["attachment_community"],
                network["attachment_root"],
                len(network["community"]),
                seed,
                f"revision_r2c3_{threshold_slug}",
            )
            for seed in isolation.REPLICATE_SEEDS
        ]
        totals_by_threshold[threshold_name] = {}
        for service_name in service.SERVICE_CLASSES:
            values = np.asarray(
                [
                    np.nansum(result[0][service_name] * population)
                    for result in seed_results
                ],
                dtype=float,
            )
            totals_by_threshold[threshold_name][service_name] = float(values.mean())
            resolved, source = network["service_source_counts"][service_name]
            rows.append(
                {
                    "threshold_geography": threshold_name,
                    "service_class": service_name,
                    "expected_population_losing_reachability_mean": float(values.mean()),
                    "expected_population_losing_reachability_min": float(values.min()),
                    "expected_population_losing_reachability_max": float(values.max()),
                    "expected_population_losing_reachability_sd": float(values.std(ddof=1)),
                    "resolved_service_features": int(resolved),
                    "source_service_features": int(source),
                    "attached_service_features": int(
                        network["service_attached_counts"][service_name]
                    ),
                    "conditional_sensitivity": service_name == "Emergency water",
                }
            )
    frame = pd.DataFrame(rows)
    for service_name in service.SERVICE_CLASSES:
        base = totals_by_threshold["Baseline f=1.00"][service_name]
        official = totals_by_threshold["Official geography"][service_name]
        mask = frame["service_class"].eq(service_name)
        frame.loc[mask, "official_minus_baseline_population"] = official - base
        frame.loc[mask, "official_to_baseline_ratio"] = official / base if base else np.inf
    return frame


def load_or_build_single_close(
    screen_positions: np.ndarray,
    network: dict[str, object],
    population: np.ndarray,
) -> np.ndarray:
    path = OUT / "single_section_consequence.npy"
    values = np.zeros(len(network["candidate_ids"]), dtype="float64")
    for count, position in enumerate(screen_positions, start=1):
        values[position] = intervention.single_section_closed_population(
            int(position),
            network["candidate_u"],
            network["candidate_v"],
            network["candidate_edge_section"],
            network["root_count"],
            network["target_roots"],
            network["attachment_community"],
            network["attachment_root"],
            population,
        )
        if count % 250 == 0:
            print(f"  completed {count:,}/{len(screen_positions):,} single-road checks", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    np.save(path, values)
    return values


def intervention_results(
    roads: pd.DataFrame,
    road_scores: dict[str, dict[str, np.ndarray]],
    network: dict[str, object],
    replicate: dict[str, dict[str, list[np.ndarray]]],
    propensities: dict[str, np.ndarray],
) -> tuple[pd.DataFrame, dict[str, float]]:
    candidate_index = network["candidate_road_index"]
    official_candidate_score = road_scores["Official geography"]["Heavy"][candidate_index]
    population = network["community"]["Total_Population"].to_numpy(dtype=float)
    root_degree = np.bincount(
        np.concatenate([network["candidate_u"], network["candidate_v"]]),
        minlength=network["root_count"],
    ).astype(float)
    scarcity = np.zeros(len(network["candidate_ids"]), dtype="float64")
    edge_scarcity = 1.0 / np.sqrt(
        np.maximum(
            np.minimum(
                root_degree[network["candidate_u"]], root_degree[network["candidate_v"]]
            ),
            1.0,
        )
    )
    np.maximum.at(scarcity, network["candidate_edge_section"], edge_scarcity)
    emergency = (
        roads.loc[candidate_index, "Emergency Route Membership"]
        .astype("string")
        .ne("None")
        .to_numpy()
    )
    official_frequency = np.mean(
        np.vstack(replicate["Official geography"]["Heavy"]), axis=0
    )
    official_burden = intervention.section_burden_from_frequency(
        official_frequency,
        population,
        network["attachment_community"],
        network["attachment_root"],
        network["candidate_u"],
        network["candidate_v"],
        network["candidate_edge_section"],
        network["root_count"],
        len(network["candidate_ids"]),
    )
    preliminary = (
        official_candidate_score
        * np.log1p(official_burden)
        * (1.0 + scarcity)
        * np.where(emergency, 1.20, 1.0)
    )
    screen = np.argsort(preliminary)[-intervention.SINGLE_CLOSE_SCREEN_COUNT :]
    single_close = load_or_build_single_close(screen, network, population)
    actions = intervention.action_assignment(
        roads.loc[candidate_index, "Emergency Route Membership"],
        official_candidate_score,
        float(network["upper"]),
        scarcity,
    )
    length_km = roads.loc[candidate_index, "Road Section Length (m)"].to_numpy(float) / 1000.0
    base_cost = np.select(
        [actions == "Temporary reinforcement", actions == "Alternative-route protection"],
        [3.0 + 2.0 * length_km, 2.5 + 1.2 * length_km],
        default=1.5 + 0.5 * length_km,
    ).astype("float64")
    setting_cost = base_cost * intervention.COST_MULTIPLIER["Central"]
    setting_effect = np.asarray(
        [intervention.ACTION_EFFECT[str(action)]["Central"] for action in actions], dtype=float
    )

    priorities: dict[str, np.ndarray] = {}
    rows: list[dict[str, object]] = []
    for threshold_name in THRESHOLDS:
        mean_frequency = np.mean(np.vstack(replicate[threshold_name]["Heavy"]), axis=0)
        burden = intervention.section_burden_from_frequency(
            mean_frequency,
            population,
            network["attachment_community"],
            network["attachment_root"],
            network["candidate_u"],
            network["candidate_v"],
            network["candidate_edge_section"],
            network["root_count"],
            len(network["candidate_ids"]),
        )
        proxy = single_close + 0.15 * burden
        priority = intervention.assigned_action_priority_score(proxy, actions, base_cost)
        priorities[threshold_name] = priority

    official_order = np.argsort(priorities["Official geography"])[::-1]
    budget = float(setting_cost[official_order[:100]].sum())
    comparison_rho = safe_spearman(
        priorities["Baseline f=1.00"], priorities["Official geography"]
    )
    top_official = set(official_order[: intervention.PORTFOLIO_CANDIDATE_COUNT].tolist())
    baseline_order = np.argsort(priorities["Baseline f=1.00"])[::-1]
    top_baseline = set(baseline_order[: intervention.PORTFOLIO_CANDIDATE_COUNT].tolist())
    overlap = len(top_official & top_baseline) / intervention.PORTFOLIO_CANDIDATE_COUNT

    for threshold_name, slug in (
        ("Baseline f=1.00", "baseline"),
        ("Official geography", "official"),
    ):
        order = np.argsort(priorities[threshold_name])[::-1]
        portfolio_candidates = order[: intervention.PORTFOLIO_CANDIDATE_COUNT]
        selected, spent = intervention.select_under_budget(
            portfolio_candidates, setting_cost, budget
        )
        adjusted = propensities[threshold_name].copy()
        adjusted[selected] *= 1.0 - setting_effect[selected]
        protected = []
        source_frequencies = replicate[threshold_name]["Heavy"]
        for seed, original in zip(isolation.REPLICATE_SEEDS, source_frequencies, strict=True):
            changed = intervention.cached_intervention_frequency(
                f"revision_r2c3_{slug}_native_maxbudget_seed_{seed}",
                network["candidate_u"],
                network["candidate_v"],
                network["candidate_edge_section"],
                adjusted,
                network["root_count"],
                network["target_roots"],
                network["attachment_community"],
                network["attachment_root"],
                len(network["community"]),
                seed,
            )
            reduction = np.maximum(original.astype(float) - changed.astype(float), 0.0)
            protected.append(float(np.sum(population * reduction)))
        rows.append(
            {
                "threshold_geography": threshold_name,
                "priority_spearman_rho": comparison_rho,
                "top150_overlap": overlap,
                "nominal_budget_planning_units": budget,
                "selected_road_sections": int(len(selected)),
                "realized_cost_planning_units": float(spent),
                "protected_population_mean": float(np.mean(protected)),
                "protected_population_min": float(np.min(protected)),
                "protected_population_max": float(np.max(protected)),
            }
        )
    return pd.DataFrame(rows), {
        "priority_spearman_rho": comparison_rho,
        "top150_overlap": overlap,
        "budget": budget,
    }


def main() -> None:
    required = [
        SPEC,
        ROOT / "Rev/docs/analysis-spec-reviewer-2-comment-2.md",
        ROOT / "Rev/docs/analysis-spec-reviewer-2-comment-4.md",
        terrain_score.DEM_PATH,
        terrain_score.WARNING_PATH,
        terrain_score.LANDSLIDE_PATH,
        road_exposure.SCENARIO_PATH,
        road_exposure.THRESHOLD_PATH,
        road_exposure.ADMIN_PATH,
        road_exposure.ROAD_PATH,
        road_exposure.EDGE_PATH,
        isolation.NODE_PATH,
        isolation.MESH_PATH,
        isolation.GROUP_PATH,
        service.DESIGNATED_SHELTER_PATH,
        service.EVACUATION_SITE_PATH,
        service.CURRENT_SHELTER_PATH,
        service.WATER_PATH,
        service.FIRE_PATH,
        service.MUNICIPAL_PATH,
        Path(terrain_score.__file__),
        Path(road_exposure.__file__),
        Path(isolation.__file__),
        Path(service.__file__),
        Path(intervention.__file__),
        Path(parameter_sensitivity.__file__),
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
        [(admin_union, 1)],
        out_shape=shape,
        transform=transform,
        fill=0,
        all_touched=True,
        dtype="uint8",
    ).astype(bool)

    official_slope, loads, model_mode, elevation = road_exposure.load_or_build_landslide_scores(
        admin, admin_geometry, admin_union, extent, shape, transform
    )
    factor_grid = parameter_sensitivity.build_factor_grid(
        admin, admin_geometry, shape, transform, admin_mask
    )
    context, reconstruction_error = parameter_sensitivity.derive_terrain_logit(
        official_slope, loads, factor_grid
    )
    baseline_slope: dict[str, np.ndarray] = {}
    for scenario in SCENARIOS:
        official_values = official_slope[scenario].astype(float)
        values = expit(
            logit(np.clip(official_values, 1e-7, 1 - 1e-7))
            + np.log(np.clip(factor_grid, 1e-7, None))
        ).astype("float32")
        values[~np.isfinite(official_values)] = np.nan
        baseline_slope[scenario] = values

    roads = pd.read_parquet(
        road_exposure.ROAD_PATH,
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
    official_road = road_exposure.load_or_build_road_scores(
        road_geometry, official_slope, extent, elevation
    )
    baseline_road = road_exposure.road_scores(
        road_geometry, baseline_slope, extent, elevation
    )
    road_scores = {
        "Baseline f=1.00": baseline_road,
        "Official geography": official_road,
    }

    score_rows = []
    for scenario in SCENARIOS:
        score_rows.append(
            score_comparison_row(
                "Slope cell", scenario, baseline_slope[scenario], official_slope[scenario], False
            )
        )
        score_rows.append(
            score_comparison_row(
                "Road section", scenario, baseline_road[scenario], official_road[scenario], True
            )
        )
    score_frame = pd.DataFrame(score_rows)

    network = setup_downstream(roads, official_road["Heavy"], admin_union)
    isolation_frame, replicate, propensities = isolation_results(
        road_scores, roads, network
    )
    service_frame = service_results(network, propensities)
    intervention_frame, intervention_summary = intervention_results(
        roads, road_scores, network, replicate, propensities
    )

    slope_monotone = bool(
        np.all(
            score_frame.loc[
                score_frame["analysis_level"].eq("Slope cell"),
                "official_ge_baseline_fraction",
            ].to_numpy()
            >= 0.99999
        )
    )
    road_monotone = bool(
        np.all(
            score_frame.loc[
                score_frame["analysis_level"].eq("Road section"),
                "official_ge_baseline_fraction",
            ].to_numpy()
            >= 0.99999
        )
    )
    iso_pivot = isolation_frame.pivot(
        index="scenario", columns="threshold_geography", values="expected_isolated_population_mean"
    )
    isolation_monotone = bool(
        np.all(iso_pivot["Official geography"] + 1e-6 >= iso_pivot["Baseline f=1.00"])
    )
    service_pivot = service_frame.pivot(
        index="service_class",
        columns="threshold_geography",
        values="expected_population_losing_reachability_mean",
    )
    service_monotone = bool(
        np.all(service_pivot["Official geography"] + 1e-6 >= service_pivot["Baseline f=1.00"])
    )
    print(
        json.dumps(
            {
                "slope_monotonicity_pass": slope_monotone,
                "road_monotonicity_pass": road_monotone,
                "isolation_monotonicity_pass": isolation_monotone,
                "service_monotonicity_pass": service_monotone,
                "minimum_score_monotone_fraction": float(
                    score_frame["official_ge_baseline_fraction"].min()
                ),
                "isolation_means": iso_pivot.to_dict(),
                "service_means": service_pivot.to_dict(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        flush=True,
    )
    if not all((slope_monotone, road_monotone, isolation_monotone, service_monotone)):
        raise RuntimeError("A predeclared monotonicity validation failed")

    heavy_base = float(iso_pivot.loc["Heavy", "Baseline f=1.00"])
    heavy_official = float(iso_pivot.loc["Heavy", "Official geography"])
    decision = {
        "reviewer_unit": "reviewer-2/comment-3",
        "spec_sha256": sha256(SPEC),
        "model_mode": model_mode,
        "terrain_reconstruction_max_abs_error": reconstruction_error,
        "threshold_interpretation": "no-retention-adjustment model baseline, not a physical no-earthquake counterfactual",
        "candidate_road_sections": int(len(network["candidate_ids"])),
        "seed_count": len(isolation.REPLICATE_SEEDS),
        "draws_per_seed": 1_000,
        "slope_monotonicity_pass": slope_monotone,
        "road_monotonicity_pass": road_monotone,
        "isolation_monotonicity_pass": isolation_monotone,
        "service_monotonicity_pass": service_monotone,
        "baseline_heavy_expected_isolated_population": heavy_base,
        "official_heavy_expected_isolated_population": heavy_official,
        "official_heavy_increment": heavy_official - heavy_base,
        "official_heavy_ratio": heavy_official / heavy_base if heavy_base else None,
        "intervention_priority_spearman_rho": intervention_summary["priority_spearman_rho"],
        "intervention_top150_overlap": intervention_summary["top150_overlap"],
        "community_diagnostics": network["diagnostics"],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    score_frame.to_csv(OUT / "slope_and_road_threshold_comparison.csv", index=False)
    isolation_frame.to_csv(OUT / "community_isolation_threshold_comparison.csv", index=False)
    service_frame.to_csv(OUT / "service_reachability_threshold_comparison.csv", index=False)
    intervention_frame.to_csv(OUT / "intervention_threshold_propagation.csv", index=False)
    np.savez_compressed(
        OUT / "threshold_score_arrays.npz",
        **{f"baseline_slope_{key}": value for key, value in baseline_slope.items()},
        **{f"official_slope_{key}": value for key, value in official_slope.items()},
        **{f"baseline_road_{key}": value for key, value in baseline_road.items()},
        **{f"official_road_{key}": value for key, value in official_road.items()},
    )
    np.savez_compressed(
        OUT / "community_isolation_frequency_arrays.npz",
        **{
            f"{threshold.replace(' ', '_').replace('=', '')}_{scenario}_seed_{seed}": frequency
            for threshold, scenario_values in replicate.items()
            for scenario, frequencies in scenario_values.items()
            for seed, frequency in zip(isolation.REPLICATE_SEEDS, frequencies, strict=True)
        },
    )
    input_hashes = pd.DataFrame(
        [
            {
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in required
        ]
    )
    input_hashes.to_csv(OUT / "input_hashes.csv", index=False)
    (OUT / "decision.json").write_text(
        json.dumps(decision, ensure_ascii=False, indent=2, default=float) + "\n",
        encoding="utf-8",
    )
    report = [
        "# Baseline versus Official Threshold Comparison",
        "",
        "- Reviewer unit: `reviewer-2/comment-3`",
        f"- Frozen specification SHA-256: `{sha256(SPEC)}`",
        "- Baseline interpretation: all-area `f=1.00` disables threshold retention adjustment; it is not a complete physical no-earthquake counterfactual.",
        f"- Baseline Heavy expected isolated population: {heavy_base:.1f}",
        f"- Official-geography Heavy expected isolated population: {heavy_official:.1f}",
        f"- Official-threshold increment: {heavy_official - heavy_base:.1f} ({heavy_official / heavy_base - 1:.1%})",
        f"- Intervention priority Spearman correlation: {intervention_summary['priority_spearman_rho']:.4f}",
        f"- Intervention top-150 overlap: {intervention_summary['top150_overlap']:.1%}",
        "",
        "## Slope and road scores",
        "",
        score_frame.to_markdown(index=False),
        "",
        "## Community isolation",
        "",
        isolation_frame.to_markdown(index=False),
        "",
        "## Heavy service reachability",
        "",
        service_frame.to_markdown(index=False),
        "",
        "## Current intervention-screening propagation",
        "",
        intervention_frame.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "The paired contrast isolates the numerical effect of the declared official threshold-retention geography within the current model. It does not estimate the total causal effect of earthquake damage. Final intervention interpretation remains gated by Batch D.",
        "",
    ]
    (OUT / "comparison_report.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps(decision, ensure_ascii=False, indent=2, default=float))


if __name__ == "__main__":
    main()
