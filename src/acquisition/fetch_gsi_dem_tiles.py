#!/usr/bin/env python3
"""Fetch GSI DEM10B text tiles covering the Kumamoto Prefecture bounding box."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BBOX = (129.938762776, 32.094920198, 131.329504877, 33.195175486)
USER_AGENT = "KE01e-earthquake-rainfall-landslide-research/1.0"


def lon_to_x(lon: float, zoom: int) -> int:
    return int((lon + 180.0) / 360.0 * (2**zoom))


def lat_to_y(lat: float, zoom: int) -> int:
    latitude = math.radians(lat)
    return int((1.0 - math.asinh(math.tan(latitude)) / math.pi) / 2.0 * (2**zoom))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tile_jobs(bbox: tuple[float, float, float, float], zoom: int) -> list[tuple[int, int, int]]:
    west, south, east, north = bbox
    x_min, x_max = lon_to_x(west, zoom), lon_to_x(east, zoom)
    y_min, y_max = lat_to_y(north, zoom), lat_to_y(south, zoom)
    return [(zoom, x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1)]


def fetch_tile(job: tuple[int, int, int], tile_format: str) -> dict[str, str | int]:
    zoom, x, y = job
    layer = "dem_png" if tile_format == "png" else "dem"
    extension = "png" if tile_format == "png" else "txt"
    output_root = ROOT / "data/raw/gsi_dem" / ("dem10b_png" if tile_format == "png" else "dem10b_text")
    url = f"https://cyberjapandata.gsi.go.jp/xyz/{layer}/{zoom}/{x}/{y}.{extension}"
    destination = output_root / str(zoom) / str(x) / f"{y}.{extension}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size > 0:
        return {
            "zoom": zoom,
            "x": x,
            "y": y,
            "url": url,
            "destination_path": str(destination.relative_to(ROOT)),
            "bytes": destination.stat().st_size,
            "sha256": sha256(destination),
            "status": "existing",
            "error": "",
        }
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
        if not payload:
            raise OSError("empty response")
        if tile_format == "png" and not payload.startswith(b"\x89PNG\r\n\x1a\n"):
            raise OSError("response is not a PNG file")
        temporary = destination.with_suffix(destination.suffix + ".part")
        temporary.write_bytes(payload)
        temporary.replace(destination)
        return {
            "zoom": zoom,
            "x": x,
            "y": y,
            "url": url,
            "destination_path": str(destination.relative_to(ROOT)),
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "status": "downloaded",
            "error": "",
        }
    except (OSError, urllib.error.URLError) as exc:
        return {
            "zoom": zoom,
            "x": x,
            "y": y,
            "url": url,
            "destination_path": str(destination.relative_to(ROOT)),
            "bytes": 0,
            "sha256": "",
            "status": "failed",
            "error": str(exc),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zoom", type=int, default=14)
    parser.add_argument("--bbox", nargs=4, type=float, metavar=("W", "S", "E", "N"), default=DEFAULT_BBOX)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit", type=int, help="Download only the first N tiles for a connectivity pilot")
    parser.add_argument("--format", choices=("png", "txt"), default="png")
    args = parser.parse_args()
    bbox = tuple(args.bbox)
    jobs = tile_jobs(bbox, args.zoom)
    if args.limit:
        jobs = jobs[: args.limit]
    print(f"Tiles scheduled: {len(jobs)} at zoom {args.zoom}; bbox={bbox}")

    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(fetch_tile, job, args.format) for job in jobs]
        for completed, future in enumerate(as_completed(futures), start=1):
            rows.append(future.result())
            if completed % 250 == 0 or completed == len(futures):
                print(f"Completed {completed}/{len(futures)}")

    retrieved_at = datetime.now(timezone.utc).isoformat()
    for row in rows:
        row["retrieved_at_utc"] = retrieved_at
    rows.sort(key=lambda row: (int(row["zoom"]), int(row["x"]), int(row["y"])))
    manifest_path = ROOT / "data/raw/_manifests" / f"gsi_dem10b_{args.format}_tiles.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    headers = ["zoom", "x", "y", "url", "destination_path", "bytes", "sha256", "status", "error", "retrieved_at_utc"]
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    counts = {status: sum(row["status"] == status for row in rows) for status in {str(row["status"]) for row in rows}}
    print(f"Status: {counts}")
    print(f"Manifest: {manifest_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
