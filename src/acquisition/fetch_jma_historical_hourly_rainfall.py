#!/usr/bin/env python3
"""Download rate-limited JMA hourly rainfall CSV batches for representative Kumamoto stations."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT / "data/raw/jma_historical_hourly_rainfall"
MANIFEST_PATH = ROOT / "data/raw/_manifests/jma_historical_hourly_rainfall.csv"
ENDPOINT = "https://www.data.jma.go.jp/risk/obsdl/show/table"
USER_AGENT = "KE01e-earthquake-rainfall-landslide-research/1.0"
REQUEST_DELAY_SECONDS = 3.0

STATIONS = {
    "kumamoto": ("s47819", "熊本"),
    "kikuchi": ("a0835", "菊池"),
    "takamori": ("a0840", "高森"),
    "kosa": ("a0842", "甲佐"),
    "matsushima": ("a0843", "松島"),
    "yatsushiro": ("a0846", "八代"),
    "hitoyoshi": ("s47824", "人吉"),
    "ushibuka": ("s47838", "牛深"),
    "minamata": ("a0924", "水俣"),
    "misumi": ("a1081", "三角"),
}

CORE_STATIONS = {"kumamoto", "kosa", "matsushima", "yatsushiro", "misumi"}

PERIODS = {
    "2016_2017": ["2016", "2017", "1", "12", "1", "31"],
    "2018_2019": ["2018", "2019", "1", "12", "1", "31"],
    "2020_2021": ["2020", "2021", "1", "12", "1", "31"],
    "2022_2023": ["2022", "2023", "1", "12", "1", "31"],
    "2024_2025": ["2024", "2025", "1", "12", "1", "31"],
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def request_payload(station_id: str, ymd: list[str]) -> bytes:
    fields = {
        "stationNumList": json.dumps([station_id]),
        "aggrgPeriod": "9",
        "elementNumList": json.dumps([["101", ""]]),
        "interAnnualType": "1",
        "ymdList": json.dumps(ymd),
        "optionNumList": "[]",
        "downloadFlag": "true",
        "rmkFlag": "1",
        "disconnectFlag": "1",
        "youbiFlag": "0",
        "fukenFlag": "1",
        "kijiFlag": "0",
        "csvFlag": "1",
        "jikantaiFlag": "0",
        "jikantaiList": "[]",
        "ymdLiteral": "1",
    }
    body = urllib.parse.urlencode(fields).encode("ascii")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.data.jma.go.jp/risk/obsdl/index.php",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def validate_csv(payload: bytes) -> tuple[int, str]:
    if payload.lstrip().startswith((b"<!DOCTYPE", b"<html")):
        raise ValueError("JMA returned HTML instead of CSV")
    text = payload.decode("cp932")
    lines = text.splitlines()
    data_rows = sum(1 for line in lines if line[:4].isdigit() and "/" in line[:12])
    if data_rows < 100:
        raise ValueError(f"Too few data rows in JMA response: {data_rows}")
    return data_rows, text.splitlines()[0] if text.splitlines() else ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-stations", action="store_true", help="Fetch all ten representative stations instead of the five core event stations")
    args = parser.parse_args()
    selected_stations = STATIONS if args.all_stations else {slug: STATIONS[slug] for slug in STATIONS if slug in CORE_STATIONS}
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    rows = []
    request_number = 0
    total_requests = len(selected_stations) * len(PERIODS)
    for station_slug, (station_id, station_name) in selected_stations.items():
        for period_id, ymd in PERIODS.items():
            request_number += 1
            destination = OUTPUT_ROOT / station_slug / f"hourly_rainfall_{period_id}.csv"
            destination.parent.mkdir(parents=True, exist_ok=True)
            status = "existing"
            error = ""
            try:
                if destination.exists() and destination.stat().st_size > 0:
                    payload = destination.read_bytes()
                else:
                    payload = request_payload(station_id, ymd)
                    validate_csv(payload)
                    temporary = destination.with_suffix(".csv.part")
                    temporary.write_bytes(payload)
                    temporary.replace(destination)
                    status = "downloaded"
                data_rows, response_header = validate_csv(payload)
                digest = sha256(payload)
                file_bytes = len(payload)
            except Exception as exc:  # noqa: BLE001
                status = "failed"
                error = str(exc)
                data_rows = 0
                response_header = ""
                digest = ""
                file_bytes = 0
            rows.append(
                {
                    "station_slug": station_slug,
                    "station_id": station_id,
                    "station_name_ja": station_name,
                    "period_id": period_id,
                    "start_date": f"{ymd[0]}-{int(ymd[2]):02d}-{int(ymd[4]):02d}",
                    "end_date": f"{ymd[1]}-{int(ymd[3]):02d}-{int(ymd[5]):02d}",
                    "element": "hourly precipitation (previous 1 hour)",
                    "source_url": ENDPOINT,
                    "destination_path": str(destination.relative_to(ROOT)),
                    "data_rows": data_rows,
                    "bytes": file_bytes,
                    "sha256": digest,
                    "response_header": response_header,
                    "status": status,
                    "error": error,
                    "retrieved_at_utc": retrieved_at,
                }
            )
            print(f"{request_number}/{total_requests} {station_slug} {period_id}: {status}, rows={data_rows}", flush=True)
            if request_number < total_requests and status != "existing":
                time.sleep(REQUEST_DELAY_SECONDS)

    manifested_paths = {str(row["destination_path"]) for row in rows}
    for destination in sorted(OUTPUT_ROOT.glob("*/hourly_rainfall_*.csv")):
        relative_destination = str(destination.relative_to(ROOT))
        if relative_destination in manifested_paths:
            continue
        station_slug = destination.parent.name
        station_id, station_name = STATIONS[station_slug]
        period_id = destination.stem.removeprefix("hourly_rainfall_")
        start_year, end_year = period_id.split("_", 1)
        payload = destination.read_bytes()
        data_rows, response_header = validate_csv(payload)
        rows.append(
            {
                "station_slug": station_slug,
                "station_id": station_id,
                "station_name_ja": station_name,
                "period_id": period_id,
                "start_date": f"{start_year}-01-01",
                "end_date": f"{end_year}-12-31",
                "element": "hourly precipitation (previous 1 hour)",
                "source_url": ENDPOINT,
                "destination_path": relative_destination,
                "data_rows": data_rows,
                "bytes": len(payload),
                "sha256": sha256(payload),
                "response_header": response_header,
                "status": "existing_supplementary",
                "error": "",
                "retrieved_at_utc": retrieved_at,
            }
        )
        print(f"supplementary {station_slug} {period_id}: existing, rows={data_rows}", flush=True)

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    headers = list(rows[0])
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Manifest: {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
