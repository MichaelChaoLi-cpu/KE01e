#!/usr/bin/env python3
"""Summarize validated R3C2 evidence without rerunning other parameter families."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "data/exp/revision"
OUT = EXP / "reviewer-3-comment-2"
SOURCES = [
    "reviewer-3-comment-2/terrain_weight_summary.csv",
    "reviewer-3-comment-2/terrain_weight_by_seed.csv",
    "reviewer-3-comment-2/score_diagnostics.csv",
    "reviewer-2-comment-4/community_isolation_parameter_sensitivity.csv",
    "reviewer-2-comment-4/road_score_sensitivity.csv",
    "reviewer-2-comment-5/downstream_network_sensitivity.csv",
    "reviewer-3-comment-5/spatially_correlated_closure_summary.csv",
    "reviewer-4-comment-4/closure_mapping_summary.csv",
    "reviewer-2-comment-6/intervention_parameter_sensitivity.csv",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def interval(series):
    return f"{series.min():,.1f}–{series.max():,.1f}"


def main():
    decision=json.loads((OUT/"decision.json").read_text())
    assert decision["status"] == "validated"
    inputs={p:pd.read_csv(EXP/p) for p in SOURCES}
    terrain=inputs[SOURCES[0]]
    seeds=inputs[SOURCES[1]]
    diagnostics=inputs[SOURCES[2]]
    rainfall=inputs[SOURCES[3]]
    transfer=inputs[SOURCES[5]]
    transfer=transfer.loc[transfer.scenario.eq("Heavy")]
    dependence=inputs[SOURCES[6]]
    dependence=dependence.loc[dependence.scenario.eq("Heavy")]
    closure=inputs[SOURCES[7]]
    actions=inputs[SOURCES[8]]
    assert len(terrain)==9 and len(seeds)==45 and len(diagnostics)==54
    assert terrain.specification.is_unique
    weights=pd.read_csv(OUT/"weight_vectors.csv")
    assert np.allclose(weights.iloc[:,1:].sum(axis=1),2.25,atol=1e-12,rtol=0)
    paired=[]
    for row in terrain.itertuples(index=False):
        name=row.specification
        community=pd.read_csv(OUT/f"community_{name}.csv")
        pop=community.Total_Population.to_numpy()
        older=community.Population_Age_65.to_numpy()
        b=dict(np.load(OUT/f"baseline_{name}.npz",allow_pickle=False))
        a=dict(np.load(OUT/f"intervention_{name}.npz",allow_pickle=False))
        reconstructed=[]
        for seed in decision["seeds"]:
            x,y=b[str(seed)].astype(float),a[str(seed)].astype(float)
            assert np.all((x>=0)&(x<=1)&(y>=0)&(y<=x))
            assert np.allclose(x*1000,np.round(x*1000),atol=1e-4,rtol=0)
            observed=seeds.loc[seeds.specification.eq(name)&seeds.seed.eq(seed)].iloc[0]
            vals=[float(pop@x),float(older@x),float(pop@(x-y))]
            assert np.allclose(vals,observed[["isolated_population","older_isolated_population","protected_population"]].to_numpy(dtype=float),atol=1e-9,rtol=0)
            reconstructed.append(vals)
            ref=seeds.loc[seeds.specification.eq("central")&seeds.seed.eq(seed)].iloc[0]
            paired.append(dict(specification=name,seed=seed,
                isolated_population_difference=vals[0]-ref.isolated_population,
                protected_population_difference=vals[2]-ref.protected_population))
        assert np.allclose(np.mean(reconstructed,axis=0),
            [row.isolated_population,row.older_isolated_population,row.protected_population],atol=1e-9,rtol=0)
        assert abs(pop.sum()-row.eligible_population)<1e-6
        assert abs(older.sum()-row.older_population)<1e-6
    pd.DataFrame(paired).to_csv(OUT/"paired_seed_differences.csv",index=False)
    rows=[]
    def add(family,rationale,tested,endpoints,result,boundary,evidence):
        rows.append(dict(assumption_family=family,rationale=rationale,tested_alternatives=tested,
            propagated_endpoints=endpoints,observed_sensitivity=result,interpretation_limit=boundary,
            evidence=evidence))
    add("Terrain composition","Transparent fixed standardized context; not fitted effects",
        "Central plus eight one-weight x0.50/x1.50 alternatives, each normalized to sum 2.25; original scaler frozen",
        "Slope/road scores: all 9 x 3 rainfall scenarios; Heavy disconnection and fixed-budget Central intervention: all 9, five seeds x 1000 draws",
        f"Heavy disconnected residents {interval(terrain.isolated_population)}; protected residents {interval(terrain.protected_population)}; minimum community/intervention Top-30 overlap {terrain.community_top30_overlap.min():.1%}/{terrain.intervention_top30_overlap.min():.1%}",
        "Declared composition stress, not empirical coefficient bounds; no service endpoint propagation or cross-family combinations",
        SOURCES[0]+"; "+SOURCES[2])
    add("Rainfall windows and gamma","Equal-window and unit-gamma transparent references; operational-indicator compatibility checked separately",
        "Five duration-weight profiles x gamma 0.5/1/2",
        "Slope/road scores: 15 x 3 scenarios; Heavy disconnection: five prespecified settings, five seeds x 1000 draws",
        f"Heavy disconnected residents {interval(rainfall.expected_isolated_population_mean)}",
        "Not every setting propagated to every endpoint; older section-based validation superseded by event-clustered validation; not local parameter estimation",
        SOURCES[3]+"; reviewer-2-comment-7/rainfall_parameter_event_clustered_validation.csv")
    add("Slope-to-road transfer","Directional regional screening rather than calibrated physical runout",
        "15 one-parameter specifications; central/strict/permissive joint transfer settings downstream",
        "Road support/rank and matched correspondence; three rainfall scenarios for disconnection and service reachability",
        f"Heavy disconnected residents {interval(transfer.expected_isolated_population_mean)}",
        "Within-transfer boundary combinations are not a full cross-stage joint uncertainty analysis; old matched validation statistics not reused here",
        SOURCES[5]+"; reviewer-2-comment-5/downstream_service_sensitivity.csv")
    add("Closure mapping","Bounded monotone stress mapping preserves within-scenario score order",
        "Maximum propensity 0.15/0.30/0.45","Heavy Primary Emergency Road disconnection, five seeds x 1000 draws",
        f"Disconnected residents {interval(closure['Expected Disconnected Population'])}",
        "Conditional mapping range, not a calibrated closure distribution or confidence interval",SOURCES[7])
    add("Spatial closure dependence","Test the independent-road simplifying assumption",
        "Independent plus 1/3 km clusters crossed with rho 0.25/0.50",
        "Three rainfall scenarios; disconnection means, tails and community rankings, five seeds x 1000 draws",
        f"Heavy disconnected residents {interval(dependence.expected_isolated_population_mean)}",
        "Cluster scales and dependence are stress settings, not inferred co-failure parameters",SOURCES[6])
    for family,label,tested,rationale,boundary in [
        ("Effectiveness","Intervention effectiveness","Conservative/Central/Optimistic effects; Central costs and lambda fixed","Declared action-specific reduction scenarios","No measured engineering efficacy"),
        ("Cost","Intervention cost","Global x0.8/x1.2; equal-action; length-only costs; effects and lambda fixed","Relative planning units with explicit one-kilometre anchors","No local currency calibration or constructability; top-150 search can leave budget unused"),
        ("Equation 17 coefficient","Attachment coefficient","lambda=0/0.075/0.15/0.30/0.50; Central costs/effects fixed","Declared weight combining simulated attachment burden and single-road consequences","Coefficient-zero all-road correlation is tie-sensitive; no engineering interpretation")]:
        a=actions.loc[actions['Parameter Family'].isin([family,"Reference"])]
        add(label,rationale,tested,"Heavy fixed-budget intervention, five seeds x 1000 draws",
            f"Protected residents {interval(a['Protected Population'])}; minimum Top-30 overlap {a['Top-30 Overlap vs Central'].min():.1%}",boundary,SOURCES[8])
    pd.DataFrame(rows).to_csv(OUT/"staged_uncertainty_coverage.csv",index=False)
    display=terrain[["specification","isolated_population","older_isolated_population","protected_population",
        "community_top30_overlap","intervention_top30_overlap","portfolio_overlap_central"]].copy()
    md=["# Reviewer 3 Comment 2 — validated terrain sensitivity and staged uncertainty",
        "", "Status: analysis validated; manuscript/Appendix changes still require approval.", "",
        "## Terrain results", "", display.to_markdown(index=False,floatfmt=".3f"), "",
        "All values are conditional simulation outputs. Each row changes only relative terrain-weight composition; all other declared parameter families stay fixed. Population results average five 1,000-draw seed sets. Rank overlaps compare against Central. The portfolio overlap denominator is the Central selected count; this is not Jaccard similarity.", "",
        "Exact normalized coefficients are in weight_vectors.csv. Full seed means/ranges/SDs, eligible support, candidate overlap, all 27 slope/road pairs and road-level priorities are retained in the accompanying CSV/NPZ files. Quantile ties are retained in the road upper-1% sets; fixed Top-30 lists use existing NumPy argsort order.", "",
        "## Staged coverage", ""]
    for row in rows:
        md.extend([f"### {row['assumption_family']}","",
            f"- Rationale: {row['rationale']}",f"- Tested: {row['tested_alternatives']}",
            f"- Endpoints: {row['propagated_endpoints']}",f"- Finding: {row['observed_sensitivity']}",
            f"- Boundary: {row['interpretation_limit']}",f"- Evidence: `{row['evidence']}`",""])
    md.extend(["## Verification and interpretation", "",
        "Central reconstruction has zero maximum absolute difference for all three slope and road score arrays. Central Heavy disconnection reproduces 1063.5975980699063 residents and intervention protection reproduces 62.31300017163157 at budget 269.1310356545067. The first Central seed is repeated uncached and agrees exactly with the canonical simulator. Original production outputs, data inputs and manuscript assets retain their hashes.", "",
        "Shared candidate roads receive the same random variates by road-section ID even when membership changes. New candidate IDs use a separate fixed stream over their sorted union. Every evaluated intervention draw has no newly disconnected community compared with its paired baseline. Eligible mesh/community identity and population totals agree across all nine specifications. An independent post-run aggregation check reproduces all 45 seed rows and all nine summary rows from frequency archives.", "",
        "The implementation initially stopped at a tuple-unpacking error before any intervention calculation. The one-line return-value correction, original/corrected source hashes and retained valid upstream caches are disclosed in input_manifest.json; the frozen experimental specification is unchanged.", "",
        "Seed ranges/SDs describe Monte Carlo variation at a fixed specification. Parameter stress ranges describe model dependence. Inventory/coverage/matching limitations concern evidence support. These are distinct uncertainties: their ranges must not be added, pooled into a confidence interval, or called comprehensive probabilistic propagation. Existing rainfall-weight/gamma combinations and joint intervention effect/global-cost profiles do not assess cross-family interactions through the complete chain.", "",
        "No new service-endpoint sensitivity, calibrated weight estimation, alternative model selection, new validation fit or rerun of completed parameter families is performed. Formal figures, workbooks, Appendix, AnaSOP and reviewer response remain unchanged pending a complete approved manuscript proposal.", ""])
    (OUT/"analysis_report.md").write_text("\n".join(md))
    provenance={p:digest(EXP/p) for p in SOURCES}
    write=dict(status="passed",seed_rows_reaggregated=45,summary_rows_reaggregated=9,
               source_hashes=provenance,report_source_sha256=digest(Path(__file__)))
    (OUT/"synthesis_verification.json").write_text(json.dumps(write,indent=2)+"\n")
    outputs={str(p.relative_to(OUT)):digest(p) for p in OUT.iterdir() if p.is_file() and p.name!="output_hashes.json"}
    (OUT/"output_hashes.json").write_text(json.dumps(outputs,indent=2)+"\n")
    print(display.to_string(index=False))
    print("Independent reaggregation and staged synthesis passed.")


if __name__=="__main__":
    main()
