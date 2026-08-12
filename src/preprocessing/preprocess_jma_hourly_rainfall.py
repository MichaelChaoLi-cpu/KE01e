#!/usr/bin/env python3
"""Combine JMA CP932 hourly-rainfall chunks without spatial interpolation."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data/raw/_manifests/jma_historical_hourly_rainfall.csv"
STATION_METADATA = (
    ROOT
    / "data/raw/reused_local/KE01/jma_amedas_station_metadata/amedastable_2026-08-02.json"
)
OUTPUT = ROOT / "data/processed/jma_hourly_rainfall_preprocessed.parquet"
EVENT_OUTPUT = ROOT / "data/processed/jma_rainfall_event_maxima_preprocessed.parquet"
SCENARIO_OUTPUT = ROOT / "data/processed/jma_rainfall_scenario_quantiles_preprocessed.parquet"

WINDOWS = (1, 3, 24, 72)
SCENARIOS = (("Moderate", 0.75), ("Heavy", 0.90), ("Extreme", 0.99))
SUPPORTS = (
    ("Central: 7 stations, 2016-2020", None, 2016, 2020),
    (
        "Sensitivity: 5 stations, 2016-2025",
        {"kosa", "kumamoto", "matsushima", "misumi", "yatsushiro"},
        2016,
        2025,
    ),
)


def read_chunk(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, encoding="cp932", skiprows=6, header=None, low_memory=False)
    if frame.shape[1] == 5:
        frame.columns = [
            "observation_time",
            "hourly_rainfall_mm",
            "no_phenomenon_flag",
            "quality_flag",
            "homogeneity_number",
        ]
    elif frame.shape[1] == 4:
        frame.columns = [
            "observation_time",
            "hourly_rainfall_mm",
            "quality_flag",
            "homogeneity_number",
        ]
        frame["no_phenomenon_flag"] = pd.NA
    else:
        raise ValueError(f"Unexpected JMA column count {frame.shape[1]} in {path}")
    return frame


def decimal_degrees(parts: list[float]) -> float:
    """Convert JMA [degrees, decimal minutes] coordinates to decimal degrees."""
    return float(parts[0]) + float(parts[1]) / 60.0


def station_coordinates() -> dict[str, tuple[float, float]]:
    metadata = json.loads(STATION_METADATA.read_text(encoding="utf-8"))
    coordinates: dict[str, tuple[float, float]] = {}
    for record in metadata.values():
        name = str(record.get("kjName", ""))
        latitude = record.get("lat")
        longitude = record.get("lon")
        if name and latitude and longitude:
            coordinates[name] = (decimal_degrees(latitude), decimal_degrees(longitude))
    return coordinates


def event_maxima_for_support(
    data: pd.DataFrame,
    support_name: str,
    station_slugs: set[str] | None,
    start_year: int,
    end_year: int,
) -> pd.DataFrame:
    selected = data[data["Observation Time"].dt.year.between(start_year, end_year)].copy()
    if station_slugs is not None:
        selected = selected[selected["Station Slug"].isin(station_slugs)].copy()

    rows: list[dict[str, object]] = []
    for station_slug, frame in selected.groupby("Station Slug", sort=True):
        frame = frame.sort_values("Observation Time").drop_duplicates("Observation Time", keep="last")
        index = pd.date_range(
            frame["Observation Time"].min().floor("h"),
            frame["Observation Time"].max().floor("h"),
            freq="h",
        )
        hourly = frame.set_index("Observation Time")["Hourly Rainfall"].reindex(index)
        quality = frame.set_index("Observation Time")["Quality Flag"].reindex(index)
        analysis_rainfall = hourly.where(quality.eq(8))
        wet_positions = np.flatnonzero(
            analysis_rainfall.notna().to_numpy() & analysis_rainfall.fillna(0).gt(0).to_numpy()
        )
        if wet_positions.size == 0:
            continue

        event_ids = np.full(len(index), -1, dtype=int)
        event_id = 0
        previous = int(wet_positions[0])
        event_ids[previous] = event_id
        for position_value in wet_positions[1:]:
            position = int(position_value)
            gap = analysis_rainfall.iloc[previous + 1 : position]
            missing_break = gap.isna().any()
            dry_break = len(gap) >= 24 and gap.eq(0).all()
            if missing_break or dry_break:
                event_id += 1
            event_ids[position] = event_id
            previous = position

        rolling = {
            window: analysis_rainfall.rolling(window, min_periods=window).sum()
            for window in WINDOWS
        }
        station_info = frame.iloc[0]
        for current_event in range(event_id + 1):
            positions = np.flatnonzero(event_ids == current_event)
            if positions.size == 0:
                continue
            event_row: dict[str, object] = {
                "Support Specification": support_name,
                "Station Slug": station_slug,
                "Station ID": station_info["Station ID"],
                "Station Name (Japanese)": station_info["Station Name (Japanese)"],
                "Station Latitude": station_info["Station Latitude"],
                "Station Longitude": station_info["Station Longitude"],
                "Rainfall Event ID": f"{station_slug}-{start_year}-{end_year}-{current_event + 1:04d}",
                "Event Start": index[int(positions.min())],
                "Event End": index[int(positions.max())],
                "Event Wet Hour Count": int(positions.size),
            }
            for window in WINDOWS:
                values = rolling[window].iloc[positions].dropna()
                event_row[f"Event Maximum {window} h Rainfall"] = (
                    float(values.max()) if not values.empty else np.nan
                )
            rows.append(event_row)
    return pd.DataFrame(rows)


def scenario_quantiles(events: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    group_columns = [
        "Support Specification",
        "Station Slug",
        "Station ID",
        "Station Name (Japanese)",
        "Station Latitude",
        "Station Longitude",
    ]
    for keys, frame in events.groupby(group_columns, sort=True, dropna=False):
        base = dict(zip(group_columns, keys, strict=True))
        for scenario, quantile in SCENARIOS:
            row = {
                **base,
                "Rainfall Scenario": scenario,
                "Event Quantile": quantile,
                "Rainfall Event Count": int(len(frame)),
            }
            for window in WINDOWS:
                column = f"Event Maximum {window} h Rainfall"
                row[f"Scenario {window} h Rainfall"] = float(frame[column].quantile(quantile))
            rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    manifest = pd.read_csv(MANIFEST, dtype={"station_id": "string"})
    # Include both the five full-period core stations and explicitly marked
    # supplementary mountain/northern stations.
    usable = manifest["status"].astype("string").str.startswith(("existing", "downloaded"), na=False)
    manifest = manifest[usable].copy()
    chunks: list[pd.DataFrame] = []
    for row in manifest.itertuples(index=False):
        path = ROOT / str(row.destination_path)
        frame = read_chunk(path)
        frame.insert(0, "station_name_ja", str(row.station_name_ja))
        frame.insert(0, "station_id", str(row.station_id))
        frame.insert(0, "station_slug", str(row.station_slug))
        chunks.append(frame)

    data = pd.concat(chunks, ignore_index=True)
    data["observation_time"] = pd.to_datetime(data["observation_time"], errors="coerce").dt.tz_localize(
        "Asia/Tokyo", ambiguous="NaT", nonexistent="shift_forward"
    )
    data["hourly_rainfall_mm"] = pd.to_numeric(data["hourly_rainfall_mm"], errors="coerce")
    for column in ["no_phenomenon_flag", "quality_flag", "homogeneity_number"]:
        data[column] = pd.to_numeric(data[column], errors="coerce").astype("Int64")

    data = data.rename(
        columns={
            "station_slug": "Station Slug",
            "station_id": "Station ID",
            "station_name_ja": "Station Name (Japanese)",
            "observation_time": "Observation Time",
            "hourly_rainfall_mm": "Hourly Rainfall",
            "no_phenomenon_flag": "No-Phenomenon Flag",
            "quality_flag": "Quality Flag",
            "homogeneity_number": "Homogeneity Number",
        }
    )
    coordinates = station_coordinates()
    data["Station Latitude"] = data["Station Name (Japanese)"].map(
        lambda name: coordinates.get(str(name), (np.nan, np.nan))[0]
    )
    data["Station Longitude"] = data["Station Name (Japanese)"].map(
        lambda name: coordinates.get(str(name), (np.nan, np.nan))[1]
    )
    if data[["Station Latitude", "Station Longitude"]].isna().any(axis=None):
        missing_names = sorted(
            data.loc[
                data[["Station Latitude", "Station Longitude"]].isna().any(axis=1),
                "Station Name (Japanese)",
            ].unique()
        )
        raise ValueError(f"Missing JMA station coordinates for: {missing_names}")
    data = data.sort_values(["Station ID", "Observation Time"], kind="stable")
    data = data.drop_duplicates(["Station ID", "Observation Time"], keep="last").reset_index(drop=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_parquet(OUTPUT, index=False)
    event_frames = [
        event_maxima_for_support(data, support_name, station_slugs, start_year, end_year)
        for support_name, station_slugs, start_year, end_year in SUPPORTS
    ]
    events = pd.concat(event_frames, ignore_index=True)
    events.to_parquet(EVENT_OUTPUT, index=False)
    scenarios = scenario_quantiles(events)
    scenarios.to_parquet(SCENARIO_OUTPUT, index=False)
    print(
        f"Saved {len(data):,} station-hour rows x {len(data.columns)} cols -> "
        f"{OUTPUT.relative_to(ROOT)}"
    )
    print(f"Saved {len(events):,} station-event rows -> {EVENT_OUTPUT.relative_to(ROOT)}")
    print(f"Saved {len(scenarios):,} station-scenario rows -> {SCENARIO_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
