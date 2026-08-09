#!/usr/bin/env python3
"""Import selected KE01-series assets into KE01e without modifying source projects."""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESEARCH_ROOT = ROOT.parent
DESTINATION_ROOT = ROOT / "data/raw/reused_local"
MANIFEST_PATH = ROOT / "data/raw/_manifests/local_reference_assets.csv"
ALLOWED_PROJECTS = {"KE01", "KE01b", "KE01c", "KE01d"}

ASSETS = {
    "administrative_areas": ("KE01b", "data/processed/kumamoto_administrative_areas_preprocessed.parquet"),
    "road_sections": ("KE01b", "data/processed/kumamoto_road_sections_preprocessed.parquet"),
    "road_edges": ("KE01b", "data/processed/kumamoto_routable_road_edges_preprocessed.parquet"),
    "road_nodes": ("KE01b", "data/processed/kumamoto_routable_road_nodes_preprocessed.parquet"),
    "emergency_transport_roads": ("KE01b", "data/processed/kumamoto_emergency_transport_roads_2024_preprocessed.parquet"),
    "landslide_warning_zones": ("KE01b", "data/processed/kumamoto_landslide_warning_zones_2025_preprocessed.parquet"),
    "population_mesh_125m": ("KE01b", "data/processed/kumamoto_population_mesh_125m_preprocessed.parquet"),
    "population_disclosure_groups": ("KE01b", "data/processed/kumamoto_population_disclosure_groups_preprocessed.parquet"),
    "evacuation_facilities": ("KE01b", "data/processed/kumamoto_evacuation_facilities_2012_preprocessed.parquet"),
    "fire_stations": ("KE01b", "data/processed/kumamoto_fire_stations_2012_preprocessed.parquet"),
    "designated_shelters": ("KE01c", "data/processed/designated_shelters_preprocessed.parquet"),
    "emergency_evacuation_sites": ("KE01c", "data/processed/emergency_evacuation_sites_preprocessed.parquet"),
    "earthquake_damage_evidence": ("KE01c", "data/processed/earthquake_damage_evidence_reference_preprocessed.parquet"),
    "road_restrictions": ("KE01d", "data/processed/road_restrictions_preprocessed.parquet"),
    "road_restriction_edge_matches": ("KE01d", "data/processed/road_restriction_edge_matches_preprocessed.parquet"),
    "current_shelters": ("KE01d", "data/processed/shelters_current_preprocessed.parquet"),
    "emergency_water_points": ("KE01d", "data/processed/emergency_water_points_preprocessed.parquet"),
    "public_offices_halls": ("KE01", "data/processed/kumamoto_mlit_public_offices_halls_preprocessed.parquet"),
    "jma_amedas_event_window": ("KE01", "data/raw/weather/jma_amedas/event_window"),
    "jma_amedas_station_metadata": ("KE01", "data/raw/weather/jma_amedas/stations/amedastable_2026-08-02.json"),
    "jma_amedas_event_manifest": ("KE01", "data/raw/_manifests/kumamoto_jma_event_window_refresh.csv"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(item for item in path.rglob("*") if item.is_file())


def import_assets(selected: set[str] | None) -> list[dict[str, str | int]]:
    imported_at = datetime.now(timezone.utc).isoformat()
    rows: list[dict[str, str | int]] = []
    for asset_id, (project, relative_source) in ASSETS.items():
        if selected and asset_id not in selected:
            continue
        if project not in ALLOWED_PROJECTS:
            raise ValueError(f"Source project is not allowed: {project}")
        project_root = (RESEARCH_ROOT / project).resolve()
        source = (project_root / relative_source).resolve()
        source.relative_to(project_root)
        if not source.exists():
            raise FileNotFoundError(source)
        for source_file in source_files(source):
            suffix = source_file.relative_to(source) if source.is_dir() else Path(source_file.name)
            destination = DESTINATION_ROOT / project / asset_id / suffix
            destination.parent.mkdir(parents=True, exist_ok=True)
            source_hash = sha256(source_file)
            status = "copied"
            if destination.exists() and sha256(destination) == source_hash:
                status = "unchanged"
            else:
                shutil.copy2(source_file, destination)
                if sha256(destination) != source_hash:
                    raise OSError(f"Checksum mismatch after copy: {destination}")
            rows.append(
                {
                    "asset_id": asset_id,
                    "source_project": project,
                    "source_path": str(source_file),
                    "destination_path": str(destination.relative_to(ROOT)),
                    "source_stage": "processed" if "/data/processed/" in str(source_file) else "raw",
                    "bytes": source_file.stat().st_size,
                    "sha256": source_hash,
                    "status": status,
                    "imported_at_utc": imported_at,
                }
            )
    return rows


def write_manifest(rows: list[dict[str, str | int]]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    headers = [
        "asset_id",
        "source_project",
        "source_path",
        "destination_path",
        "source_stage",
        "bytes",
        "sha256",
        "status",
        "imported_at_utc",
    ]
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", action="append", choices=sorted(ASSETS))
    args = parser.parse_args()
    rows = import_assets(set(args.asset) if args.asset else None)
    write_manifest(rows)
    print(f"Imported {len(rows)} files from {len({row['asset_id'] for row in rows})} assets")
    print(f"Manifest: {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
