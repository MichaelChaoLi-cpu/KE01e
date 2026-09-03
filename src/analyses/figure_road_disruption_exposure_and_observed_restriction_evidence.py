#!/usr/bin/env python3
"""Road Disruption Exposure and Observed Restriction Evidence.

Plan: Map scenario road-disruption exposure and compare the Heavy scenario
ranking with reliably matched rockfall and slope-collapse restriction evidence.
Framework: Section 5 road-ranking validation; Section 6 slope-to-road transfer
score D_e = sum(q_ie H_i) / sum(q_ie); Section 7 validation of slope-to-road
translation. Scores are screening indices, not road-closure probabilities.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

from affine import Affine
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import resvg_py
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from scipy.ndimage import maximum_filter
from scipy.special import expit
import seaborn as sns
import shapely

import figure_official_threshold_adjusted_landslide_disruption_score as terrain_score
from cache_fingerprint import cache_matches, content_signature
from road_restriction_event_validation import (
    build_matched_design,
    event_weighted_concordance,
    load_restriction_evidence,
)


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
WARNING_PATH = PROCESSED / "landslide_warning_zones_preprocessed.parquet"
LANDSLIDE_PATH = PROCESSED / "gsi_2016_landslide_inventory_preprocessed.parquet"
SCENARIO_PATH = PROCESSED / "jma_rainfall_scenario_quantiles_preprocessed.parquet"
THRESHOLD_PATH = PROCESSED / "official_threshold_factors_preprocessed.parquet"
ROAD_PATH = PROCESSED / "road_sections_preprocessed.parquet"
EDGE_PATH = PROCESSED / "road_edges_preprocessed.parquet"
MATCH_PATH = PROCESSED / "road_restriction_edge_matches_preprocessed.parquet"
RESTRICTION_PATH = PROCESSED / "road_restrictions_preprocessed.parquet"
OUT = ROOT / "data/results/figures/Figure_road_disruption_exposure_and_observed_restriction_evidence.png"
SVG_OUT = OUT.with_suffix(".svg")
INTERMEDIATE = ROOT / "data/results/intermediate"
TRIGGER_DECISION_PATH = (
    ROOT / "data/exp/revision/reviewer-2-comment-7/decision.json"
)

DISPLAY_WIDTH = 950
SAMPLE_FRACTIONS = (0.20, 0.50, 0.80)
UPSLOPE_RADIUS_CELLS = 3
MIN_UPSLOPE_RELIEF_M = 10.0
MIN_DOWNSLOPE_ALIGNMENT = 0.20
LANDSLIDE_REASON_PATTERN = "落石|法面崩落|土砂流入"
REASON_LABELS = {
    "落石": "Rockfall restriction",
    "法面崩落": "Slope-collapse restriction",
    "土砂流入": "Sediment-inflow restriction",
}
REASON_COLORS = {
    "落石": "#11D9E6",
    "法面崩落": "#35D07F",
    "土砂流入": "#4EA1FF",
}


def decode_geometry(series: pd.Series) -> np.ndarray:
    """Decode a geometry column while preserving row alignment."""
    geometry = shapely.from_wkb(series.to_numpy())
    if np.any(shapely.is_missing(geometry) | shapely.is_empty(geometry)):
        raise RuntimeError("A required geometry layer contains missing or empty features.")
    return geometry


def line_segments(geometry: np.ndarray) -> list[np.ndarray]:
    """Convert line-like geometries to Matplotlib segments."""
    segments: list[np.ndarray] = []
    for part in shapely.get_parts(geometry):
        coordinates = shapely.get_coordinates(part)[:, :2]
        if len(coordinates) >= 2:
            segments.append(coordinates)
    return segments


def build_landslide_scores(
    admin: pd.DataFrame,
    admin_geometry: np.ndarray,
    admin_union: object,
    extent: tuple[float, float, float, float],
    display_shape: tuple[int, int],
    display_transform: Affine,
    yatsushiro_factor: float = 0.75,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], str, np.ndarray]:
    """Reproduce the accepted official-threshold-adjusted terrain score grid."""
    native_features, aggregated_transform, source_crs = terrain_score.native_terrain_features()
    features = {
        name: terrain_score.reproject_feature(
            array,
            aggregated_transform,
            source_crs,
            display_shape,
            display_transform,
        )
        for name, array in native_features.items()
    }
    admin_mask = rasterize(
        [(admin_union, 1)],
        out_shape=display_shape,
        transform=display_transform,
        fill=0,
        all_touched=True,
        dtype="uint8",
    ).astype(bool)

    current_warning_geometry, _ = terrain_score.warning_zone_geometry()
    validation_warning_geometry, _ = terrain_score.warning_zone_geometry(
        terrain_score.LANDSLIDE_VALIDATION_DATE
    )
    features["Warning-Zone Exposure"] = terrain_score.warning_zone_grid(
        current_warning_geometry,
        display_shape,
        display_transform,
    )
    validation_features = features.copy()
    validation_features["Warning-Zone Exposure"] = terrain_score.warning_zone_grid(
        validation_warning_geometry,
        display_shape,
        display_transform,
    )

    curvature_scale = np.nanpercentile(np.abs(features["Terrain Curvature"]), 99.5)
    if not np.isfinite(curvature_scale) or curvature_scale <= 0:
        raise RuntimeError("Terrain curvature could not be scaled.")
    features["Terrain Curvature"] = np.clip(
        features["Terrain Curvature"],
        -curvature_scale,
        curvature_scale,
    )
    validation_features["Terrain Curvature"] = features["Terrain Curvature"]
    valid = admin_mask.copy()
    for feature in terrain_score.FEATURE_NAMES:
        valid &= np.isfinite(features[feature])

    landslides = pd.read_parquet(LANDSLIDE_PATH, columns=["Geometry"])
    landslide_geometry = decode_geometry(landslides["Geometry"])
    landslide_geometry = landslide_geometry[shapely.intersects(landslide_geometry, admin_union)]
    model, _, _, _, model_mode = terrain_score.fit_presence_background_model(
        validation_features,
        valid,
        landslide_geometry,
        extent,
    )
    valid_row, valid_column = np.nonzero(valid)
    matrix = np.column_stack(
        [features[name][valid_row, valid_column] for name in terrain_score.FEATURE_NAMES]
    )
    terrain_logit = np.full(display_shape, np.nan, dtype="float32")
    terrain_logit[valid] = model.decision_function(matrix).astype("float32")

    scenario_values = pd.read_parquet(SCENARIO_PATH)
    scenario_loads = terrain_score.event_scenario_loads(
        scenario_values,
        extent,
        display_shape,
    )
    threshold = pd.read_parquet(THRESHOLD_PATH)
    factors, mixed = terrain_score.threshold_categories(admin, threshold)
    factors[mixed] = float(yatsushiro_factor)
    factor_grid = rasterize(
        ((geometry, float(factor)) for geometry, factor in zip(admin_geometry, factors)),
        out_shape=display_shape,
        transform=display_transform,
        fill=1.0,
        all_touched=True,
        dtype="float32",
    )
    factor_grid[~admin_mask] = np.nan

    scores: dict[str, np.ndarray] = {}
    for scenario in ("Moderate", "Heavy", "Extreme"):
        rainfall_loading = scenario_loads[scenario] / factor_grid
        score = expit(
            terrain_logit
            + terrain_score.RAINFALL_LOADING_GAMMA
            * np.log(np.clip(rainfall_loading, 1e-6, None))
        ).astype("float32")
        score[~valid] = np.nan
        scores[scenario] = score
    return scores, scenario_loads, model_mode, features["Elevation"]


def load_or_build_landslide_scores(
    admin: pd.DataFrame,
    admin_geometry: np.ndarray,
    admin_union: object,
    extent: tuple[float, float, float, float],
    display_shape: tuple[int, int],
    display_transform: Affine,
    yatsushiro_factor: float = 0.75,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], str, np.ndarray]:
    """Reuse the accepted event-IDW terrain grids to limit peak memory."""
    factor_tag = f"{int(round(yatsushiro_factor * 100)):03d}"
    terrain_cache = INTERMEDIATE / f"landslide_score_grids_event_idw_v4_y{factor_tag}.npz"
    signature = content_signature(
        "landslide-score-grids-event-idw-v4",
        files=(
            terrain_score.DEM_PATH,
            ADMIN_PATH,
            WARNING_PATH,
            LANDSLIDE_PATH,
            SCENARIO_PATH,
            THRESHOLD_PATH,
            Path(terrain_score.__file__),
            Path(__file__),
        ),
        parameters={
            "extent": tuple(float(value) for value in extent),
            "shape": tuple(int(value) for value in display_shape),
            "aggregation_factor": terrain_score.AGGREGATION_FACTOR,
            "windows": terrain_score.WINDOWS,
            "scenario_quantiles": terrain_score.SCENARIO_QUANTILES,
            "central_support": terrain_score.CENTRAL_SUPPORT,
            "distance_stabilizer_degrees": terrain_score.DISTANCE_STABILIZER_DEGREES,
            "rainfall_loading_gamma": terrain_score.RAINFALL_LOADING_GAMMA,
            "fallback_weights": terrain_score.FALLBACK_WEIGHTS,
            "yatsushiro_factor": float(yatsushiro_factor),
        },
    )
    if terrain_cache.exists():
        cached = np.load(terrain_cache, allow_pickle=False)
        if cache_matches(cached, signature):
            scores = {
                scenario: cached[f"score_{scenario}"].astype("float32")
                for scenario in ("Moderate", "Heavy", "Extreme")
            }
            loads = {
                scenario: cached[f"load_{scenario}"].astype("float32")
                for scenario in ("Moderate", "Heavy", "Extreme")
            }
            return scores, loads, str(cached["model_mode"]), cached["elevation"].astype("float32")

    scores, loads, model_mode, elevation = build_landslide_scores(
        admin,
        admin_geometry,
        admin_union,
        extent,
        display_shape,
        display_transform,
        yatsushiro_factor,
    )
    terrain_cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        terrain_cache,
        signature=np.asarray(signature),
        extent=np.asarray(extent, dtype=float),
        shape=np.asarray(display_shape, dtype=int),
        model_mode=np.asarray(model_mode),
        elevation=elevation,
        **{f"score_{scenario}": value for scenario, value in scores.items()},
        **{f"load_{scenario}": value for scenario, value in loads.items()},
    )
    return scores, loads, model_mode, elevation


def sample_grid(
    grid: np.ndarray,
    coordinates: np.ndarray,
    extent: tuple[float, float, float, float],
) -> np.ndarray:
    """Sample a north-up WGS84 grid at point coordinates."""
    west, east, south, north = extent
    rows, columns = grid.shape
    column = np.floor((coordinates[:, 0] - west) / (east - west) * columns).astype(int)
    row = np.floor((north - coordinates[:, 1]) / (north - south) * rows).astype(int)
    inside = (row >= 0) & (row < rows) & (column >= 0) & (column < columns)
    values = np.zeros(len(coordinates), dtype="float32")
    values[inside] = grid[row[inside], column[inside]]
    values[~np.isfinite(values)] = 0.0
    return values


def road_scores(
    geometry: np.ndarray,
    terrain_scores: dict[str, np.ndarray],
    extent: tuple[float, float, float, float],
    elevation_grid: np.ndarray,
) -> dict[str, np.ndarray]:
    """Translate directionally plausible upslope terrain scores to road sections.

    Candidate source cells must be above the sampled road point and have a local
    downhill gradient directed toward it. Distance decay and directional alignment
    form q_ie; scenario scores are normalized directional weighted means.
    """
    parts, parent_index = shapely.get_parts(geometry, return_index=True)
    print(f"Road-score parts prepared: {len(parts):,}.", flush=True)
    sampled_points = [
        shapely.line_interpolate_point(parts, fraction, normalized=True)
        for fraction in SAMPLE_FRACTIONS
    ]
    rows, columns = elevation_grid.shape
    west, east, south, north = extent
    filled_elevation = np.where(
        np.isfinite(elevation_grid),
        elevation_grid,
        float(np.nanmedian(elevation_grid)),
    )
    gradient_y, gradient_x = np.gradient(filled_elevation.astype("float64"))
    part_weighted_score = {
        scenario: np.zeros(len(parts), dtype="float64") for scenario in terrain_scores
    }
    part_weight = np.zeros(len(parts), dtype="float64")
    offsets = [
        (dy, dx)
        for dy in range(-UPSLOPE_RADIUS_CELLS, UPSLOPE_RADIUS_CELLS + 1)
        for dx in range(-UPSLOPE_RADIUS_CELLS, UPSLOPE_RADIUS_CELLS + 1)
        if dx or dy
    ]
    for sample_index, points in enumerate(sampled_points, start=1):
        coordinates = shapely.get_coordinates(points)[:, :2]
        column = np.floor((coordinates[:, 0] - west) / (east - west) * columns).astype(int)
        row = np.floor((north - coordinates[:, 1]) / (north - south) * rows).astype(int)
        point_inside = (row >= 0) & (row < rows) & (column >= 0) & (column < columns)
        road_elevation = np.full(len(parts), np.nan, dtype="float64")
        road_elevation[point_inside] = elevation_grid[row[point_inside], column[point_inside]]
        for dy, dx in offsets:
            neighbour_row = row + dy
            neighbour_column = column + dx
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
            rr = neighbour_row[positions]
            cc = neighbour_column[positions]
            neighbour_elevation = elevation_grid[rr, cc]
            relief = neighbour_elevation - road_elevation[positions]
            gx = gradient_x[rr, cc]
            gy = gradient_y[rr, cc]
            distance = float(np.hypot(dx, dy))
            alignment = (gx * dx + gy * dy) / np.maximum(
                np.hypot(gx, gy) * distance,
                1e-6,
            )
            plausible = (
                np.isfinite(neighbour_elevation)
                & np.isfinite(relief)
                & (relief >= MIN_UPSLOPE_RELIEF_M)
                & (alignment >= MIN_DOWNSLOPE_ALIGNMENT)
            )
            if not plausible.any():
                continue
            selected = positions[plausible]
            rr = rr[plausible]
            cc = cc[plausible]
            q_ie = (
                np.exp(-distance / 2.5)
                * np.clip(alignment[plausible], 0.0, 1.0)
                * np.clip(relief[plausible] / 100.0, 0.20, 1.0)
            )
            np.add.at(part_weight, selected, q_ie)
            for scenario, score_grid in terrain_scores.items():
                contribution = np.nan_to_num(score_grid[rr, cc], nan=0.0) * q_ie
                np.add.at(
                    part_weighted_score[scenario],
                    selected,
                    contribution,
                )
        print(f"Completed road sample fraction {sample_index}/{len(sampled_points)}.", flush=True)

    road_results: dict[str, np.ndarray] = {}
    road_weight = np.zeros(len(geometry), dtype="float64")
    np.add.at(road_weight, parent_index, part_weight)
    for scenario, part_numerator in part_weighted_score.items():
        road_numerator = np.zeros(len(geometry), dtype="float64")
        np.add.at(road_numerator, parent_index, part_numerator)
        result = np.zeros(len(geometry), dtype="float32")
        supported = road_weight > 0
        result[supported] = (road_numerator[supported] / road_weight[supported]).astype("float32")
        road_results[scenario] = result
    return road_results


def load_or_build_road_scores(
    geometry: np.ndarray,
    terrain_scores: dict[str, np.ndarray],
    extent: tuple[float, float, float, float],
    elevation_grid: np.ndarray,
    yatsushiro_factor: float = 0.75,
) -> dict[str, np.ndarray]:
    """Reuse normalized road scores across downstream consequence analyses."""
    factor_tag = f"{int(round(yatsushiro_factor * 100)):03d}"
    road_score_cache = INTERMEDIATE / f"road_disruption_scores_normalized_v4_y{factor_tag}.npz"
    signature = content_signature(
        "road-disruption-scores-normalized-v4",
        files=(ROAD_PATH, Path(__file__)),
        arrays={
            "elevation_grid": elevation_grid,
            **{
                f"terrain_score_{scenario}": terrain_scores[scenario]
                for scenario in ("Moderate", "Heavy", "Extreme")
            },
        },
        parameters={
            "road_count": len(geometry),
            "extent": tuple(float(value) for value in extent),
            "sample_fractions": SAMPLE_FRACTIONS,
            "upslope_radius_cells": UPSLOPE_RADIUS_CELLS,
            "minimum_upslope_relief_m": MIN_UPSLOPE_RELIEF_M,
            "minimum_downslope_alignment": MIN_DOWNSLOPE_ALIGNMENT,
            "yatsushiro_factor": float(yatsushiro_factor),
        },
    )
    if road_score_cache.exists():
        cached = np.load(road_score_cache, allow_pickle=False)
        if cache_matches(cached, signature):
            return {
                scenario: cached[f"score_{scenario}"].astype("float32")
                for scenario in ("Moderate", "Heavy", "Extreme")
            }
    scores = road_scores(geometry, terrain_scores, extent, elevation_grid)
    road_score_cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        road_score_cache,
        signature=np.asarray(signature),
        road_count=np.asarray(len(geometry), dtype=int),
        **{f"score_{scenario}": value for scenario, value in scores.items()},
    )
    return scores


def rasterize_road_scores(
    geometry: np.ndarray,
    scores: np.ndarray,
    display_shape: tuple[int, int],
    display_transform: Affine,
) -> np.ndarray:
    """Rasterize roads in ascending order so locally higher scores remain visible."""
    order = np.argsort(scores)
    return rasterize(
        ((geometry[index], float(scores[index])) for index in order),
        out_shape=display_shape,
        transform=display_transform,
        fill=np.nan,
        all_touched=True,
        dtype="float32",
    )


def matched_road_concordance(
    roads: pd.DataFrame,
    road_geometry: np.ndarray,
    heavy_score: np.ndarray,
    event_section_pairs: pd.DataFrame,
    admin_geometry: np.ndarray,
    display_shape: tuple[int, int],
    display_transform: Affine,
    extent: tuple[float, float, float, float],
) -> dict[str, object]:
    """Compare restriction episodes with matched pseudo-background roads."""
    design = build_matched_design(
        roads,
        road_geometry,
        event_section_pairs,
        admin_geometry,
        display_shape,
        display_transform,
        extent,
        sample_grid,
    )
    return event_weighted_concordance(
        np.asarray(heavy_score, dtype=float),
        design,
        event_section_pairs,
    )


def style_map_axis(ax: plt.Axes, extent: tuple[float, float, float, float]) -> None:
    """Apply the accepted longitude-latitude grid, ticks, and full frame."""
    west, east, south, north = extent
    ax.set_xlim(west, east)
    ax.set_ylim(south, north)
    ax.set_aspect(1 / np.cos(np.deg2rad((south + north) / 2)))
    ax.set_xticks(np.arange(np.ceil(west * 5) / 5, east + 0.001, 0.2))
    ax.set_yticks(np.arange(np.ceil(south * 5) / 5, north + 0.001, 0.2))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.1f}°E"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.1f}°N"))
    ax.tick_params(axis="both", labelsize=7.2, colors="#475467", length=3, width=0.7)
    ax.set_xlabel("Longitude", fontsize=8.2, color="#344054", labelpad=4)
    ax.set_ylabel("Latitude", fontsize=8.2, color="#344054", labelpad=4)
    ax.grid(True, color="#98A2B3", linewidth=0.45, linestyle=(0, (3, 3)), alpha=0.55)
    ax.set_axisbelow(False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.85)
        spine.set_color("#344054")


def add_panel_label(ax: plt.Axes, label: str) -> None:
    """Add the required lowercase panel label."""
    ax.text(
        -0.035,
        1.015,
        label,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        color="#172033",
        ha="left",
        va="bottom",
    )


def main() -> None:
    sns.set_theme(style="white", context="paper")

    admin = pd.read_parquet(ADMIN_PATH, columns=["Municipality Name", "Geometry"])
    admin_geometry = decode_geometry(admin.pop("Geometry"))
    admin_union = shapely.union_all(admin_geometry)
    min_x, min_y, max_x, max_y = shapely.bounds(admin_union)
    pad_x = (max_x - min_x) * 0.025
    pad_y = (max_y - min_y) * 0.025
    extent = (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)
    west, east, south, north = extent
    display_height = max(650, round(DISPLAY_WIDTH * (north - south) / (east - west)))
    display_shape = (display_height, DISPLAY_WIDTH)
    display_transform = from_bounds(west, south, east, north, DISPLAY_WIDTH, display_height)

    landslide_scores, scenario_loads, model_mode, elevation_grid = load_or_build_landslide_scores(
        admin,
        admin_geometry,
        admin_union,
        extent,
        display_shape,
        display_transform,
    )
    print("Completed terrain and rainfall score grids.", flush=True)

    roads = pd.read_parquet(
        ROAD_PATH,
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
    road_geometry = decode_geometry(roads.pop("Geometry"))
    scores = load_or_build_road_scores(
        road_geometry,
        landslide_scores,
        extent,
        elevation_grid,
    )
    print("Completed normalized directional road scores.", flush=True)
    score_rasters = {
        scenario: rasterize_road_scores(
            road_geometry,
            values,
            display_shape,
            display_transform,
        )
        for scenario, values in scores.items()
    }

    restriction_evidence = load_restriction_evidence(
        RESTRICTION_PATH,
        MATCH_PATH,
        EDGE_PATH,
        roads["Road Section ID"],
    )
    edges = pd.read_parquet(
        EDGE_PATH,
        columns=["Road Edge ID", "Road Section ID", "Geometry"],
    )
    evidence_edges = restriction_evidence.episode_matches.drop(
        columns=["Geometry"],
        errors="ignore",
    ).merge(
        edges[["Road Edge ID", "Geometry"]],
        on="Road Edge ID",
        how="inner",
        validate="many_to_one",
    ).drop_duplicates(["Episode ID", "Road Edge ID"])
    evidence_geometry = decode_geometry(evidence_edges["Geometry"])
    episode_geometry = np.asarray(
        [
            shapely.from_geojson(value)
            for value in restriction_evidence.retained_episodes["Geometry JSON"]
        ],
        dtype=object,
    )
    episode_points = shapely.centroid(episode_geometry)
    episode_coordinates = shapely.get_coordinates(episode_points)[:, :2]
    trigger_decision = json.loads(TRIGGER_DECISION_PATH.read_text(encoding="utf-8"))
    if trigger_decision["retained_physical_episodes"] != len(episode_points):
        raise RuntimeError("Trigger-audit episode count does not match the figure evidence.")
    print("Completed restriction linkage funnel.", flush=True)

    heavy_lookup = pd.Series(scores["Heavy"], index=roads["Road Section ID"])
    evidence_scores = (
        restriction_evidence.event_section_pairs["Road Section ID"]
        .map(heavy_lookup)
        .dropna()
        .to_numpy()
    )
    valid_heavy = scores["Heavy"][np.isfinite(scores["Heavy"])]
    median_percentile = float(
        np.median(np.searchsorted(np.sort(valid_heavy), evidence_scores, side="right") / len(valid_heavy))
    )
    top_quartile_share = float(
        np.mean(evidence_scores >= np.quantile(valid_heavy, 0.75))
    )
    matched_metrics = matched_road_concordance(
        roads,
        road_geometry,
        scores["Heavy"],
        restriction_evidence.event_section_pairs,
        admin_geometry,
        display_shape,
        display_transform,
        extent,
    )
    yatsushiro_bound_metrics: dict[str, dict[str, float]] = {}
    yatsushiro_bound_scores: dict[str, np.ndarray] = {}
    for bound_factor in (0.70, 0.80):
        bound_landslide_scores, _, _, _ = load_or_build_landslide_scores(
            admin,
            admin_geometry,
            admin_union,
            extent,
            display_shape,
            display_transform,
            yatsushiro_factor=bound_factor,
        )
        bound_score = load_or_build_road_scores(
            road_geometry,
            bound_landslide_scores,
            extent,
            elevation_grid,
            yatsushiro_factor=bound_factor,
        )["Heavy"]
        label = f"{bound_factor:.2f}"
        yatsushiro_bound_scores[label] = bound_score
        yatsushiro_bound_metrics[label] = matched_road_concordance(
            roads,
            road_geometry,
            bound_score,
            restriction_evidence.event_section_pairs,
            admin_geometry,
            display_shape,
            display_transform,
            extent,
        )
    bound_concordance = [
        values["Road Score Concordance"]
        for values in yatsushiro_bound_metrics.values()
    ]
    bound_max_change = max(
        float(np.nanmax(np.abs(bound_score - scores["Heavy"])))
        for bound_score in yatsushiro_bound_scores.values()
    )
    print("Completed matched road validation.", flush=True)

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
    image_extent = (west, east, south, north)
    boundary_segments = line_segments(shapely.boundary(admin_geometry))
    panel_specs = [
        ("Moderate rainfall", score_rasters["Moderate"]),
        ("Heavy rainfall", score_rasters["Heavy"]),
        ("Extreme rainfall", score_rasters["Extreme"]),
        ("Earthquake-proximate restriction correspondence\nHeavy score background", score_rasters["Heavy"]),
    ]

    image = None
    for index, (axis, (annotation, raster)) in enumerate(zip(axes, panel_specs)):
        axis.set_facecolor("#F8FAFC")
        image = axis.imshow(
            raster,
            extent=image_extent,
            origin="upper",
            cmap="magma",
            vmin=0,
            vmax=1,
            interpolation="nearest",
            zorder=2,
        )
        axis.add_collection(
            LineCollection(
                boundary_segments,
                colors="#667085",
                linewidths=0.46,
                alpha=0.85,
                zorder=8,
            )
        )
        axis.text(
            0.018,
            0.982,
            annotation,
            transform=axis.transAxes,
            ha="left",
            va="top",
            fontsize=8.5,
            fontweight="bold",
            color="#172033",
            bbox={
                "boxstyle": "round,pad=0.28",
                "facecolor": "white",
                "edgecolor": "#D0D5DD",
                "alpha": 0.92,
            },
            zorder=20,
        )
        style_map_axis(axis, extent)
        add_panel_label(axis, "abcd"[index])

    emergency = roads["Emergency Route Membership"].astype("string").ne("None").to_numpy()
    emergency_segments = line_segments(road_geometry[emergency])
    axes[2].add_collection(
        LineCollection(
            emergency_segments,
            colors="#00B7D6",
            linewidths=0.55,
            alpha=0.85,
            zorder=12,
        )
    )
    axes[2].legend(
        handles=[
            Line2D([0], [0], color="#00B7D6", linewidth=1.6, label="Emergency transport road")
        ],
        loc="lower left",
        fontsize=7.4,
        frameon=True,
        framealpha=0.94,
    )

    evidence_handles: list[Line2D] = []
    reason_markers = {"落石": "o", "法面崩落": "s", "土砂流入": "^"}
    episode_reasons = restriction_evidence.retained_episodes[
        "Restriction Reason"
    ].astype("string")
    for reason in ("落石", "法面崩落", "土砂流入"):
        selected_edges = evidence_edges["Restriction Reason"].astype("string").eq(reason).to_numpy()
        selected_episodes = episode_reasons.eq(reason).to_numpy()
        if not np.any(selected_episodes):
            continue
        segments = line_segments(evidence_geometry[selected_edges])
        axes[3].add_collection(
            LineCollection(
                segments,
                colors="white",
                linewidths=2.5,
                alpha=0.90,
                zorder=13,
            )
        )
        axes[3].add_collection(
            LineCollection(
                segments,
                colors=REASON_COLORS[reason],
                linewidths=1.2,
                alpha=0.72,
                zorder=14,
            )
        )
        axes[3].scatter(
            episode_coordinates[selected_episodes, 0],
            episode_coordinates[selected_episodes, 1],
            s=34,
            marker=reason_markers[reason],
            facecolor=REASON_COLORS[reason],
            edgecolor="white",
            linewidth=0.9,
            zorder=16,
        )
        evidence_handles.append(
            Line2D(
                [0],
                [0],
                marker=reason_markers[reason],
                linestyle="none",
                markerfacecolor=REASON_COLORS[reason],
                markeredgecolor="white",
                markersize=6,
                label=REASON_LABELS[reason],
            )
        )
    axes[3].legend(
        handles=evidence_handles,
        loc="lower left",
        fontsize=7.2,
        frameon=True,
        framealpha=0.94,
    )
    axes[3].text(
        0.982,
        0.018,
        (
            f"{int(matched_metrics['Physical Episodes']):,} physical episodes\n"
            "0 confirmed rainfall-triggered\n"
            "Preceding 72-h rainfall: 0 mm\n"
            f"Heavy episode concordance: {matched_metrics['Road Score Concordance']:.2f} "
            f"({matched_metrics['Road Score CI Low']:.2f}–"
            f"{matched_metrics['Road Score CI High']:.2f})\n"
            "Supplementary correspondence only"
        ),
        transform=axes[3].transAxes,
        ha="right",
        va="bottom",
        fontsize=7.3,
        color="#172033",
        bbox={
            "boxstyle": "round,pad=0.32",
            "facecolor": "white",
            "edgecolor": "#D0D5DD",
            "alpha": 0.94,
        },
        zorder=20,
    )

    if image is None:
        raise RuntimeError("No road-score image was generated.")
    colorbar = fig.colorbar(image, cax=colorbar_axis)
    colorbar.set_label("Relative road disruption score", fontsize=9)
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
    print(f"Road sections scored: {len(roads):,}")
    print(f"Terrain-score construction: {model_mode}")
    print("Road pooling: normalized directional weighted mean")
    print(
        "Physical restriction episodes: "
        f"{len(restriction_evidence.retained_episodes):,}"
    )
    print(f"Matched restriction edges: {evidence_edges['Road Edge ID'].nunique():,}")
    print(f"Median matched-edge Heavy score percentile: {median_percentile:.3f}")
    print(f"Matched-edge share in Heavy top quartile: {top_quartile_share:.3f}")
    print("Matched pseudo-background validation:")
    for key, value in matched_metrics.items():
        if isinstance(value, (int, float, np.integer, np.floating)):
            print(f"  {key}: {float(value):.4f}")
    print(
        "Yatsushiro 0.70-0.80 Heavy sensitivity: "
        f"matched concordance={min(bound_concordance):.4f}-"
        f"{max(bound_concordance):.4f}; maximum road-score change={bound_max_change:.6f}"
    )
    print("Scenario loading medians:")
    for scenario, value in scenario_loads.items():
        print(f"  {scenario}: {np.nanmedian(value):.4f}")
    print("Road-score zero shares and rank correlations:")
    for scenario, value in scores.items():
        print(f"  {scenario} zero share: {np.mean(value == 0):.4%}")
    for left, right in (("Moderate", "Heavy"), ("Heavy", "Extreme")):
        correlation = pd.Series(scores[left]).corr(pd.Series(scores[right]), method="spearman")
        print(f"  {left} vs {right}: {correlation:.6f}")
    print("Interpretation: relative road-disruption ranking; not a closure probability")


if __name__ == "__main__":
    main()
