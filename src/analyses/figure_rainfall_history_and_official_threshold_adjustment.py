#!/usr/bin/env python3
"""Rainfall History and Official Threshold Adjustment.

Plan: Show station rainfall history, cumulative rainfall, Moderate, Heavy, and
Extreme scenarios, and official 70 percent and 80 percent threshold settings.
Framework: Section 5 scenario contrasts; Section 6 rolling rainfall and
quantile-based rainfall scenarios; Section 7 rainfall/threshold scenario step.
The figure does not imply fine-resolution rainfall interpolation or a causal
earthquake effect.
"""
from __future__ import annotations

from calendar import isleap
import os
from pathlib import Path

# Prevent external projection paths from overriding the project geospatial stack.
os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Polygon as MplPolygon
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import seaborn as sns
import shapely


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
RAIN_PATH = PROCESSED / "jma_hourly_rainfall_preprocessed.parquet"
THRESHOLD_PATH = PROCESSED / "official_threshold_factors_preprocessed.parquet"
ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
OUT = ROOT / "data/results/figures/Figure_rainfall_history_and_official_threshold_adjustment.png"

WINDOWS = [1, 3, 24, 72]
SCENARIOS = {
    "Moderate (75th percentile)": (0.75, "#2A9D8F"),
    "Heavy (90th percentile)": (0.90, "#F4A261"),
    "Extreme (99th percentile)": (0.99, "#C23B33"),
}
THRESHOLD_COLORS = {
    "No temporary reduction": "#E4E7EC",
    "0.80 retention": "#F4A261",
    "0.70 retention": "#C23B33",
    "Mixed 0.70 / 0.80": "#7B61A8",
}
STATION_LABELS = {
    "a0835": "Kikuchi",
    "a0840": "Takamori",
    "a0842": "Kosa",
    "a0843": "Matsushima",
    "a0846": "Yatsushiro",
    "a1081": "Misumi",
    "s47819": "Kumamoto",
}


def decode_geometry(series: pd.Series) -> np.ndarray:
    """Decode project-standard WKB geometry and reject missing shapes."""
    geometry = shapely.from_wkb(series.to_numpy())
    valid = ~shapely.is_missing(geometry) & ~shapely.is_empty(geometry)
    if not valid.all():
        raise ValueError("Administrative geometry contains missing or empty features.")
    return geometry


def line_segments(geometry: np.ndarray) -> list[np.ndarray]:
    """Convert line or multiline geometry into LineCollection segments."""
    segments: list[np.ndarray] = []
    for part in shapely.get_parts(geometry):
        coordinates = shapely.get_coordinates(part)[:, :2]
        if len(coordinates) >= 2:
            segments.append(coordinates)
    return segments


def polygon_patches(geometry: np.ndarray) -> list[MplPolygon]:
    """Convert polygon and multipolygon geometry into Matplotlib patches."""
    patches: list[MplPolygon] = []
    for polygon in shapely.get_parts(geometry):
        if shapely.get_type_id(polygon) != 3:
            continue
        coordinates = shapely.get_coordinates(shapely.get_exterior_ring(polygon))[:, :2]
        if len(coordinates) >= 3:
            patches.append(MplPolygon(coordinates, closed=True))
    return patches


def add_panel_label(ax: plt.Axes, label: str) -> None:
    """Add the required lowercase panel label."""
    ax.text(
        -0.055,
        1.025,
        label,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        color="#172033",
        ha="left",
        va="bottom",
    )


def style_chart_axis(ax: plt.Axes) -> None:
    """Apply a compact publication chart style."""
    ax.grid(True, color="#D0D5DD", linewidth=0.55, alpha=0.75)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=8, colors="#475467")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#667085")
    ax.spines["bottom"].set_color("#667085")


def style_map_axis(ax: plt.Axes, bounds: tuple[float, float, float, float]) -> None:
    """Apply the accepted coordinate-grid and frame convention."""
    west, south, east, north = bounds
    pad_x = (east - west) * 0.025
    pad_y = (north - south) * 0.025
    west -= pad_x
    east += pad_x
    south -= pad_y
    north += pad_y
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
    ax.grid(True, color="#98A2B3", linewidth=0.45, linestyle=(0, (3, 3)), alpha=0.58)
    ax.set_axisbelow(False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.85)
        spine.set_color("#344054")


def build_rainfall_summaries(
    rain: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Construct quality-screened annual maxima and wet-window quantiles."""
    annual_rows: list[dict[str, object]] = []
    quantile_rows: list[dict[str, object]] = []

    for station_id, group in rain.groupby("Station ID", sort=True):
        group = group.sort_values("Observation Time")
        station_name = str(group["Station Name (Japanese)"].iloc[0])
        values = group.set_index("Observation Time")["Hourly Rainfall"].astype(float)
        full_index = pd.date_range(values.index.min(), values.index.max(), freq="h", tz=values.index.tz)
        values = values.reindex(full_index)

        rolling: dict[int, pd.Series] = {1: values}
        for window in WINDOWS[1:]:
            rolling[window] = values.rolling(window=window, min_periods=window).sum()

        hourly_by_year = values.groupby(values.index.year)
        for year, hourly_values in hourly_by_year:
            expected = 8784 if isleap(int(year)) else 8760
            coverage = hourly_values.notna().sum() / expected
            if coverage < 0.95:
                continue
            annual_maximum = rolling[24].loc[rolling[24].index.year == year].max()
            annual_rows.append(
                {
                    "Station ID": station_id,
                    "Station Name (Japanese)": station_name,
                    "Year": int(year),
                    "Annual Maximum 24 h Rainfall (mm)": float(annual_maximum),
                    "Hourly Coverage": float(coverage),
                }
            )

        for window in WINDOWS:
            wet_windows = rolling[window].loc[rolling[window] > 0].dropna()
            if wet_windows.empty:
                raise ValueError(f"No complete wet windows for station {station_id}, window {window} h.")
            for scenario, (quantile, _) in SCENARIOS.items():
                quantile_rows.append(
                    {
                        "Station ID": station_id,
                        "Window (h)": window,
                        "Scenario": scenario,
                        "Quantile": quantile,
                        "Rainfall (mm)": float(wet_windows.quantile(quantile)),
                        "Wet Window Count": int(len(wet_windows)),
                    }
                )

    return pd.DataFrame(annual_rows), pd.DataFrame(quantile_rows)


def classify_threshold_areas(
    admin: pd.DataFrame,
    threshold: pd.DataFrame,
) -> pd.Series:
    """Map official municipality/subarea factors without inventing subarea boundaries."""
    threshold = threshold.copy()
    threshold["Municipality Key"] = (
        threshold["Municipality or Subarea (Japanese)"]
        .str.replace("西部", "", regex=False)
        .str.replace("東部", "", regex=False)
    )
    factor_sets = threshold.groupby("Municipality Key")["Rainfall Threshold Retention Factor"].agg(
        lambda values: tuple(sorted(set(float(value) for value in values)))
    )

    categories: list[str] = []
    for municipality in admin["Municipality Name"].astype(str):
        factors = factor_sets.get(municipality, tuple())
        if factors == (0.7,):
            categories.append("0.70 retention")
        elif factors == (0.8,):
            categories.append("0.80 retention")
        elif factors == (0.7, 0.8):
            categories.append("Mixed 0.70 / 0.80")
        else:
            categories.append("No temporary reduction")
    return pd.Series(categories, index=admin.index, dtype="string")


def main() -> None:
    sns.set_theme(style="white", context="paper")

    rain = pd.read_parquet(
        RAIN_PATH,
        columns=[
            "Station ID",
            "Station Name (Japanese)",
            "Observation Time",
            "Hourly Rainfall",
            "Quality Flag",
        ],
    )
    rain = rain.loc[rain["Hourly Rainfall"].notna()].copy()
    annual, quantiles = build_rainfall_summaries(rain)

    threshold = pd.read_parquet(THRESHOLD_PATH)
    admin = pd.read_parquet(
        ADMIN_PATH,
        columns=["Municipality Name", "Municipality Label", "Geometry"],
    )
    admin_geometry = decode_geometry(admin.pop("Geometry"))
    admin["Threshold Category"] = classify_threshold_areas(admin, threshold)
    admin_union = shapely.union_all(admin_geometry)
    map_bounds = tuple(float(value) for value in shapely.bounds(admin_union))

    fig, axes = plt.subplots(2, 2, figsize=(14, 10.5), constrained_layout=True)
    axes = axes.ravel()

    # a: annual maximum 24-hour rainfall for years with at least 95% hourly coverage.
    palette = sns.color_palette("colorblind", n_colors=annual["Station ID"].nunique())
    for color, (station_id, group) in zip(palette, annual.groupby("Station ID", sort=True)):
        axes[0].plot(
            group["Year"],
            group["Annual Maximum 24 h Rainfall (mm)"],
            marker="o",
            markersize=3.8,
            linewidth=1.35,
            color=color,
            label=STATION_LABELS.get(str(station_id), str(station_id)),
        )
    axes[0].set_xlabel("Year", fontsize=9)
    axes[0].set_ylabel("Annual maximum 24 h rainfall (mm)", fontsize=9)
    axes[0].set_xticks(sorted(annual["Year"].unique()))
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].legend(ncol=2, fontsize=7.6, frameon=True, framealpha=0.92, loc="upper right")
    style_chart_axis(axes[0])

    # b: station distribution of wet-window scenario quantiles.
    scenario_summary = (
        quantiles.groupby(["Scenario", "Window (h)"])["Rainfall (mm)"]
        .agg(Median="median", Minimum="min", Maximum="max")
        .reset_index()
    )
    for scenario, (_, color) in SCENARIOS.items():
        group = scenario_summary.loc[scenario_summary["Scenario"].eq(scenario)].sort_values("Window (h)")
        x = group["Window (h)"].to_numpy(dtype=float)
        axes[1].fill_between(
            x,
            group["Minimum"].to_numpy(dtype=float),
            group["Maximum"].to_numpy(dtype=float),
            color=color,
            alpha=0.14,
            linewidth=0,
        )
        axes[1].plot(
            x,
            group["Median"].to_numpy(dtype=float),
            marker="o",
            markersize=4.2,
            linewidth=1.8,
            color=color,
            label=scenario,
        )
    axes[1].set_xscale("log")
    axes[1].set_xticks(WINDOWS, [str(window) for window in WINDOWS])
    axes[1].set_xlabel("Accumulation window (h)", fontsize=9)
    axes[1].set_ylabel("Wet-window rainfall quantile (mm)", fontsize=9)
    axes[1].legend(fontsize=7.6, frameon=True, framealpha=0.92, loc="upper left")
    style_chart_axis(axes[1])

    # c: official temporary threshold categories by available municipality geometry.
    for category, color in THRESHOLD_COLORS.items():
        mask = admin["Threshold Category"].eq(category).to_numpy()
        if not mask.any():
            continue
        collection = PatchCollection(
            polygon_patches(admin_geometry[mask]),
            facecolor=color,
            edgecolor="#FFFFFF",
            linewidth=0.45,
            zorder=2,
        )
        axes[2].add_collection(collection)
    axes[2].add_collection(
        LineCollection(
            line_segments(shapely.boundary(admin_geometry)),
            colors="#475467",
            linewidths=0.45,
            alpha=0.85,
            zorder=7,
        )
    )
    axes[2].legend(
        handles=[Patch(facecolor=color, edgecolor="#667085", label=category) for category, color in THRESHOLD_COLORS.items()],
        loc="lower left",
        fontsize=7.6,
        frameon=True,
        framealpha=0.94,
    )
    style_map_axis(axes[2], map_bounds)

    # d: direct threshold-retention mechanics, independent of window weights.
    rainfall_share = np.linspace(0, 1.2, 121)
    factor_styles = [
        (1.0, "Baseline 1.00", "#667085"),
        (0.8, "Central 0.80", "#F4A261"),
        (0.7, "High 0.70", "#C23B33"),
    ]
    for factor, label, color in factor_styles:
        axes[3].plot(
            rainfall_share * 100,
            rainfall_share / factor,
            linewidth=2.0,
            color=color,
            label=label,
        )
        axes[3].scatter([factor * 100], [1.0], s=30, color=color, edgecolors="white", linewidths=0.5, zorder=8)
    axes[3].axhline(1.0, color="#344054", linestyle=(0, (4, 3)), linewidth=0.9)
    axes[3].set_xlim(0, 120)
    axes[3].set_ylim(0, 1.8)
    axes[3].set_xlabel("Rainfall relative to baseline threshold (%)", fontsize=9)
    axes[3].set_ylabel("Threshold-relative rainfall loading", fontsize=9)
    axes[3].legend(fontsize=7.8, frameon=True, framealpha=0.92, loc="upper left")
    style_chart_axis(axes[3])

    for label, axis in zip("abcd", axes):
        add_panel_label(axis, label)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUT.relative_to(ROOT)}")
    print(f"Rainfall stations: {rain['Station ID'].nunique()}")
    print(f"Complete station-years shown: {len(annual)}")
    print(f"Wet-window scenario records: {len(quantiles)}")
    print("Threshold map categories:")
    print(admin["Threshold Category"].value_counts().to_string())


if __name__ == "__main__":
    main()
