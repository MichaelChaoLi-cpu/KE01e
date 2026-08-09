#!/usr/bin/env python3
"""Road Disruption Exposure and Observed Restriction Evidence.

Plan: Map scenario road-disruption exposure and compare the Heavy scenario
ranking with reliably matched rockfall and slope-collapse restriction evidence.
Framework: Section 5 road-ranking validation; Section 6 slope-to-road transfer
score D_e = 1 - product(1 - H_i q_ie); Section 7 validation of slope-to-road
translation. Scores are screening indices, not road-closure probabilities.
"""
from __future__ import annotations

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
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from scipy.ndimage import maximum_filter
from scipy.special import expit
import seaborn as sns
import shapely

import figure_official_threshold_adjusted_landslide_disruption_score as terrain_score


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
WARNING_PATH = PROCESSED / "landslide_warning_zones_preprocessed.parquet"
LANDSLIDE_PATH = PROCESSED / "gsi_2016_landslide_inventory_preprocessed.parquet"
RAIN_PATH = PROCESSED / "jma_hourly_rainfall_preprocessed.parquet"
THRESHOLD_PATH = PROCESSED / "official_threshold_factors_preprocessed.parquet"
ROAD_PATH = PROCESSED / "road_sections_preprocessed.parquet"
EDGE_PATH = PROCESSED / "road_edges_preprocessed.parquet"
MATCH_PATH = PROCESSED / "road_restriction_edge_matches_preprocessed.parquet"
OUT = ROOT / "data/results/figures/Figure_road_disruption_exposure_and_observed_restriction_evidence.png"

DISPLAY_WIDTH = 950
TRANSFER_WEIGHT = 0.10
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
) -> tuple[dict[str, np.ndarray], dict[str, float], str, np.ndarray]:
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

    warning = pd.read_parquet(WARNING_PATH, columns=["Geometry"])
    warning_geometry = decode_geometry(warning["Geometry"])
    features["Warning-Zone Exposure"] = rasterize(
        ((geometry, 1) for geometry in warning_geometry),
        out_shape=display_shape,
        transform=display_transform,
        fill=0,
        all_touched=True,
        dtype="uint8",
    ).astype("float32")

    curvature_scale = np.nanpercentile(np.abs(features["Terrain Curvature"]), 99.5)
    if not np.isfinite(curvature_scale) or curvature_scale <= 0:
        raise RuntimeError("Terrain curvature could not be scaled.")
    features["Terrain Curvature"] = np.clip(
        features["Terrain Curvature"],
        -curvature_scale,
        curvature_scale,
    )
    valid = admin_mask.copy()
    for feature in terrain_score.FEATURE_NAMES:
        valid &= np.isfinite(features[feature])

    landslides = pd.read_parquet(LANDSLIDE_PATH, columns=["Geometry"])
    landslide_geometry = decode_geometry(landslides["Geometry"])
    landslide_geometry = landslide_geometry[shapely.intersects(landslide_geometry, admin_union)]
    model, _, _, _, model_mode = terrain_score.fit_presence_background_model(
        features,
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

    rain = pd.read_parquet(
        RAIN_PATH,
        columns=["Station ID", "Observation Time", "Hourly Rainfall"],
    )
    rain = rain.loc[rain["Hourly Rainfall"].notna()].copy()
    scenario_loads = terrain_score.wet_window_scenario_loads(rain)
    threshold = pd.read_parquet(THRESHOLD_PATH)
    factors, _ = terrain_score.threshold_categories(admin, threshold)
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
        score = expit(terrain_logit + rainfall_loading - 1.0).astype("float32")
        score[~valid] = np.nan
        scores[scenario] = score
    return scores, scenario_loads, model_mode, features["Elevation"]


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
    form q_ie; scenario scores are then combined as one-minus-product survival.
    """
    parts, parent_index = shapely.get_parts(geometry, return_index=True)
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
    part_log_survival = {
        scenario: np.zeros(len(parts), dtype="float64") for scenario in terrain_scores
    }
    offsets = [
        (dy, dx)
        for dy in range(-UPSLOPE_RADIUS_CELLS, UPSLOPE_RADIUS_CELLS + 1)
        for dx in range(-UPSLOPE_RADIUS_CELLS, UPSLOPE_RADIUS_CELLS + 1)
        if dx or dy
    ]
    for points in sampled_points:
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
                TRANSFER_WEIGHT
                * np.exp(-distance / 2.5)
                * np.clip(alignment[plausible], 0.0, 1.0)
                * np.clip(relief[plausible] / 100.0, 0.20, 1.0)
            )
            for scenario, score_grid in terrain_scores.items():
                contribution = np.clip(
                    np.nan_to_num(score_grid[rr, cc], nan=0.0) * q_ie,
                    0.0,
                    0.95,
                )
                np.add.at(
                    part_log_survival[scenario],
                    selected,
                    np.log1p(-contribution),
                )

    road_results: dict[str, np.ndarray] = {}
    for scenario, part_log in part_log_survival.items():
        road_log_survival = np.zeros(len(geometry), dtype="float64")
        np.add.at(road_log_survival, parent_index, part_log)
        road_results[scenario] = (1.0 - np.exp(road_log_survival)).astype("float32")
    return road_results


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

    landslide_scores, scenario_loads, model_mode, elevation_grid = build_landslide_scores(
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
            "Road Category",
            "Road Section Length (m)",
            "Emergency Route Membership",
            "Network Analysis Eligible",
            "Geometry",
        ],
    )
    roads = roads.loc[roads["Network Analysis Eligible"]].reset_index(drop=True)
    road_geometry = decode_geometry(roads.pop("Geometry"))
    scores = road_scores(road_geometry, landslide_scores, extent, elevation_grid)
    score_rasters = {
        scenario: rasterize_road_scores(
            road_geometry,
            values,
            display_shape,
            display_transform,
        )
        for scenario, values in scores.items()
    }

    matches = pd.read_parquet(
        MATCH_PATH,
        columns=[
            "Restriction Observation ID",
            "Snapshot Time",
            "Restriction Reason",
            "Restriction Status",
            "Matched Road Edge ID",
            "Road Edge Match Distance (m)",
            "Road Edge Match Status",
        ],
    )
    reliable = (
        matches["Restriction Reason"].astype("string").str.contains(LANDSLIDE_REASON_PATTERN, na=False)
        & matches["Road Edge Match Status"].eq("matched_primary")
        & matches["Road Edge Match Distance (m)"].le(50)
    )
    evidence = matches.loc[reliable].drop_duplicates(
        ["Restriction Observation ID", "Snapshot Time", "Matched Road Edge ID"]
    )
    evidence_observations = evidence.drop_duplicates(
        ["Restriction Observation ID", "Snapshot Time"]
    )
    edges = pd.read_parquet(
        EDGE_PATH,
        columns=["Road Edge ID", "Road Section ID", "Geometry"],
    )
    evidence_edges = evidence.merge(
        edges,
        left_on="Matched Road Edge ID",
        right_on="Road Edge ID",
        how="inner",
        validate="many_to_one",
    ).drop_duplicates(["Road Edge ID", "Restriction Reason"])
    evidence_geometry = decode_geometry(evidence_edges["Geometry"])

    heavy_lookup = pd.Series(scores["Heavy"], index=roads["Road Section ID"])
    evidence_scores = evidence_edges["Road Section ID"].map(heavy_lookup).dropna().to_numpy()
    valid_heavy = scores["Heavy"][np.isfinite(scores["Heavy"])]
    median_percentile = float(
        np.median(np.searchsorted(np.sort(valid_heavy), evidence_scores, side="right") / len(valid_heavy))
    )
    top_quartile_share = float(
        np.mean(evidence_scores >= np.quantile(valid_heavy, 0.75))
    )

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
        ("Observed restriction evidence\nHeavy rainfall score background", score_rasters["Heavy"]),
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
    for reason in ("落石", "法面崩落", "土砂流入"):
        selected = evidence_edges["Restriction Reason"].astype("string").eq(reason).to_numpy()
        if not np.any(selected):
            continue
        segments = line_segments(evidence_geometry[selected])
        axes[3].add_collection(
            LineCollection(
                segments,
                colors=REASON_COLORS[reason],
                linewidths=1.35,
                alpha=0.95,
                zorder=14,
            )
        )
        evidence_handles.append(
            Line2D(
                [0],
                [0],
                color=REASON_COLORS[reason],
                linewidth=2.0,
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
            f"{len(evidence_observations):,} deduplicated observations\n"
            f"{evidence_edges['Road Edge ID'].nunique():,} reliably matched edges\n"
            f"Median score percentile: {median_percentile:.0%}\n"
            f"Share in top quartile: {top_quartile_share:.0%}"
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
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Saved: {OUT.relative_to(ROOT)}")
    print(f"Road sections scored: {len(roads):,}")
    print(f"Terrain-score construction: {model_mode}")
    print(f"Transfer weight per sampled influence point: {TRANSFER_WEIGHT:.2f}")
    print(f"Reliable deduplicated restriction observations: {len(evidence_observations):,}")
    print(f"Reliable matched restriction edges: {evidence_edges['Road Edge ID'].nunique():,}")
    print(f"Median matched-edge Heavy score percentile: {median_percentile:.3f}")
    print(f"Matched-edge share in Heavy top quartile: {top_quartile_share:.3f}")
    print("Scenario loads relative to Heavy:")
    for scenario, value in scenario_loads.items():
        print(f"  {scenario}: {value:.4f}")
    print("Interpretation: relative road-disruption ranking; not a closure probability")


if __name__ == "__main__":
    main()
