#!/usr/bin/env python3
"""Matched-seed closure-mapping sensitivity for Reviewer 4 Comment 4.

This revision-only audit compares the frozen Low, Central, and High Heavy-scenario
score-to-closure mappings with the same five prespecified seeds. It does not alter
the candidate-road set, road-score ordering, production tables, or manuscript.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

import figure_community_isolation_frequency_and_exposed_population as isolation
import revision_service_destination_rerouting_audit as context_builder


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data/exp/revision/reviewer-4-comment-4"
CACHE_DIR = OUT_DIR / "cache"
SUMMARY_PATH = OUT_DIR / "closure_mapping_summary.csv"
COMMUNITY_PATH = OUT_DIR / "closure_mapping_community.csv"
DECISION_PATH = OUT_DIR / "decision.json"
HASH_PATH = OUT_DIR / "input_hashes.csv"
REPORT_PATH = OUT_DIR / "audit_report.md"

MAPPINGS = {"Low": 0.15, "Central": 0.30, "High": 0.45}
TOP_N = 30
MATERIAL_FREQUENCY_CHANGE = 0.05


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def array_digest(array: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(array)
    digest = hashlib.sha256()
    digest.update(str(contiguous.dtype).encode())
    digest.update(str(contiguous.shape).encode())
    digest.update(contiguous.tobytes())
    return digest.hexdigest()


def cached_frequency(
    label: str,
    maximum: float,
    seed: int,
    context: dict[str, object],
) -> np.ndarray:
    central_propensity = np.asarray(context["section_propensity"], dtype="float32")
    propensity = (central_propensity * (maximum / isolation.MAX_CLOSURE_PROPENSITY)).astype(
        "float32"
    )
    signature_payload = {
        "label": label,
        "maximum": maximum,
        "seed": seed,
        "draws": isolation.MONTE_CARLO_DRAWS,
        "propensity": array_digest(propensity),
        "candidate_u": array_digest(np.asarray(context["candidate_u"])),
        "candidate_v": array_digest(np.asarray(context["candidate_v"])),
        "candidate_edge_section": array_digest(
            np.asarray(context["candidate_edge_section"])
        ),
        "target_roots": array_digest(np.asarray(context["target_roots"])),
        "attachment_community": array_digest(
            np.asarray(context["attachment_community"])
        ),
        "attachment_root": array_digest(np.asarray(context["attachment_root"])),
    }
    signature = hashlib.sha256(
        json.dumps(signature_payload, sort_keys=True).encode()
    ).hexdigest()
    path = CACHE_DIR / f"{label.lower()}_seed_{seed}_m1000.npz"
    if path.exists():
        cached = np.load(path, allow_pickle=False)
        if str(cached["signature"].item()) == signature:
            print(f"Loaded {path.name}", flush=True)
            return cached["frequency"].astype("float32")
    frequency = isolation.simulate_isolation(
        np.asarray(context["candidate_u"]),
        np.asarray(context["candidate_v"]),
        np.asarray(context["candidate_edge_section"]),
        propensity,
        int(context["root_count"]),
        np.asarray(context["target_roots"]),
        np.asarray(context["attachment_community"]),
        np.asarray(context["attachment_root"]),
        len(context["community"]),
        seed,
        draws=isolation.MONTE_CARLO_DRAWS,
        report_progress=False,
    )
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, signature=np.asarray(signature), frequency=frequency)
    print(f"Saved {path.name}", flush=True)
    return frequency


def top_positions(burden: np.ndarray, community_ids: np.ndarray) -> np.ndarray:
    order = np.lexsort((community_ids.astype(str), -burden))
    return order[: min(TOP_N, len(order))]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    context = context_builder.build_context()
    community = context["community"].copy()
    population = community["Total_Population"].to_numpy(dtype="float64")
    community_ids = community["Community ID"].astype(str).to_numpy()

    seed_frequencies: dict[str, list[np.ndarray]] = {}
    mean_frequencies: dict[str, np.ndarray] = {}
    seed_populations: dict[str, np.ndarray] = {}
    top_sets: dict[str, set[str]] = {}
    for label, maximum in MAPPINGS.items():
        seed_frequencies[label] = [
            cached_frequency(label, maximum, seed, context)
            for seed in isolation.REPLICATE_SEEDS
        ]
        stacked = np.vstack(seed_frequencies[label])
        mean_frequencies[label] = np.mean(stacked, axis=0).astype("float64")
        seed_populations[label] = np.asarray(
            [float(np.sum(population * frequency)) for frequency in stacked]
        )
        burden = population * mean_frequencies[label]
        positions = top_positions(burden, community_ids)
        top_sets[label] = set(community_ids[positions])

    central_population = float(np.mean(seed_populations["Central"]))
    central_frequency = mean_frequencies["Central"]
    central_top = top_sets["Central"]
    summary_rows: list[dict[str, object]] = []
    for label, maximum in MAPPINGS.items():
        values = seed_populations[label]
        frequency = mean_frequencies[label]
        correlation = float(spearmanr(central_frequency, frequency).statistic)
        overlap = len(central_top & top_sets[label]) / len(central_top)
        summary_rows.append(
            {
                "Closure Mapping": label,
                "Maximum Section Closure Propensity": maximum,
                "Expected Disconnected Population": float(np.mean(values)),
                "Seed Minimum": float(np.min(values)),
                "Seed Maximum": float(np.max(values)),
                "Seed Standard Deviation": float(np.std(values, ddof=1)),
                "Relative Change from Central": float(
                    np.mean(values) / central_population - 1.0
                ),
                "Frequency Spearman Correlation with Central": correlation,
                "Top-30 Burden Overlap with Central": overlap,
                "Communities with Absolute Frequency Change >= 0.05": int(
                    np.count_nonzero(np.abs(frequency - central_frequency) >= 0.05)
                ),
            }
        )
    summary = pd.DataFrame(summary_rows)

    community_output = community[
        ["Community ID", "Total_Population", "Population_Age_65", "Longitude", "Latitude"]
    ].copy()
    for label in MAPPINGS:
        community_output[f"{label} Mean Disconnection Frequency"] = mean_frequencies[label]
        community_output[f"{label} Population-Weighted Burden"] = (
            population * mean_frequencies[label]
        )
        community_output[f"{label} Top-30 Burden"] = community_output["Community ID"].isin(
            top_sets[label]
        )

    three_way = set.intersection(*(top_sets[label] for label in MAPPINGS))
    central_seed_sd = float(
        summary.loc[
            summary["Closure Mapping"] == "Central", "Seed Standard Deviation"
        ].iloc[0]
    )
    structural_span = float(
        summary["Expected Disconnected Population"].max()
        - summary["Expected Disconnected Population"].min()
    )
    decision = {
        "scenario": "Heavy",
        "target": isolation.PRIMARY_TARGET_NAME,
        "draws_per_seed": isolation.MONTE_CARLO_DRAWS,
        "seeds": list(isolation.REPLICATE_SEEDS),
        "mapping_maxima": MAPPINGS,
        "low_high_expected_population_span": structural_span,
        "central_seed_standard_deviation": central_seed_sd,
        "span_to_central_seed_sd_ratio": structural_span / central_seed_sd,
        "three_way_top_30_intersection_count": len(three_way),
        "three_way_top_30_intersection_share": len(three_way) / TOP_N,
        "interpretation": (
            "Use Central as the transparent reference, High for capacity stress testing, "
            "and priorities common across all mappings for robust action. Treat local rank "
            "changes as targets for data collection; Low/High are not confidence limits."
        ),
    }

    summary.to_csv(SUMMARY_PATH, index=False, float_format="%.10g")
    community_output.to_csv(COMMUNITY_PATH, index=False, float_format="%.10g")
    DECISION_PATH.write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")

    input_paths = [
        Path(__file__),
        Path(context_builder.__file__).resolve(),
        Path(isolation.__file__).resolve(),
        context_builder.ADMIN_PATH,
        context_builder.ROAD_PATH,
        context_builder.EDGE_PATH,
        context_builder.NODE_PATH,
        isolation.MESH_PATH,
        isolation.GROUP_PATH,
    ]
    pd.DataFrame(
        [{"Path": str(path.relative_to(ROOT)), "SHA-256": sha256(path)} for path in input_paths]
    ).to_csv(HASH_PATH, index=False)

    low_value = float(
        summary.loc[
            summary["Closure Mapping"] == "Low", "Expected Disconnected Population"
        ].iloc[0]
    )
    high_value = float(
        summary.loc[
            summary["Closure Mapping"] == "High", "Expected Disconnected Population"
        ].iloc[0]
    )
    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Reviewer 4 Comment 4 Audit",
                "",
                "## Matched-estimator result",
                "",
                f"The five-seed Low-to-High range is {low_value:,.1f}–{high_value:,.1f} expected disconnected residents.",
                f"The Central five-seed estimate is {central_population:,.1f}; its across-seed SD is {central_seed_sd:,.1f}.",
                f"The Low-to-High structural span is {structural_span:,.1f}, or {structural_span / central_seed_sd:,.1f} times the Central seed SD.",
                f"The three mappings share {len(three_way)} of the top {TOP_N} population-burden communities ({len(three_way) / TOP_N:.1%}).",
                "",
                "## Decision interpretation",
                "",
                "The mapping range represents structural planning uncertainty, not a confidence interval. Central remains the reference case; High is a capacity stress test rather than a default forecast. Common priorities support robust action, while locations with material rank or frequency changes should be prioritized for road-failure and slope-to-road blockage data collection.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(summary.to_string(index=False), flush=True)
    print(json.dumps(decision, indent=2), flush=True)


if __name__ == "__main__":
    main()
