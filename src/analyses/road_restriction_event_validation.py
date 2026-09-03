#!/usr/bin/env python3
"""Shared event-level road-restriction correspondence utilities.

The official restriction data contain repeated snapshots.  This module keeps
snapshot rows, physical restriction episodes, matched network sections, and
matched controls as distinct units and treats the physical episode as the
independent resampling unit.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from rasterio.features import rasterize
import shapely


PROCESS_REASONS = ("落石", "法面崩落", "土砂流入")
EPISODE_KEYS = [
    "Start Address",
    "End Address",
    "Restriction Reason",
    "Restriction Start Time",
]


@dataclass(frozen=True)
class RestrictionEvidence:
    restrictions: pd.DataFrame
    process_snapshots: pd.DataFrame
    retained_snapshots: pd.DataFrame
    retained_episodes: pd.DataFrame
    observation_episode: pd.DataFrame
    episode_matches: pd.DataFrame
    event_section_pairs: pd.DataFrame
    funnel: pd.DataFrame


def load_restriction_evidence(
    restriction_path: Path,
    match_path: Path,
    edge_path: Path,
    eligible_section_ids: pd.Series,
) -> RestrictionEvidence:
    """Reconstruct physical episodes and their eligible road links."""
    restrictions = pd.read_parquet(restriction_path).reset_index(drop=True)
    restrictions.insert(
        0,
        "Restriction Observation ID",
        [f"RR-{index:06d}" for index in range(1, len(restrictions) + 1)],
    )
    matches = pd.read_parquet(match_path)
    edges = pd.read_parquet(edge_path, columns=["Road Edge ID", "Road Section ID"])
    eligible_sections = set(eligible_section_ids.astype(str))

    process_snapshots = restrictions[
        restrictions["Restriction Reason"].isin(PROCESS_REASONS)
    ].copy()
    reliable = (
        matches["Restriction Reason"].isin(PROCESS_REASONS)
        & matches["Road Edge Match Status"].eq("matched_primary")
        & matches["Road Edge Match Distance (m)"].le(50)
    )
    reliable_matches = matches.loc[reliable].drop_duplicates(
        ["Restriction Observation ID", "Snapshot Time", "Matched Road Edge ID"]
    )
    retained_snapshots = restrictions.merge(
        reliable_matches[["Restriction Observation ID"]].drop_duplicates(),
        on="Restriction Observation ID",
        how="inner",
        validate="one_to_one",
    )

    all_episodes = process_snapshots.drop_duplicates(EPISODE_KEYS)
    retained_episodes = (
        retained_snapshots.drop_duplicates(EPISODE_KEYS)
        .sort_values(
            ["Restriction Start Time", "Start Address", "End Address"],
            kind="stable",
        )
        .reset_index(drop=True)
    )
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

    unique_edges = episode_matches["Road Edge ID"].nunique()
    unique_sections = event_section_pairs["Road Section ID"].nunique()
    funnel = pd.DataFrame(
        [
            ("All official restriction snapshot rows", len(restrictions)),
            (
                "Snapshot rows with rockfall, slope collapse, or sediment inflow reason",
                len(process_snapshots),
            ),
            ("Physical process episodes before spatial matching", len(all_episodes)),
            (
                "Snapshot rows retained by matched_primary and <=50 m rule",
                retained_snapshots["Restriction Observation ID"].nunique(),
            ),
            ("Physical episodes retained in the Kumamoto network", len(retained_episodes)),
            ("Unique matched network edges", unique_edges),
            ("Unique matched network sections", unique_sections),
            ("Event-section pairs", len(event_section_pairs)),
        ],
        columns=["Stage", "Count"],
    )
    return RestrictionEvidence(
        restrictions=restrictions,
        process_snapshots=process_snapshots,
        retained_snapshots=retained_snapshots,
        retained_episodes=retained_episodes,
        observation_episode=observation_episode,
        episode_matches=episode_matches,
        event_section_pairs=event_section_pairs,
        funnel=funnel,
    )


def build_matched_design(
    roads: pd.DataFrame,
    road_geometry: np.ndarray,
    event_section_pairs: pd.DataFrame,
    admin_geometry: np.ndarray,
    display_shape: tuple[int, int],
    display_transform: object,
    extent: tuple[float, float, float, float],
    sample_grid: Callable[[np.ndarray, np.ndarray, tuple[float, float, float, float]], np.ndarray],
) -> pd.DataFrame:
    """Build the fixed section-level matched-control design."""
    municipality_grid = rasterize(
        ((geometry, index + 1) for index, geometry in enumerate(admin_geometry)),
        out_shape=display_shape,
        transform=display_transform,
        fill=0,
        all_touched=True,
        dtype="int16",
    )
    midpoints = shapely.line_interpolate_point(road_geometry, 0.5, normalized=True)
    municipality_index = sample_grid(
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
        event_section_pairs["Road Section ID"]
        .astype(str)
        .drop_duplicates()
        .map(lookup)
        .dropna()
        .astype(int)
    )
    evidence_set = set(evidence_positions.tolist())
    random = np.random.default_rng(20260812)
    rows: list[dict[str, object]] = []
    for position in evidence_positions:
        eligible = (
            (municipality_index == municipality_index[position])
            & (road_category == road_category[position])
            & (emergency_class == emergency_class[position])
            & (length_decile == length_decile[position])
        )
        candidates = np.array(
            [candidate for candidate in np.flatnonzero(eligible) if candidate not in evidence_set],
            dtype=int,
        )
        if not candidates.size:
            continue
        controls = random.choice(candidates, size=min(10, candidates.size), replace=False)
        rows.append(
            {
                "Road Section ID": roads.iloc[position]["Road Section ID"],
                "Evidence Position": int(position),
                "Control Positions": controls,
                "Control Count": len(controls),
            }
        )
    return pd.DataFrame(rows)


def event_weighted_concordance(
    scores: np.ndarray,
    design: pd.DataFrame,
    event_section_pairs: pd.DataFrame,
    bootstrap_seed: int = 20260903,
    bootstrap_draws: int = 20_000,
    bootstrap_random: np.random.Generator | None = None,
) -> dict[str, object]:
    """Compute equal-episode concordance and episode-cluster uncertainty."""
    section_rows: list[dict[str, object]] = []
    for record in design.itertuples(index=False):
        position = int(record[1])
        controls = np.asarray(record[2], dtype=int)
        difference = scores[position] - scores[controls]
        section_rows.append(
            {
                "Road Section ID": record[0],
                "Section Concordance": float(
                    np.mean((difference > 0) + 0.5 * (difference == 0))
                ),
                "Control Count": int(record[3]),
            }
        )
    section = pd.DataFrame(section_rows)
    event_values = (
        event_section_pairs.merge(
            section,
            on="Road Section ID",
            how="inner",
            validate="many_to_one",
        )
        .groupby("Episode ID", sort=True)["Section Concordance"]
        .mean()
    )
    random = (
        bootstrap_random
        if bootstrap_random is not None
        else np.random.default_rng(bootstrap_seed)
    )
    values = event_values.to_numpy(dtype=float)
    bootstrap = np.array(
        [random.choice(values, size=len(values), replace=True).mean() for _ in range(bootstrap_draws)]
    )
    return {
        "Physical Episodes": int(len(values)),
        "Evidence Sections": int(event_section_pairs["Road Section ID"].nunique()),
        "Matched Evidence Sections": int(len(section)),
        "Matched Controls": int(section["Control Count"].sum()),
        "Road Score Concordance": float(values.mean()),
        "Road Score CI Low": float(np.quantile(bootstrap, 0.025)),
        "Road Score CI High": float(np.quantile(bootstrap, 0.975)),
        "Event Concordance Values": event_values,
        "Section Concordance": section,
    }


def paired_event_contrast(
    left: pd.Series,
    right: pd.Series,
    bootstrap_seed: int = 20260903,
    bootstrap_draws: int = 20_000,
    bootstrap_random: np.random.Generator | None = None,
) -> tuple[float, float, float]:
    """Return a paired equal-episode contrast and cluster-bootstrap interval."""
    paired = pd.concat([left.rename("left"), right.rename("right")], axis=1).dropna()
    values = (paired["left"] - paired["right"]).to_numpy(dtype=float)
    random = (
        bootstrap_random
        if bootstrap_random is not None
        else np.random.default_rng(bootstrap_seed)
    )
    bootstrap = np.array(
        [random.choice(values, size=len(values), replace=True).mean() for _ in range(bootstrap_draws)]
    )
    return (
        float(values.mean()),
        float(np.quantile(bootstrap, 0.025)),
        float(np.quantile(bootstrap, 0.975)),
    )
