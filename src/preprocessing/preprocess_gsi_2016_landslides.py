#!/usr/bin/env python3
"""Parse the GSI 2016 air-photo-interpreted landslide KML into point Parquet."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pandas as pd
from shapely.geometry import Point


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/raw/official_reference/2016_inventory/gsi_airphoto_interpreted_landslides.zip"
OUTPUT = ROOT / "data/processed/gsi_2016_landslide_inventory_preprocessed.parquet"
KML_NAME = "20160728_houkaichi.kml"
NS = {"kml": "http://www.opengis.net/kml/2.2"}
INVENTORY_UPDATE_DATE = datetime(2016, 7, 28)


def source_photo_dates(description: str) -> tuple[str, datetime, datetime]:
    """Parse the official air-photo acquisition label and date interval."""
    match = re.search(
        r"(\d{4})/(\d{1,2})/(\d{1,2})(?:[～～-](?:(\d{1,2})/)?(\d{1,2}))?",
        description,
    )
    if match is None:
        raise ValueError(f"Unresolved GSI source-photo date: {description!r}")
    year, month, day = (int(match.group(index)) for index in (1, 2, 3))
    end_month = int(match.group(4)) if match.group(4) else month
    end_day = int(match.group(5)) if match.group(5) else day
    start = datetime(year, month, day)
    end = datetime(year, end_month, end_day)
    label = f"{start:%Y-%m-%d}" if start == end else f"{start:%Y-%m-%d} to {end:%Y-%m-%d}"
    return label, start, end


def main() -> None:
    with ZipFile(SOURCE) as archive:
        root = ET.fromstring(archive.read(KML_NAME))

    rows: list[dict[str, object]] = []
    for placemark in root.findall(".//kml:Placemark", NS):
        coordinates = placemark.findtext(".//kml:Point/kml:coordinates", default="", namespaces=NS).strip()
        if not coordinates:
            continue
        longitude, latitude, *_ = [float(value) for value in coordinates.split(",")]
        size_class = placemark.findtext("kml:name", default="", namespaces=NS).strip()
        description = placemark.findtext(
            "kml:description", default="", namespaces=NS
        ).strip()
        photo_label, photo_start, photo_end = source_photo_dates(description)
        point = Point(longitude, latitude)
        rows.append(
            {
                "Landslide Inventory ID": f"GSI2016-{len(rows) + 1:05d}",
                "Landslide Size Class": size_class,
                "Source Photo Date Label": photo_label,
                "Source Photo Start Date": photo_start,
                "Source Photo End Date": photo_end,
                "Inventory Update Date": INVENTORY_UPDATE_DATE,
                "Longitude": longitude,
                "Latitude": latitude,
                "Geometry": point.wkb,
                "Source File": KML_NAME,
            }
        )

    data = pd.DataFrame(rows)
    if data.empty:
        raise ValueError("No point placemarks parsed from the 2016 GSI inventory")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_parquet(OUTPUT, index=False)
    print(f"Saved {len(data):,} landslide points x {len(data.columns)} cols -> {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
