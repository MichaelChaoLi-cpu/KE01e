#!/usr/bin/env python3
"""Audit the first KE01e acquisition batch without creating analysis-ready data."""

from __future__ import annotations

import csv
import json
import math
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

import pandas as pd
import pyarrow.parquet as pq
from shapely import box, from_wkb, union_all


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "data/exp/acquisition-audit"
ADMIN_PATH = ROOT / "data/raw/reused_local/KE01b/administrative_areas/kumamoto_administrative_areas_preprocessed.parquet"
LOCAL_MANIFEST = ROOT / "data/raw/_manifests/local_reference_assets.csv"
OFFICIAL_MANIFEST = ROOT / "data/raw/_manifests/official_reference_sources.csv"
DEM_MANIFEST = ROOT / "data/raw/_manifests/gsi_dem10b_png_tiles.csv"
RAINFALL_MANIFEST = ROOT / "data/raw/_manifests/jma_historical_hourly_rainfall.csv"
LANDSLIDE_ZIP = ROOT / "data/raw/official_reference/2016_inventory/gsi_airphoto_interpreted_landslides.zip"
WARNING_ZIP = ROOT / "data/raw/official_reference/hazard_zones/A33-25_43_GEOJSON.zip"


THRESHOLD_GROUPS = [
    ("70%", 0.70, "宇城市"),
    ("70%", 0.70, "氷川町"),
    ("70%", 0.70, "熊本市"),
    ("70%", 0.70, "八代市西部"),
    ("70%", 0.70, "宇土市"),
    ("70%", 0.70, "美里町"),
    ("70%", 0.70, "益城町"),
    ("70%", 0.70, "合志市"),
    ("70%", 0.70, "大津町"),
    ("70%", 0.70, "西原村"),
    ("70%", 0.70, "御船町"),
    ("70%", 0.70, "上天草市"),
    ("70%", 0.70, "芦北町"),
    ("70%", 0.70, "嘉島町"),
    ("70%", 0.70, "甲佐町"),
    ("80%", 0.80, "八代市東部"),
    ("80%", 0.80, "山鹿市"),
    ("80%", 0.80, "菊池市"),
    ("80%", 0.80, "菊陽町"),
    ("80%", 0.80, "水俣市"),
    ("80%", 0.80, "天草市"),
    ("80%", 0.80, "津奈木町"),
]


def tile_bounds(zoom: int, x: int, y: int):
    scale = 2**zoom
    west = x / scale * 360.0 - 180.0
    east = (x + 1) / scale * 360.0 - 180.0

    def latitude(row: int) -> float:
        return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * row / scale))))

    north = latitude(y)
    south = latitude(y + 1)
    return box(west, south, east, north)


def admin_geometry():
    table = pq.read_table(ADMIN_PATH, columns=["Geometry"])
    return union_all(from_wkb(table["Geometry"].to_pylist()))


def audit_dem(prefecture) -> dict[str, int | float]:
    rows = list(csv.DictReader(DEM_MANIFEST.open(encoding="utf-8")))
    failed_inside = []
    valid_tiles = []
    for row in rows:
        geometry = tile_bounds(int(row["zoom"]), int(row["x"]), int(row["y"]))
        if row["status"] == "failed":
            overlap = geometry.intersection(prefecture).area
            if overlap > 0:
                failed_inside.append((row, overlap))
        else:
            valid_tiles.append(geometry)
    valid_coverage = union_all(valid_tiles)
    uncovered = prefecture.difference(valid_coverage)
    uncovered_pct = 100.0 * uncovered.area / prefecture.area
    return {
        "scheduled_tiles": len(rows),
        "available_tiles": sum(row["status"] != "failed" for row in rows),
        "failed_tiles": sum(row["status"] == "failed" for row in rows),
        "failed_tiles_intersecting_prefecture": len(failed_inside),
        "prefecture_area_uncovered_pct_degree_area": uncovered_pct,
        "bytes": sum(int(row["bytes"]) for row in rows),
    }


def audit_2016_inventory() -> dict[str, object]:
    namespace = {"kml": "http://www.opengis.net/kml/2.2"}
    with zipfile.ZipFile(LANDSLIDE_ZIP) as archive:
        payload = archive.read("20160728_houkaichi.kml")
    root = ElementTree.fromstring(payload)
    placemarks = root.findall(".//kml:Placemark", namespace)
    coordinates = []
    for node in root.findall(".//kml:Point/kml:coordinates", namespace):
        if node.text:
            parts = node.text.strip().split(",")
            coordinates.append((float(parts[0]), float(parts[1])))
    bounds = None
    if coordinates:
        bounds = [
            min(point[0] for point in coordinates),
            min(point[1] for point in coordinates),
            max(point[0] for point in coordinates),
            max(point[1] for point in coordinates),
        ]
    return {"placemarks": len(placemarks), "point_coordinates": len(coordinates), "bounds": bounds}


def audit_warning_zones() -> dict[str, object]:
    with zipfile.ZipFile(WARNING_ZIP) as archive:
        name = next(name for name in archive.namelist() if name.endswith("Polygon.geojson"))
        collection = json.loads(archive.read(name))
    features = collection["features"]
    hazard_codes = Counter(str(feature["properties"].get("A33_001")) for feature in features)
    zone_codes = Counter(str(feature["properties"].get("A33_002")) for feature in features)
    return {"features": len(features), "hazard_codes": dict(hazard_codes), "zone_codes": dict(zone_codes)}


def local_inventory() -> list[dict[str, object]]:
    manifest = pd.read_csv(LOCAL_MANIFEST)
    rows = []
    for asset_id, group in manifest.groupby("asset_id", sort=True):
        parquet_paths = [ROOT / path for path in group["destination_path"] if str(path).endswith(".parquet")]
        record_count = sum(pq.ParquetFile(path).metadata.num_rows for path in parquet_paths)
        rows.append(
            {
                "asset_id": asset_id,
                "files": len(group),
                "bytes": int(group["bytes"].sum()),
                "parquet_rows": record_count if parquet_paths else "",
                "source_projects": ";".join(sorted(group["source_project"].unique())),
            }
        )
    return rows


def road_restriction_summary() -> dict[str, object]:
    path = ROOT / "data/raw/reused_local/KE01d/road_restrictions/road_restrictions_preprocessed.parquet"
    data = pd.read_parquet(path)
    reasons = data["Restriction Reason"].value_counts(dropna=False)
    return {
        "snapshot_rows": len(data),
        "kumamoto_rows": int(data["Prefecture Name"].eq("熊本県").sum()),
        "rockfall_rows": int(reasons.get("落石", 0)),
        "slope_collapse_rows": int(reasons.get("法面崩落", 0)),
        "sediment_inflow_rows": int(reasons.get("土砂流入", 0)),
        "snapshot_count": int(data["Snapshot Time"].nunique()),
    }


def rainfall_summary() -> tuple[dict[str, object], list[dict[str, object]]]:
    core_stations = {"kumamoto", "kosa", "matsushima", "yatsushiro", "misumi"}
    manifest = pd.read_csv(RAINFALL_MANIFEST)
    manifest = manifest.loc[manifest["station_slug"].isin(core_stations) & manifest["status"].ne("failed")]
    station_rows = []
    all_frames = []
    for station_slug, group in manifest.groupby("station_slug", sort=True):
        frames = []
        for relative_path in group.sort_values("start_date")["destination_path"]:
            frame = pd.read_csv(
                ROOT / relative_path,
                encoding="cp932",
                skiprows=6,
                header=None,
            )
            if frame.shape[1] == 5:
                frame.columns = ["time", "rainfall_mm", "no_phenomenon", "quality", "homogeneity"]
            elif frame.shape[1] == 4:
                frame.columns = ["time", "rainfall_mm", "quality", "homogeneity"]
                frame["no_phenomenon"] = pd.NA
            else:
                raise ValueError(f"Unexpected JMA CSV width {frame.shape[1]}: {relative_path}")
            frames.append(frame)
        data = pd.concat(frames, ignore_index=True)
        data["time"] = pd.to_datetime(data["time"], errors="coerce")
        data["rainfall_mm"] = pd.to_numeric(data["rainfall_mm"], errors="coerce")
        data["quality"] = pd.to_numeric(data["quality"], errors="coerce")
        data = data.drop_duplicates("time").sort_values("time")
        series = data.set_index("time")["rainfall_mm"]
        wet = series.loc[series.gt(0)]
        station_rows.append(
            {
                "station_slug": station_slug,
                "station_name_ja": group["station_name_ja"].iloc[0],
                "start_time": data["time"].min().isoformat(),
                "end_time": data["time"].max().isoformat(),
                "hourly_rows": len(data),
                "missing_rainfall_pct": 100.0 * series.isna().mean(),
                "normal_quality_pct": 100.0 * data["quality"].eq(8).mean(),
                "wet_hours": int(wet.count()),
                "wet_hour_p90_mm": wet.quantile(0.90),
                "wet_hour_p95_mm": wet.quantile(0.95),
                "wet_hour_p99_mm": wet.quantile(0.99),
                "maximum_1h_mm": series.max(),
                "maximum_3h_mm": series.rolling(3, min_periods=3).sum().max(),
                "maximum_24h_mm": series.rolling(24, min_periods=24).sum().max(),
                "maximum_72h_mm": series.rolling(72, min_periods=72).sum().max(),
            }
        )
        data["station_slug"] = station_slug
        all_frames.append(data)
    combined = pd.concat(all_frames, ignore_index=True)
    return (
        {
            "stations": len(station_rows),
            "hourly_rows": len(combined),
            "start_time": combined["time"].min().isoformat(),
            "end_time": combined["time"].max().isoformat(),
            "missing_rainfall_pct": 100.0 * combined["rainfall_mm"].isna().mean(),
        },
        station_rows,
    )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    prefecture = admin_geometry()
    dem = audit_dem(prefecture)
    inventory_2016 = audit_2016_inventory()
    warning = audit_warning_zones()
    restrictions = road_restriction_summary()
    rainfall, rainfall_rows = rainfall_summary()
    local_rows = local_inventory()
    write_csv(OUTPUT / "local_asset_inventory.csv", local_rows)
    write_csv(OUTPUT / "historical_rainfall_coverage.csv", rainfall_rows)
    threshold_rows = [
        {
            "temporary_threshold_group": group,
            "baseline_fraction": fraction,
            "municipality_or_subarea": municipality,
            "source": "MLIT/JMA press release 2026-07-28",
        }
        for group, fraction, municipality in THRESHOLD_GROUPS
    ]
    write_csv(OUTPUT / "official_threshold_factors.csv", threshold_rows)

    official = pd.read_csv(OFFICIAL_MANIFEST)
    lines = [
        "# Acquisition audit",
        "",
        "## Acquisition outcome",
        "",
        f"- Local reusable assets: {len(local_rows)} asset groups and {sum(int(row['files']) for row in local_rows)} files.",
        f"- Official static sources: {len(official)} sources; {(official['status'] != 'failed').sum()} available and {(official['status'] == 'failed').sum()} failed.",
        f"- GSI DEM10B: {dem['available_tiles']:,} available tiles ({dem['bytes'] / 1024**2:.1f} MiB) from {dem['scheduled_tiles']:,} scheduled tiles.",
        f"- DEM 404 tiles intersecting the prefecture geometry: {dem['failed_tiles_intersecting_prefecture']}; approximate uncovered prefecture area: {dem['prefecture_area_uncovered_pct_degree_area']:.6f}%.",
        f"- JMA historical rainfall: {rainfall['hourly_rows']:,} hourly rows for {rainfall['stations']} core stations from {rainfall['start_time']} through {rainfall['end_time']}; rainfall missingness is {rainfall['missing_rainfall_pct']:.4f}%.",
        "",
        "## Newly operational evidence",
        "",
        f"- The 2016 GSI KML contains {inventory_2016['placemarks']:,} placemarks and {inventory_2016['point_coordinates']:,} point coordinates; its point bounds are {inventory_2016['bounds']}.",
        f"- The official 2025 MLIT warning-zone GeoJSON contains {warning['features']:,} polygon features.",
        "- The 2026 MLIT/JMA temporary rule sets warning thresholds to 70% of baseline in 15 Kumamoto municipalities/subareas and 80% in 7. These are official operational factors, not estimated landslide probabilities.",
        f"- The road-restriction source contains {restrictions['snapshot_rows']:,} snapshot rows across {restrictions['snapshot_count']} snapshots, including {restrictions['kumamoto_rows']:,} Kumamoto rows, {restrictions['rockfall_rows']} rockfall rows, {restrictions['slope_collapse_rows']} slope-collapse rows, and {restrictions['sediment_inflow_rows']} sediment-inflow rows. These counts include repeated snapshots and require event deduplication.",
        "",
        "## Feasibility after acquisition",
        "",
        "The minimum scenario study is now operational in principle: terrain, ten years of hourly rainfall for five core stations, official threshold-reduction factors, road topology, warning zones, population, services, and observed road-disruption snapshots are present. RQ3-RQ5 can proceed after preprocessing and linkage validation.",
        "",
        "RQ2 remains probability-limited. The 2016 GSI inventory is an air-photo-interpreted point inventory with known coverage and completeness limits, while no complete 2026 landslide inventory has been acquired. The first model must therefore use official 70%/80% threshold-adjustment scenarios and report disruption scores unless later inventory auditing supports calibrated probability estimation.",
        "",
        "## Remaining high-priority gaps",
        "",
        "1. Gridded analysed precipitation remains desirable for within-prefecture rainfall surfaces; the five-station history is sufficient for temporal scenario calibration but not a 1 km event field.",
        "2. A spatial shaking measure finer than municipality-level intensity if PGA/PGV interaction estimation is attempted.",
        "3. A cause-classified, deduplicated 2026 landslide and road-closure inventory.",
        "4. Land cover, geology, and soil covariates for the stronger model; these do not block the first scenario version.",
        "",
        "## Interpretation limits",
        "",
        "- DEM tiles are web-tile representations of GSI DEM10B and must be decoded and mosaicked with the published encoding rule before terrain derivation.",
        "- The official 70%/80% factors apply to warning criteria; they support scenario adjustment but do not equal a cell-level landslide probability multiplier.",
        "- Repeated road-restriction rows are observations over time, not independent failures.",
        "- The 2016 inventory combines several mass-movement types and maps event centres rather than exact polygons.",
    ]
    (OUTPUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"dem": dem, "rainfall": rainfall, "inventory_2016": inventory_2016, "warning_zones": warning, "road_restrictions": restrictions}, ensure_ascii=False, indent=2))
    print(f"Report: {(OUTPUT / 'README.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
