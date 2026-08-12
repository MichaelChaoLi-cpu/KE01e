#!/usr/bin/env python3
"""Rainfall History and Official Threshold Adjustment.

Plan: Show station rainfall history, cumulative rainfall, Moderate, Heavy, and
Extreme scenarios, official 70 percent and 80 percent threshold settings, and
the analyst-defined 0.75 Yatsushiro midpoint with 0.70-0.80 bounds.
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
import resvg_py
import seaborn as sns
import shapely


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
RAIN_PATH = PROCESSED / "jma_hourly_rainfall_preprocessed.parquet"
SCENARIO_PATH = PROCESSED / "jma_rainfall_scenario_quantiles_preprocessed.parquet"
THRESHOLD_PATH = PROCESSED / "official_threshold_factors_preprocessed.parquet"
ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
OUT = ROOT / "data/results/figures/Figure_rainfall_history_and_official_threshold_adjustment.png"
SVG_OUT = OUT.with_suffix(".svg")

WINDOWS = [1, 3, 24, 72]
SCENARIOS = {
    "Moderate": (0.75, "#2A9D8F"),
    "Heavy": (0.90, "#F4A261"),
    "Extreme": (0.99, "#C23B33"),
}
THRESHOLD_COLORS = {
    "No temporary reduction": "#E4E7EC",
    "Official 0.80 retention": "#F4A261",
    "Official 0.70 retention": "#C23B33",
    "Yatsushiro official 0.70 / 0.80 subareas": "#7B61A8",
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


def build_annual_maxima(rain: pd.DataFrame) -> pd.DataFrame:
    """Construct quality-screened annual 24-hour maxima."""
    annual_rows: list[dict[str, object]] = []

    for station_id, group in rain.groupby("Station ID", sort=True):
        group = group.sort_values("Observation Time")
        station_name = str(group["Station Name (Japanese)"].iloc[0])
        valid_rainfall = group["Hourly Rainfall"].where(group["Quality Flag"].eq(8))
        values = pd.Series(
            valid_rainfall.to_numpy(dtype=float),
            index=group["Observation Time"],
        )
        full_index = pd.date_range(values.index.min(), values.index.max(), freq="h", tz=values.index.tz)
        values = values.reindex(full_index)

        rolling_24h = values.rolling(window=24, min_periods=24).sum()

        hourly_by_year = values.groupby(values.index.year)
        for year, hourly_values in hourly_by_year:
            expected = 8784 if isleap(int(year)) else 8760
            coverage = hourly_values.notna().sum() / expected
            if coverage < 0.95:
                continue
            annual_maximum = rolling_24h.loc[rolling_24h.index.year == year].max()
            annual_rows.append(
                {
                    "Station ID": station_id,
                    "Station Name (Japanese)": station_name,
                    "Year": int(year),
                    "Annual Maximum 24 h Rainfall (mm)": float(annual_maximum),
                    "Hourly Coverage": float(coverage),
                }
            )

    return pd.DataFrame(annual_rows)


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
            categories.append("Official 0.70 retention")
        elif factors == (0.8,):
            categories.append("Official 0.80 retention")
        elif factors == (0.7, 0.8):
            categories.append("Yatsushiro official 0.70 / 0.80 subareas")
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
    annual = build_annual_maxima(rain)
    scenario_values = pd.read_parquet(SCENARIO_PATH)
    central_scenarios = scenario_values.loc[
        scenario_values["Support Specification"].eq("Central: 7 stations, 2016-2020")
    ].copy()
    sensitivity_scenarios = scenario_values.loc[
        scenario_values["Support Specification"].eq("Sensitivity: 5 stations, 2016-2025")
    ].copy()
    if central_scenarios["Station ID"].nunique() != 7:
        raise RuntimeError("Central rainfall scenario support must contain seven stations.")
    if sensitivity_scenarios["Station ID"].nunique() != 5:
        raise RuntimeError("Temporal-support sensitivity must contain five stations.")

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

    # b: station distribution of independent-event maximum quantiles.
    scenario_rows: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        subset = central_scenarios.loc[central_scenarios["Rainfall Scenario"].eq(scenario)]
        for window in WINDOWS:
            values = subset[f"Scenario {window} h Rainfall"].astype(float)
            scenario_rows.append(
                {
                    "Scenario": scenario,
                    "Window (h)": window,
                    "Median": float(values.median()),
                    "Minimum": float(values.min()),
                    "Maximum": float(values.max()),
                }
            )
    scenario_summary = pd.DataFrame(scenario_rows)
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
            label=f"{scenario} ({int(SCENARIOS[scenario][0] * 100)}th)",
        )
    axes[1].set_xscale("log")
    axes[1].set_xticks(WINDOWS, [str(window) for window in WINDOWS])
    axes[1].set_xlabel("Accumulation window (h)", fontsize=9)
    axes[1].set_ylabel("Independent-event rainfall quantile (mm)", fontsize=9)
    axes[1].legend(fontsize=7.6, frameon=True, framealpha=0.92, loc="upper left")
    style_chart_axis(axes[1])

    # c: official temporary threshold categories and the seven station supports.
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
    station_support = central_scenarios[
        ["Station ID", "Station Latitude", "Station Longitude"]
    ].drop_duplicates()
    axes[2].scatter(
        station_support["Station Longitude"],
        station_support["Station Latitude"],
        s=30,
        marker="o",
        c="#1565C0",
        edgecolors="white",
        linewidths=0.7,
        zorder=12,
    )
    label_offsets = {
        "Kikuchi": (5, 4),
        "Takamori": (5, -10),
        "Kosa": (5, 4),
        "Matsushima": (-48, 4),
        "Yatsushiro": (5, -10),
        "Misumi": (-35, -10),
        "Kumamoto": (5, 4),
    }
    for row in station_support.itertuples(index=False):
        station_name = STATION_LABELS.get(str(row[0]), str(row[0]))
        axes[2].annotate(
            station_name,
            xy=(float(row[2]), float(row[1])),
            xytext=label_offsets.get(station_name, (5, 4)),
            textcoords="offset points",
            fontsize=7.1,
            color="#173A5E",
            fontweight="bold",
            bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "edgecolor": "none", "alpha": 0.78},
            zorder=13,
        )
    axes[2].legend(
        handles=[
            *[
                Patch(facecolor=color, edgecolor="#667085", label=category)
                for category, color in THRESHOLD_COLORS.items()
            ],
            Line2D(
                [0],
                [0],
                marker="o",
                color="none",
                markerfacecolor="#1565C0",
                markeredgecolor="white",
                markersize=6,
                label="JMA rainfall station",
            ),
        ],
        loc="lower left",
        fontsize=7.6,
        frameon=True,
        framealpha=0.94,
    )
    axes[2].text(
        0.985,
        0.985,
        "Yatsushiro subarea boundary unresolved\n"
        "Downstream municipal analysis: analyst midpoint 0.75\n"
        "Bounding assignments: 0.70 and 0.80",
        transform=axes[2].transAxes,
        ha="right",
        va="top",
        fontsize=7.2,
        color="#344054",
        linespacing=1.25,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "white",
            "edgecolor": "#98A2B3",
            "linewidth": 0.7,
            "alpha": 0.94,
        },
        zorder=20,
    )
    style_map_axis(axes[2], map_bounds)

    # d: temporal-support sensitivity, expressed as a ratio to the common-period median.
    for scenario, (_, color) in SCENARIOS.items():
        central_subset = central_scenarios.loc[
            central_scenarios["Rainfall Scenario"].eq(scenario)
        ]
        sensitivity_subset = sensitivity_scenarios.loc[
            sensitivity_scenarios["Rainfall Scenario"].eq(scenario)
        ]
        ratios = []
        for window in WINDOWS:
            central_median = central_subset[f"Scenario {window} h Rainfall"].median()
            sensitivity_median = sensitivity_subset[f"Scenario {window} h Rainfall"].median()
            ratios.append(100.0 * sensitivity_median / central_median)
        axes[3].plot(
            WINDOWS,
            ratios,
            marker="o",
            markersize=4.2,
            linewidth=2.0,
            color=color,
            label=scenario,
        )
    axes[3].axhline(100.0, color="#344054", linestyle=(0, (4, 3)), linewidth=0.9)
    axes[3].set_xscale("log")
    axes[3].set_xticks(WINDOWS, [str(window) for window in WINDOWS])
    axes[3].set_xlabel("Accumulation window (h)", fontsize=9)
    axes[3].set_ylabel("2016–2025 / 2016–2020 scenario median (%)", fontsize=9)
    axes[3].legend(fontsize=7.8, frameon=True, framealpha=0.92, loc="upper left")
    style_chart_axis(axes[3])

    for label, axis in zip("abcd", axes):
        add_panel_label(axis, label)

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
    print(f"Rainfall stations: {rain['Station ID'].nunique()}")
    print(f"Complete station-years shown: {len(annual)}")
    print(f"Independent-event scenario records: {len(scenario_values)}")
    print("Threshold map categories:")
    print(admin["Threshold Category"].value_counts().to_string())


if __name__ == "__main__":
    main()
