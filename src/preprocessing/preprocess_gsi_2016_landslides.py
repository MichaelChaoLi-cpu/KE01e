#!/usr/bin/env python3
"""Parse the GSI 2016 air-photo-interpreted landslide KML into point Parquet."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pandas as pd
from shapely.geometry import Point


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/raw/official_reference/2016_inventory/gsi_airphoto_interpreted_landslides.zip"
OUTPUT = ROOT / "data/processed/gsi_2016_landslide_inventory_preprocessed.parquet"
KML_NAME = "20160728_houkaichi.kml"
NS = {"kml": "http://www.opengis.net/kml/2.2"}


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
        point = Point(longitude, latitude)
        rows.append(
            {
                "Landslide Inventory ID": f"GSI2016-{len(rows) + 1:05d}",
                "Landslide Size Class": size_class,
                "Observation Date": datetime(2016, 7, 28),
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
