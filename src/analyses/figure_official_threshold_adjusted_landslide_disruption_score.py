#!/usr/bin/env python3
"""Official-Threshold-Adjusted Landslide Disruption Score.

Plan: Compare baseline and rainfall-scenario slope disruption scores while
retaining score-based language unless independent event labels support
probability calibration.
Framework: Section 5 presence-background spatial ranking calibration; Section 6
terrain derivatives, warning-zone exposure, rainfall scenario loading, and the
logistic Landslide Disruption Score; Section 7 terrain-score workflow.

Native DEM derivatives are computed in chunks and aggregated only after slope
and curvature calculation. The displayed values are relative scenario scores,
not calibrated landslide occurrence probabilities.
"""
from __future__ import annotations

import os
from pathlib import Path
import warnings

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

from affine import Affine
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from rasterio.warp import Resampling, reproject
from rasterio.windows import Window
from scipy.special import expit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import shapely


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
DEM_PATH = PROCESSED / "gsi_dem10b_elevation_preprocessed.tif"
ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
LANDSLIDE_PATH = PROCESSED / "gsi_2016_landslide_inventory_preprocessed.parquet"
WARNING_PATH = PROCESSED / "landslide_warning_zones_preprocessed.parquet"
RAIN_PATH = PROCESSED / "jma_hourly_rainfall_preprocessed.parquet"
THRESHOLD_PATH = PROCESSED / "official_threshold_factors_preprocessed.parquet"
OUT = ROOT / "data/results/figures/Figure_official_threshold_adjusted_landslide_disruption_score.png"

AGGREGATION_FACTOR = 16
CHUNK_OUTPUT_ROWS = 32
DISPLAY_WIDTH = 950
WINDOWS = [1, 3, 24, 72]
SCENARIO_QUANTILES = {
    "Moderate": 0.75,
    "Heavy": 0.90,
    "Extreme": 0.99,
}
FEATURE_NAMES = ["Elevation", "Terrain Slope", "Terrain Curvature", "Warning-Zone Exposure"]
FALLBACK_WEIGHTS = {
    "Elevation": 0.15,
    "Terrain Slope": 1.00,
    "Terrain Curvature": 0.35,
    "Warning-Zone Exposure": 0.75,
}


class TransparentStandardizedScore:
    """Fixed, inspectable standardized terrain score used only as a fallback."""

    def __init__(self, weights: dict[str, float]) -> None:
        self.weights = np.asarray([weights[name] for name in FEATURE_NAMES], dtype=float)
        self.scaler = StandardScaler()

    def fit(self, matrix: np.ndarray) -> "TransparentStandardizedScore":
        """Estimate only feature means and scales; keep declared weights fixed."""
        self.scaler.fit(matrix)
        return self

    def decision_function(self, matrix: np.ndarray) -> np.ndarray:
        """Return the weighted standardized index on a stable logit-like scale."""
        standardized = self.scaler.transform(matrix)
        denominator = np.sum(np.abs(self.weights))
        return standardized @ self.weights / denominator


def decode_geometry(series: pd.Series) -> np.ndarray:
    """Decode WKB and retain non-empty geometry."""
    geometry = shapely.from_wkb(series.to_numpy())
    valid = ~shapely.is_missing(geometry) & ~shapely.is_empty(geometry)
    return geometry[valid]


def line_segments(geometry: np.ndarray) -> list[np.ndarray]:
    """Convert line and multiline geometry to Matplotlib segments."""
    segments: list[np.ndarray] = []
    for part in shapely.get_parts(geometry):
        coordinates = shapely.get_coordinates(part)[:, :2]
        if len(coordinates) >= 2:
            segments.append(coordinates)
    return segments


def aggregate_blocks(
    array: np.ndarray,
    factor: int,
    statistic: str = "mean",
) -> np.ndarray:
    """Aggregate native cells using a declared screening-scale statistic."""
    rows = array.shape[0] // factor
    columns = array.shape[1] // factor
    trimmed = array[: rows * factor, : columns * factor]
    reshaped = trimmed.reshape(rows, factor, columns, factor)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        if statistic == "mean":
            result = np.nanmean(reshaped, axis=(1, 3))
        elif statistic == "p90":
            result = np.nanpercentile(reshaped, 90, axis=(1, 3))
        else:
            raise ValueError(f"Unsupported aggregation statistic: {statistic}")
    return result.astype("float32")


def native_terrain_features() -> tuple[dict[str, np.ndarray], Affine, object]:
    """Compute native DEM derivatives in row chunks, then aggregate for screening."""
    with rasterio.open(DEM_PATH) as source:
        if source.width % AGGREGATION_FACTOR or source.height % AGGREGATION_FACTOR:
            raise ValueError("DEM dimensions must be divisible by the aggregation factor.")
        output_rows = source.height // AGGREGATION_FACTOR
        output_columns = source.width // AGGREGATION_FACTOR
        elevation = np.full((output_rows, output_columns), np.nan, dtype="float32")
        slope = np.full_like(elevation, np.nan)
        curvature = np.full_like(elevation, np.nan)
        x_resolution = abs(source.transform.a)
        y_resolution = abs(source.transform.e)
        halo = 2

        for output_start in range(0, output_rows, CHUNK_OUTPUT_ROWS):
            output_stop = min(output_start + CHUNK_OUTPUT_ROWS, output_rows)
            native_start = output_start * AGGREGATION_FACTOR
            native_stop = output_stop * AGGREGATION_FACTOR
            read_start = max(0, native_start - halo)
            read_stop = min(source.height, native_stop + halo)
            data = source.read(
                1,
                window=Window(0, read_start, source.width, read_stop - read_start),
            ).astype("float32")
            data[data == source.nodata] = np.nan

            gradient_y, gradient_x = np.gradient(data, y_resolution, x_resolution)
            native_slope = np.degrees(np.arctan(np.hypot(gradient_x, gradient_y))).astype("float32")
            second_y = np.gradient(gradient_y, y_resolution, axis=0)
            second_x = np.gradient(gradient_x, x_resolution, axis=1)
            native_curvature = (second_x + second_y).astype("float32")

            inner_start = native_start - read_start
            inner_stop = inner_start + (native_stop - native_start)
            elevation[output_start:output_stop] = aggregate_blocks(
                data[inner_start:inner_stop], AGGREGATION_FACTOR
            )
            slope[output_start:output_stop] = aggregate_blocks(
                native_slope[inner_start:inner_stop], AGGREGATION_FACTOR, statistic="p90"
            )
            curvature[output_start:output_stop] = aggregate_blocks(
                np.abs(native_curvature[inner_start:inner_stop]), AGGREGATION_FACTOR
            )

        aggregated_transform = source.transform * Affine.scale(
            AGGREGATION_FACTOR,
            AGGREGATION_FACTOR,
        )
        return (
            {"Elevation": elevation, "Terrain Slope": slope, "Terrain Curvature": curvature},
            aggregated_transform,
            source.crs,
        )


def reproject_feature(
    source_array: np.ndarray,
    source_transform: Affine,
    source_crs: object,
    destination_shape: tuple[int, int],
    destination_transform: Affine,
) -> np.ndarray:
    """Reproject an aggregated terrain feature to the common WGS84 grid."""
    destination = np.full(destination_shape, np.nan, dtype="float32")
    reproject(
        source=source_array,
        destination=destination,
        src_transform=source_transform,
        src_crs=source_crs,
        src_nodata=np.nan,
        dst_transform=destination_transform,
        dst_crs="EPSG:4326",
        dst_nodata=np.nan,
        resampling=Resampling.bilinear,
    )
    return destination


def wet_window_scenario_loads(rain: pd.DataFrame) -> dict[str, float]:
    """Return equal-window mean scenario loads relative to the Heavy quantile."""
    station_window_quantiles: list[dict[str, float | str | int]] = []
    for station_id, group in rain.groupby("Station ID", sort=True):
        values = group.sort_values("Observation Time").set_index("Observation Time")["Hourly Rainfall"]
        full_index = pd.date_range(values.index.min(), values.index.max(), freq="h", tz=values.index.tz)
        values = values.reindex(full_index).astype(float)
        for window in WINDOWS:
            accumulated = values if window == 1 else values.rolling(window, min_periods=window).sum()
            wet = accumulated.loc[accumulated > 0].dropna()
            record: dict[str, float | str | int] = {"Station ID": str(station_id), "Window": window}
            for scenario, quantile in SCENARIO_QUANTILES.items():
                record[scenario] = float(wet.quantile(quantile))
            station_window_quantiles.append(record)

    quantiles = pd.DataFrame(station_window_quantiles)
    ratios: dict[str, float] = {}
    for scenario in SCENARIO_QUANTILES:
        ratios[scenario] = float((quantiles[scenario] / quantiles["Heavy"]).mean())
    return ratios


def threshold_categories(admin: pd.DataFrame, threshold: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Assign map factors and flag Yatsushiro's unresolved mixed subarea."""
    threshold = threshold.copy()
    threshold["Municipality Key"] = (
        threshold["Municipality or Subarea (Japanese)"]
        .str.replace("西部", "", regex=False)
        .str.replace("東部", "", regex=False)
    )
    grouped = threshold.groupby("Municipality Key")["Rainfall Threshold Retention Factor"].agg(
        lambda values: tuple(sorted(set(float(value) for value in values)))
    )
    factors = np.ones(len(admin), dtype="float32")
    mixed = np.zeros(len(admin), dtype=bool)
    for index, municipality in enumerate(admin["Municipality Name"].astype(str)):
        values = grouped.get(municipality, tuple())
        if values == (0.7,):
            factors[index] = 0.7
        elif values == (0.8,):
            factors[index] = 0.8
        elif values == (0.7, 0.8):
            factors[index] = 0.75
            mixed[index] = True
    return factors, mixed


def grid_indices(
    coordinates: np.ndarray,
    extent: tuple[float, float, float, float],
    shape: tuple[int, int],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Map longitude-latitude point coordinates to common-grid row and column indices."""
    west, east, south, north = extent
    rows, columns = shape
    column = np.floor((coordinates[:, 0] - west) / (east - west) * columns).astype(int)
    row = np.floor((north - coordinates[:, 1]) / (north - south) * rows).astype(int)
    inside = (row >= 0) & (row < rows) & (column >= 0) & (column < columns)
    return row, column, inside


def spatial_groups(
    row: np.ndarray,
    column: np.ndarray,
    extent: tuple[float, float, float, float],
    shape: tuple[int, int],
) -> np.ndarray:
    """Assign 0.2-degree spatial block identifiers to sampled grid cells."""
    west, east, south, north = extent
    rows, columns = shape
    longitude = west + (column + 0.5) / columns * (east - west)
    latitude = north - (row + 0.5) / rows * (north - south)
    block_x = np.floor((longitude - west) / 0.2).astype(int)
    block_y = np.floor((latitude - south) / 0.2).astype(int)
    return block_y * 100 + block_x


def fit_presence_background_model(
    features: dict[str, np.ndarray],
    valid: np.ndarray,
    landslide_geometry: np.ndarray,
    extent: tuple[float, float, float, float],
) -> tuple[object, dict[str, float], int, int, str]:
    """Fit a validated model or transparently fall back to a fixed terrain score."""
    shape = valid.shape
    coordinates = shapely.get_coordinates(landslide_geometry)
    row, column, inside = grid_indices(coordinates, extent, shape)
    row = row[inside]
    column = column[inside]
    cell_pairs = np.unique(np.column_stack([row, column]), axis=0)
    cell_pairs = cell_pairs[valid[cell_pairs[:, 0], cell_pairs[:, 1]]]
    if len(cell_pairs) < 200:
        raise RuntimeError("Too few valid unique landslide cells for spatial calibration.")

    presence_flat = np.ravel_multi_index((cell_pairs[:, 0], cell_pairs[:, 1]), shape)
    available_flat = np.flatnonzero(valid.ravel())
    background_pool = np.setdiff1d(available_flat, presence_flat, assume_unique=False)
    random = np.random.default_rng(20260809)
    background_count = min(len(background_pool), len(presence_flat) * 10)
    background_flat = random.choice(background_pool, size=background_count, replace=False)
    sampled_flat = np.concatenate([presence_flat, background_flat])
    sampled_row, sampled_column = np.unravel_index(sampled_flat, shape)

    matrix = np.column_stack(
        [features[name][sampled_row, sampled_column] for name in FEATURE_NAMES]
    )
    outcome = np.concatenate(
        [np.ones(len(presence_flat), dtype=int), np.zeros(len(background_flat), dtype=int)]
    )
    groups = spatial_groups(sampled_row, sampled_column, extent, shape)

    logistic = make_pipeline(
        StandardScaler(),
        LogisticRegression(C=1.0, class_weight="balanced", max_iter=1000, random_state=20260809),
    )
    splitter = GroupKFold(n_splits=5)
    logistic_auc_values: list[float] = []
    fallback_auc_values: list[float] = []
    elevation_warning_auc_values: list[float] = []
    for train, test in splitter.split(matrix, outcome, groups):
        if len(np.unique(outcome[test])) < 2:
            continue
        logistic.fit(matrix[train], outcome[train])
        logistic_auc_values.append(
            float(roc_auc_score(outcome[test], logistic.decision_function(matrix[test])))
        )
        fallback_fold = TransparentStandardizedScore(FALLBACK_WEIGHTS).fit(matrix[train])
        fallback_auc_values.append(
            float(roc_auc_score(outcome[test], fallback_fold.decision_function(matrix[test])))
        )
        elevation_warning = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                C=1.0,
                class_weight="balanced",
                max_iter=1000,
                random_state=20260809,
            ),
        )
        elevation_warning.fit(matrix[train][:, [0, 3]], outcome[train])
        elevation_warning_auc_values.append(
            float(
                roc_auc_score(
                    outcome[test],
                    elevation_warning.decision_function(matrix[test][:, [0, 3]]),
                )
            )
        )
    if len(logistic_auc_values) < 4:
        raise RuntimeError("Spatial validation produced fewer than four evaluable folds.")
    logistic_mean_auc = float(np.mean(logistic_auc_values))
    fallback_mean_auc = float(np.mean(fallback_auc_values))
    elevation_warning_mean_auc = float(np.mean(elevation_warning_auc_values))
    validation_metrics = {
        "Logistic Mean Spatial AUC": logistic_mean_auc,
        "Logistic Minimum Spatial AUC": float(np.min(logistic_auc_values)),
        "Logistic Maximum Spatial AUC": float(np.max(logistic_auc_values)),
        "Fixed Score Mean Spatial AUC": fallback_mean_auc,
        "Fixed Score Minimum Spatial AUC": float(np.min(fallback_auc_values)),
        "Elevation + Warning Mean Spatial AUC": elevation_warning_mean_auc,
    }
    # Pre-declared conservative selection: retain the fitted logistic score only when
    # it clears 0.60 mean AUC, has no fold below 0.50, beats the required
    # elevation-plus-warning comparator, and is within 0.02 AUC of the transparent
    # fixed score. Otherwise use the more spatially stable transparent scenario score.
    logistic_supported = (
        logistic_mean_auc >= 0.60
        and float(np.min(logistic_auc_values)) >= 0.50
        and logistic_mean_auc >= elevation_warning_mean_auc
        and logistic_mean_auc >= fallback_mean_auc - 0.02
    )
    if logistic_supported:
        logistic.fit(matrix, outcome)
        model = logistic
        coefficients = dict(
            zip(
                (f"Calibrated {name} Coefficient" for name in FEATURE_NAMES),
                model.named_steps["logisticregression"].coef_[0].astype(float),
            )
        )
        metrics = {**validation_metrics, **coefficients}
        mode = "Validation-selected presence-background score"
    else:
        model = TransparentStandardizedScore(FALLBACK_WEIGHTS).fit(matrix)
        metrics = {
            **validation_metrics,
            **{f"Fixed {name} Weight": value for name, value in FALLBACK_WEIGHTS.items()},
        }
        mode = "Validation-selected transparent scenario score"
    return model, metrics, len(presence_flat), len(background_flat), mode


def style_map_axis(ax: plt.Axes, extent: tuple[float, float, float, float]) -> None:
    """Apply accepted longitude-latitude grids and frames."""
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

    native_features, aggregated_transform, source_crs = native_terrain_features()
    features = {
        name: reproject_feature(
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
    warning_grid = rasterize(
        ((geometry, 1) for geometry in warning_geometry),
        out_shape=display_shape,
        transform=display_transform,
        fill=0,
        all_touched=True,
        dtype="uint8",
    ).astype("float32")
    features["Warning-Zone Exposure"] = warning_grid

    curvature_scale = np.nanpercentile(np.abs(features["Terrain Curvature"]), 99.5)
    if not np.isfinite(curvature_scale) or curvature_scale <= 0:
        raise RuntimeError("Terrain curvature could not be scaled.")
    features["Terrain Curvature"] = np.clip(
        features["Terrain Curvature"], -curvature_scale, curvature_scale
    )

    valid = admin_mask.copy()
    for feature in FEATURE_NAMES:
        valid &= np.isfinite(features[feature])

    landslides = pd.read_parquet(
        LANDSLIDE_PATH,
        columns=["Landslide Inventory ID", "Geometry"],
    )
    landslide_geometry = decode_geometry(landslides["Geometry"])
    inside = shapely.intersects(landslide_geometry, admin_union)
    landslide_geometry = landslide_geometry[inside]

    model, metrics, presence_count, background_count, model_mode = fit_presence_background_model(
        features,
        valid,
        landslide_geometry,
        extent,
    )
    valid_row, valid_column = np.nonzero(valid)
    all_matrix = np.column_stack(
        [features[name][valid_row, valid_column] for name in FEATURE_NAMES]
    )
    terrain_logit = np.full(display_shape, np.nan, dtype="float32")
    terrain_logit[valid] = model.decision_function(all_matrix).astype("float32")

    rain = pd.read_parquet(
        RAIN_PATH,
        columns=["Station ID", "Observation Time", "Hourly Rainfall"],
    )
    rain = rain.loc[rain["Hourly Rainfall"].notna()].copy()
    scenario_loads = wet_window_scenario_loads(rain)

    threshold = pd.read_parquet(THRESHOLD_PATH)
    factors, mixed = threshold_categories(admin, threshold)
    factor_grid = rasterize(
        ((geometry, float(factor)) for geometry, factor in zip(admin_geometry, factors)),
        out_shape=display_shape,
        transform=display_transform,
        fill=1.0,
        all_touched=True,
        dtype="float32",
    )
    factor_grid[~admin_mask] = np.nan

    panels = [
        ("Baseline threshold\nHeavy rainfall", np.ones(display_shape, dtype="float32")),
        ("Official threshold\nModerate rainfall", scenario_loads["Moderate"] / factor_grid),
        ("Official threshold\nHeavy rainfall", scenario_loads["Heavy"] / factor_grid),
        ("Official threshold\nExtreme rainfall", scenario_loads["Extreme"] / factor_grid),
    ]
    score_maps: list[np.ndarray] = []
    for _, rainfall_loading in panels:
        score = expit(terrain_logit + rainfall_loading - 1.0).astype("float32")
        score[~valid] = np.nan
        score_maps.append(score)

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
    mixed_segments = line_segments(shapely.boundary(admin_geometry[mixed]))
    landslide_coordinates = shapely.get_coordinates(landslide_geometry)

    image = None
    for index, (axis, (annotation, _), score) in enumerate(zip(axes, panels, score_maps)):
        image = axis.imshow(
            score,
            extent=image_extent,
            origin="upper",
            cmap="magma",
            vmin=0,
            vmax=1,
            interpolation="bilinear",
            zorder=1,
        )
        axis.add_collection(
            LineCollection(
                boundary_segments,
                colors="#475467",
                linewidths=0.40,
                alpha=0.78,
                zorder=7,
            )
        )
        if index > 0 and mixed_segments:
            axis.add_collection(
                LineCollection(
                    mixed_segments,
                    colors="#5E3C99",
                    linewidths=1.3,
                    linestyles=(0, (4, 2)),
                    zorder=10,
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
            bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "#D0D5DD", "alpha": 0.92},
            zorder=20,
        )
        style_map_axis(axis, extent)
        add_panel_label(axis, "abcd"[index])

    axes[0].scatter(
        landslide_coordinates[:, 0],
        landslide_coordinates[:, 1],
        s=3.5,
        c="#42F5E9",
        edgecolors="none",
        alpha=0.65,
        zorder=12,
    )
    axes[0].legend(
        handles=[
            Line2D([0], [0], marker="o", color="none", markerfacecolor="#42F5E9", markersize=5, label="2016 interpreted landslide")
        ],
        loc="lower left",
        fontsize=7.6,
        frameon=True,
        framealpha=0.92,
    )
    if mixed.any():
        axes[2].legend(
            handles=[
                Line2D([0], [0], color="#5E3C99", linewidth=1.4, linestyle=(0, (4, 2)), label="Yatsushiro 0.70–0.80 midpoint display")
            ],
            loc="lower left",
            fontsize=7.2,
            frameon=True,
            framealpha=0.92,
        )

    if image is None:
        raise RuntimeError("No score image was generated.")
    colorbar = fig.colorbar(image, cax=colorbar_axis)
    colorbar.set_label(
        f"Relative landslide disruption score\n({model_mode.lower()})",
        fontsize=9,
    )
    colorbar.ax.tick_params(labelsize=8)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Saved: {OUT.relative_to(ROOT)}")
    print(f"Score construction: {model_mode}")
    print(f"Unique presence cells: {presence_count:,}; background cells: {background_count:,}")
    print("Spatial validation and standardized coefficients:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")
    print("Scenario loads relative to Heavy:")
    for scenario, value in scenario_loads.items():
        print(f"  {scenario}: {value:.4f}")
    print("Interpretation: relative scenario score; not an occurrence probability")


if __name__ == "__main__":
    main()
