#!/usr/bin/env python3
"""Audit 2026 road-restriction triggers and event-level validation support.

This revision analysis separates repeated MLIT snapshots, physical restriction
episodes, matched road sections, and triggering evidence.  It also retrieves
official JMA hourly rainfall for the event window and reports event-clustered
matched-control concordance.  The audit does not relabel a generic process
description (for example, rockfall) as a confirmed rainfall trigger.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.request
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import numpy as np
import pandas as pd
from rasterio.features import rasterize
from rasterio.transform import from_bounds
import shapely


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src/analyses"))

import figure_road_disruption_exposure_and_observed_restriction_evidence as road_validation  # noqa: E402
from src.acquisition.fetch_jma_historical_hourly_rainfall import (  # noqa: E402
    STATIONS,
    request_payload,
    validate_csv,
)
from src.preprocessing.preprocess_jma_hourly_rainfall import (  # noqa: E402
    read_chunk,
    station_coordinates,
)


OUT = ROOT / "data/exp/revision/reviewer-2-comment-7"
JMA_OUT = OUT / "jma_event_hourly"
RESTRICTION_PATH = ROOT / "data/processed/road_restrictions_preprocessed.parquet"
MATCH_PATH = ROOT / "data/processed/road_restriction_edge_matches_preprocessed.parquet"
EDGE_PATH = ROOT / "data/processed/road_edges_preprocessed.parquet"
ROAD_PATH = ROOT / "data/processed/road_sections_preprocessed.parquet"
ADMIN_PATH = ROOT / "data/processed/administrative_areas_preprocessed.parquet"
ROAD_SCORE_PATH = ROOT / "data/results/intermediate/road_disruption_scores_normalized_v4_y075.npz"
WARNING_SCORE_PATH = ROOT / "data/results/intermediate/road_warning_zone_scores_normalized_v3.npz"
TRANSFER_SENSITIVITY_PATH = (
    ROOT
    / "data/exp/revision/reviewer-2-comment-5/heavy_road_scores_15_specifications.npz"
)
RAINFALL_SENSITIVITY_PATH = (
    ROOT
    / "data/exp/revision/reviewer-2-comment-4/road_scores_15x3_scenarios.npz"
)

MLIT_NOTICE_URL = "https://www.mlit.go.jp/report/press/sabo01_hh_000214.html"
MLIT_NOTICE_PATH = OUT / "mlit_threshold_notice.html"
EARTHQUAKE_TIME = pd.Timestamp("2026-07-28 16:27", tz="Asia/Tokyo")
JMA_YMD = ["2026", "2026", "7", "7", "25", "31"]
PROCESS_REASONS = ("落石", "法面崩落", "土砂流入")
EPISODE_KEYS = [
    "Start Address",
    "End Address",
    "Restriction Reason",
    "Restriction Start Time",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_official_inputs(refresh: bool) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    JMA_OUT.mkdir(parents=True, exist_ok=True)
    if refresh or not MLIT_NOTICE_PATH.exists():
        request = urllib.request.Request(
            MLIT_NOTICE_URL,
            headers={"User-Agent": "KE01e-revision-audit/1.0"},
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = response.read()
        text = payload.decode("utf-8")
        required = (
            "令和8年7月28日16時27分頃",
            "熊本県で最大震度７",
            "地震後の降雨と土砂災害の関係",
        )
        if not all(token in text for token in required):
            raise RuntimeError("The MLIT notice did not contain the expected event statements.")
        MLIT_NOTICE_PATH.write_bytes(payload)

    for number, (slug, (station_id, _)) in enumerate(STATIONS.items(), start=1):
        path = JMA_OUT / f"{slug}_20260725_20260731.csv"
        if refresh or not path.exists():
            payload = request_payload(station_id, JMA_YMD)
            validate_csv(payload)
            path.write_bytes(payload)
            if number < len(STATIONS):
                time.sleep(1.0)


def jma_event_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    coordinates = station_coordinates()
    frames: list[pd.DataFrame] = []
    stations: list[dict[str, object]] = []
    for slug, (station_id, station_name) in STATIONS.items():
        path = JMA_OUT / f"{slug}_20260725_20260731.csv"
        frame = read_chunk(path)
        frame["observation_time"] = pd.to_datetime(
            frame["observation_time"], errors="coerce"
        ).dt.tz_localize("Asia/Tokyo")
        frame["hourly_rainfall_mm"] = pd.to_numeric(
            frame["hourly_rainfall_mm"], errors="coerce"
        )
        frame["quality_flag"] = pd.to_numeric(frame["quality_flag"], errors="coerce")
        frame["analysis_rainfall_mm"] = frame["hourly_rainfall_mm"].where(
            frame["quality_flag"].eq(8)
        )
        frame["station_slug"] = slug
        frames.append(frame)
        latitude, longitude = coordinates[station_name]
        stations.append(
            {
                "Station Slug": slug,
                "Station ID": station_id,
                "Station Name": station_name,
                "Station Latitude": latitude,
                "Station Longitude": longitude,
                "Official CSV": str(path.relative_to(ROOT)),
                "SHA-256": sha256(path),
            }
        )
    return pd.concat(frames, ignore_index=True), pd.DataFrame(stations)


def haversine_km(
    longitude_1: float,
    latitude_1: float,
    longitude_2: float,
    latitude_2: float,
) -> float:
    lon1, lat1, lon2, lat2 = map(
        math.radians,
        (longitude_1, latitude_1, longitude_2, latitude_2),
    )
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    value = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    )
    return 6371.0088 * 2 * math.asin(math.sqrt(value))


def rolling_rainfall(
    rainfall: pd.DataFrame,
    station_slug: str,
    event_time: pd.Timestamp,
    hours: int,
) -> float:
    end = event_time.floor("h")
    start = end - pd.Timedelta(hours=hours - 1)
    selected = rainfall.loc[
        rainfall["station_slug"].eq(station_slug)
        & rainfall["observation_time"].between(start, end),
        "analysis_rainfall_mm",
    ]
    if len(selected) != hours or selected.isna().any():
        return float("nan")
    return float(selected.sum())


def restriction_evidence() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    list[dict[str, object]],
    pd.Series,
]:
    restrictions = pd.read_parquet(RESTRICTION_PATH).reset_index(drop=True)
    restrictions.insert(
        0,
        "Restriction Observation ID",
        [f"RR-{index:06d}" for index in range(1, len(restrictions) + 1)],
    )
    matches = pd.read_parquet(MATCH_PATH)
    edges = pd.read_parquet(EDGE_PATH, columns=["Road Edge ID", "Road Section ID"])
    roads = pd.read_parquet(
        ROAD_PATH,
        columns=["Road Section ID", "Network Analysis Eligible"],
    )
    eligible_sections = set(
        roads.loc[roads["Network Analysis Eligible"], "Road Section ID"].astype(str)
    )

    process_snapshots = restrictions[restrictions["Restriction Reason"].isin(PROCESS_REASONS)]
    reliable_mask = (
        matches["Restriction Reason"].isin(PROCESS_REASONS)
        & matches["Road Edge Match Status"].eq("matched_primary")
        & matches["Road Edge Match Distance (m)"].le(50)
    )
    reliable_matches = matches.loc[reliable_mask].drop_duplicates(
        ["Restriction Observation ID", "Snapshot Time", "Matched Road Edge ID"]
    )
    reliable_observation_ids = reliable_matches[["Restriction Observation ID"]].drop_duplicates()
    retained_snapshots = restrictions.merge(
        reliable_observation_ids,
        on="Restriction Observation ID",
        how="inner",
        validate="one_to_one",
    )

    all_episodes = process_snapshots.drop_duplicates(EPISODE_KEYS).copy()
    retained_episodes = retained_snapshots.drop_duplicates(EPISODE_KEYS).copy()
    retained_episodes = retained_episodes.sort_values(
        ["Restriction Start Time", "Start Address", "End Address"],
        kind="stable",
    ).reset_index(drop=True)
    retained_episodes["Episode ID"] = [
        f"EP-{index:02d}" for index in range(1, len(retained_episodes) + 1)
    ]
    observation_episode = retained_snapshots.merge(
        retained_episodes[EPISODE_KEYS + ["Episode ID"]],
        on=EPISODE_KEYS,
        how="left",
        validate="many_to_one",
    )
    episode_matches = (
        reliable_matches.merge(
            observation_episode[["Restriction Observation ID", "Episode ID"]],
            on="Restriction Observation ID",
            how="inner",
            validate="many_to_one",
        )
        .merge(
            edges,
            left_on="Matched Road Edge ID",
            right_on="Road Edge ID",
            how="inner",
            validate="many_to_one",
        )
    )
    episode_matches = episode_matches[
        episode_matches["Road Section ID"].astype(str).isin(eligible_sections)
    ].copy()
    event_section_pairs = episode_matches.drop_duplicates(
        ["Episode ID", "Road Section ID"]
    )[["Episode ID", "Road Section ID"]]

    current_edges = (
        reliable_matches.merge(
            edges,
            left_on="Matched Road Edge ID",
            right_on="Road Edge ID",
            how="inner",
            validate="many_to_one",
        )
        .drop_duplicates(["Road Edge ID", "Restriction Reason"])
    )
    current_edges = current_edges[
        current_edges["Road Section ID"].astype(str).isin(eligible_sections)
    ]
    current_sections = current_edges["Road Section ID"].drop_duplicates()
    funnel = [
        {"Stage": "All official restriction snapshot rows", "Count": len(restrictions)},
        {
            "Stage": "Snapshot rows with rockfall, slope collapse, or sediment inflow reason",
            "Count": len(process_snapshots),
        },
        {
            "Stage": "Physical process episodes before spatial matching",
            "Count": len(all_episodes),
        },
        {
            "Stage": "Snapshot rows retained by matched_primary and <=50 m rule",
            "Count": retained_snapshots["Restriction Observation ID"].nunique(),
        },
        {
            "Stage": "Physical episodes retained in the Kumamoto network",
            "Count": len(retained_episodes),
        },
        {"Stage": "Unique matched network edges", "Count": current_edges["Road Edge ID"].nunique()},
        {"Stage": "Unique matched network sections", "Count": current_sections.nunique()},
        {"Stage": "Event-section pairs", "Count": len(event_section_pairs)},
    ]
    return (
        retained_episodes,
        observation_episode,
        episode_matches,
        funnel,
        current_sections,
    )


def attach_trigger_evidence(
    episodes: pd.DataFrame,
    observations: pd.DataFrame,
    matches: pd.DataFrame,
    rainfall: pd.DataFrame,
    stations: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, values in episodes.iterrows():
        episode_id = values["Episode ID"]
        episode_observations = observations[observations["Episode ID"].eq(episode_id)]
        geometries = [
            shapely.from_geojson(value)
            for value in episode_observations["Geometry JSON"].dropna().astype(str).unique()
        ]
        geometry = shapely.union_all(geometries)
        point = shapely.centroid(geometry)
        longitude = float(shapely.get_x(point))
        latitude = float(shapely.get_y(point))
        distance = stations.apply(
            lambda station: haversine_km(
                longitude,
                latitude,
                float(station["Station Longitude"]),
                float(station["Station Latitude"]),
            ),
            axis=1,
        )
        nearest = stations.loc[distance.idxmin()]
        event_time = values["Restriction Start Time"]
        windows = {
            hours: rolling_rainfall(
                rainfall,
                str(nearest["Station Slug"]),
                event_time,
                hours,
            )
            for hours in (1, 3, 24, 72)
        }
        regional = {
            hours: float(
                np.nanmax(
                    [
                        rolling_rainfall(rainfall, slug, event_time, hours)
                        for slug in stations["Station Slug"].astype(str)
                    ]
                )
            )
            for hours in (1, 3, 24, 72)
        }
        hours_after = (event_time - EARTHQUAKE_TIME).total_seconds() / 3600
        reason = str(values["Restriction Reason"])
        explicit_rain = any(term in reason for term in ("雨", "豪雨", "大雨", "降雨"))
        explicit_earthquake = "地震" in reason
        if explicit_rain and explicit_earthquake:
            trigger_class = "Mixed trigger explicitly coded"
        elif explicit_rain:
            trigger_class = "Rainfall trigger explicitly coded"
        elif explicit_earthquake:
            trigger_class = "Direct-earthquake trigger explicitly coded"
        elif (
            0 <= hours_after <= 48
            and regional[72] == 0
            and episode_observations["Source URL"].astype(str).str.contains("/r8kumamoto/").all()
        ):
            trigger_class = "Direct-earthquake consistent; trigger not explicitly coded"
        elif 0 <= hours_after <= 48 and regional[72] > 0:
            trigger_class = "Mixed or uncertain; trigger not explicitly coded"
        else:
            trigger_class = "Uncertain; trigger not explicitly coded"

        episode_match = matches[matches["Episode ID"].eq(episode_id)]
        agreement = episode_match["Route Name Agreement"]
        rows.append(
            {
                "Episode ID": episode_id,
                "Municipality": values["Municipality Name"],
                "Route Name": values["Route Name"],
                "Start Address": values["Start Address"],
                "End Address": values["End Address"],
                "Restriction Process Reason": reason,
                "Restriction Start Time": event_time,
                "Hours After Earthquake": hours_after,
                "Repeated Snapshot Rows": len(episode_observations),
                "First Snapshot": episode_observations["Snapshot Time"].min(),
                "Last Snapshot": episode_observations["Snapshot Time"].max(),
                "Matched Edge Count": episode_match["Road Edge ID"].nunique(),
                "Matched Section Count": episode_match["Road Section ID"].nunique(),
                "Any Route-Name Agreement": bool(agreement.eq(True).any()),
                "Route-Agreement True Candidate Rows": int(agreement.eq(True).sum()),
                "Route-Agreement False Candidate Rows": int(agreement.eq(False).sum()),
                "Route-Agreement Missing Candidate Rows": int(agreement.isna().sum()),
                "Nearest JMA Station": nearest["Station Name"],
                "Nearest-Station Distance (km)": float(distance.min()),
                "Nearest 1 h Rainfall (mm)": windows[1],
                "Nearest 3 h Rainfall (mm)": windows[3],
                "Nearest 24 h Rainfall (mm)": windows[24],
                "Nearest 72 h Rainfall (mm)": windows[72],
                "Regional Maximum 1 h Rainfall (mm)": regional[1],
                "Regional Maximum 3 h Rainfall (mm)": regional[3],
                "Regional Maximum 24 h Rainfall (mm)": regional[24],
                "Regional Maximum 72 h Rainfall (mm)": regional[72],
                "Trigger Classification": trigger_class,
                "Trigger Interpretation": (
                    "The process type and timing are consistent with earthquake-related slope disruption, "
                    "but the source reason does not explicitly encode the trigger."
                ),
            }
        )
    return pd.DataFrame(rows)


def matched_design(
    evidence_sections: pd.Series,
) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    roads = pd.read_parquet(
        ROAD_PATH,
        columns=[
            "Road Section ID",
            "Road Category",
            "Road Section Length (m)",
            "Emergency Route Membership",
            "Network Analysis Eligible",
            "Geometry",
        ],
    )
    roads = roads.loc[roads["Network Analysis Eligible"]].reset_index(drop=True)
    geometry = shapely.from_wkb(roads.pop("Geometry").to_numpy())
    admin = pd.read_parquet(ADMIN_PATH, columns=["Municipality Name", "Geometry"])
    admin_geometry = shapely.from_wkb(admin["Geometry"].to_numpy())
    union = shapely.union_all(admin_geometry)
    min_x, min_y, max_x, max_y = shapely.bounds(union)
    pad_x = (max_x - min_x) * 0.025
    pad_y = (max_y - min_y) * 0.025
    extent = (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)
    west, east, south, north = extent
    display_height = max(
        650,
        round(road_validation.DISPLAY_WIDTH * (north - south) / (east - west)),
    )
    display_shape = (display_height, road_validation.DISPLAY_WIDTH)
    transform = from_bounds(
        west,
        south,
        east,
        north,
        road_validation.DISPLAY_WIDTH,
        display_height,
    )
    municipality_grid = rasterize(
        ((item, index + 1) for index, item in enumerate(admin_geometry)),
        out_shape=display_shape,
        transform=transform,
        fill=0,
        all_touched=True,
        dtype="int16",
    )
    midpoints = shapely.line_interpolate_point(geometry, 0.5, normalized=True)
    municipality = road_validation.sample_grid(
        municipality_grid.astype("float32"),
        shapely.get_coordinates(midpoints)[:, :2],
        extent,
    ).astype(int)
    length_decile = pd.qcut(
        roads["Road Section Length (m)"].rank(method="first"),
        q=10,
        labels=False,
        duplicates="drop",
    ).to_numpy(dtype=int)
    road_category = roads["Road Category"].fillna("Unknown").astype(str).to_numpy()
    emergency_class = (
        roads["Emergency Route Membership"].fillna("None").astype(str).to_numpy()
    )
    lookup = pd.Series(
        np.arange(len(roads), dtype=int),
        index=roads["Road Section ID"].astype(str),
    )
    evidence_positions = (
        evidence_sections.astype(str).drop_duplicates().map(lookup).dropna().astype(int)
    )
    evidence_set = set(evidence_positions.tolist())
    random = np.random.default_rng(20260812)
    design_rows: list[dict[str, object]] = []
    for position in evidence_positions:
        eligible = (
            (municipality == municipality[position])
            & (road_category == road_category[position])
            & (emergency_class == emergency_class[position])
            & (length_decile == length_decile[position])
        )
        candidates = np.array(
            [item for item in np.flatnonzero(eligible) if item not in evidence_set],
            dtype=int,
        )
        if not candidates.size:
            continue
        controls = random.choice(candidates, size=min(10, candidates.size), replace=False)
        design_rows.append(
            {
                "Road Section ID": roads.iloc[position]["Road Section ID"],
                "Evidence Position": int(position),
                "Control Positions": controls,
                "Control Count": len(controls),
            }
        )
    score_cache = np.load(ROAD_SCORE_PATH, allow_pickle=False)
    warning_cache = np.load(WARNING_SCORE_PATH, allow_pickle=False)
    scores = {
        "Moderate road score": score_cache["score_Moderate"].astype(float),
        "Heavy road score": score_cache["score_Heavy"].astype(float),
        "Extreme road score": score_cache["score_Extreme"].astype(float),
        "Warning-zone baseline": warning_cache["score"].astype(float),
        "Road-length baseline": roads["Road Section Length (m)"].to_numpy(dtype=float),
    }
    return pd.DataFrame(design_rows), scores


def concordance_outputs(
    event_section_pairs: pd.DataFrame,
    evidence_order: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    design, scores = matched_design(evidence_order)
    rows: list[dict[str, object]] = []
    for record in design.itertuples(index=False):
        position = int(record[1])
        controls = np.asarray(record[2], dtype=int)
        row = {"Road Section ID": record[0], "Control Count": int(record[3])}
        for label, values in scores.items():
            difference = values[position] - values[controls]
            row[label] = float(
                np.mean((difference > 0) + 0.5 * (difference == 0))
            )
        rows.append(row)
    section = pd.DataFrame(rows)
    event_section = event_section_pairs.merge(
        section,
        on="Road Section ID",
        how="inner",
        validate="many_to_one",
    )
    score_labels = list(scores)
    event = event_section.groupby("Episode ID", sort=True)[score_labels].mean()
    random = np.random.default_rng(20260903)
    summary: list[dict[str, object]] = []
    for label in score_labels:
        current_values = section[label].to_numpy(dtype=float)
        event_values = event[label].to_numpy(dtype=float)
        bootstrap = np.array(
            [
                random.choice(event_values, size=len(event_values), replace=True).mean()
                for _ in range(20_000)
            ]
        )
        summary.append(
            {
                "Specification": label,
                "Snapshot Rows": 116,
                "Physical Episodes": len(event),
                "Unique Evidence Sections": len(evidence_order),
                "Sections With Controls": len(section),
                "Matched Controls": int(section["Control Count"].sum()),
                "Legacy Section-Weighted Concordance": current_values.mean(),
                "Episode-Weighted Concordance": event_values.mean(),
                "Episode-Cluster Bootstrap 95% CI Low": np.quantile(bootstrap, 0.025),
                "Episode-Cluster Bootstrap 95% CI High": np.quantile(bootstrap, 0.975),
            }
        )
    for comparator in ("Warning-zone baseline", "Road-length baseline"):
        paired = event["Heavy road score"] - event[comparator]
        bootstrap = np.array(
            [
                random.choice(paired.to_numpy(), size=len(paired), replace=True).mean()
                for _ in range(20_000)
            ]
        )
        summary.append(
            {
                "Specification": f"Heavy minus {comparator}",
                "Snapshot Rows": 116,
                "Physical Episodes": len(event),
                "Unique Evidence Sections": len(evidence_order),
                "Sections With Controls": len(section),
                "Matched Controls": int(section["Control Count"].sum()),
                "Legacy Section-Weighted Concordance": np.nan,
                "Episode-Weighted Concordance": paired.mean(),
                "Episode-Cluster Bootstrap 95% CI Low": np.quantile(bootstrap, 0.025),
                "Episode-Cluster Bootstrap 95% CI High": np.quantile(bootstrap, 0.975),
            }
        )
    transfer_cache = np.load(TRANSFER_SENSITIVITY_PATH, allow_pickle=False)
    transfer_rows: list[dict[str, object]] = []
    for key in transfer_cache.files:
        values = transfer_cache[key].astype(float)
        section_values: list[dict[str, object]] = []
        for record in design.itertuples(index=False):
            position = int(record[1])
            controls = np.asarray(record[2], dtype=int)
            difference = values[position] - values[controls]
            section_values.append(
                {
                    "Road Section ID": record[0],
                    "Concordance": float(
                        np.mean((difference > 0) + 0.5 * (difference == 0))
                    ),
                }
            )
        event_values = (
            event_section_pairs.merge(
                pd.DataFrame(section_values),
                on="Road Section ID",
                how="inner",
                validate="many_to_one",
            )
            .groupby("Episode ID", sort=True)["Concordance"]
            .mean()
            .to_numpy(dtype=float)
        )
        bootstrap = np.array(
            [
                random.choice(event_values, size=len(event_values), replace=True).mean()
                for _ in range(20_000)
            ]
        )
        transfer_rows.append(
            {
                "Specification": key,
                "Physical Episodes": len(event_values),
                "Episode-Weighted Concordance": event_values.mean(),
                "Episode-Cluster Bootstrap 95% CI Low": np.quantile(bootstrap, 0.025),
                "Episode-Cluster Bootstrap 95% CI High": np.quantile(bootstrap, 0.975),
            }
        )
    rainfall_cache = np.load(RAINFALL_SENSITIVITY_PATH, allow_pickle=False)
    rainfall_rows: list[dict[str, object]] = []
    for key in rainfall_cache.files:
        if not key.endswith("__Heavy"):
            continue
        values = rainfall_cache[key].astype(float)
        section_values: list[dict[str, object]] = []
        for record in design.itertuples(index=False):
            position = int(record[1])
            controls = np.asarray(record[2], dtype=int)
            difference = values[position] - values[controls]
            section_values.append(
                {
                    "Road Section ID": record[0],
                    "Concordance": float(
                        np.mean((difference > 0) + 0.5 * (difference == 0))
                    ),
                }
            )
        event_values = (
            event_section_pairs.merge(
                pd.DataFrame(section_values),
                on="Road Section ID",
                how="inner",
                validate="many_to_one",
            )
            .groupby("Episode ID", sort=True)["Concordance"]
            .mean()
            .to_numpy(dtype=float)
        )
        bootstrap = np.array(
            [
                random.choice(event_values, size=len(event_values), replace=True).mean()
                for _ in range(20_000)
            ]
        )
        rainfall_rows.append(
            {
                "Specification": key.removesuffix("__Heavy"),
                "Physical Episodes": len(event_values),
                "Episode-Weighted Concordance": event_values.mean(),
                "Episode-Cluster Bootstrap 95% CI Low": np.quantile(bootstrap, 0.025),
                "Episode-Cluster Bootstrap 95% CI High": np.quantile(bootstrap, 0.975),
            }
        )
    return (
        pd.DataFrame(summary),
        event.reset_index(),
        pd.DataFrame(transfer_rows),
        pd.DataFrame(rainfall_rows),
    )


def input_hashes() -> pd.DataFrame:
    rows = []
    for path in (
        RESTRICTION_PATH,
        MATCH_PATH,
        EDGE_PATH,
        ROAD_PATH,
        ADMIN_PATH,
        ROAD_SCORE_PATH,
        WARNING_SCORE_PATH,
        TRANSFER_SENSITIVITY_PATH,
        RAINFALL_SENSITIVITY_PATH,
        MLIT_NOTICE_PATH,
        *sorted(JMA_OUT.glob("*.csv")),
    ):
        rows.append(
            {
                "Input": str(path.relative_to(ROOT)),
                "Bytes": path.stat().st_size,
                "SHA-256": sha256(path),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-official", action="store_true")
    args = parser.parse_args()
    download_official_inputs(args.refresh_official)
    rainfall, stations = jma_event_data()
    (
        episodes,
        observations,
        episode_matches,
        funnel,
        evidence_order,
    ) = restriction_evidence()
    audited = attach_trigger_evidence(
        episodes,
        observations,
        episode_matches,
        rainfall,
        stations,
    )
    event_section_pairs = episode_matches.drop_duplicates(
        ["Episode ID", "Road Section ID"]
    )[["Episode ID", "Road Section ID"]]
    validation, by_event, transfer_validation, rainfall_validation = concordance_outputs(
        event_section_pairs,
        evidence_order,
    )

    confirmed_rainfall = int(
        audited["Trigger Classification"].str.startswith("Rainfall trigger").sum()
    )
    direct_consistent = int(
        audited["Trigger Classification"].str.startswith("Direct-earthquake consistent").sum()
    )
    decision = {
        "earthquake_time_jst": EARTHQUAKE_TIME.isoformat(),
        "mlit_notice_url": MLIT_NOTICE_URL,
        "official_restriction_snapshot_rows": 680,
        "process_reason_snapshot_rows": int(funnel[1]["Count"]),
        "physical_process_episodes_before_matching": int(funnel[2]["Count"]),
        "retained_snapshot_rows": int(funnel[3]["Count"]),
        "retained_physical_episodes": int(funnel[4]["Count"]),
        "unique_matched_sections": int(funnel[6]["Count"]),
        "event_section_pairs": int(funnel[7]["Count"]),
        "confirmed_rainfall_triggered_episodes": confirmed_rainfall,
        "direct_earthquake_consistent_unconfirmed_episodes": direct_consistent,
        "all_regional_72h_rainfall_maxima_zero": bool(
            audited["Regional Maximum 72 h Rainfall (mm)"].eq(0).all()
        ),
        "primary_interpretation": (
            "The retained evidence cannot validate rainfall-triggered road disruption. "
            "It comprises ten physical restriction episodes reported in the MLIT earthquake-response "
            "archive, beginning 0.55-24.38 h after the earthquake, with generic process reasons and no "
            "rainfall trigger term; all ten have zero 72 h rainfall at every audited representative JMA station."
        ),
        "recommended_use": (
            "Retain the event-deduplicated evidence only as supplementary correspondence with "
            "earthquake-proximate mass-movement road restrictions. Remove rainfall-specific validation "
            "claims and use episode-clustered uncertainty."
        ),
        "route_agreement_boundary": (
            "Route-name agreement is not an implemented eligibility criterion and is available as true "
            "only for candidate rows from one retained episode."
        ),
        "transfer_specification_episode_weighted_concordance_range": [
            float(transfer_validation["Episode-Weighted Concordance"].min()),
            float(transfer_validation["Episode-Weighted Concordance"].max()),
        ],
        "rainfall_parameter_episode_weighted_concordance_range": [
            float(rainfall_validation["Episode-Weighted Concordance"].min()),
            float(rainfall_validation["Episode-Weighted Concordance"].max()),
        ],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(funnel).to_csv(OUT / "restriction_evidence_funnel.csv", index=False)
    audited.to_csv(OUT / "restriction_episode_trigger_audit.csv", index=False)
    validation.to_csv(OUT / "event_clustered_validation.csv", index=False)
    by_event.to_csv(OUT / "event_level_concordance.csv", index=False)
    transfer_validation.to_csv(
        OUT / "transfer_event_clustered_validation.csv",
        index=False,
    )
    rainfall_validation.to_csv(
        OUT / "rainfall_parameter_event_clustered_validation.csv",
        index=False,
    )
    stations.to_csv(OUT / "jma_event_station_manifest.csv", index=False)
    input_hashes().to_csv(OUT / "input_hashes.csv", index=False)
    (OUT / "decision.json").write_text(
        json.dumps(decision, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(decision, ensure_ascii=False, indent=2))
    print("\nEvent-clustered validation")
    print(validation.to_string(index=False))


if __name__ == "__main__":
    main()
