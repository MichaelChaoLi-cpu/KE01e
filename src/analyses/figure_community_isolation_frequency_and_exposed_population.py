#!/usr/bin/env python3
"""Community Isolation Frequency and Exposed Population.

Plan: Map simulation-conditional community isolation frequency and the associated
total and older-population exposure under Moderate, Heavy, and Extreme scenarios.
Framework: Section 5 scenario consequence estimand; Section 6 monotone road-score
to closure-propensity mapping and 1,000-draw connectivity simulation; Section 7
baseline community definition and network disruption workflow.

The central screening specification treats the upper 15% of positive Heavy-score road sections as
closure candidates. Remaining roads are held open, communities are fixed before
simulation, and frequencies are not interpreted as calibrated real-world probabilities.
"""
from __future__ import annotations

import os
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import resvg_py
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
import seaborn as sns
import shapely

import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure
from cache_fingerprint import cache_matches, content_signature


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
ROAD_PATH = PROCESSED / "road_sections_preprocessed.parquet"
EDGE_PATH = PROCESSED / "road_edges_preprocessed.parquet"
NODE_PATH = PROCESSED / "road_nodes_preprocessed.parquet"
MESH_PATH = PROCESSED / "population_mesh_125m_preprocessed.parquet"
GROUP_PATH = PROCESSED / "population_disclosure_groups_preprocessed.parquet"
OUT = ROOT / "data/results/figures/Figure_community_isolation_frequency_and_exposed_population.png"
SVG_OUT = OUT.with_suffix(".svg")
SIMULATION_CACHE_DIR = (
    ROOT / "data/results/intermediate/community_isolation_event_idw_v3"
)

DISPLAY_WIDTH = 950
ATTACHMENT_LIMIT_M = 500.0
MESH_NEIGHBOR_LIMIT_M = 190.0
CANDIDATE_QUANTILE = 0.85
UPPER_MAPPING_QUANTILE = 0.995
MAX_CLOSURE_PROPENSITY = 0.30
MONTE_CARLO_DRAWS = 1000
RANDOM_SEED = 20260809
REPLICATE_SEEDS = tuple(RANDOM_SEED + 1000 * index for index in range(5))


def planar_coordinates(longitude_latitude: np.ndarray, reference_latitude: float) -> np.ndarray:
    """Convert local longitude-latitude coordinates to approximate metres."""
    longitude_scale = 111_320.0 * np.cos(np.deg2rad(reference_latitude))
    latitude_scale = 110_540.0
    return np.column_stack(
        [longitude_latitude[:, 0] * longitude_scale, longitude_latitude[:, 1] * latitude_scale]
    )


def external_target_definitions(
    nodes: pd.DataFrame,
    node_geometry: np.ndarray,
    stable_labels: np.ndarray,
    edges: pd.DataFrame,
    edge_u: np.ndarray,
    edge_v: np.ndarray,
    admin_union: object,
) -> tuple[dict[str, np.ndarray], set[str]]:
    """Define fixed external/backbone anchors and two robustness alternatives."""
    membership = edges["Emergency Route Membership"].astype("string")
    primary_edge = membership.eq("Primary Emergency Road").to_numpy()
    any_emergency_edge = membership.ne("None").to_numpy()
    primary_nodes = np.unique(np.concatenate([edge_u[primary_edge], edge_v[primary_edge]]))
    emergency_nodes = np.unique(
        np.concatenate([edge_u[any_emergency_edge], edge_v[any_emergency_edge]])
    )
    boundary = shapely.boundary(admin_union)
    primary_boundary = primary_nodes[
        shapely.distance(node_geometry[primary_nodes], boundary) <= 0.02
    ]
    emergency_boundary = emergency_nodes[
        shapely.distance(node_geometry[emergency_nodes], boundary) <= 0.02
    ]
    if len(primary_boundary) < 4:
        raise RuntimeError("Too few primary emergency-route boundary anchors.")
    targets = {
        "Primary boundary gateways": np.unique(stable_labels[primary_boundary]).astype("int32"),
        "All emergency boundary gateways": np.unique(stable_labels[emergency_boundary]).astype("int32"),
        "All primary-route roots": np.unique(stable_labels[primary_nodes]).astype("int32"),
    }
    target_components = set(
        nodes.iloc[primary_boundary]["Network Component ID"].astype(str).unique()
    )
    return targets, target_components


def community_labels(
    mesh_xy: np.ndarray,
    network_component: np.ndarray,
) -> np.ndarray:
    """Cluster adjacent populated meshes within the same baseline network component."""
    pairs = cKDTree(mesh_xy).query_pairs(MESH_NEIGHBOR_LIMIT_M, output_type="ndarray")
    if len(pairs):
        pairs = pairs[network_component[pairs[:, 0]] == network_component[pairs[:, 1]]]
    if len(pairs):
        rows = np.concatenate([pairs[:, 0], pairs[:, 1]])
        columns = np.concatenate([pairs[:, 1], pairs[:, 0]])
        adjacency = coo_matrix(
            (np.ones(len(rows), dtype="uint8"), (rows, columns)),
            shape=(len(mesh_xy), len(mesh_xy)),
        ).tocsr()
    else:
        adjacency = coo_matrix((len(mesh_xy), len(mesh_xy)), dtype="uint8").tocsr()
    _, labels = connected_components(adjacency, directed=False, return_labels=True)
    return labels.astype("int32")


def build_baseline_communities(
    nodes: pd.DataFrame,
    node_geometry: np.ndarray,
    stable_labels: np.ndarray,
    target_network_components: set[str],
) -> tuple[
    pd.DataFrame,
    np.ndarray,
    np.ndarray,
    dict[str, float],
    pd.DataFrame,
    np.ndarray,
]:
    """Attach populated meshes, cluster them, and return community-root attachments."""
    mesh = pd.read_parquet(
        MESH_PATH,
        columns=["Mesh Code", "Disclosure Group Code", "Total Population", "Geometry"],
    )
    groups = pd.read_parquet(
        GROUP_PATH,
        columns=[
            "Disclosure Group Code",
            "Population Age 65+ Share",
            "Population Age 75+ Share",
        ],
    )
    mesh = mesh.merge(groups, on="Disclosure Group Code", how="left", validate="many_to_one")
    mesh["Population Age 65+"] = (
        mesh["Total Population"].astype(float)
        * mesh["Population Age 65+ Share"].fillna(0).astype(float)
    )
    mesh["Population Age 75+"] = (
        mesh["Total Population"].astype(float)
        * mesh["Population Age 75+ Share"].fillna(0).astype(float)
    )

    mesh_geometry = road_exposure.decode_geometry(mesh.pop("Geometry"))
    mesh_centroid = shapely.centroid(mesh_geometry)
    mesh_coordinates = shapely.get_coordinates(mesh_centroid)[:, :2]
    node_coordinates = shapely.get_coordinates(node_geometry)[:, :2]
    reference_latitude = float(np.mean(node_coordinates[:, 1]))
    mesh_xy = planar_coordinates(mesh_coordinates, reference_latitude)
    node_xy = planar_coordinates(node_coordinates, reference_latitude)
    distance, nearest_node = cKDTree(node_xy).query(mesh_xy, k=1, workers=-1)

    nearest_component = nodes["Network Component ID"].to_numpy()[nearest_node]
    attached = distance <= ATTACHMENT_LIMIT_M
    baseline_target = np.array(
        [str(component) in target_network_components for component in nearest_component],
        dtype=bool,
    )
    eligible = attached & baseline_target
    if eligible.sum() < len(mesh) * 0.75:
        raise RuntimeError(
            "Fewer than 75% of populated meshes attach to a baseline component with an "
            "emergency-road target."
        )

    selected = mesh.loc[eligible].reset_index(drop=True)
    selected_geometry = mesh_geometry[eligible]
    selected_coordinates = mesh_coordinates[eligible]
    selected_xy = mesh_xy[eligible]
    selected_component = nearest_component[eligible]
    selected_node = nearest_node[eligible]
    labels = community_labels(selected_xy, selected_component)
    selected["Community Numeric ID"] = labels
    selected["Longitude"] = selected_coordinates[:, 0]
    selected["Latitude"] = selected_coordinates[:, 1]
    selected["Stable Root"] = stable_labels[selected_node]
    selected["Attached Node Position"] = selected_node.astype("int32")

    population = selected["Total Population"].to_numpy(dtype=float)
    weighted_longitude = selected["Longitude"].to_numpy() * population
    weighted_latitude = selected["Latitude"].to_numpy() * population
    selected["Weighted Longitude"] = weighted_longitude
    selected["Weighted Latitude"] = weighted_latitude
    community = selected.groupby("Community Numeric ID", sort=True).agg(
        Total_Population=("Total Population", "sum"),
        Population_Age_65=("Population Age 65+", "sum"),
        Population_Age_75=("Population Age 75+", "sum"),
        Weighted_Longitude=("Weighted Longitude", "sum"),
        Weighted_Latitude=("Weighted Latitude", "sum"),
        Mesh_Count=("Mesh Code", "size"),
    )
    community["Longitude"] = community["Weighted_Longitude"] / community["Total_Population"]
    community["Latitude"] = community["Weighted_Latitude"] / community["Total_Population"]
    community = community.drop(columns=["Weighted_Longitude", "Weighted_Latitude"]).reset_index()
    community["Community ID"] = [f"COMMUNITY-{index + 1:05d}" for index in range(len(community))]

    label_to_position = pd.Series(
        np.arange(len(community), dtype="int32"),
        index=community["Community Numeric ID"],
    )
    selected["Community Position"] = (
        selected["Community Numeric ID"].map(label_to_position).to_numpy(dtype="int32")
    )
    attachments = selected[["Community Numeric ID", "Stable Root"]].drop_duplicates()
    attachment_community = (
        attachments["Community Numeric ID"].map(label_to_position).to_numpy(dtype="int32")
    )
    attachment_root = attachments["Stable Root"].to_numpy(dtype="int32")

    diagnostics = {
        "Populated Meshes": float(len(mesh)),
        "Attached Meshes": float(attached.sum()),
        "Baseline-Eligible Meshes": float(eligible.sum()),
        "Unresolved Population": float(mesh.loc[~eligible, "Total Population"].sum()),
        "Eligible Population": float(selected["Total Population"].sum()),
    }
    return (
        community,
        attachment_community,
        attachment_root,
        diagnostics,
        selected,
        selected_geometry,
    )


def closure_propensity(
    scores: np.ndarray,
    lower: float,
    upper: float,
    maximum: float = MAX_CLOSURE_PROPENSITY,
) -> np.ndarray:
    """Apply the declared central monotone score-to-closure mapping."""
    scaled = np.clip((scores - lower) / max(upper - lower, 1e-6), 0.0, 1.0)
    return (maximum * scaled).astype("float32")


def positive_score_quantile(scores: np.ndarray, quantile: float) -> float:
    """Return a quantile among finite positive road scores only."""
    positive = scores[np.isfinite(scores) & (scores > 0)]
    if len(positive) < 100:
        raise RuntimeError("Too few positive road scores for disruption screening.")
    return float(np.quantile(positive, quantile))


def simulate_isolation(
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
    draws: int = MONTE_CARLO_DRAWS,
    report_progress: bool = True,
) -> np.ndarray:
    """Run repeated section-level closures on the stable-component graph."""
    random = np.random.default_rng(seed)
    isolated_count = np.zeros(community_count, dtype="int32")
    for draw in range(draws):
        section_open = random.random(len(section_propensity)) >= section_propensity
        edge_open = section_open[candidate_edge_section]
        u = candidate_u[edge_open]
        v = candidate_v[edge_open]
        rows = np.concatenate([u, v])
        columns = np.concatenate([v, u])
        graph = coo_matrix(
            (np.ones(len(rows), dtype="uint8"), (rows, columns)),
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
        if report_progress and (draw + 1) % 500 == 0:
            print(f"  completed {draw + 1:,}/{draws:,} draws")
    return isolated_count.astype("float32") / draws


def cached_isolation(cache_name: str, *args: object, **kwargs: object) -> np.ndarray:
    """Persist one simulation block so long workflows can resume deterministically."""
    if len(args) < 10:
        raise ValueError("cached_isolation requires the complete simulation argument set.")
    draws = int(kwargs.get("draws", MONTE_CARLO_DRAWS))
    signature = content_signature(
        "community-isolation-event-idw-v3",
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
            "draws": draws,
        },
    )
    path = SIMULATION_CACHE_DIR / f"{cache_name}.npz"
    if path.exists():
        cached = np.load(path, allow_pickle=False)
        if cache_matches(cached, signature):
            print(f"  loaded cached simulation: {cache_name}", flush=True)
            return cached["frequency"].astype("float32")
    result = simulate_isolation(*args, **kwargs)
    SIMULATION_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        signature=np.asarray(signature),
        frequency=result.astype("float32"),
    )
    print(f"  cached simulation: {cache_name}", flush=True)
    return result


def rasterize_mesh_rgba(
    geometry: np.ndarray,
    values: np.ndarray,
    population_weight: np.ndarray,
    display_shape: tuple[int, int],
    display_transform: object,
    reference_population: float,
) -> np.ndarray:
    """Render non-overlapping mesh colors with opacity proportional to population."""
    value_raster = rasterize(
        ((item, float(value)) for item, value in zip(geometry, values)),
        out_shape=display_shape,
        transform=display_transform,
        fill=np.nan,
        all_touched=True,
        dtype="float32",
    )
    cell_alpha = np.clip(
        0.18 + 0.82 * np.sqrt(np.maximum(population_weight, 0.0) / reference_population),
        0.18,
        1.0,
    )
    alpha_raster = rasterize(
        ((item, float(alpha)) for item, alpha in zip(geometry, cell_alpha)),
        out_shape=display_shape,
        transform=display_transform,
        fill=0.0,
        all_touched=True,
        dtype="float32",
    )
    color_map = plt.get_cmap("viridis")
    rgba = color_map(np.clip(np.nan_to_num(value_raster, nan=0.0), 0.0, 1.0))
    rgba[..., 3] = np.where(np.isfinite(value_raster), alpha_raster, 0.0)
    return rgba


def main() -> None:
    sns.set_theme(style="white", context="paper")

    admin = pd.read_parquet(ADMIN_PATH, columns=["Municipality Name", "Geometry"])
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
            "Emergency Route Membership",
            "Network Analysis Eligible",
            "Geometry",
        ],
    )
    roads = roads.loc[roads["Network Analysis Eligible"]].reset_index(drop=True)
    road_geometry = road_exposure.decode_geometry(roads.pop("Geometry"))
    scores = road_exposure.load_or_build_road_scores(
        road_geometry,
        terrain_scores,
        extent,
        elevation_grid,
    )

    heavy_lower = positive_score_quantile(scores["Heavy"], CANDIDATE_QUANTILE)
    heavy_upper = positive_score_quantile(scores["Heavy"], UPPER_MAPPING_QUANTILE)
    candidate = np.isfinite(scores["Heavy"]) & (scores["Heavy"] >= heavy_lower)
    candidate_ids = roads.loc[candidate, "Road Section ID"].reset_index(drop=True)
    candidate_position = pd.Series(
        np.arange(len(candidate_ids), dtype="int32"),
        index=candidate_ids,
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

    target_definitions, target_network_components = external_target_definitions(
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
        diagnostics,
        selected_mesh,
        selected_mesh_geometry,
    ) = build_baseline_communities(
        nodes,
        node_geometry,
        stable_labels,
        target_network_components,
    )
    frequencies: dict[str, np.ndarray] = {}
    replicate_frequencies: dict[str, list[np.ndarray]] = {}
    candidate_scores: dict[str, np.ndarray] = {}
    for scenario in ("Moderate", "Heavy", "Extreme"):
        candidate_scores[scenario] = pd.Series(
            scores[scenario], index=roads["Road Section ID"]
        ).reindex(candidate_ids).to_numpy(dtype="float32")
        propensity = closure_propensity(candidate_scores[scenario], heavy_lower, heavy_upper)
        print(
            f"Simulating {scenario}: {np.count_nonzero(propensity):,} candidate sections "
            f"with non-zero closure propensity across {len(REPLICATE_SEEDS)} seed sets"
        )
        replicate_frequencies[scenario] = []
        for seed_index, seed in enumerate(REPLICATE_SEEDS):
            replicate_frequencies[scenario].append(
                cached_isolation(
                    f"central_{scenario.lower()}_seed_{seed}_m1000",
                    candidate_u,
                    candidate_v,
                    candidate_edge_section,
                    propensity,
                    root_count,
                    target_roots,
                    attachment_community,
                    attachment_root,
                    len(community),
                    seed,
                    report_progress=seed_index == 0,
                )
            )
        frequencies[scenario] = np.mean(
            np.vstack(replicate_frequencies[scenario]),
            axis=0,
        ).astype("float32")

    heavy_propensity = closure_propensity(candidate_scores["Heavy"], heavy_lower, heavy_upper)
    convergence = {
        draws: cached_isolation(
            f"convergence_heavy_seed_{RANDOM_SEED}_m{draws}",
            candidate_u,
            candidate_v,
            candidate_edge_section,
            heavy_propensity,
            root_count,
            target_roots,
            attachment_community,
            attachment_root,
            len(community),
            RANDOM_SEED,
            draws=draws,
            report_progress=False,
        )
        for draws in (500, 2000)
    }
    # Compare nested draw counts on one common seed. The primary reported Heavy
    # estimate remains the five-seed mean above; convergence is a separate
    # computational diagnostic and must not mix single-seed and averaged estimators.
    convergence[1000] = replicate_frequencies["Heavy"][0]
    target_sensitivity = {
        name: cached_isolation(
            f"target_{name.lower().replace(' ', '_')}_seed_{RANDOM_SEED}_m1000",
            candidate_u,
            candidate_v,
            candidate_edge_section,
            heavy_propensity,
            root_count,
            roots,
            attachment_community,
            attachment_root,
            len(community),
            RANDOM_SEED,
            report_progress=False,
        )
        for name, roots in target_definitions.items()
        if name != "Primary boundary gateways"
    }
    closure_sensitivity = {
        label: cached_isolation(
            f"closure_{label.lower()}_seed_{RANDOM_SEED}_m1000",
            candidate_u,
            candidate_v,
            candidate_edge_section,
            closure_propensity(candidate_scores["Heavy"], heavy_lower, heavy_upper, maximum),
            root_count,
            target_roots,
            attachment_community,
            attachment_root,
            len(community),
            RANDOM_SEED,
            report_progress=False,
        )
        for label, maximum in (("Low", 0.15), ("High", 0.45))
    }

    total_population = community["Total_Population"].to_numpy(dtype=float)
    older_population = community["Population_Age_65"].to_numpy(dtype=float)
    seed_expected_population = {
        scenario: np.asarray(
            [
                np.sum(total_population * frequency)
                for frequency in replicate_frequencies[scenario]
            ],
            dtype=float,
        )
        for scenario in ("Moderate", "Heavy", "Extreme")
    }
    heavy_seed_sd = float(np.std(seed_expected_population["Heavy"], ddof=1))
    heavy_seed_min = float(np.min(seed_expected_population["Heavy"]))
    heavy_seed_max = float(np.max(seed_expected_population["Heavy"]))
    yatsushiro_bound_expected: dict[str, float] = {}
    for bound_factor in (0.70, 0.80):
        bound_terrain_scores, _, _, _ = road_exposure.load_or_build_landslide_scores(
            admin,
            admin_geometry,
            admin_union,
            extent,
            display_shape,
            display_transform,
            yatsushiro_factor=bound_factor,
        )
        bound_road_scores = road_exposure.load_or_build_road_scores(
            road_geometry,
            bound_terrain_scores,
            extent,
            elevation_grid,
            yatsushiro_factor=bound_factor,
        )
        bound_candidate_score = pd.Series(
            bound_road_scores["Heavy"], index=roads["Road Section ID"]
        ).reindex(candidate_ids).to_numpy(dtype="float32")
        bound_propensity = closure_propensity(
            bound_candidate_score,
            heavy_lower,
            heavy_upper,
        )
        bound_frequencies = [
            cached_isolation(
                f"yatsushiro_{int(bound_factor * 100)}_heavy_seed_{seed}_m1000",
                candidate_u,
                candidate_v,
                candidate_edge_section,
                bound_propensity,
                root_count,
                target_roots,
                attachment_community,
                attachment_root,
                len(community),
                seed,
                report_progress=False,
            )
            for seed in REPLICATE_SEEDS
        ]
        bound_mean_frequency = np.mean(np.vstack(bound_frequencies), axis=0)
        yatsushiro_bound_expected[f"{bound_factor:.2f}"] = float(
            np.sum(total_population * bound_mean_frequency)
        )
    mesh_community = selected_mesh["Community Position"].to_numpy(dtype="int32")
    mesh_total_population = selected_mesh["Total Population"].to_numpy(dtype=float)
    mesh_older_population = selected_mesh["Population Age 65+"].to_numpy(dtype=float)
    total_reference = max(float(np.quantile(mesh_total_population, 0.95)), 1.0)
    older_reference = max(float(np.quantile(mesh_older_population, 0.95)), 1.0)

    fig = plt.figure(figsize=(14.5, 11), constrained_layout=True)
    grid = fig.add_gridspec(
        2,
        3,
        width_ratios=[1.0, 1.0, 0.045],
        height_ratios=[1.0, 1.0],
        wspace=0.08,
        hspace=0.08,
    )
    axes = np.array(
        [
            fig.add_subplot(grid[0, 0]),
            fig.add_subplot(grid[0, 1]),
            fig.add_subplot(grid[1, 0]),
            fig.add_subplot(grid[1, 1]),
        ]
    )
    colorbar_axis = fig.add_subplot(grid[:, 2])
    boundary_segments = road_exposure.line_segments(shapely.boundary(admin_geometry))
    emergency_segments = road_exposure.line_segments(
        road_geometry[roads["Emergency Route Membership"].astype("string").ne("None").to_numpy()]
    )
    panels = [
        (
            "Moderate rainfall\nTotal-population exposure",
            "Moderate",
            mesh_total_population,
            total_reference,
        ),
        (
            "Heavy rainfall\nTotal-population exposure",
            "Heavy",
            mesh_total_population,
            total_reference,
        ),
        (
            "Extreme rainfall\nTotal-population exposure",
            "Extreme",
            mesh_total_population,
            total_reference,
        ),
        (
            "Extreme rainfall\nPopulation age 65+ exposure",
            "Extreme",
            mesh_older_population,
            older_reference,
        ),
    ]

    scalar_mappable = ScalarMappable(norm=Normalize(vmin=0, vmax=1), cmap="viridis")
    for index, (axis, (annotation, scenario, population_weight, reference)) in enumerate(
        zip(axes, panels)
    ):
        axis.set_facecolor("#F8FAFC")
        axis.add_collection(
            LineCollection(
                emergency_segments,
                colors="#CBD5E1",
                linewidths=0.35,
                alpha=0.75,
                zorder=2,
            )
        )
        axis.add_collection(
            LineCollection(
                boundary_segments,
                colors="#667085",
                linewidths=0.52,
                alpha=0.88,
                zorder=4,
            )
        )
        mesh_rgba = rasterize_mesh_rgba(
            selected_mesh_geometry,
            frequencies[scenario][mesh_community],
            population_weight,
            display_shape,
            display_transform,
            reference,
        )
        axis.imshow(
            mesh_rgba,
            extent=(west, east, south, north),
            origin="upper",
            interpolation="nearest",
            zorder=6,
        )
        expected_total = float(np.sum(total_population * frequencies[scenario]))
        expected_older = float(np.sum(older_population * frequencies[scenario]))
        axis.text(
            0.018,
            0.982,
            (
                f"{annotation}\n"
                f"Expected isolated population: {expected_total:,.0f}\n"
                f"Expected age 65+: {expected_older:,.0f}"
            ),
            transform=axis.transAxes,
            ha="left",
            va="top",
            fontsize=8.2,
            fontweight="bold",
            color="#172033",
            bbox={
                "boxstyle": "round,pad=0.30",
                "facecolor": "white",
                "edgecolor": "#D0D5DD",
                "alpha": 0.94,
            },
            zorder=20,
        )
        road_exposure.style_map_axis(axis, extent)
        road_exposure.add_panel_label(axis, "abcd"[index])

    axes[0].legend(
        handles=[
            Patch(facecolor="#21918C", alpha=0.28, label="Lower cell population"),
            Patch(facecolor="#21918C", alpha=0.95, label="Higher cell population"),
        ],
        loc="lower left",
        fontsize=7.1,
        frameon=True,
        framealpha=0.94,
    )
    axes[3].legend(
        handles=[
            Patch(facecolor="#21918C", alpha=0.28, label="Lower cell population age 65+"),
            Patch(facecolor="#21918C", alpha=0.95, label="Higher cell population age 65+"),
        ],
        loc="lower left",
        fontsize=7.1,
        frameon=True,
        framealpha=0.94,
    )

    convergence_delta = max(
        float(np.quantile(np.abs(convergence[500] - convergence[1000]), 0.95)),
        float(np.quantile(np.abs(convergence[1000] - convergence[2000]), 0.95)),
    )
    target_expected = {
        name: float(np.sum(total_population * frequency))
        for name, frequency in target_sensitivity.items()
    }
    closure_expected = {
        name: float(np.sum(total_population * frequency))
        for name, frequency in closure_sensitivity.items()
    }
    axes[1].text(
        0.982,
        0.018,
        (
            f"M=500/1,000/2,000 95th-pct frequency difference: {convergence_delta:.3f}\n"
            f"Five-seed Heavy expected isolated: {heavy_seed_min:,.0f}–"
            f"{heavy_seed_max:,.0f} (SD {heavy_seed_sd:,.1f})\n"
            f"Yatsushiro 0.70–0.80 assignment bounds: "
            f"{min(yatsushiro_bound_expected.values()):,.0f}–"
            f"{max(yatsushiro_bound_expected.values()):,.0f}\n"
            f"Target sensitivity, expected isolated: "
            f"{min(target_expected.values()):,.0f}–{max(target_expected.values()):,.0f}\n"
            f"Closure mapping sensitivity: "
            f"{min(closure_expected.values()):,.0f}–{max(closure_expected.values()):,.0f}"
        ),
        transform=axes[1].transAxes,
        ha="right",
        va="bottom",
        fontsize=6.7,
        color="#344054",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#D0D5DD", "alpha": 0.92},
        zorder=20,
    )

    colorbar = fig.colorbar(scalar_mappable, cax=colorbar_axis)
    colorbar.set_label("Community isolation frequency\n(simulation conditional)", fontsize=9)
    colorbar.ax.tick_params(labelsize=8)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SVG_OUT, format="svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    OUT.write_bytes(
        resvg_py.svg_to_bytes(
            svg_path=str(SVG_OUT),
            dpi=300.0,
            background="white",
        )
    )

    print(f"Saved SVG: {SVG_OUT.relative_to(ROOT)}")
    print(f"Converted PNG (300 dpi): {OUT.relative_to(ROOT)}")
    print(f"Terrain-score construction: {model_mode}")
    print(f"Candidate road sections: {len(candidate_ids):,} ({candidate.mean():.1%})")
    print(f"Stable contracted network roots: {root_count:,}")
    print(f"Candidate inter-root road edges: {len(candidate_u):,}")
    print(f"Emergency-road target roots: {len(target_roots):,}")
    print(f"Baseline communities: {len(community):,}")
    for key, value in diagnostics.items():
        print(f"{key}: {value:,.0f}")
    for scenario in ("Moderate", "Heavy", "Extreme"):
        expected_total = float(np.sum(total_population * frequencies[scenario]))
        expected_older = float(np.sum(older_population * frequencies[scenario]))
        print(
            f"{scenario}: expected isolated population={expected_total:,.1f}; "
            f"age 65+={expected_older:,.1f}; maximum frequency={frequencies[scenario].max():.3f}"
        )
        values = seed_expected_population[scenario]
        print(
            f"  five-seed expected isolated population: mean={values.mean():,.1f}; "
            f"SD={values.std(ddof=1):,.1f}; range={values.min():,.1f}–{values.max():,.1f}"
        )
    print(
        "Yatsushiro 0.70-0.80 Heavy expected-isolated bounds: "
        f"{min(yatsushiro_bound_expected.values()):,.3f}-"
        f"{max(yatsushiro_bound_expected.values()):,.3f}"
    )
    print(f"Convergence 95th-percentile frequency difference: {convergence_delta:.4f}")
    print("Interpretation: Monte Carlo frequency conditional on the declared screening model")


if __name__ == "__main__":
    main()
