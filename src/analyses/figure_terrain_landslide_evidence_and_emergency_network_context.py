#!/usr/bin/env python3
"""Terrain, Landslide Evidence, and Emergency Network Context.

Plan: Establish the spatial evidence base for terrain, interpreted landslides,
warning zones, roads, emergency routes, shelters, and water points.
Framework: Section 5 spatial evidence units; Section 6 terrain and landslide-score
inputs; Section 7 terrain-context construction and baseline network evidence.
This figure is descriptive and does not display an estimated disruption score.
"""
from __future__ import annotations

import os
from pathlib import Path

# Prevent an external Anaconda PROJ database from overriding Rasterio's bundled data.
os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.collections import LineCollection
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from rasterio.warp import Resampling, reproject
import seaborn as sns
import shapely


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
OUT = ROOT / "data/results/figures/Figure_terrain_landslide_evidence_and_emergency_network_context.png"

ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
LANDSLIDE_PATH = PROCESSED / "gsi_2016_landslide_inventory_preprocessed.parquet"
DEM_PATH = PROCESSED / "gsi_dem10b_elevation_preprocessed.tif"
WARNING_PATH = PROCESSED / "landslide_warning_zones_preprocessed.parquet"
ROAD_PATH = PROCESSED / "road_edges_preprocessed.parquet"
SHELTER_PATH = PROCESSED / "designated_shelters_preprocessed.parquet"
WATER_PATH = PROCESSED / "emergency_water_points_preprocessed.parquet"

MAP_WIDTH = 1100


def read_geometry_frame(path: Path, columns: list[str]) -> tuple[pd.DataFrame, np.ndarray]:
    """Read selected columns and decode the project-standard WKB Geometry column."""
    frame = pd.read_parquet(path, columns=[*columns, "Geometry"])
    geometry = shapely.from_wkb(frame.pop("Geometry").to_numpy())
    valid = ~shapely.is_missing(geometry) & ~shapely.is_empty(geometry)
    return frame.loc[valid].reset_index(drop=True), geometry[valid]


def line_segments(geometry: np.ndarray) -> list[np.ndarray]:
    """Convert line or multiline geometry into arrays accepted by LineCollection."""
    parts = shapely.get_parts(geometry)
    return [shapely.get_coordinates(part)[:, :2] for part in parts if len(shapely.get_coordinates(part)) >= 2]


def add_admin_outline(ax: plt.Axes, admin_geometry: np.ndarray) -> None:
    """Add municipality boundaries as a subtle shared reference layer."""
    boundaries = shapely.boundary(admin_geometry)
    collection = LineCollection(
        line_segments(boundaries),
        colors="#475467",
        linewidths=0.38,
        alpha=0.80,
        zorder=8,
    )
    ax.add_collection(collection)


def set_map_frame(ax: plt.Axes, extent: tuple[float, float, float, float]) -> None:
    """Apply bounds, geographic aspect, coordinate grid, ticks, and map frame."""
    west, east, south, north = extent
    ax.set_xlim(west, east)
    ax.set_ylim(south, north)
    midpoint = (south + north) / 2
    ax.set_aspect(1 / np.cos(np.deg2rad(midpoint)))
    longitude_ticks = np.arange(np.ceil(west * 5) / 5, east + 0.001, 0.2)
    latitude_ticks = np.arange(np.ceil(south * 5) / 5, north + 0.001, 0.2)
    ax.set_xticks(longitude_ticks)
    ax.set_yticks(latitude_ticks)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.1f}°E"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.1f}°N"))
    ax.tick_params(axis="both", labelsize=7.2, colors="#475467", length=3, width=0.7)
    ax.set_xlabel("Longitude", fontsize=8.2, color="#344054", labelpad=4)
    ax.set_ylabel("Latitude", fontsize=8.2, color="#344054", labelpad=4)
    ax.grid(
        True,
        color="#98A2B3",
        linewidth=0.45,
        linestyle=(0, (3, 3)),
        alpha=0.58,
        zorder=4,
    )
    ax.set_axisbelow(False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.85)
        spine.set_color("#344054")


def add_panel_label(ax: plt.Axes, label: str) -> None:
    """Add the required lowercase panel label without a panel title."""
    ax.text(
        -0.025,
        1.015,
        label,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        color="#172033",
        ha="left",
        va="bottom",
    )


def add_north_arrow(ax: plt.Axes) -> None:
    """Add a compact north arrow to the first panel."""
    ax.annotate(
        "N",
        xy=(0.94, 0.93),
        xytext=(0.94, 0.82),
        xycoords="axes fraction",
        textcoords="axes fraction",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
        color="#172033",
        arrowprops={"arrowstyle": "-|>", "color": "#172033", "linewidth": 1.2},
        zorder=30,
    )


def prepare_dem(
    extent: tuple[float, float, float, float],
    admin_union: object,
) -> tuple[np.ndarray, object]:
    """Reproject and downsample the DEM to a plotting grid in WGS84."""
    west, east, south, north = extent
    height = max(600, round(MAP_WIDTH * (north - south) / (east - west)))
    destination = np.full((height, MAP_WIDTH), np.nan, dtype="float32")
    destination_transform = from_bounds(west, south, east, north, MAP_WIDTH, height)
    with rasterio.open(DEM_PATH) as source:
        reproject(
            source=rasterio.band(source, 1),
            destination=destination,
            src_transform=source.transform,
            src_crs=source.crs,
            src_nodata=source.nodata,
            dst_transform=destination_transform,
            dst_crs="EPSG:4326",
            dst_nodata=np.nan,
            resampling=Resampling.bilinear,
        )
    admin_mask = rasterize(
        [(admin_union, 1)],
        out_shape=destination.shape,
        transform=destination_transform,
        fill=0,
        all_touched=True,
        dtype="uint8",
    )
    destination[admin_mask == 0] = np.nan
    return destination, destination_transform


def rasterize_categories(
    geometry: np.ndarray,
    values: np.ndarray,
    shape: tuple[int, int],
    transform: object,
) -> np.ndarray:
    """Rasterize categorical geometry on the common plotting grid."""
    return rasterize(
        ((geom, int(value)) for geom, value in zip(geometry, values)),
        out_shape=shape,
        transform=transform,
        fill=0,
        all_touched=True,
        dtype="uint8",
    )


def main() -> None:
    sns.set_theme(style="white", context="paper")

    _, admin_geometry = read_geometry_frame(ADMIN_PATH, [])
    admin_union = shapely.union_all(admin_geometry)
    min_x, min_y, max_x, max_y = shapely.bounds(admin_union)
    pad_x = (max_x - min_x) * 0.025
    pad_y = (max_y - min_y) * 0.025
    extent = (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)

    landslides, landslide_geometry = read_geometry_frame(LANDSLIDE_PATH, ["Landslide Size Class"])
    landslide_inside = shapely.intersects(landslide_geometry, admin_union)
    landslides = landslides.loc[landslide_inside].reset_index(drop=True)
    landslide_geometry = landslide_geometry[landslide_inside]

    warning, warning_geometry = read_geometry_frame(WARNING_PATH, ["Hazard Type"])
    roads, road_geometry = read_geometry_frame(
        ROAD_PATH,
        ["Emergency Route Membership", "Network Analysis Eligible"],
    )
    shelters, shelter_geometry = read_geometry_frame(SHELTER_PATH, ["Shelter ID"])

    water = pd.read_parquet(
        WATER_PATH,
        columns=["Water Point Name", "Longitude", "Latitude", "Location Resolution Status"],
    )
    water_record_count = len(water)
    water = water.dropna(subset=["Longitude", "Latitude"]).copy()
    water["Longitude"] = pd.to_numeric(water["Longitude"], errors="coerce")
    water["Latitude"] = pd.to_numeric(water["Latitude"], errors="coerce")
    water = water.dropna(subset=["Longitude", "Latitude"])
    unmapped_water_count = water_record_count - len(water)

    dem, grid_transform = prepare_dem(extent, admin_union)
    grid_shape = dem.shape
    west, east, south, north = extent

    hazard_codes = {
        "Steep-Slope Collapse": 1,
        "Debris Flow": 2,
        "Landslide": 3,
    }
    hazard_values = warning["Hazard Type"].map(hazard_codes).fillna(0).to_numpy(dtype="uint8")
    hazard_grid = rasterize_categories(warning_geometry, hazard_values, grid_shape, grid_transform)

    road_values = np.ones(len(roads), dtype="uint8")
    road_grid = rasterize_categories(road_geometry, road_values, grid_shape, grid_transform)

    primary_mask = roads["Emergency Route Membership"].eq("Primary Emergency Road").to_numpy()
    secondary_mask = roads["Emergency Route Membership"].eq("Secondary Emergency Road").to_numpy()

    finite_dem = dem[np.isfinite(dem)]
    elevation_min, elevation_max = np.nanpercentile(finite_dem, [1, 99])

    fig = plt.figure(figsize=(14.5, 11), constrained_layout=True)
    grid = fig.add_gridspec(
        2,
        3,
        width_ratios=[1.0, 0.045, 1.0],
        height_ratios=[1.0, 1.0],
        wspace=0.06,
        hspace=0.08,
    )
    axes = np.array(
        [
            fig.add_subplot(grid[0, 0]),
            fig.add_subplot(grid[0, 2]),
            fig.add_subplot(grid[1, 0]),
            fig.add_subplot(grid[1, 2]),
        ]
    )
    colorbar_axis = fig.add_subplot(grid[0, 1])
    image_extent = (west, east, south, north)

    # a: terrain and interpreted landslide evidence.
    elevation_image = axes[0].imshow(
        dem,
        extent=image_extent,
        origin="upper",
        cmap="terrain",
        vmin=elevation_min,
        vmax=elevation_max,
        interpolation="bilinear",
        zorder=1,
    )
    size_class = landslides["Landslide Size Class"].fillna("Unknown")
    large = size_class.astype(str).str.contains("大", regex=False).to_numpy()
    coordinates = shapely.get_coordinates(landslide_geometry)
    axes[0].scatter(
        coordinates[~large, 0],
        coordinates[~large, 1],
        s=8,
        c="#F59E0B",
        edgecolors="white",
        linewidths=0.15,
        alpha=0.80,
        label="Smaller interpreted landslide",
        zorder=15,
    )
    axes[0].scatter(
        coordinates[large, 0],
        coordinates[large, 1],
        s=25,
        c="#B42318",
        edgecolors="white",
        linewidths=0.35,
        alpha=0.92,
        label="Larger interpreted landslide",
        zorder=16,
    )
    colorbar = fig.colorbar(elevation_image, cax=colorbar_axis)
    colorbar.set_label("Elevation (m)", fontsize=9)
    colorbar.ax.tick_params(labelsize=8)
    axes[0].legend(loc="lower left", frameon=True, framealpha=0.92, fontsize=8)
    add_north_arrow(axes[0])

    # b: official warning-zone types, rasterized for legible prefecture-scale coverage.
    hazard_cmap = ListedColormap(["#FFFFFF00", "#E76F51CC", "#E9C46ACC", "#7B2CBFCC"])
    axes[1].imshow(
        hazard_grid,
        extent=image_extent,
        origin="upper",
        cmap=hazard_cmap,
        vmin=0,
        vmax=3,
        interpolation="nearest",
        zorder=2,
    )
    axes[1].legend(
        handles=[
            Patch(facecolor="#E76F51", label="Steep-slope collapse"),
            Patch(facecolor="#E9C46A", label="Debris flow"),
            Patch(facecolor="#7B2CBF", label="Landslide"),
        ],
        loc="lower left",
        frameon=True,
        framealpha=0.92,
        fontsize=8,
    )

    # c: full road context as a raster layer with emergency routes retained as vectors.
    road_cmap = ListedColormap(["#FFFFFF00", "#98A2B366"])
    axes[2].imshow(
        road_grid,
        extent=image_extent,
        origin="upper",
        cmap=road_cmap,
        vmin=0,
        vmax=1,
        interpolation="nearest",
        zorder=2,
    )
    axes[2].add_collection(
        LineCollection(
            line_segments(road_geometry[primary_mask]),
            colors="#1565C0",
            linewidths=0.85,
            alpha=0.92,
            zorder=12,
        )
    )
    axes[2].add_collection(
        LineCollection(
            line_segments(road_geometry[secondary_mask]),
            colors="#F59E0B",
            linewidths=0.75,
            alpha=0.92,
            zorder=13,
        )
    )
    axes[2].legend(
        handles=[
            Line2D([0], [0], color="#98A2B3", linewidth=1.0, label="Analysis-eligible road network"),
            Line2D([0], [0], color="#1565C0", linewidth=2.0, label="Primary emergency road"),
            Line2D([0], [0], color="#F59E0B", linewidth=2.0, label="Secondary emergency road"),
        ],
        loc="lower left",
        frameon=True,
        framealpha=0.92,
        fontsize=8,
    )

    # d: service nodes over the same baseline road context.
    axes[3].imshow(
        road_grid,
        extent=image_extent,
        origin="upper",
        cmap=road_cmap,
        vmin=0,
        vmax=1,
        interpolation="nearest",
        zorder=2,
    )
    shelter_coordinates = shapely.get_coordinates(shelter_geometry)
    axes[3].scatter(
        shelter_coordinates[:, 0],
        shelter_coordinates[:, 1],
        s=8,
        marker="^",
        c="#1565C0",
        edgecolors="white",
        linewidths=0.2,
        alpha=0.80,
        zorder=14,
    )
    exact_water = water["Location Resolution Status"].eq("matched_exact_2012_facility").to_numpy()
    axes[3].scatter(
        water.loc[exact_water, "Longitude"],
        water.loc[exact_water, "Latitude"],
        s=30,
        marker="s",
        c="#00A6A6",
        edgecolors="white",
        linewidths=0.5,
        zorder=16,
    )
    axes[3].legend(
        handles=[
            Line2D([0], [0], marker="^", color="none", markerfacecolor="#1565C0", markeredgecolor="white", markersize=7, label="Designated shelter"),
            Line2D([0], [0], marker="s", color="none", markerfacecolor="#00A6A6", markeredgecolor="white", markersize=7, label="Exact water-point location"),
            Line2D([], [], linestyle="none", color="none", label=f"{unmapped_water_count} water-point records not mapped"),
        ],
        loc="lower left",
        frameon=True,
        framealpha=0.92,
        fontsize=8,
    )

    for label, ax in zip("abcd", axes):
        add_admin_outline(ax, admin_geometry)
        set_map_frame(ax, extent)
        add_panel_label(ax, label)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUT.relative_to(ROOT)}")
    print(f"Interpreted landslides shown: {len(landslides):,}")
    print(f"Warning zones shown: {len(warning):,}")
    print(f"Road edges shown: {len(roads):,}")
    print(f"Designated shelters shown: {len(shelters):,}")
    print(f"Water points shown: {len(water):,}; unresolved records not mapped: {unmapped_water_count:,}")


if __name__ == "__main__":
    main()
