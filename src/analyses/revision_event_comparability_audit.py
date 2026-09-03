#!/usr/bin/env python3
"""Audit the distinct 2016 and 2026 validation roles for Reviewer 4 Comment 1.

This revision-only analysis verifies official event metadata, reconstructs the
GSI air-photo interpretation footprint and source-photo timing, compares
antecedent rainfall at the two event windows, and tests the already specified
terrain-context score against pseudo-background cells sampled only inside the
GSI interpretation footprint.  It does not pool the two events or treat either
dataset as validation of a rainfall-triggered failure probability.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import numpy as np
import pandas as pd
from rasterio.features import rasterize
import shapely
from shapely.geometry import Polygon
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src/analyses"))

import _hazard_validation_shared as shared  # noqa: E402
import figure_official_threshold_adjusted_landslide_disruption_score as terrain  # noqa: E402
import table_hazard_validation as hazard_table  # noqa: E402


OUT = ROOT / "data/exp/revision/reviewer-4-comment-1"
GSI_ZIP = ROOT / "data/raw/official_reference/2016_inventory/gsi_airphoto_interpreted_landslides.zip"
JMA_2016 = OUT / "jma_2016_mainshock.html"
JMA_2026 = ROOT / "data/raw/official_reference/2026_event/jma_eew_20260728162718.html"
RAIN = ROOT / "data/processed/jma_hourly_rainfall_preprocessed.parquet"
R2C7_EPISODES = (
    ROOT
    / "data/exp/revision/reviewer-2-comment-7/restriction_episode_trigger_audit.csv"
)
KML_POINTS = "20160728_houkaichi.kml"
KML_FOOTPRINTS = ("201604_handokuhani.kml", "201607_handokuhani.kml")
NS = {"kml": "http://www.opengis.net/kml/2.2"}
EARTHQUAKE_2016 = pd.Timestamp("2016-04-16 01:25", tz="Asia/Tokyo")
WARNING_CUTOFF = pd.Timestamp("2016-04-14")
RANDOM_SEED = 20260809


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_event_html(path: Path, year: int) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if year == 2016:
        required = (
            "2016-04-16 01:25:05.4",
            "北緯32度45.2分",
            "東経130度45.7分",
            "<td>12km</td><td>7.3",
            "<td>10km</td><td>7.0",
        )
        if not all(token in text for token in required):
            raise RuntimeError("The official 2016 JMA event page did not match expected metadata.")
        return {
            "event_time_jst": "2016-04-16 01:25:05.4",
            "latitude": 32 + 45.2 / 60,
            "longitude": 130 + 45.7 / 60,
            "depth_km": 12,
            "jma_magnitude": 7.3,
            "moment_magnitude": 7.0,
            "maximum_intensity": 7,
            "source": "https://www.data.jma.go.jp/eqev/data/mech/cmt/fig/cmt20160416012505.html",
        }
    required = (
        "令和 8年07月28日16時27分15.2秒",
        "32°37.5′",
        "130°40.7′",
        "<td>16km</td><td>7.1</td><td>７</td>",
    )
    if not all(token in text for token in required):
        raise RuntimeError("The official 2026 JMA event page did not match expected metadata.")
    return {
        "event_time_jst": "2026-07-28 16:27:15.2",
        "latitude": 32 + 37.5 / 60,
        "longitude": 130 + 40.7 / 60,
        "depth_km": 16,
        "jma_magnitude": 7.1,
        "moment_magnitude": None,
        "maximum_intensity": 7,
        "source": "https://ds.data.jma.go.jp/eew/data/nc/fc_hist/2026/07/20260728162718/index.html",
    }


def haversine_km(first: dict[str, object], second: dict[str, object]) -> float:
    radius = 6371.0
    lat1, lat2 = np.radians([first["latitude"], second["latitude"]])
    dlat = lat2 - lat1
    dlon = np.radians(second["longitude"] - first["longitude"])
    value = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return float(2 * radius * np.arcsin(np.sqrt(value)))


def kml_inventory_audit() -> tuple[dict[str, object], object]:
    photo_counts: dict[str, int] = {}
    size_counts: dict[str, int] = {}
    footprint_polygons: list[Polygon] = []
    with ZipFile(GSI_ZIP) as archive:
        root = ET.fromstring(archive.read(KML_POINTS))
        for placemark in root.findall(".//kml:Placemark", NS):
            name = placemark.findtext("kml:name", default="", namespaces=NS).strip()
            description = placemark.findtext(
                "kml:description", default="", namespaces=NS
            ).strip()
            match = re.search(r"(2016/[0-9/～\-]+)", description)
            label = match.group(1) if match else "unresolved"
            photo_counts[label] = photo_counts.get(label, 0) + 1
            size_counts[name] = size_counts.get(name, 0) + 1
        for member in KML_FOOTPRINTS:
            coverage_root = ET.fromstring(archive.read(member))
            for node in coverage_root.findall(
                ".//kml:Polygon/kml:outerBoundaryIs/kml:LinearRing/kml:coordinates", NS
            ):
                coordinates = []
                for token in (node.text or "").split():
                    parts = token.split(",")
                    coordinates.append((float(parts[0]), float(parts[1])))
                footprint_polygons.append(Polygon(coordinates))
    footprint = shapely.union_all(footprint_polygons)
    total = sum(photo_counts.values())
    april = sum(count for label, count in photo_counts.items() if label.startswith("2016/04"))
    july = total - april
    return (
        {
            "inventory_points": total,
            "source_photo_counts": photo_counts,
            "april_photo_points": april,
            "july_photo_points": july,
            "size_class_counts": size_counts,
            "inventory_update_date": "2016-07-28",
            "source_interpretation": (
                "GSI describes the points as earthquake-generated mass-movement centres "
                "interpreted from air photos, without field survey; mapped classes combine "
                "steep-slope collapse, landslide, and debris flow."
            ),
            "subsurface_disturbance_depth_available": False,
        },
        footprint,
    )


def antecedent_2016_rainfall() -> dict[str, object]:
    frame = pd.read_parquet(
        RAIN,
        columns=["Station Slug", "Observation Time", "Hourly Rainfall"],
    )
    end = EARTHQUAKE_2016.floor("h")
    details: dict[str, object] = {}
    for hours in (1, 3, 24, 72):
        selected = frame.loc[
            frame["Observation Time"].le(end)
            & frame["Observation Time"].gt(end - pd.Timedelta(hours=hours))
        ]
        station = selected.groupby("Station Slug")["Hourly Rainfall"].agg(["sum", "count"])
        if len(station) != 7 or not station["count"].eq(hours).all():
            raise RuntimeError(f"Incomplete 2016 rainfall support for the {hours}-h window.")
        details[f"{hours}h_station_min_mm"] = float(station["sum"].min())
        details[f"{hours}h_station_max_mm"] = float(station["sum"].max())
    details["station_count"] = 7
    return details


def footprint_validation(footprint: object) -> tuple[pd.DataFrame, dict[str, object]]:
    original_cutoff = terrain.LANDSLIDE_VALIDATION_DATE
    try:
        # Reconstruct the current, already specified fixed score before changing
        # the historical eligibility and sampling masks used only for this audit.
        terrain.LANDSLIDE_VALIDATION_DATE = pd.Timestamp("2016-07-28")
        frozen_context = shared.prepare_context()
        frozen_fixed = terrain.TransparentStandardizedScore(terrain.FALLBACK_WEIGHTS).fit(
            np.asarray(frozen_context["matrix"], dtype=float)
        )

        terrain.LANDSLIDE_VALIDATION_DATE = WARNING_CUTOFF
        context = shared.prepare_context()
    finally:
        terrain.LANDSLIDE_VALIDATION_DATE = original_cutoff

    footprint_mask = rasterize(
        [(footprint, 1)],
        out_shape=context["shape"],
        transform=context["transform"],
        fill=0,
        all_touched=True,
        dtype="uint8",
    ).astype(bool)
    eligible = context["valid"] & footprint_mask
    coordinates = shapely.get_coordinates(context["landslide_geometry"])
    row, column, inside = terrain.grid_indices(
        coordinates, context["extent"], context["shape"]
    )
    pairs = np.unique(np.column_stack([row[inside], column[inside]]), axis=0)
    pairs = pairs[
        eligible[pairs[:, 0], pairs[:, 1]]
    ]
    presence_flat = np.ravel_multi_index((pairs[:, 0], pairs[:, 1]), context["shape"])
    available_flat = np.flatnonzero(eligible.ravel())
    background_pool = np.setdiff1d(available_flat, presence_flat, assume_unique=False)
    random = np.random.default_rng(RANDOM_SEED)
    background_flat = random.choice(
        background_pool, size=len(presence_flat) * 10, replace=False
    )
    sampled_flat = np.concatenate([presence_flat, background_flat])
    sampled_row, sampled_column = np.unravel_index(sampled_flat, context["shape"])
    matrix = np.column_stack(
        [
            context["features"][name][sampled_row, sampled_column]
            for name in terrain.FEATURE_NAMES
        ]
    )
    outcome = np.concatenate(
        [
            np.ones(len(presence_flat), dtype=int),
            np.zeros(len(background_flat), dtype=int),
        ]
    )
    groups = terrain.spatial_groups(
        sampled_row, sampled_column, context["extent"], context["shape"]
    )

    specifications = [
        ("Full terrain + warning-zone logistic", [0, 1, 2, 3], "logistic"),
        ("Terrain-only logistic", [0, 1, 2], "logistic"),
        ("Elevation + warning-zone logistic", [0, 3], "logistic"),
        ("Warning-zone-only indicator", [3], "raw"),
    ]
    rows: list[dict[str, object]] = []
    reference: np.ndarray | None = None
    for label, indices, model_kind in specifications:
        metrics, score = hazard_table.validate_specification(
            matrix, outcome, groups, indices, model_kind
        )
        if reference is None:
            reference = score
        rows.append(
            {
                "Specification": label,
                **metrics,
                "Rank Correlation vs Full": float(spearmanr(score, reference).statistic),
            }
        )

    # Evaluate the exact fixed score already propagated downstream. No outcome
    # information or footprint-restricted refit enters this score.
    splitter = GroupKFold(n_splits=5)
    frozen_score = frozen_fixed.decision_function(matrix)
    auc_values: list[float] = []
    capture_values: list[float] = []
    for _, test in splitter.split(matrix, outcome, groups):
        if len(np.unique(outcome[test])) < 2:
            continue
        test_score = frozen_score[test]
        auc_values.append(float(roc_auc_score(outcome[test], test_score)))
        threshold = float(np.quantile(test_score, 0.75))
        capture_values.append(
            float(np.mean(test_score[outcome[test] == 1] >= threshold))
        )
    rows.append(
        {
            "Specification": "Frozen fixed standardized terrain score",
            "Spatial Folds": len(auc_values),
            "Mean Spatial AUC": float(np.mean(auc_values)),
            "Spatial AUC Range": f"{np.min(auc_values):.3f}–{np.max(auc_values):.3f}",
            "Held-Out Top-Quartile Capture": float(np.mean(capture_values)),
            "Rank Correlation vs Full": float(
                spearmanr(frozen_score, reference).statistic
            ),
        }
    )
    prefecture_footprint_pct = float(
        100
        * shapely.area(shapely.intersection(footprint, context["admin_union"]))
        / shapely.area(context["admin_union"])
    )
    metadata = {
        "warning_zone_cutoff": WARNING_CUTOFF.date().isoformat(),
        "eligible_warning_zones": int(context["validation_warning_counts"]["selected"]),
        "interpretation_footprint_pct_of_prefecture": prefecture_footprint_pct,
        "unique_presence_cells": int(len(presence_flat)),
        "pseudo_background_cells": int(len(background_flat)),
        "spatial_groups": int(len(np.unique(groups))),
        "random_seed": RANDOM_SEED,
        "fixed_score_status": (
            "Frozen existing downstream score; the audit changes only where its "
            "historical alignment is evaluated, not the propagated score itself."
        ),
    }
    return pd.DataFrame(rows), metadata


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    event_2016 = parse_event_html(JMA_2016, 2016)
    event_2026 = parse_event_html(JMA_2026, 2026)
    inventory, footprint = kml_inventory_audit()
    rain_2016 = antecedent_2016_rainfall()
    episodes = pd.read_csv(R2C7_EPISODES)
    if len(episodes) != 10:
        raise RuntimeError("Expected 10 retained 2026 physical road-restriction episodes.")
    rain_2026_max = {
        f"{hours}h_station_max_mm": float(
            episodes[f"Regional Maximum {hours} h Rainfall (mm)"].max()
        )
        for hours in (1, 3, 24, 72)
    }
    validation, validation_metadata = footprint_validation(footprint)

    event_rows = [
        {
            "Event": "2016 Kumamoto earthquake inventory",
            "JMA Magnitude": event_2016["jma_magnitude"],
            "Depth (km)": event_2016["depth_km"],
            "Maximum JMA Intensity": event_2016["maximum_intensity"],
            "Rainfall Evidence": (
                "0 mm over preceding 24 h at seven stations; "
                f"{rain_2016['72h_station_min_mm']:.1f}–"
                f"{rain_2016['72h_station_max_mm']:.1f} mm over preceding 72 h"
            ),
            "Spatial Evidence": (
                f"{inventory['inventory_points']:,} interpreted centre points inside an "
                f"air-photo footprint covering {validation_metadata['interpretation_footprint_pct_of_prefecture']:.1f}% "
                "of Kumamoto"
            ),
            "Subsurface Disturbance Depth": "Not observed",
            "Permitted Role": (
                "Historical alignment of the frozen terrain-context ranking within the "
                "interpretation footprint; no 2026 rainfall or shaking validation"
            ),
        },
        {
            "Event": "2026 earthquake-proximate road restrictions",
            "JMA Magnitude": event_2026["jma_magnitude"],
            "Depth (km)": event_2026["depth_km"],
            "Maximum JMA Intensity": event_2026["maximum_intensity"],
            "Rainfall Evidence": (
                "0 mm over preceding 1, 3, 24, and 72 h across the ten-station audit"
            ),
            "Spatial Evidence": "10 physical episodes linked to 94 road sections",
            "Subsurface Disturbance Depth": "Not observed",
            "Permitted Role": (
                "Supplementary terrain-to-road ranking correspondence only; no validation "
                "of rainfall triggering or closure probability"
            ),
        },
    ]
    pd.DataFrame(event_rows).to_csv(OUT / "event_comparability_audit.csv", index=False)
    validation.to_csv(OUT / "footprint_restricted_hazard_validation.csv", index=False)
    decision = {
        "event_2016": event_2016,
        "event_2026": event_2026,
        "epicentral_distance_km": haversine_km(event_2016, event_2026),
        "inventory": inventory,
        "antecedent_rainfall_2016": rain_2016,
        "antecedent_rainfall_2026_maxima": rain_2026_max,
        "validation": validation_metadata,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (GSI_ZIP, JMA_2016, JMA_2026, RAIN, R2C7_EPISODES)
        },
        "interpretation": (
            "The events are geographically relevant but not physically interchangeable. "
            "Similar large magnitudes, shallow depths, maximum JMA intensity 7, and nearby "
            "epicentres support a same-region comparison of persistent terrain context. "
            "Different shaking footprints, absent point-specific 2016 failure timing, and "
            "no commensurate subsurface disturbance-depth measurements preclude cross-event "
            "validation of rainfall response, shaking effects, or physical susceptibility."
        ),
    }
    (OUT / "decision.json").write_text(
        json.dumps(decision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    print(validation.to_string(index=False))


if __name__ == "__main__":
    main()
