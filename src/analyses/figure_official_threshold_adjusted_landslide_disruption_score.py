#!/usr/bin/env python3
"""Official-Threshold-Adjusted Landslide Disruption Score.

Plan: Compare baseline and rainfall-scenario slope disruption scores using
official resolved threshold values, an analyst-defined 0.75 municipality-wide
Yatsushiro midpoint, and municipality-wide 0.70-0.80 Yatsushiro bounds while
retaining score-based language.
Framework: Section 5 presence-background spatial ranking calibration; Section 6
terrain derivatives, warning-zone exposure, rainfall scenario loading, and the
logistic Landslide Disruption Score; Section 7 terrain-score workflow.

Native DEM derivatives are computed in chunks and aggregated only after slope
and curvature calculation. The displayed values are relative scenario scores,
not calibrated landslide occurrence probabilities.
"""
from __future__ import annotations

import gc
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
import resvg_py
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from rasterio.warp import Resampling, reproject
from rasterio.windows import Window
from scipy.special import expit
from scipy.stats import spearmanr
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
SCENARIO_PATH = PROCESSED / "jma_rainfall_scenario_quantiles_preprocessed.parquet"
THRESHOLD_PATH = PROCESSED / "official_threshold_factors_preprocessed.parquet"
OUT = ROOT / "data/results/figures/Figure_official_threshold_adjusted_landslide_disruption_score.png"
SVG_OUT = OUT.with_suffix(".svg")

AGGREGATION_FACTOR = 16
CHUNK_OUTPUT_ROWS = 32
DISPLAY_WIDTH = 950
WINDOWS = [1, 3, 24, 72]
SCENARIO_QUANTILES = {
    "Moderate": 0.75,
    "Heavy": 0.90,
    "Extreme": 0.99,
}
CENTRAL_SUPPORT = "Central: 7 stations, 2016-2020"
DISTANCE_STABILIZER_DEGREES = 0.02
RAINFALL_LOADING_GAMMA = 1.0
LANDSLIDE_VALIDATION_DATE = pd.Timestamp("2016-07-28")
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
        return standardized @ self.weights


def decode_geometry(series: pd.Series) -> np.ndarray:
    """Decode WKB and retain non-empty geometry."""
    geometry = shapely.from_wkb(series.to_numpy())
    valid = ~shapely.is_missing(geometry) & ~shapely.is_empty(geometry)
    return geometry[valid]


def warning_zone_geometry(
    as_of: pd.Timestamp | None = None,
) -> tuple[np.ndarray, dict[str, int]]:
    """Return current or temporally eligible warning-zone geometry.

    The historical landslide validation may use only designations available by
    the validation event date. Current operational screening continues to use
    the complete reference layer.
    """
    warning = pd.read_parquet(WARNING_PATH, columns=["Designation Date", "Geometry"])
    designation_date = pd.to_datetime(warning["Designation Date"], errors="coerce")
    known = designation_date.notna() & designation_date.lt(pd.Timestamp("9999-01-01"))
    if as_of is None:
        selected = np.ones(len(warning), dtype=bool)
    else:
        selected = known & designation_date.le(as_of)
    counts = {
        "total": int(len(warning)),
        "selected": int(selected.sum()),
        "post_event": int((known & designation_date.gt(as_of)).sum()) if as_of is not None else 0,
        "unknown_or_sentinel": int((~known).sum()),
    }
    return decode_geometry(warning.loc[selected, "Geometry"]), counts


def warning_zone_grid(
    geometry: np.ndarray,
    shape: tuple[int, int],
    transform: Affine,
) -> np.ndarray:
    """Rasterize warning zones to the common binary exposure grid."""
    return rasterize(
        ((feature, 1) for feature in geometry),
        out_shape=shape,
        transform=transform,
        fill=0,
        all_touched=True,
        dtype="uint8",
    ).astype("float32")


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


def event_scenario_loads(
    scenario_values: pd.DataFrame,
    extent: tuple[float, float, float, float],
    shape: tuple[int, int],
) -> dict[str, np.ndarray]:
    """Build coarse inverse-distance event-quantile rainfall loading surfaces."""
    central = scenario_values.loc[
        scenario_values["Support Specification"].eq(CENTRAL_SUPPORT)
    ].copy()
    if central["Station ID"].nunique() != 7:
        raise RuntimeError("Central rainfall loading requires seven stations.")

    stations = (
        central[
            ["Station ID", "Station Latitude", "Station Longitude"]
        ]
        .drop_duplicates()
        .sort_values("Station ID")
        .reset_index(drop=True)
    )
    west, east, south, north = extent
    rows, columns = shape
    longitude = west + (np.arange(columns) + 0.5) / columns * (east - west)
    latitude = north - (np.arange(rows) + 0.5) / rows * (north - south)
    longitude_grid, latitude_grid = np.meshgrid(longitude, latitude)

    station_longitude = stations["Station Longitude"].to_numpy(dtype=float)
    station_latitude = stations["Station Latitude"].to_numpy(dtype=float)
    cosine = np.cos(np.deg2rad(latitude_grid))[..., None]
    distance_squared = (
        ((longitude_grid[..., None] - station_longitude) * cosine) ** 2
        + (latitude_grid[..., None] - station_latitude) ** 2
        + DISTANCE_STABILIZER_DEGREES**2
    )
    inverse_distance = 1.0 / distance_squared
    station_weights = inverse_distance / inverse_distance.sum(axis=2, keepdims=True)

    heavy = central.loc[central["Rainfall Scenario"].eq("Heavy")]
    references = {
        window: float(heavy[f"Scenario {window} h Rainfall"].median())
        for window in WINDOWS
    }
    loads: dict[str, np.ndarray] = {}
    for scenario in SCENARIO_QUANTILES:
        subset = (
            central.loc[central["Rainfall Scenario"].eq(scenario)]
            .set_index("Station ID")
            .reindex(stations["Station ID"])
        )
        window_surfaces = []
        for window in WINDOWS:
            station_ratio = (
                subset[f"Scenario {window} h Rainfall"].to_numpy(dtype=float)
                / references[window]
            )
            window_surfaces.append(
                np.sum(station_weights * station_ratio[None, None, :], axis=2)
            )
        loads[scenario] = np.mean(window_surfaces, axis=0).astype("float32")
    return loads


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
    """Evaluate comparators and fit the pre-specified transparent terrain score."""
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
    warning_only_auc_values: list[float] = []
    logistic_capture_values: list[float] = []
    fallback_capture_values: list[float] = []
    for train, test in splitter.split(matrix, outcome, groups):
        if len(np.unique(outcome[test])) < 2:
            continue
        logistic.fit(matrix[train], outcome[train])
        logistic_prediction = logistic.decision_function(matrix[test])
        logistic_auc_values.append(
            float(roc_auc_score(outcome[test], logistic_prediction))
        )
        fallback_fold = TransparentStandardizedScore(FALLBACK_WEIGHTS).fit(matrix[train])
        fallback_prediction = fallback_fold.decision_function(matrix[test])
        fallback_auc_values.append(
            float(roc_auc_score(outcome[test], fallback_prediction))
        )
        test_presence = outcome[test].eq(1) if isinstance(outcome[test], pd.Series) else outcome[test] == 1
        logistic_capture_values.append(
            float(
                np.mean(
                    logistic_prediction[test_presence]
                    >= np.quantile(logistic_prediction, 0.75)
                )
            )
        )
        fallback_capture_values.append(
            float(
                np.mean(
                    fallback_prediction[test_presence]
                    >= np.quantile(fallback_prediction, 0.75)
                )
            )
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
        warning_only_auc_values.append(
            float(roc_auc_score(outcome[test], matrix[test, 3]))
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
        "Fixed Score Maximum Spatial AUC": float(np.max(fallback_auc_values)),
        "Fixed Score Mean Held-Out Top-Quartile Capture": float(np.mean(fallback_capture_values)),
        "Logistic Mean Held-Out Top-Quartile Capture": float(np.mean(logistic_capture_values)),
        "Elevation + Warning Mean Spatial AUC": elevation_warning_mean_auc,
        "Warning-Only Mean Spatial AUC": float(np.mean(warning_only_auc_values)),
    }
    model = TransparentStandardizedScore(FALLBACK_WEIGHTS).fit(matrix)
    metrics = {
        **validation_metrics,
        **{f"Fixed {name} Weight": value for name, value in FALLBACK_WEIGHTS.items()},
    }
    mode = "Pre-specified transparent terrain-context score"
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

    current_warning_geometry, current_warning_counts = warning_zone_geometry()
    validation_warning_geometry, validation_warning_counts = warning_zone_geometry(
        LANDSLIDE_VALIDATION_DATE
    )
    features["Warning-Zone Exposure"] = warning_zone_grid(
        current_warning_geometry,
        display_shape,
        display_transform,
    )
    validation_features = features.copy()
    validation_features["Warning-Zone Exposure"] = warning_zone_grid(
        validation_warning_geometry,
        display_shape,
        display_transform,
    )

    curvature_scale = np.nanpercentile(np.abs(features["Terrain Curvature"]), 99.5)
    if not np.isfinite(curvature_scale) or curvature_scale <= 0:
        raise RuntimeError("Terrain curvature could not be scaled.")
    features["Terrain Curvature"] = np.clip(
        features["Terrain Curvature"], -curvature_scale, curvature_scale
    )
    validation_features["Terrain Curvature"] = features["Terrain Curvature"]

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
        validation_features,
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

    scenario_values = pd.read_parquet(SCENARIO_PATH)
    scenario_loads = event_scenario_loads(scenario_values, extent, display_shape)

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

    yatsushiro_grid = rasterize(
        ((geometry, 1) for geometry in admin_geometry[mixed]),
        out_shape=display_shape,
        transform=display_transform,
        fill=0,
        all_touched=True,
        dtype="uint8",
    ).astype(bool)
    yatsushiro_grid &= valid
    if not yatsushiro_grid.any():
        raise RuntimeError("Yatsushiro threshold-support geometry was not resolved on the score grid.")
    factor_grid_070 = factor_grid.copy()
    factor_grid_080 = factor_grid.copy()
    factor_grid_070[yatsushiro_grid] = 0.70
    factor_grid_080[yatsushiro_grid] = 0.80

    panels = [
        ("Baseline threshold\nHeavy rainfall", scenario_loads["Heavy"]),
        ("Adjusted threshold\nModerate rainfall", scenario_loads["Moderate"] / factor_grid),
        ("Adjusted threshold\nHeavy rainfall", scenario_loads["Heavy"] / factor_grid),
        ("Adjusted threshold\nExtreme rainfall", scenario_loads["Extreme"] / factor_grid),
    ]
    score_maps: list[np.ndarray] = []
    for _, rainfall_loading in panels:
        score = expit(
            terrain_logit
            + RAINFALL_LOADING_GAMMA * np.log(np.clip(rainfall_loading, 1e-6, None))
        ).astype("float32")
        score[~valid] = np.nan
        score_maps.append(score)

    yatsushiro_summaries: list[tuple[float, float, float] | None] = [None]
    for scenario in ("Moderate", "Heavy", "Extreme"):
        scenario_scores: dict[str, np.ndarray] = {}
        for label, scenario_factor_grid in (
            ("0.70", factor_grid_070),
            ("0.75", factor_grid),
            ("0.80", factor_grid_080),
        ):
            score = expit(
                terrain_logit
                + RAINFALL_LOADING_GAMMA
                * np.log(
                    np.clip(
                        scenario_loads[scenario] / scenario_factor_grid,
                        1e-6,
                        None,
                    )
                )
            ).astype("float32")
            score[~valid] = np.nan
            scenario_scores[label] = score
        midpoint_mean = float(np.nanmean(scenario_scores["0.75"][yatsushiro_grid]))
        bound_means = [
            float(np.nanmean(scenario_scores[label][yatsushiro_grid]))
            for label in ("0.70", "0.80")
        ]
        yatsushiro_summaries.append(
            (midpoint_mean, min(bound_means), max(bound_means))
        )

    print(f"Score construction: {model_mode}")
    print(
        "Warning-zone temporal support: "
        f"2016 validation={validation_warning_counts['selected']:,} designated by "
        f"{LANDSLIDE_VALIDATION_DATE.date()}; "
        f"post-event excluded={validation_warning_counts['post_event']:,}; "
        f"unknown/sentinel excluded={validation_warning_counts['unknown_or_sentinel']:,}; "
        f"2026 screening={current_warning_counts['selected']:,} current polygons"
    )
    print(f"Unique presence cells: {presence_count:,}; background cells: {background_count:,}")
    print("Spatial validation and standardized coefficients:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")
    print("Scenario loading and score diagnostics:")
    for scenario, value in scenario_loads.items():
        finite_loading = value[valid]
        print(
            f"  {scenario} loading: median={np.median(finite_loading):.4f}; "
            f"p05={np.quantile(finite_loading, 0.05):.4f}; "
            f"p95={np.quantile(finite_loading, 0.95):.4f}"
        )
    for (annotation, _), score in zip(panels, score_maps):
        finite_score = score[valid]
        print(
            f"  {annotation.replace(chr(10), ' ')}: "
            f"median={np.median(finite_score):.4f}; "
            f"score<0.01={np.mean(finite_score < 0.01):.4%}; "
            f"score>0.99={np.mean(finite_score > 0.99):.4%}"
        )
    print("Yatsushiro municipality-wide threshold-support sensitivity:")
    for scenario, summary in zip(("Moderate", "Heavy", "Extreme"), yatsushiro_summaries[1:]):
        if summary is None:
            continue
        midpoint_mean, lower_mean, upper_mean = summary
        print(
            f"  {scenario}: analyst midpoint 0.75 mean={midpoint_mean:.4f}; "
            f"0.70-0.80 bounding means={lower_mean:.4f}-{upper_mean:.4f}"
        )
    official_scores = score_maps[1:]
    for left_index, left_name in enumerate(("Moderate", "Heavy", "Extreme")):
        for right_index, right_name in enumerate(("Moderate", "Heavy", "Extreme")):
            if right_index <= left_index:
                continue
            correlation = spearmanr(
                official_scores[left_index][valid],
                official_scores[right_index][valid],
            ).statistic
            print(f"  Rank correlation {left_name} vs {right_name}: {correlation:.6f}")
    print("Interpretation: relative scenario score; not an occurrence probability", flush=True)

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
    for index, (axis, (annotation, _), score, yatsushiro_summary) in enumerate(
        zip(axes, panels, score_maps, yatsushiro_summaries)
    ):
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
        if yatsushiro_summary is not None:
            midpoint_mean, lower_mean, upper_mean = yatsushiro_summary
            axis.text(
                0.982,
                0.018,
                "Yatsushiro mean score\n"
                f"analyst midpoint 0.75: {midpoint_mean:.3f}\n"
                f"0.70-0.80 bounds: {lower_mean:.3f}-{upper_mean:.3f}",
                transform=axis.transAxes,
                ha="right",
                va="bottom",
                fontsize=7.0,
                color="#344054",
                linespacing=1.18,
                bbox={
                    "boxstyle": "round,pad=0.28",
                    "facecolor": "white",
                    "edgecolor": "#98A2B3",
                    "linewidth": 0.65,
                    "alpha": 0.93,
                },
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
                Line2D(
                    [0],
                    [0],
                    color="#5E3C99",
                    linewidth=1.4,
                    linestyle=(0, (4, 2)),
                    label="Yatsushiro: official subarea boundary unresolved",
                )
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
    fig.savefig(SVG_OUT, format="svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Saved SVG: {SVG_OUT.relative_to(ROOT)}")

    del (
        fig,
        image,
        native_features,
        features,
        all_matrix,
        terrain_logit,
        scenario_loads,
        score_maps,
        official_scores,
        panels,
        yatsushiro_summaries,
        yatsushiro_grid,
        factor_grid_070,
        factor_grid_080,
    )
    gc.collect()
    OUT.write_bytes(
        resvg_py.svg_to_bytes(
            svg_path=str(SVG_OUT),
            dpi=300.0,
            background="white",
        )
    )
    print(f"Converted PNG (300 dpi): {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
