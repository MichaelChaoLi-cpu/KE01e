#!/usr/bin/env python3
"""Decode GSI DEM10B PNG tiles into a georeferenced raster and tile QA table."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

# Prevent unrelated Anaconda PROJ/GDAL settings inherited from the shell from
# overriding the self-contained databases bundled with this project's Rasterio.
os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)
os.environ.pop("GDAL_DATA", None)

import rasterio
from PIL import Image
from rasterio.enums import Resampling
from rasterio.transform import Affine


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data/raw/_manifests/gsi_dem10b_png_tiles.csv"
RASTER_OUT = ROOT / "data/processed/gsi_dem10b_elevation_preprocessed.tif"
SUMMARY_OUT = ROOT / "data/processed/gsi_dem10b_tile_summary_preprocessed.parquet"
NODATA = np.float32(-9999.0)
WEB_MERCATOR_HALF_WORLD = 20037508.342789244


def decode_elevation(path: Path) -> np.ndarray:
    rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.int32)
    encoded = rgb[:, :, 0] * 65536 + rgb[:, :, 1] * 256 + rgb[:, :, 2]
    elevation = np.where(encoded < 2**23, encoded, encoded - 2**24).astype(np.float32) * 0.01
    elevation[encoded == 2**23] = NODATA
    return elevation


def main() -> None:
    manifest = pd.read_csv(MANIFEST)
    zooms = manifest["zoom"].dropna().astype(int).unique()
    if len(zooms) != 1:
        raise ValueError(f"Expected one zoom level, found {zooms.tolist()}")
    zoom = int(zooms[0])
    min_x, max_x = int(manifest["x"].min()), int(manifest["x"].max())
    min_y, max_y = int(manifest["y"].min()), int(manifest["y"].max())
    resolution = (2 * WEB_MERCATOR_HALF_WORLD) / (256 * 2**zoom)
    width = (max_x - min_x + 1) * 256
    height = (max_y - min_y + 1) * 256
    left = -WEB_MERCATOR_HALF_WORLD + min_x * 256 * resolution
    top = WEB_MERCATOR_HALF_WORLD - min_y * 256 * resolution
    transform = Affine(resolution, 0.0, left, 0.0, -resolution, top)

    RASTER_OUT.parent.mkdir(parents=True, exist_ok=True)
    profile = {
        "driver": "GTiff",
        "width": width,
        "height": height,
        "count": 1,
        "dtype": "float32",
        "crs": "EPSG:3857",
        "transform": transform,
        "nodata": float(NODATA),
        "tiled": True,
        "blockxsize": 256,
        "blockysize": 256,
        "compress": "deflate",
        "predictor": 3,
        "BIGTIFF": "YES",
        "SPARSE_OK": "TRUE",
    }

    summaries: list[dict[str, object]] = []
    with rasterio.open(RASTER_OUT, "w", **profile) as dst:
        dst.update_tags(
            source="Geospatial Information Authority of Japan DEM10B elevation tiles",
            source_manifest=str(MANIFEST.relative_to(ROOT)),
            elevation_unit="metre",
            effective_pixel_size_note="Web Mercator pixel size; ground spacing varies with latitude",
        )
        for row in manifest.itertuples(index=False):
            tile_x, tile_y = int(row.x), int(row.y)
            window = rasterio.windows.Window(
                (tile_x - min_x) * 256,
                (tile_y - min_y) * 256,
                256,
                256,
            )
            source_path = ROOT / str(row.destination_path)
            available = str(row.status) in {"existing", "downloaded"} and source_path.exists()
            if available:
                elevation = decode_elevation(source_path)
            else:
                elevation = np.full((256, 256), NODATA, dtype=np.float32)
            dst.write(elevation, 1, window=window)

            valid = elevation != NODATA
            values = elevation[valid]
            summaries.append(
                {
                    "Tile X": tile_x,
                    "Tile Y": tile_y,
                    "Status": "available" if available else "missing",
                    "Valid Pixel Count": int(valid.sum()),
                    "Elevation Minimum (m)": float(values.min()) if values.size else np.nan,
                    "Elevation Mean (m)": float(values.mean()) if values.size else np.nan,
                    "Elevation Maximum (m)": float(values.max()) if values.size else np.nan,
                    "Raster Path": str(RASTER_OUT.relative_to(ROOT)),
                }
            )

        factors = [2, 4, 8, 16, 32]
        dst.build_overviews(factors, Resampling.average)
        dst.update_tags(ns="rio_overview", resampling="average")

    summary = pd.DataFrame(summaries).sort_values(["Tile Y", "Tile X"]).reset_index(drop=True)
    summary.to_parquet(SUMMARY_OUT, index=False)
    print(
        f"Saved elevation raster {width:,} x {height:,} -> {RASTER_OUT.relative_to(ROOT)}; "
        f"tile QA {len(summary):,} rows -> {SUMMARY_OUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
