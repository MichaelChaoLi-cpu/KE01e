#!/usr/bin/env python3
"""Basic Service Reachability Loss.

Plan: Map Heavy-scenario reachability loss for shelter, emergency-water, and fire
services and summarize population exposure and reachable-route travel-time penalties
for shelter, water, fire, and municipal facilities.
Framework: Section 5 secondary consequence estimands; Section 6 service reachability
loss and excess travel time; Section 7 nearest-service routing on the accepted
community and road-disruption screening network.

The 1,000-draw loss frequency is conditional on the central candidate-road closure
mapping. Excess time is estimated on the complete weighted road graph using 100
rerouting draws and remains a scenario estimate rather than observed response time.
"""
from __future__ import annotations

import os
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
from rasterio.transform import from_bounds
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.spatial import cKDTree
import seaborn as sns
import shapely

import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
ROAD_PATH = PROCESSED / "road_sections_preprocessed.parquet"
EDGE_PATH = PROCESSED / "road_edges_preprocessed.parquet"
NODE_PATH = PROCESSED / "road_nodes_preprocessed.parquet"
DESIGNATED_SHELTER_PATH = PROCESSED / "designated_shelters_preprocessed.parquet"
EVACUATION_SITE_PATH = PROCESSED / "emergency_evacuation_sites_preprocessed.parquet"
CURRENT_SHELTER_PATH = PROCESSED / "current_shelters_preprocessed.parquet"
WATER_PATH = PROCESSED / "emergency_water_points_preprocessed.parquet"
FIRE_PATH = PROCESSED / "fire_stations_preprocessed.parquet"
MUNICIPAL_PATH = PROCESSED / "public_offices_halls_preprocessed.parquet"
OUT = ROOT / "data/results/figures/Figure_basic_service_reachability_loss.png"

DISPLAY_WIDTH = 950
SERVICE_ATTACHMENT_LIMIT_M = 500.0
SERVICE_CLASSES = ("Shelter", "Emergency water", "Fire service", "Municipal facility")
SERVICE_COLORS = {
    "Shelter": "#2A9D8F",
    "Emergency water": "#3A86FF",
    "Fire service": "#E76F51",
    "Municipal facility": "#7A5195",
}
FULL_GRAPH_TRAVEL_DRAWS = 100
FULL_GRAPH_CACHE = ROOT / "data/exp/analysis_cache/full_graph_service_times.npz"


def point_geometry_from_coordinates(frame: pd.DataFrame) -> np.ndarray:
    """Create point geometries from resolved longitude-latitude records."""
    resolved = frame["Longitude"].notna() & frame["Latitude"].notna()
    return shapely.points(
        frame.loc[resolved, "Longitude"].to_numpy(dtype=float),
        frame.loc[resolved, "Latitude"].to_numpy(dtype=float),
    )


def service_geometries() -> tuple[dict[str, np.ndarray], dict[str, tuple[int, int]]]:
    """Load the four declared service classes and report resolved counts."""
    designated = pd.read_parquet(DESIGNATED_SHELTER_PATH, columns=["Geometry"])
    evacuation = pd.read_parquet(EVACUATION_SITE_PATH, columns=["Geometry"])
    current = pd.read_parquet(
        CURRENT_SHELTER_PATH,
        columns=["Latitude", "Longitude"],
    )
    designated_geometry = road_exposure.decode_geometry(designated["Geometry"])
    evacuation_geometry = road_exposure.decode_geometry(evacuation["Geometry"])
    current_geometry = point_geometry_from_coordinates(current)
    shelter_geometry = np.concatenate(
        [designated_geometry, evacuation_geometry, current_geometry]
    )

    water = pd.read_parquet(WATER_PATH, columns=["Latitude", "Longitude"])
    water_geometry = point_geometry_from_coordinates(water)
    fire = pd.read_parquet(FIRE_PATH, columns=["Geometry"])
    fire_geometry = road_exposure.decode_geometry(fire["Geometry"])
    municipal = pd.read_parquet(MUNICIPAL_PATH, columns=["Geometry"])
    municipal_geometry = road_exposure.decode_geometry(municipal["Geometry"])

    geometry = {
        "Shelter": shelter_geometry,
        "Emergency water": water_geometry,
        "Fire service": fire_geometry,
        "Municipal facility": municipal_geometry,
    }
    counts = {
        "Shelter": (len(shelter_geometry), len(designated) + len(evacuation) + len(current)),
        "Emergency water": (len(water_geometry), len(water)),
        "Fire service": (len(fire_geometry), len(fire)),
        "Municipal facility": (len(municipal_geometry), len(municipal)),
    }
    return geometry, counts


def attach_services_to_roots(
    geometry: dict[str, np.ndarray],
    node_geometry: np.ndarray,
    stable_labels: np.ndarray,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], dict[str, int]]:
    """Attach service features to their nearest road root within the declared limit."""
    node_coordinates = shapely.get_coordinates(node_geometry)[:, :2]
    reference_latitude = float(np.mean(node_coordinates[:, 1]))
    node_xy = isolation.planar_coordinates(node_coordinates, reference_latitude)
    tree = cKDTree(node_xy)
    service_roots: dict[str, np.ndarray] = {}
    service_nodes: dict[str, np.ndarray] = {}
    attached_counts: dict[str, int] = {}
    for service, features in geometry.items():
        coordinates = shapely.get_coordinates(shapely.centroid(features))[:, :2]
        feature_xy = isolation.planar_coordinates(coordinates, reference_latitude)
        distance, nearest_node = tree.query(feature_xy, k=1, workers=-1)
        attached = distance <= SERVICE_ATTACHMENT_LIMIT_M
        service_nodes[service] = np.unique(nearest_node[attached]).astype("int32")
        service_roots[service] = np.unique(stable_labels[nearest_node[attached]]).astype("int32")
        attached_counts[service] = int(attached.sum())
    return service_roots, service_nodes, attached_counts


def full_graph_service_excess_time(
    edge_u: np.ndarray,
    edge_v: np.ndarray,
    edge_time: np.ndarray,
    edge_candidate_position: np.ndarray,
    section_propensity: np.ndarray,
    node_count: int,
    service_nodes: dict[str, np.ndarray],
    mesh_community: np.ndarray,
    mesh_node: np.ndarray,
    community_count: int,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    """Estimate full-network excess time with 100 weighted rerouting draws."""
    signature = (
        f"v2|{len(edge_u)}|{node_count}|{len(section_propensity)}|"
        f"{float(np.sum(section_propensity)):.6f}|{FULL_GRAPH_TRAVEL_DRAWS}|"
        + "|".join(f"{name}:{len(service_nodes[name])}" for name in SERVICE_CLASSES)
    )
    if FULL_GRAPH_CACHE.exists():
        cached = np.load(FULL_GRAPH_CACHE, allow_pickle=False)
        if str(cached["signature"].item()) == signature:
            return (
                {name: cached[f"excess_{name}"].astype("float32") for name in SERVICE_CLASSES},
                {name: cached[f"baseline_{name}"].astype("float64") for name in SERVICE_CLASSES},
            )

    def graph_for(section_open: np.ndarray | None) -> object:
        if section_open is None:
            keep = np.ones(len(edge_u), dtype=bool)
        else:
            keep = (edge_candidate_position < 0) | section_open[
                np.maximum(edge_candidate_position, 0)
            ]
        u = edge_u[keep]
        v = edge_v[keep]
        weight = edge_time[keep]
        return coo_matrix(
            (
                np.concatenate([weight, weight]),
                (np.concatenate([u, v]), np.concatenate([v, u])),
            ),
            shape=(node_count, node_count),
        ).tocsr()

    def community_node_distance(node_distance: np.ndarray) -> np.ndarray:
        result = np.full(community_count, np.inf, dtype="float64")
        np.minimum.at(result, mesh_community, node_distance[mesh_node])
        return result

    baseline_graph = graph_for(None)
    baseline: dict[str, np.ndarray] = {}
    for service in SERVICE_CLASSES:
        distance = dijkstra(
            baseline_graph,
            directed=False,
            indices=service_nodes[service],
            min_only=True,
        )
        baseline[service] = community_node_distance(distance)

    excess_sum = {service: np.zeros(community_count, dtype="float64") for service in SERVICE_CLASSES}
    excess_count = {service: np.zeros(community_count, dtype="int32") for service in SERVICE_CLASSES}
    random = np.random.default_rng(isolation.RANDOM_SEED + 80_000)
    for draw in range(FULL_GRAPH_TRAVEL_DRAWS):
        section_open = random.random(len(section_propensity)) >= section_propensity
        graph = graph_for(section_open)
        for service in SERVICE_CLASSES:
            distance = dijkstra(
                graph,
                directed=False,
                indices=service_nodes[service],
                min_only=True,
            )
            disrupted = community_node_distance(distance)
            reachable = np.isfinite(baseline[service]) & np.isfinite(disrupted)
            excess_sum[service][reachable] += np.maximum(
                disrupted[reachable] - baseline[service][reachable],
                0.0,
            )
            excess_count[service][reachable] += 1
        if (draw + 1) % 20 == 0:
            print(f"  completed {draw + 1:,}/{FULL_GRAPH_TRAVEL_DRAWS:,} full-network travel draws")

    mean_excess: dict[str, np.ndarray] = {}
    for service in SERVICE_CLASSES:
        values = np.full(community_count, np.nan, dtype="float32")
        available = excess_count[service] > 0
        values[available] = (
            excess_sum[service][available] / excess_count[service][available]
        ).astype("float32")
        mean_excess[service] = values
    FULL_GRAPH_CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        FULL_GRAPH_CACHE,
        signature=np.asarray(signature),
        **{f"excess_{name}": mean_excess[name] for name in SERVICE_CLASSES},
        **{f"baseline_{name}": baseline[name] for name in SERVICE_CLASSES},
    )
    return mean_excess, baseline


def prepare_pair_reduction(
    root_u: np.ndarray,
    root_v: np.ndarray,
    edge_section: np.ndarray,
    edge_time: np.ndarray,
    root_count: int,
) -> dict[str, np.ndarray]:
    """Pre-sort parallel contracted edges for per-draw minimum-time reduction."""
    low = np.minimum(root_u, root_v).astype("int64")
    high = np.maximum(root_u, root_v).astype("int64")
    key = low * np.int64(root_count) + high
    order = np.argsort(key, kind="stable")
    sorted_key = key[order]
    start = np.r_[0, np.flatnonzero(np.diff(sorted_key)) + 1].astype("int64")
    return {
        "order": order,
        "start": start,
        "pair_u": low[order][start].astype("int32"),
        "pair_v": high[order][start].astype("int32"),
        "edge_section": edge_section[order],
        "edge_time": edge_time[order],
    }


def weighted_draw_graph(
    section_open: np.ndarray,
    pair_reduction: dict[str, np.ndarray],
    root_count: int,
) -> object:
    """Create a symmetric minimum-time root graph for one closure draw."""
    candidate_weight = np.where(
        section_open[pair_reduction["edge_section"]],
        pair_reduction["edge_time"],
        np.inf,
    )
    pair_weight = np.minimum.reduceat(candidate_weight, pair_reduction["start"])
    keep = np.isfinite(pair_weight)
    u = pair_reduction["pair_u"][keep]
    v = pair_reduction["pair_v"][keep]
    weight = pair_weight[keep]
    return coo_matrix(
        (
            np.concatenate([weight, weight]),
            (np.concatenate([u, v]), np.concatenate([v, u])),
        ),
        shape=(root_count, root_count),
    ).tocsr()


def community_distance(
    root_distance: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
) -> np.ndarray:
    """Return the minimum root distance among each community's road attachments."""
    distance = np.full(community_count, np.inf, dtype="float64")
    np.minimum.at(distance, attachment_community, root_distance[attachment_root])
    return distance


def simulate_service_loss(
    section_propensity: np.ndarray,
    pair_reduction: dict[str, np.ndarray],
    root_count: int,
    service_roots: dict[str, np.ndarray],
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], dict[str, np.ndarray]]:
    """Estimate Heavy-scenario reachability loss and conditional excess travel time."""
    all_open = np.ones(len(section_propensity), dtype=bool)
    baseline_graph = weighted_draw_graph(all_open, pair_reduction, root_count)
    baseline: dict[str, np.ndarray] = {}
    for service in SERVICE_CLASSES:
        root_distance = dijkstra(
            baseline_graph,
            directed=False,
            indices=service_roots[service],
            min_only=True,
        )
        baseline[service] = community_distance(
            root_distance,
            attachment_community,
            attachment_root,
            community_count,
        )

    loss_count = {service: np.zeros(community_count, dtype="int32") for service in SERVICE_CLASSES}
    excess_sum = {service: np.zeros(community_count, dtype="float64") for service in SERVICE_CLASSES}
    excess_count = {service: np.zeros(community_count, dtype="int32") for service in SERVICE_CLASSES}
    random = np.random.default_rng(isolation.RANDOM_SEED + 80_000)
    for draw in range(isolation.MONTE_CARLO_DRAWS):
        section_open = random.random(len(section_propensity)) >= section_propensity
        graph = weighted_draw_graph(section_open, pair_reduction, root_count)
        for service in SERVICE_CLASSES:
            root_distance = dijkstra(
                graph,
                directed=False,
                indices=service_roots[service],
                min_only=True,
            )
            disrupted = community_distance(
                root_distance,
                attachment_community,
                attachment_root,
                community_count,
            )
            baseline_reachable = np.isfinite(baseline[service])
            reachable = baseline_reachable & np.isfinite(disrupted)
            loss_count[service] += baseline_reachable & ~np.isfinite(disrupted)
            excess_sum[service][reachable] += np.maximum(
                disrupted[reachable] - baseline[service][reachable],
                0.0,
            )
            excess_count[service][reachable] += 1
        if (draw + 1) % 250 == 0:
            print(f"  completed {draw + 1:,}/{isolation.MONTE_CARLO_DRAWS:,} service draws")

    loss_frequency: dict[str, np.ndarray] = {}
    mean_excess: dict[str, np.ndarray] = {}
    for service in SERVICE_CLASSES:
        baseline_reachable = np.isfinite(baseline[service])
        loss = np.full(community_count, np.nan, dtype="float32")
        loss[baseline_reachable] = (
            loss_count[service][baseline_reachable].astype("float32")
            / isolation.MONTE_CARLO_DRAWS
        )
        loss_frequency[service] = loss
        excess = np.full(community_count, np.nan, dtype="float32")
        has_reachable_draw = excess_count[service] > 0
        excess[has_reachable_draw] = (
            excess_sum[service][has_reachable_draw]
            / excess_count[service][has_reachable_draw]
        ).astype("float32")
        mean_excess[service] = excess
    return loss_frequency, mean_excess, baseline


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

    terrain_scores, _, model_mode, elevation_grid = road_exposure.build_landslide_scores(
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
    road_scores = road_exposure.road_scores(road_geometry, terrain_scores, extent, elevation_grid)
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
    candidate_heavy_scores = pd.Series(
        road_scores["Heavy"], index=roads["Road Section ID"]
    ).reindex(candidate_ids).to_numpy(dtype="float32")
    section_propensity = isolation.closure_propensity(
        candidate_heavy_scores,
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
            "Baseline Edge Travel Time (min)",
            "Network Analysis Eligible",
        ],
    )
    edges = edges.loc[edges["Network Analysis Eligible"]].reset_index(drop=True)
    edge_u = node_index.get_indexer(edges["From Node ID"])
    edge_v = node_index.get_indexer(edges["To Node ID"])
    if np.any(edge_u < 0) or np.any(edge_v < 0):
        raise RuntimeError("Road edges reference missing network nodes.")
    edge_candidate = edges["Road Section ID"].isin(candidate_ids).to_numpy()
    edge_candidate_position_full = (
        edges["Road Section ID"].map(candidate_position).fillna(-1).to_numpy(dtype="int32")
    )

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
    candidate_edge_time = edges.loc[
        edge_candidate, "Baseline Edge Travel Time (min)"
    ].to_numpy(dtype="float64")
    between_root = candidate_u != candidate_v
    pair_reduction = prepare_pair_reduction(
        candidate_u[between_root],
        candidate_v[between_root],
        candidate_edge_section[between_root],
        candidate_edge_time[between_root],
        root_count,
    )

    _, target_network_components = isolation.external_target_definitions(
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
        community_diagnostics,
        selected_mesh,
        selected_mesh_geometry,
    ) = isolation.build_baseline_communities(
        nodes,
        node_geometry,
        stable_labels,
        target_network_components,
    )

    geometry, source_counts = service_geometries()
    service_roots, service_nodes, attached_counts = attach_services_to_roots(
        geometry,
        node_geometry,
        stable_labels,
    )
    for service in SERVICE_CLASSES:
        if len(service_roots[service]) == 0:
            raise RuntimeError(f"No {service} features could be attached to the road network.")

    loss_frequency, _, _ = simulate_service_loss(
        section_propensity,
        pair_reduction,
        root_count,
        service_roots,
        attachment_community,
        attachment_root,
        len(community),
    )
    mean_excess, baseline_distance = full_graph_service_excess_time(
        edge_u,
        edge_v,
        edges["Baseline Edge Travel Time (min)"].to_numpy(dtype="float64"),
        edge_candidate_position_full,
        section_propensity,
        len(nodes),
        service_nodes,
        selected_mesh["Community Position"].to_numpy(dtype="int32"),
        selected_mesh["Attached Node Position"].to_numpy(dtype="int32"),
        len(community),
    )

    total_population = community["Total_Population"].to_numpy(dtype=float)
    mesh_community = selected_mesh["Community Position"].to_numpy(dtype="int32")
    mesh_population = selected_mesh["Total Population"].to_numpy(dtype=float)
    population_reference = max(float(np.quantile(mesh_population, 0.95)), 1.0)
    expected_loss_population = {
        service: float(np.nansum(loss_frequency[service] * total_population))
        for service in SERVICE_CLASSES
    }
    median_excess = {
        service: float(np.nanmedian(mean_excess[service]))
        for service in SERVICE_CLASSES
    }

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
    map_services = ("Shelter", "Emergency water", "Fire service")
    for index, (axis, service) in enumerate(zip(axes[:3], map_services)):
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
        mesh_rgba = isolation.rasterize_mesh_rgba(
            selected_mesh_geometry,
            loss_frequency[service][mesh_community],
            mesh_population,
            display_shape,
            display_transform,
            population_reference,
        )
        axis.imshow(
            mesh_rgba,
            extent=(west, east, south, north),
            origin="upper",
            interpolation="nearest",
            zorder=6,
        )
        axis.add_collection(
            LineCollection(
                boundary_segments,
                colors="#667085",
                linewidths=0.52,
                alpha=0.88,
                zorder=8,
            )
        )
        coverage_note = (
            f"\nResolved-point lower bound: {source_counts[service][0]}/{source_counts[service][1]} located"
            if service == "Emergency water"
            else ""
        )
        axis.text(
            0.018,
            0.982,
            (
                f"{service} reachability loss\n"
                f"Heavy rainfall\n"
                f"Expected affected population: {expected_loss_population[service]:,.0f}\n"
                f"Median excess time: {median_excess[service]:.2f} min"
                f"{coverage_note}"
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
        road_exposure.add_panel_label(axis, "abc"[index])

    axes[0].legend(
        handles=[
            Patch(facecolor="#667085", alpha=0.28, label="Lower cell population"),
            Patch(facecolor="#667085", alpha=0.95, label="Higher cell population"),
        ],
        loc="lower left",
        fontsize=7.1,
        frameon=True,
        framealpha=0.94,
    )

    bar_axis = axes[3]
    y = np.arange(len(SERVICE_CLASSES))
    affected = np.array([expected_loss_population[service] for service in SERVICE_CLASSES])
    excess = np.array([median_excess[service] for service in SERVICE_CLASSES])
    bar_axis.barh(
        y,
        affected,
        color=[SERVICE_COLORS[service] for service in SERVICE_CLASSES],
        alpha=0.88,
        height=0.58,
        zorder=3,
    )
    bar_axis.set_yticks(y, labels=SERVICE_CLASSES)
    bar_axis.invert_yaxis()
    bar_axis.set_xlabel("Expected population losing reachability", fontsize=8.7)
    bar_axis.set_xlim(0, affected.max() * 1.08)
    bar_axis.tick_params(axis="both", labelsize=8)
    bar_axis.grid(axis="x", color="#D0D5DD", linewidth=0.55, linestyle=(0, (3, 3)))
    bar_axis.set_axisbelow(True)
    for index, value in enumerate(affected):
        large_bar = value > affected.max() * 0.80
        bar_axis.text(
            value - affected.max() * 0.012 if large_bar else value + affected.max() * 0.010,
            index,
            f"{value:,.0f}",
            va="center",
            ha="right" if large_bar else "left",
            fontsize=7.5,
            color="white" if large_bar else "#172033",
            fontweight="bold",
        )
    time_axis = bar_axis.twiny()
    time_axis.scatter(
        excess,
        y,
        color="#172033",
        s=28,
        zorder=6,
    )
    time_axis.set_xlabel(
        f"Median full-network excess travel time when reachable (min; {FULL_GRAPH_TRAVEL_DRAWS} draws)",
        fontsize=8.7,
    )
    time_axis.tick_params(axis="x", labelsize=8)
    for index, value in enumerate(excess):
        time_axis.text(
            value,
            index - 0.20,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=7.2,
            color="#172033",
        )
    road_exposure.add_panel_label(bar_axis, "d")
    for spine in bar_axis.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.85)
        spine.set_color("#344054")

    scalar_mappable = ScalarMappable(norm=Normalize(vmin=0, vmax=1), cmap="viridis")
    colorbar = fig.colorbar(scalar_mappable, cax=colorbar_axis)
    colorbar.set_label("Service reachability loss frequency\n(simulation conditional)", fontsize=9)
    colorbar.ax.tick_params(labelsize=8)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Saved: {OUT.relative_to(ROOT)}")
    print(f"Terrain-score construction: {model_mode}")
    print(f"Communities evaluated: {len(community):,}")
    print(f"Eligible population: {community_diagnostics['Eligible Population']:,.0f}")
    for service in SERVICE_CLASSES:
        resolved, total = source_counts[service]
        baseline_reachable = int(np.isfinite(baseline_distance[service]).sum())
        print(
            f"{service}: resolved source features={resolved:,}/{total:,}; "
            f"road-attached={attached_counts[service]:,}; roots={len(service_roots[service]):,}; "
            f"baseline-reachable communities={baseline_reachable:,}; "
            f"expected affected population={expected_loss_population[service]:,.1f}; "
            f"median excess time={median_excess[service]:.3f} min"
        )
    print("Interpretation: conditional reachability loss; excess time uses the full weighted road graph")


if __name__ == "__main__":
    main()
