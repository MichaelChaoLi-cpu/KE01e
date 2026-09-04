#!/usr/bin/env python3
"""Spatially correlated road-closure sensitivity for Reviewer 3 Comment 5.

The analysis preserves the existing section-level marginal closure propensities
and varies only their within-draw dependence through a spatial-cluster Gaussian
copula.  Outputs are revision evidence, not calibrated failure probabilities.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import numpy as np
import pandas as pd
from rasterio.transform import from_bounds
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.special import ndtri
from scipy.stats import spearmanr
import shapely

from cache_fingerprint import cache_matches, content_signature
import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "Rev/docs/analysis-spec-reviewer-3-comment-5.md"
OUT = ROOT / "data/exp/revision/reviewer-3-comment-5"
CACHE = OUT / "cache"
SCENARIOS = ("Moderate", "Heavy", "Extreme")
SETTINGS = (
    ("Independent", 0, 0.00),
    ("Local weak", 1_000, 0.25),
    ("Local strong", 1_000, 0.50),
    ("Broad weak", 3_000, 0.25),
    ("Broad strong", 3_000, 0.50),
)
DRAWS = 1_000
DECISION_RECORD = "KILA-D-20260903-027"
MARGINAL_MEAN_ABS_TOLERANCE = 0.010
MARGINAL_MEAN_BIAS_TOLERANCE = 0.002


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_spearman(left: np.ndarray, right: np.ndarray) -> float:
    valid = np.isfinite(left) & np.isfinite(right)
    if valid.sum() < 3 or np.unique(left[valid]).size < 2 or np.unique(right[valid]).size < 2:
        return np.nan
    return float(spearmanr(left[valid], right[valid]).statistic)


def top_n_overlap(left: np.ndarray, right: np.ndarray, n: int = 30) -> float:
    count = min(n, len(left), len(right))
    left_order = np.argsort(-left, kind="stable")[:count]
    right_order = np.argsort(-right, kind="stable")[:count]
    return float(len(set(left_order.tolist()) & set(right_order.tolist())) / count)


def prepare_inputs() -> dict[str, object]:
    admin = pd.read_parquet(
        isolation.ADMIN_PATH,
        columns=["Municipality Name", "Geometry"],
    )
    admin_geometry = road_exposure.decode_geometry(admin.pop("Geometry"))
    admin_union = shapely.union_all(admin_geometry)
    min_lon, min_lat, max_lon, max_lat = shapely.bounds(admin_union)
    pad_x = (max_lon - min_lon) * 0.025
    pad_y = (max_lat - min_lat) * 0.025
    extent = (min_lon - pad_x, max_lon + pad_x, min_lat - pad_y, max_lat + pad_y)
    west, east, south, north = extent
    display_height = max(
        650,
        round(road_exposure.DISPLAY_WIDTH * (north - south) / (east - west)),
    )
    display_shape = (display_height, road_exposure.DISPLAY_WIDTH)
    display_transform = from_bounds(
        west,
        south,
        east,
        north,
        road_exposure.DISPLAY_WIDTH,
        display_height,
    )

    terrain_scores, _, model_mode, elevation_grid = road_exposure.load_or_build_landslide_scores(
        admin,
        admin_geometry,
        admin_union,
        extent,
        display_shape,
        display_transform,
    )
    roads = pd.read_parquet(
        isolation.ROAD_PATH,
        columns=[
            "Road Section ID",
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
    candidate_mask = np.isfinite(road_scores["Heavy"]) & (
        road_scores["Heavy"] >= heavy_lower
    )
    candidate_ids = roads.loc[candidate_mask, "Road Section ID"].reset_index(drop=True)
    candidate_position = pd.Series(
        np.arange(len(candidate_ids), dtype="int32"),
        index=candidate_ids,
    )
    candidate_geometry = road_geometry[candidate_mask]

    nodes = pd.read_parquet(
        isolation.NODE_PATH,
        columns=["Network Node ID", "Network Component ID", "Geometry"],
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
        edges.loc[edge_candidate, "Road Section ID"]
        .map(candidate_position)
        .to_numpy(dtype="int32")
    )
    between_root = candidate_u != candidate_v
    candidate_u = candidate_u[between_root]
    candidate_v = candidate_v[between_root]
    candidate_edge_section = candidate_edge_section[between_root]

    targets, target_network_components = isolation.external_target_definitions(
        nodes,
        node_geometry,
        stable_labels,
        edges,
        edge_u,
        edge_v,
        admin_union,
    )
    (
        community,
        attachment_community,
        attachment_root,
        diagnostics,
        _,
        _,
    ) = isolation.build_baseline_communities(
        nodes,
        node_geometry,
        stable_labels,
        target_network_components,
    )

    centroids = shapely.centroid(candidate_geometry)
    coordinates = np.column_stack(
        [
            np.asarray(shapely.get_x(centroids), dtype=float),
            np.asarray(shapely.get_y(centroids), dtype=float),
        ]
    )
    reference_latitude = float((min_lat + max_lat) / 2.0)
    candidate_xy = isolation.planar_coordinates(coordinates, reference_latitude)
    bounds_xy = isolation.planar_coordinates(
        np.asarray([[min_lon, min_lat], [max_lon, max_lat]], dtype=float),
        reference_latitude,
    )
    cluster_labels: dict[int, np.ndarray] = {}
    cluster_metadata: dict[int, dict[str, float | int]] = {}
    for scale in (1_000, 3_000):
        origin_x = float(np.floor(bounds_xy[0, 0] / scale) * scale)
        origin_y = float(np.floor(bounds_xy[0, 1] / scale) * scale)
        cells = np.column_stack(
            [
                np.floor((candidate_xy[:, 0] - origin_x) / scale).astype("int32"),
                np.floor((candidate_xy[:, 1] - origin_y) / scale).astype("int32"),
            ]
        )
        _, labels = np.unique(cells, axis=0, return_inverse=True)
        cluster_labels[scale] = labels.astype("int32")
        cluster_metadata[scale] = {
            "cluster_count": int(labels.max() + 1),
            "origin_x_m": origin_x,
            "origin_y_m": origin_y,
        }

    candidate_scores = {
        scenario: np.asarray(road_scores[scenario][candidate_mask], dtype="float32")
        for scenario in SCENARIOS
    }
    propensities = {
        scenario: isolation.closure_propensity(
            candidate_scores[scenario],
            heavy_lower,
            heavy_upper,
        )
        for scenario in SCENARIOS
    }
    return {
        "model_mode": model_mode,
        "heavy_lower": heavy_lower,
        "heavy_upper": heavy_upper,
        "candidate_ids": candidate_ids,
        "candidate_u": candidate_u,
        "candidate_v": candidate_v,
        "candidate_edge_section": candidate_edge_section,
        "root_count": int(root_count),
        "target_roots": targets[isolation.PRIMARY_TARGET_NAME],
        "target_definitions": targets,
        "nodes": nodes,
        "node_geometry": node_geometry,
        "stable_labels": stable_labels,
        "edges": edges,
        "edge_u": edge_u,
        "edge_v": edge_v,
        "admin_union": admin_union,
        "attachment_community": attachment_community,
        "attachment_root": attachment_root,
        "community": community,
        "diagnostics": diagnostics,
        "propensities": propensities,
        "cluster_labels": cluster_labels,
        "cluster_metadata": cluster_metadata,
    }


def simulate_block(
    *,
    candidate_u: np.ndarray,
    candidate_v: np.ndarray,
    candidate_edge_section: np.ndarray,
    propensity: np.ndarray,
    root_count: int,
    target_roots: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    population: np.ndarray,
    older_population: np.ndarray,
    seed: int,
    cluster_label: np.ndarray | None,
    scale_m: int,
    rho: float,
    draws: int = DRAWS,
) -> dict[str, np.ndarray]:
    section_rng = np.random.default_rng(seed)
    cluster_rng = None
    cluster_count = 0
    if cluster_label is not None:
        cluster_count = int(cluster_label.max() + 1)
        cluster_rng = np.random.default_rng(seed + 10_000_000 + scale_m)
    threshold = ndtri(np.asarray(propensity, dtype=float))
    isolated_count = np.zeros(len(population), dtype="int32")
    closure_count = np.zeros(len(propensity), dtype="int32")
    draw_population = np.zeros(draws, dtype="float64")
    draw_older = np.zeros(draws, dtype="float64")
    draw_communities = np.zeros(draws, dtype="int32")

    for draw in range(draws):
        section_uniform = section_rng.random(len(propensity))
        if rho == 0.0:
            section_closed = section_uniform < propensity
        else:
            independent_normal = ndtri(section_uniform)
            cluster_normal = cluster_rng.standard_normal(cluster_count)
            latent = (
                np.sqrt(rho) * cluster_normal[cluster_label]
                + np.sqrt(1.0 - rho) * independent_normal
            )
            section_closed = latent <= threshold
        closure_count += section_closed
        edge_open = ~section_closed[candidate_edge_section]
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
            graph,
            directed=False,
            return_labels=True,
        )
        target_component = np.zeros(component_count, dtype=bool)
        target_component[labels[target_roots]] = True
        root_accessible = target_component[labels]
        community_accessible = np.zeros(len(population), dtype="uint8")
        np.maximum.at(
            community_accessible,
            attachment_community,
            root_accessible[attachment_root].astype("uint8"),
        )
        isolated = community_accessible == 0
        isolated_count += isolated
        draw_population[draw] = float(np.sum(population[isolated]))
        draw_older[draw] = float(np.sum(older_population[isolated]))
        draw_communities[draw] = int(np.count_nonzero(isolated))

    return {
        "frequency": isolated_count.astype("float32") / draws,
        "empirical_closure": closure_count.astype("float32") / draws,
        "draw_population": draw_population,
        "draw_older": draw_older,
        "draw_communities": draw_communities,
    }


def cached_block(
    cache_name: str,
    *,
    scenario: str,
    setting: str,
    scale_m: int,
    rho: float,
    seed: int,
    inputs: dict[str, object],
) -> dict[str, np.ndarray]:
    propensity = np.asarray(inputs["propensities"][scenario])
    cluster_label = None if scale_m == 0 else np.asarray(inputs["cluster_labels"][scale_m])
    signature = content_signature(
        "reviewer-3-comment-5-spatial-copula-v1",
        files=(Path(__file__), SPEC),
        arrays={
            "candidate_u": np.asarray(inputs["candidate_u"]),
            "candidate_v": np.asarray(inputs["candidate_v"]),
            "candidate_edge_section": np.asarray(inputs["candidate_edge_section"]),
            "propensity": propensity,
            "target_roots": np.asarray(inputs["target_roots"]),
            "attachment_community": np.asarray(inputs["attachment_community"]),
            "attachment_root": np.asarray(inputs["attachment_root"]),
            "population": inputs["community"]["Total_Population"].to_numpy(dtype=float),
            "older_population": inputs["community"]["Population_Age_65"].to_numpy(dtype=float),
            "cluster_label": np.asarray([], dtype="int32") if cluster_label is None else cluster_label,
        },
        parameters={
            "scenario": scenario,
            "setting": setting,
            "scale_m": scale_m,
            "rho": rho,
            "seed": seed,
            "draws": DRAWS,
            "root_count": int(inputs["root_count"]),
        },
    )
    path = CACHE / f"{cache_name}.npz"
    if path.exists():
        cached = np.load(path, allow_pickle=False)
        if cache_matches(cached, signature):
            return {
                key: cached[key]
                for key in (
                    "frequency",
                    "empirical_closure",
                    "draw_population",
                    "draw_older",
                    "draw_communities",
                )
            }
    result = simulate_block(
        candidate_u=np.asarray(inputs["candidate_u"]),
        candidate_v=np.asarray(inputs["candidate_v"]),
        candidate_edge_section=np.asarray(inputs["candidate_edge_section"]),
        propensity=propensity,
        root_count=int(inputs["root_count"]),
        target_roots=np.asarray(inputs["target_roots"]),
        attachment_community=np.asarray(inputs["attachment_community"]),
        attachment_root=np.asarray(inputs["attachment_root"]),
        population=inputs["community"]["Total_Population"].to_numpy(dtype=float),
        older_population=inputs["community"]["Population_Age_65"].to_numpy(dtype=float),
        seed=seed,
        cluster_label=cluster_label,
        scale_m=scale_m,
        rho=rho,
    )
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, signature=np.asarray(signature), **result)
    return result


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
    inputs = prepare_inputs()
    community = inputs["community"].copy()
    population = community["Total_Population"].to_numpy(dtype=float)
    older_population = community["Population_Age_65"].to_numpy(dtype=float)

    blocks: dict[tuple[str, str, int], dict[str, np.ndarray]] = {}
    for scenario in SCENARIOS:
        for setting, scale_m, rho in SETTINGS:
            for seed in isolation.REPLICATE_SEEDS:
                print(
                    f"Simulating {scenario} / {setting} / seed {seed} "
                    f"({DRAWS:,} draws)",
                    flush=True,
                )
                blocks[(scenario, setting, seed)] = cached_block(
                    f"{scenario.lower()}_{setting.lower().replace(' ', '_')}_seed_{seed}",
                    scenario=scenario,
                    setting=setting,
                    scale_m=scale_m,
                    rho=rho,
                    seed=seed,
                    inputs=inputs,
                )

    exact_reproduction: dict[str, bool] = {}
    for scenario in SCENARIOS:
        propensity = np.asarray(inputs["propensities"][scenario])
        for seed in isolation.REPLICATE_SEEDS:
            reference = isolation.cached_isolation(
                f"central_{scenario.lower()}_seed_{seed}_m1000",
                np.asarray(inputs["candidate_u"]),
                np.asarray(inputs["candidate_v"]),
                np.asarray(inputs["candidate_edge_section"]),
                propensity,
                int(inputs["root_count"]),
                np.asarray(inputs["target_roots"]),
                np.asarray(inputs["attachment_community"]),
                np.asarray(inputs["attachment_root"]),
                len(community),
                seed,
                report_progress=False,
            )
            key = f"{scenario}|{seed}"
            exact_reproduction[key] = bool(
                np.array_equal(reference, blocks[(scenario, "Independent", seed)]["frequency"])
            )
    if not all(exact_reproduction.values()):
        failed = [key for key, passed in exact_reproduction.items() if not passed]
        raise RuntimeError(f"Independent implementation failed exact reproduction: {failed}")

    summary_rows: list[dict[str, object]] = []
    community_rows: list[dict[str, object]] = []
    seed_rows: list[dict[str, object]] = []
    marginal_checks: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        independent_frequency = np.mean(
            np.vstack(
                [
                    blocks[(scenario, "Independent", seed)]["frequency"]
                    for seed in isolation.REPLICATE_SEEDS
                ]
            ),
            axis=0,
        )
        independent_burden = population * independent_frequency
        independent_seed_population = {
            seed: float(blocks[(scenario, "Independent", seed)]["draw_population"].mean())
            for seed in isolation.REPLICATE_SEEDS
        }
        for setting, scale_m, rho in SETTINGS:
            setting_blocks = [
                blocks[(scenario, setting, seed)] for seed in isolation.REPLICATE_SEEDS
            ]
            frequencies = np.vstack([block["frequency"] for block in setting_blocks])
            mean_frequency = frequencies.mean(axis=0)
            draw_population = np.concatenate(
                [block["draw_population"] for block in setting_blocks]
            )
            draw_older = np.concatenate([block["draw_older"] for block in setting_blocks])
            draw_communities = np.concatenate(
                [block["draw_communities"] for block in setting_blocks]
            )
            empirical_closure = np.mean(
                np.vstack([block["empirical_closure"] for block in setting_blocks]),
                axis=0,
            )
            propensity = np.asarray(inputs["propensities"][scenario], dtype=float)
            marginal_error = empirical_closure - propensity
            marginal_mae = float(np.mean(np.abs(marginal_error)))
            marginal_bias = float(np.mean(marginal_error))
            marginal_checks.append(
                {
                    "scenario": scenario,
                    "dependence_setting": setting,
                    "mean_absolute_error": marginal_mae,
                    "mean_bias": marginal_bias,
                    "maximum_absolute_error": float(np.max(np.abs(marginal_error))),
                }
            )
            if marginal_mae > MARGINAL_MEAN_ABS_TOLERANCE:
                raise RuntimeError(
                    f"Marginal MAE exceeds tolerance for {scenario}/{setting}: {marginal_mae}"
                )
            if abs(marginal_bias) > MARGINAL_MEAN_BIAS_TOLERANCE:
                raise RuntimeError(
                    f"Marginal bias exceeds tolerance for {scenario}/{setting}: {marginal_bias}"
                )

            seed_population = np.asarray(
                [float(block["draw_population"].mean()) for block in setting_blocks],
                dtype=float,
            )
            seed_older = np.asarray(
                [float(block["draw_older"].mean()) for block in setting_blocks],
                dtype=float,
            )
            metadata = (
                {"cluster_count": 0, "origin_x_m": np.nan, "origin_y_m": np.nan}
                if scale_m == 0
                else inputs["cluster_metadata"][scale_m]
            )
            summary_rows.append(
                {
                    "scenario": scenario,
                    "dependence_setting": setting,
                    "cluster_scale_km": scale_m / 1_000,
                    "rho": rho,
                    "cluster_count": int(metadata["cluster_count"]),
                    "candidate_sections": len(inputs["candidate_ids"]),
                    "nonzero_propensity_sections": int(np.count_nonzero(propensity)),
                    "seed_count": len(isolation.REPLICATE_SEEDS),
                    "draws_per_seed": DRAWS,
                    "expected_isolated_population_mean": float(seed_population.mean()),
                    "expected_isolated_population_min": float(seed_population.min()),
                    "expected_isolated_population_max": float(seed_population.max()),
                    "expected_isolated_older_population_mean": float(seed_older.mean()),
                    "draw_isolated_population_p50": float(np.quantile(draw_population, 0.50)),
                    "draw_isolated_population_p90": float(np.quantile(draw_population, 0.90)),
                    "draw_isolated_population_p95": float(np.quantile(draw_population, 0.95)),
                    "draw_isolated_population_p99": float(np.quantile(draw_population, 0.99)),
                    "draw_isolated_older_population_p95": float(np.quantile(draw_older, 0.95)),
                    "mean_isolated_communities_per_draw": float(draw_communities.mean()),
                    "community_frequency_spearman_vs_independent": safe_spearman(
                        independent_frequency, mean_frequency
                    ),
                    "top30_burden_overlap_vs_independent": top_n_overlap(
                        independent_burden, population * mean_frequency
                    ),
                    "communities_abs_frequency_change_ge_0_05": int(
                        np.count_nonzero(np.abs(mean_frequency - independent_frequency) >= 0.05)
                    ),
                    "marginal_closure_mean_absolute_error": marginal_mae,
                    "marginal_closure_mean_bias": marginal_bias,
                    "marginal_closure_maximum_absolute_error": float(
                        np.max(np.abs(marginal_error))
                    ),
                }
            )
            for seed, block in zip(isolation.REPLICATE_SEEDS, setting_blocks, strict=True):
                expected_population = float(block["draw_population"].mean())
                seed_rows.append(
                    {
                        "scenario": scenario,
                        "dependence_setting": setting,
                        "cluster_scale_km": scale_m / 1_000,
                        "rho": rho,
                        "seed": seed,
                        "expected_isolated_population": expected_population,
                        "independent_expected_isolated_population": independent_seed_population[seed],
                        "paired_difference": expected_population
                        - independent_seed_population[seed],
                        "draw_isolated_population_p95": float(
                            np.quantile(block["draw_population"], 0.95)
                        ),
                    }
                )
            delta_frequency = mean_frequency - independent_frequency
            for position, row in community.iterrows():
                community_rows.append(
                    {
                        "scenario": scenario,
                        "dependence_setting": setting,
                        "cluster_scale_km": scale_m / 1_000,
                        "rho": rho,
                        "community_id": row["Community ID"],
                        "total_population": float(row["Total_Population"]),
                        "population_age_65_plus": float(row["Population_Age_65"]),
                        "isolation_frequency": float(mean_frequency[position]),
                        "independent_isolation_frequency": float(independent_frequency[position]),
                        "frequency_difference": float(delta_frequency[position]),
                        "population_weighted_burden": float(
                            population[position] * mean_frequency[position]
                        ),
                    }
                )

    summary = pd.DataFrame(summary_rows)
    community_output = pd.DataFrame(community_rows)
    seed_output = pd.DataFrame(seed_rows)
    summary_path = OUT / "spatially_correlated_closure_summary.csv"
    community_path = OUT / "spatially_correlated_closure_community.csv"
    seed_path = OUT / "spatially_correlated_closure_seed_differences.csv"
    summary.to_csv(summary_path, index=False, float_format="%.9f")
    community_output.to_csv(community_path, index=False, float_format="%.9f")
    seed_output.to_csv(seed_path, index=False, float_format="%.9f")

    decision = {
        "reviewer_id": "reviewer-3",
        "comment_id": "comment-5",
        "decision_record": DECISION_RECORD,
        "interpretation": (
            "Sensitivity bounds for spatial closure dependence with fixed marginal "
            "propensities; not a calibrated failure forecast."
        ),
        "scenarios": list(SCENARIOS),
        "settings": [
            {"label": label, "cluster_scale_m": scale, "rho": rho}
            for label, scale, rho in SETTINGS
        ],
        "seeds": list(isolation.REPLICATE_SEEDS),
        "draws_per_seed": DRAWS,
        "model_mode": inputs["model_mode"],
        "candidate_sections": len(inputs["candidate_ids"]),
        "candidate_network_edges": len(inputs["candidate_edge_section"]),
        "community_count": len(community),
        "heavy_lower": float(inputs["heavy_lower"]),
        "heavy_upper": float(inputs["heavy_upper"]),
        "cluster_metadata": {
            str(scale): metadata for scale, metadata in inputs["cluster_metadata"].items()
        },
        "independent_exact_reproduction": exact_reproduction,
        "marginal_checks": marginal_checks,
        "input_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in required
            if path.is_file()
        },
        "output_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (summary_path, community_path, seed_path)
        },
    }
    decision_path = OUT / "decision.json"
    decision_path.write_text(
        json.dumps(decision, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {summary_path.relative_to(ROOT)}")
    print(f"Wrote {community_path.relative_to(ROOT)}")
    print(f"Wrote {seed_path.relative_to(ROOT)}")
    print(f"Wrote {decision_path.relative_to(ROOT)}")
    print(
        summary[
            [
                "scenario",
                "dependence_setting",
                "expected_isolated_population_mean",
                "draw_isolated_population_p95",
                "community_frequency_spearman_vs_independent",
                "top30_burden_overlap_vs_independent",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
