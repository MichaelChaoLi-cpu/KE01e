#!/usr/bin/env python3
"""Download immutable official reference sources for the KE01e hazard study."""

from __future__ import annotations

import csv
import hashlib
import shutil
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT / "data/raw/official_reference"
MANIFEST_PATH = ROOT / "data/raw/_manifests/official_reference_sources.csv"
USER_AGENT = "KE01e-earthquake-rainfall-landslide-research/1.0"

SOURCES = [
    {
        "dataset_id": "mlit-2026-temporary-landslide-warning-thresholds",
        "organization": "MLIT and JMA",
        "url": "https://www.mlit.go.jp/report/press/content/002014050.pdf",
        "relative_path": "2026_event/mlit_jma_temporary_landslide_warning_thresholds_20260728.pdf",
        "role": "Official municipality-level 70% and 80% post-earthquake warning-threshold factors",
    },
    {
        "dataset_id": "mlit-2026-earthquake-damage-report-26",
        "organization": "MLIT",
        "url": "https://www.mlit.go.jp/common/002015347.pdf",
        "relative_path": "2026_event/mlit_damage_report_26_20260804_1330.pdf",
        "role": "Intensity by municipality, road damage, rockfall, slope failure, and isolation status",
    },
    {
        "dataset_id": "gsi-2026-two-and-a-half-dimensional-displacement",
        "organization": "GSI",
        "url": "https://www.gsi.go.jp/common/000279833.pdf",
        "relative_path": "2026_event/gsi_2p5d_displacement_20260731.pdf",
        "role": "Event ground-displacement context; not a shaking probability surface",
    },
    {
        "dataset_id": "gsi-2026-earthquake-sar-page",
        "organization": "GSI",
        "url": "https://www.gsi.go.jp/uchusokuchi/20260728kumamoto.html",
        "relative_path": "2026_event/gsi_sar_event_page_20260809.html",
        "role": "Versioned official SAR interpretation page",
    },
    {
        "dataset_id": "jma-2026-earthquake-early-warning-page",
        "organization": "JMA",
        "url": "https://ds.data.jma.go.jp/eew/data/nc/fc_hist/2026/07/20260728162718/index.html",
        "relative_path": "2026_event/jma_eew_20260728162718.html",
        "role": "Official event time, epicentre, magnitude, and maximum intensity",
    },
    {
        "dataset_id": "gsi-2016-airphoto-interpreted-landslides",
        "organization": "GSI",
        "url": "https://www.gsi.go.jp/common/000143456.zip",
        "relative_path": "2016_inventory/gsi_airphoto_interpreted_landslides.zip",
        "role": "2016 air-photo-interpreted landslide points for calibration screening",
    },
    {
        "dataset_id": "mlit-2025-kumamoto-landslide-warning-zones",
        "organization": "MLIT National Land Numerical Information",
        "url": "https://nlftp.mlit.go.jp/ksj/gml/data/A33/A33-25/A33-25_43_GEOJSON.zip",
        "relative_path": "hazard_zones/A33-25_43_GEOJSON.zip",
        "role": "Official 2025 landslide warning and special-warning zones",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    context = ssl.create_default_context()
    legacy_connect = getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0)
    context.options |= legacy_connect
    with urllib.request.urlopen(request, timeout=120, context=context) as response, temporary.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    temporary.replace(destination)
    return sha256(destination)


def main() -> None:
    retrieved_at = datetime.now(timezone.utc).isoformat()
    rows = []
    for source in SOURCES:
        destination = OUTPUT_ROOT / source["relative_path"]
        error = ""
        try:
            status = "downloaded"
            if destination.exists() and destination.stat().st_size > 0:
                status = "existing"
                digest = sha256(destination)
            else:
                digest = download(source["url"], destination)
            file_bytes = destination.stat().st_size
        except Exception as exc:  # noqa: BLE001
            status = "failed"
            digest = ""
            file_bytes = 0
            error = str(exc)
        rows.append(
            {
                **source,
                "destination_path": str(destination.relative_to(ROOT)),
                "bytes": file_bytes,
                "sha256": digest,
                "status": status,
                "error": error,
                "retrieved_at_utc": retrieved_at,
            }
        )
        print(f"{status}: {source['dataset_id']} ({file_bytes:,} bytes){': ' + error if error else ''}")

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    headers = [
        "dataset_id",
        "organization",
        "url",
        "relative_path",
        "role",
        "destination_path",
        "bytes",
        "sha256",
        "status",
        "error",
        "retrieved_at_utc",
    ]
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Manifest: {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
