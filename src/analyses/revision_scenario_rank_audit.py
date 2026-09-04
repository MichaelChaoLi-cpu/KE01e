#!/usr/bin/env python3
"""Read-only audit of frozen cross-rainfall road rankings for Reviewer 3 C3.

Print JSON to stdout. Never rebuild caches, refit a model, or run simulations.
Use average-rank Spearman statistics; top-1% sets include quantile-boundary
ties, with intersection divided by the smaller selected set (project rule).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
SCENARIOS = ("Moderate", "Heavy", "Extreme")
PATHS = {
    "paired": ROOT / "data/exp/revision/reviewer-2-comment-3/threshold_score_arrays.npz",
    "production_roads": ROOT / "data/results/intermediate/road_disruption_scores_normalized_v4_y075.npz",
    "production_terrain": ROOT / "data/results/intermediate/landslide_score_grids_event_idw_v4_y075.npz",
    "parameter_roads": ROOT / "data/exp/revision/reviewer-2-comment-4/road_scores_15x3_scenarios.npz",
}


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main() -> None:
    hashes = {str(p.relative_to(ROOT)): sha256(p) for p in PATHS.values()}
    archives = {key: np.load(path, allow_pickle=False) for key, path in PATHS.items()}
    paired, production, terrain, parameters = (
        archives[key] for key in ("paired", "production_roads", "production_terrain", "parameter_roads")
    )
    roads = {s: paired[f"official_road_{s}"] for s in SCENARIOS}
    checks = {}
    for s in SCENARIOS:
        checks[f"production_road_equal_{s}"] = bool(np.array_equal(roads[s], production[f"score_{s}"], equal_nan=True))
        checks[f"production_slope_equal_{s}"] = bool(np.array_equal(paired[f"official_slope_{s}"], terrain[f"score_{s}"], equal_nan=True))
        checks[f"parameter_central_equal_{s}"] = bool(np.allclose(roads[s], parameters[f"equal__g1.00__{s}"], atol=1e-6, rtol=0, equal_nan=True))
    finite = np.logical_and.reduce([np.isfinite(roads[s]) for s in SCENARIOS])
    positive = finite & np.logical_or.reduce([roads[s] > 0 for s in SCENARIOS])
    checks["identical_positive_support"] = all(np.array_equal(roads[s] > 0, positive) for s in SCENARIOS)
    checks["ordered_road_magnitudes"] = bool(np.all(roads["Moderate"][finite] <= roads["Heavy"][finite] + 1e-7) and np.all(roads["Heavy"][finite] <= roads["Extreme"][finite] + 1e-7))
    comparisons = []
    for scenario in ("Moderate", "Extreme"):
        for support_name, mask in (("all_finite_sections", finite), ("positive_score_union", positive)):
            x, y = roads[scenario][mask], roads["Heavy"][mask]
            tx, ty = x >= np.quantile(x, .99), y >= np.quantile(y, .99)
            comparisons.append({
                "scenario": scenario, "reference": "Heavy", "support": support_name,
                "n": int(mask.sum()), "spearman_rho": float(spearmanr(x, y).statistic),
                "top1_scenario_count": int(tx.sum()), "top1_reference_count": int(ty.sum()),
                "top1_intersection": int((tx & ty).sum()),
                "top1_overlap": float((tx & ty).sum() / min(tx.sum(), ty.sum())),
            })
    loading = {}
    for scenario in ("Moderate", "Extreme"):
        mask = np.isfinite(terrain["score_Heavy"]) & (terrain["load_Heavy"] > 0) & (terrain[f"load_{scenario}"] > 0)
        log_ratio = np.log(terrain[f"load_{scenario}"][mask] / terrain["load_Heavy"][mask])
        loading[scenario] = dict(zip(("min", "p05", "p50", "p95", "max"), map(float, np.quantile(log_ratio, [0, .05, .5, .95, 1]))))
    checks["inputs_unchanged"] = all(sha256(ROOT / p) == h for p, h in hashes.items())
    report = {
        "comment": "reviewer-3/comment-3", "input_sha256": hashes,
        "audit_script_sha256": sha256(Path(__file__)), "checks": checks,
        "all_checks_pass": all(checks.values()), "common_zero_sections": int((finite & ~positive).sum()),
        "positive_score_medians": {s: float(np.median(roads[s][positive])) for s in SCENARIOS},
        "rank_comparisons": comparisons, "terrain_log_loading_ratio_vs_heavy": loading,
        "interpretation": "Near-invariant ordering persists after common-zero removal. Loading ratios vary spatially, so exact rank invariance is not an algebraic identity. These diagnostics do not validate rainfall-triggered failures or an event-specific spatial forecast.",
    }
    print(json.dumps(report, indent=2, allow_nan=False))
    if not report["all_checks_pass"]:
        raise SystemExit("Frozen-input agreement check failed; do not use report for manuscript edits.")


if __name__ == "__main__":
    main()
