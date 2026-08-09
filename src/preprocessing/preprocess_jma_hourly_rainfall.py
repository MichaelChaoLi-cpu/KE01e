#!/usr/bin/env python3
"""Combine JMA CP932 hourly-rainfall chunks without spatial interpolation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data/raw/_manifests/jma_historical_hourly_rainfall.csv"
OUTPUT = ROOT / "data/processed/jma_hourly_rainfall_preprocessed.parquet"


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
    data = data.sort_values(["Station ID", "Observation Time"], kind="stable")
    data = data.drop_duplicates(["Station ID", "Observation Time"], keep="last").reset_index(drop=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_parquet(OUTPUT, index=False)
    print(
        f"Saved {len(data):,} station-hour rows x {len(data.columns)} cols -> "
        f"{OUTPUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
