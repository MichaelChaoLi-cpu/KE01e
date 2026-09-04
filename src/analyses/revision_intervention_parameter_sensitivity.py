#!/usr/bin/env python3
"""One-family-at-a-time intervention sensitivity for Reviewer 2 Comment 6.

The audit holds the Heavy scenario, candidate-road set, Primary Emergency Road
target, action assignment, fixed Central budget, and Monte Carlo streams constant.
It changes action effects, cost structure, or Equation 17's attachment coefficient
one family at a time. Outputs are revision evidence and do not alter formal results.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_intervention_priorities_and_budgeted_benefits as intervention
import table_priority_road_sections as priority_table


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data/exp/revision/reviewer-2-comment-6"
CACHE_DIR = OUT_DIR / "cache"
SUMMARY_PATH = OUT_DIR / "intervention_parameter_sensitivity.csv"
SEED_PATH = OUT_DIR / "intervention_parameter_sensitivity_by_seed.csv"
DECISION_PATH = OUT_DIR / "decision.json"
HASH_PATH = OUT_DIR / "input_hashes.csv"
REPORT_PATH = OUT_DIR / "audit_report.md"

TOP_N = 30
PORTFOLIO_POOL = 150
REFERENCE_LAMBDA = 0.15
REFERENCE_EFFECTS = {
    "Temporary reinforcement": 0.45,
    "Clearance pre-positioning": 0.20,
    "Alternative-route protection": 0.35,
}
EFFECT_PROFILES = {
    "Conservative effects": {
        "Temporary reinforcement": 0.25,
        "Clearance pre-positioning": 0.10,
        "Alternative-route protection": 0.20,
    },
    "Central reference": REFERENCE_EFFECTS,
    "Optimistic effects": {
        "Temporary reinforcement": 0.60,
        "Clearance pre-positioning": 0.30,
        "Alternative-route protection": 0.50,
    },
}
LAMBDA_VALUES = {
    "Lambda 0": 0.0,
    "Lambda 0.075": 0.075,
    "Central reference": REFERENCE_LAMBDA,
    "Lambda 0.30": 0.30,
    "Lambda 0.50": 0.50,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def array_digest(array: np.ndarray) -> str:
    value = np.ascontiguousarray(array)
    digest = hashlib.sha256()
    digest.update(str(value.dtype).encode())
    digest.update(str(value.shape).encode())
    digest.update(value.tobytes())
    return digest.hexdigest()


def action_vector(actions: np.ndarray, values: dict[str, float]) -> np.ndarray:
    return np.asarray([values[str(action)] for action in actions], dtype="float64")


def recover_length_km(actions: np.ndarray, base_cost: np.ndarray) -> np.ndarray:
    length = np.empty(len(actions), dtype="float64")
    reinforcement = actions == "Temporary reinforcement"
    alternative = actions == "Alternative-route protection"
    clearance = ~(reinforcement | alternative)
    length[reinforcement] = (base_cost[reinforcement] - 3.0) / 2.0
    length[alternative] = (base_cost[alternative] - 2.5) / 1.2
    length[clearance] = (base_cost[clearance] - 1.5) / 0.5
    if np.any(length < -1e-9):
        raise RuntimeError("Recovered a negative road length from the reference costs.")
    return np.maximum(length, 0.0)


def cost_profiles(
    actions: np.ndarray,
    reference_cost: np.ndarray,
) -> dict[str, np.ndarray]:
    length = recover_length_km(actions, reference_cost)
    anchor = action_vector(
        actions,
        {
            "Temporary reinforcement": 5.0,
            "Clearance pre-positioning": 2.0,
            "Alternative-route protection": 3.7,
        },
    )
    return {
        "Global cost x0.8": reference_cost * 0.8,
        "Central reference": reference_cost,
        "Global cost x1.2": reference_cost * 1.2,
        "Equal-action cost": 2.0 + length,
        "Length-only cost": anchor * length,
    }


def cached_frequency(
    label: str,
    selected: np.ndarray,
    effects: np.ndarray,
    seed: int,
    context: dict[str, object],
) -> np.ndarray:
    propensity = np.asarray(context["Section Propensity"], dtype="float64").copy()
    propensity[selected] *= 1.0 - effects[selected]
    arrays = {
        "selected": selected,
        "effects": effects,
        "propensity": propensity,
        "candidate_u": np.asarray(context["Candidate U"]),
        "candidate_v": np.asarray(context["Candidate V"]),
        "candidate_edge_section": np.asarray(context["Candidate Edge Section"]),
        "target_roots": np.asarray(context["Target Roots"]),
        "attachment_community": np.asarray(context["Attachment Community"]),
        "attachment_root": np.asarray(context["Attachment Root"]),
    }
    signature_payload = {
        "label": label,
        "seed": seed,
        "draws": isolation.MONTE_CARLO_DRAWS,
        **{key: array_digest(value) for key, value in arrays.items()},
    }
    signature = hashlib.sha256(
        json.dumps(signature_payload, sort_keys=True).encode()
    ).hexdigest()
    safe_label = label.lower().replace(" ", "_").replace(".", "p")
    path = CACHE_DIR / f"{safe_label}_seed_{seed}_m1000.npz"
    if path.exists():
        cached = np.load(path, allow_pickle=False)
        if str(cached["signature"].item()) == signature:
            print(f"Loaded {path.name}", flush=True)
            return cached["frequency"].astype("float32")
    frequency = intervention.quiet_isolation_frequency(
        np.asarray(context["Candidate U"]),
        np.asarray(context["Candidate V"]),
        np.asarray(context["Candidate Edge Section"]),
        propensity,
        int(context["Root Count"]),
        np.asarray(context["Target Roots"]),
        np.asarray(context["Attachment Community"]),
        np.asarray(context["Attachment Root"]),
        len(np.asarray(context["Community Population"])),
        seed,
    )
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, signature=np.asarray(signature), frequency=frequency)
    print(f"Saved {path.name}", flush=True)
    return frequency


def setting_specs(
    actions: np.ndarray,
    reference_cost: np.ndarray,
) -> list[dict[str, object]]:
    specs: list[dict[str, object]] = []
    for label, effects in EFFECT_PROFILES.items():
        if label == "Central reference":
            continue
        specs.append(
            {
                "family": "Effectiveness",
                "setting": label,
                "lambda": REFERENCE_LAMBDA,
                "effects": action_vector(actions, effects),
                "costs": reference_cost,
            }
        )
    for label, costs in cost_profiles(actions, reference_cost).items():
        if label == "Central reference":
            continue
        specs.append(
            {
                "family": "Cost",
                "setting": label,
                "lambda": REFERENCE_LAMBDA,
                "effects": action_vector(actions, REFERENCE_EFFECTS),
                "costs": costs,
            }
        )
    for label, coefficient in LAMBDA_VALUES.items():
        if label == "Central reference":
            continue
        specs.append(
            {
                "family": "Equation 17 coefficient",
                "setting": label,
                "lambda": coefficient,
                "effects": action_vector(actions, REFERENCE_EFFECTS),
                "costs": reference_cost,
            }
        )
    return specs


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _, context = priority_table.build_table()
    actions = np.asarray(context["Actions"], dtype=object)
    reference_cost = np.asarray(context["Base Cost"], dtype="float64")
    population = np.asarray(context["Community Population"], dtype="float64")
    baseline = {
        int(seed): np.asarray(frequency, dtype="float64")
        for seed, frequency in dict(context["Baseline Frequencies"]).items()
    }
    baseline_mean = np.mean(np.vstack(list(baseline.values())), axis=0)
    burden = intervention.section_burden_from_frequency(
        baseline_mean,
        population,
        np.asarray(context["Attachment Community"]),
        np.asarray(context["Attachment Root"]),
        np.asarray(context["Candidate U"]),
        np.asarray(context["Candidate V"]),
        np.asarray(context["Candidate Edge Section"]),
        int(context["Root Count"]),
        len(actions),
    )
    current_proxy = np.asarray(context["Consequence Proxy"], dtype="float64")
    single_close = current_proxy - REFERENCE_LAMBDA * burden
    reference_effect = action_vector(actions, REFERENCE_EFFECTS)
    reference_score = current_proxy * reference_effect / np.maximum(reference_cost, 1e-9)
    reference_order = np.argsort(reference_score)[::-1]
    production_order = np.asarray(context["Priority Order"])
    if not np.array_equal(reference_order, production_order):
        raise RuntimeError("Central reference does not reproduce the formal priority order.")
    reference_budget = float(reference_cost[reference_order[:100]].sum())

    specs = [
        {
            "family": "Reference",
            "setting": "Central reference",
            "lambda": REFERENCE_LAMBDA,
            "effects": reference_effect,
            "costs": reference_cost,
        }
    ] + setting_specs(actions, reference_cost)

    result_rows: list[dict[str, object]] = []
    seed_rows: list[dict[str, object]] = []
    reference_top30 = set(reference_order[:TOP_N])
    reference_top150 = set(reference_order[:PORTFOLIO_POOL])
    selected_reference, _ = intervention.select_under_budget(
        reference_order[:PORTFOLIO_POOL], reference_cost, reference_budget
    )
    reference_selected_set = set(selected_reference.tolist())

    raw_results: list[dict[str, object]] = []
    for spec in specs:
        label = str(spec["setting"])
        coefficient = float(spec["lambda"])
        effects = np.asarray(spec["effects"], dtype="float64")
        costs = np.asarray(spec["costs"], dtype="float64")
        consequence = single_close + coefficient * burden
        score = consequence * effects / np.maximum(costs, 1e-9)
        order = np.argsort(score)[::-1]
        selected, spent = intervention.select_under_budget(
            order[:PORTFOLIO_POOL], costs, reference_budget
        )
        protected_values: list[float] = []
        cache_label = f"{spec['family']}_{label}"
        for seed in isolation.REPLICATE_SEEDS:
            frequency = cached_frequency(cache_label, selected, effects, seed, context).astype(
                "float64"
            )
            reduction = np.maximum(baseline[int(seed)] - frequency, 0.0)
            protected = float(np.sum(population * reduction))
            protected_values.append(protected)
            seed_rows.append(
                {
                    "Parameter Family": spec["family"],
                    "Setting": label,
                    "Seed": int(seed),
                    "Protected Population": protected,
                }
            )
        selected_actions = actions[selected]
        raw_results.append(
            {
                "Parameter Family": spec["family"],
                "Setting": label,
                "Attachment Coefficient": coefficient,
                "Positive Score Road Count": int(np.count_nonzero(score > 0)),
                "Score Spearman vs Central": float(
                    spearmanr(reference_score, score).statistic
                ),
                "Top-30 Overlap vs Central": len(reference_top30 & set(order[:TOP_N]))
                / TOP_N,
                "Top-150 Overlap vs Central": len(
                    reference_top150 & set(order[:PORTFOLIO_POOL])
                )
                / PORTFOLIO_POOL,
                "Selected Road Count": len(selected),
                "Selected-Portfolio Overlap vs Central": len(
                    reference_selected_set & set(selected.tolist())
                )
                / max(len(reference_selected_set), 1),
                "Realized Planning Cost": spent,
                "Temporary Reinforcement Count": int(
                    np.count_nonzero(selected_actions == "Temporary reinforcement")
                ),
                "Clearance Pre-positioning Count": int(
                    np.count_nonzero(selected_actions == "Clearance pre-positioning")
                ),
                "Alternative-route Protection Count": int(
                    np.count_nonzero(selected_actions == "Alternative-route protection")
                ),
                "Protected Population": float(np.mean(protected_values)),
                "Protected Population Seed Minimum": float(np.min(protected_values)),
                "Protected Population Seed Maximum": float(np.max(protected_values)),
            }
        )

    reference_protected = next(
        row["Protected Population"]
        for row in raw_results
        if row["Parameter Family"] == "Reference"
    )
    for row in raw_results:
        row["Protected Population Change vs Central"] = (
            float(row["Protected Population"]) / float(reference_protected) - 1.0
        )
        result_rows.append(row)
    summary = pd.DataFrame(result_rows)
    seed_output = pd.DataFrame(seed_rows)
    summary.to_csv(SUMMARY_PATH, index=False, float_format="%.10g")
    seed_output.to_csv(SEED_PATH, index=False, float_format="%.10g")

    alternatives = summary.loc[summary["Parameter Family"] != "Reference"].copy()
    minimum_spearman = float(alternatives["Score Spearman vs Central"].min())
    minimum_top30 = float(alternatives["Top-30 Overlap vs Central"].min())
    maximum_change = float(
        alternatives["Protected Population Change vs Central"].abs().max()
    )
    decision = {
        "scenario": "Heavy",
        "target": isolation.PRIMARY_TARGET_NAME,
        "draws_per_seed": isolation.MONTE_CARLO_DRAWS,
        "seeds": list(isolation.REPLICATE_SEEDS),
        "fixed_budget_relative_planning_units": reference_budget,
        "reference_protected_population": reference_protected,
        "minimum_score_spearman": minimum_spearman,
        "minimum_top_30_overlap": minimum_top30,
        "maximum_absolute_protected_population_change": maximum_change,
        "ranking_high_stability_gate": minimum_spearman >= 0.90 and minimum_top30 >= 0.70,
        "consequence_magnitude_sensitive_gate": maximum_change >= 0.20,
        "interpretation": (
            "The tested parameters are declared planning assumptions. Stability results "
            "diagnose assumption dependence and do not validate engineering effects or costs."
        ),
    }
    DECISION_PATH.write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")

    input_paths = [
        Path(__file__),
        Path(priority_table.__file__).resolve(),
        Path(intervention.__file__).resolve(),
        Path(isolation.__file__).resolve(),
        priority_table.ADMIN_PATH,
        priority_table.ROAD_PATH,
        priority_table.EDGE_PATH,
        priority_table.NODE_PATH,
    ]
    pd.DataFrame(
        [{"Path": str(path.relative_to(ROOT)), "SHA-256": sha256(path)} for path in input_paths]
    ).to_csv(HASH_PATH, index=False)

    family_lines: list[str] = []
    for family in ("Effectiveness", "Cost", "Equation 17 coefficient"):
        subset = summary.loc[summary["Parameter Family"] == family]
        family_lines.append(
            f"- {family}: score correlations {subset['Score Spearman vs Central'].min():.3f}–"
            f"{subset['Score Spearman vs Central'].max():.3f}; Top-30 overlap "
            f"{subset['Top-30 Overlap vs Central'].min():.1%}–"
            f"{subset['Top-30 Overlap vs Central'].max():.1%}; protected population "
            f"{subset['Protected Population'].min():.1f}–"
            f"{subset['Protected Population'].max():.1f}."
        )
    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Reviewer 2 Comment 6 Audit",
                "",
                "## Design",
                "",
                f"The audit uses a fixed budget of {reference_budget:.3f} relative planning units, five prespecified seeds, and 1,000 Heavy-scenario draws per seed. Effectiveness, cost, and Equation 17's attachment coefficient are varied one family at a time.",
                "",
                "## Results",
                "",
                f"The Central reference protects {reference_protected:.1f} residents.",
                *family_lines,
                "",
                "## Decision gates",
                "",
                f"- Minimum score Spearman correlation: {minimum_spearman:.3f}.",
                f"- Minimum Top-30 overlap: {minimum_top30:.1%}.",
                f"- Maximum absolute protected-population change: {maximum_change:.1%}.",
                f"- High ranking stability gate: {'passed' if decision['ranking_high_stability_gate'] else 'failed'}.",
                f"- Consequence magnitude sensitivity gate: {'triggered' if decision['consequence_magnitude_sensitive_gate'] else 'not triggered'}.",
                "",
                "## Evidence boundary",
                "",
                "These comparisons test internal dependence on declared planning assumptions. They do not calibrate action effectiveness, convert relative planning units into currency, establish site-specific constructability, or validate lambda as an engineering coefficient.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(summary.to_string(index=False), flush=True)
    print(json.dumps(decision, indent=2), flush=True)


if __name__ == "__main__":
    main()
