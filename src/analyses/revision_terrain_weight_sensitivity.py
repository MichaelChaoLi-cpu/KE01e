#!/usr/bin/env python3
"""Frozen R3C2 terrain-composition stress test; revision-only outputs.

Run with the project Python. Reuses pure production helpers, never production
cache writers. All nine alternatives share road-ID-aligned random numbers.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import numpy as np
import pandas as pd
import shapely
from rasterio.features import rasterize
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.special import expit
from scipy.stats import spearmanr

import _hazard_validation_shared as validation
import figure_official_threshold_adjusted_landslide_disruption_score as terrain
import figure_road_disruption_exposure_and_observed_restriction_evidence as road
import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_intervention_priorities_and_budgeted_benefits as intervention

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/exp/revision/reviewer-3-comment-2"
SPEC = ROOT / "Rev/docs/analysis-spec-reviewer-3-comment-2.md"
GRID = ROOT / "data/results/intermediate/landslide_score_grids_event_idw_v4_y075.npz"
ROAD = ROOT / "data/results/intermediate/road_disruption_scores_normalized_v4_y075.npz"
SCENARIOS = ("Moderate", "Heavy", "Extreme")
BASE = np.array([0.15, 1.0, 0.35, 0.75])
BUDGET = 269.1310356545067


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def specifications():
    result = {"central": BASE.copy()}
    for i, feature in enumerate(("elevation", "slope", "curvature", "warning")):
        for multiplier in (0.5, 1.5):
            weights = BASE.copy()
            weights[i] *= multiplier
            weights *= BASE.sum() / weights.sum()
            assert abs(weights.sum() - 2.25) < 1e-12 and np.all(weights > 0)
            result[f"{feature}_x{multiplier:.1f}"] = weights
    return result


def protected_paths():
    inputs = [terrain.DEM_PATH, terrain.ADMIN_PATH, terrain.LANDSLIDE_PATH,
              terrain.WARNING_PATH, terrain.SCENARIO_PATH, terrain.THRESHOLD_PATH,
              road.ROAD_PATH, isolation.NODE_PATH, isolation.EDGE_PATH,
              isolation.MESH_PATH, isolation.GROUP_PATH]
    inputs += list((ROOT / "src/analyses").glob("*.py"))
    inputs += [p for p in (ROOT / "data/results").rglob("*") if p.is_file()]
    inputs += [ROOT / "Rev/revision" / name for name in (
        "KE01e.rev.markup.docx", "KE01e.rev.clean.docx", "Appendix.docx", "response-draft.md")]
    return sorted(set(inputs))


def check_protected(manifest):
    differences = [name for name, expected in manifest.items() if sha(ROOT / name) != expected]
    assert not differences, f"Protected inputs changed: {differences}"


def prepare_scores(specs):
    target = OUT / "road_scores.npz"
    if target.exists():
        return dict(np.load(target, allow_pickle=False))
    print("Recovering frozen standardization and terrain components", flush=True)
    assert terrain.LANDSLIDE_VALIDATION_DATE == pd.Timestamp("2016-07-28")
    context = validation.prepare_context()
    model = terrain.TransparentStandardizedScore(terrain.FALLBACK_WEIGHTS).fit(context["matrix"])
    valid = context["valid"]
    matrix = np.column_stack([context["screening_features"][n][valid] for n in terrain.FEATURE_NAMES])
    standardized = model.scaler.transform(matrix)
    original = dict(np.load(GRID, allow_pickle=False))
    assert tuple(original["shape"]) == context["shape"]
    assert np.array_equal(original["extent"], context["extent"])
    assert np.array_equal(np.isfinite(original["score_Heavy"]), valid)
    threshold = pd.read_parquet(terrain.THRESHOLD_PATH)
    factors, mixed = terrain.threshold_categories(context["admin"], threshold)
    factors[mixed] = 0.75
    factor_grid = rasterize(
        ((g, float(f)) for g, f in zip(context["admin_geometry"], factors)),
        out_shape=context["shape"], transform=context["transform"],
        fill=1.0, all_touched=True, dtype="float32")
    grids, checks = {}, {}
    for key, weights in specs.items():
        eta = np.full(context["shape"], np.nan, dtype="float32")
        eta[valid] = (standardized @ weights).astype("float32")
        for scenario in SCENARIOS:
            score = expit(eta + np.log(np.clip(original[f"load_{scenario}"] / factor_grid, 1e-6, None))).astype("float32")
            assert np.array_equal(np.isfinite(score), valid)
            assert np.all((score[valid] >= 0) & (score[valid] <= 1))
            if key == "central":
                diff = float(np.nanmax(np.abs(score - original[f"score_{scenario}"])))
                checks[f"slope_{scenario}_max_abs"] = diff
                assert diff <= 1e-6, checks
            grids[f"{key}__{scenario}"] = score
    np.savez_compressed(OUT / "frozen_components.npz", standardized=standardized,
                        valid=valid, feature_mean=model.scaler.mean_, feature_scale=model.scaler.scale_,
                        extent=original["extent"])
    np.savez_compressed(OUT / "slope_scores.npz", **grids)
    roads = pd.read_parquet(road.ROAD_PATH)
    roads = roads.loc[roads["Network Analysis Eligible"]].reset_index(drop=True)
    geometry = road.decode_geometry(roads["Geometry"])
    print("Propagating 27 slope grids through frozen directional road transfer", flush=True)
    scores = road.road_scores(geometry, grids, context["extent"], original["elevation"])
    original_roads = dict(np.load(ROAD, allow_pickle=False))
    for scenario in SCENARIOS:
        diff = float(np.max(np.abs(scores[f"central__{scenario}"] - original_roads[f"score_{scenario}"])))
        checks[f"road_{scenario}_max_abs"] = diff
        assert diff <= 1e-6, checks
        scores[f"central__{scenario}"] = original_roads[f"score_{scenario}"]
    rows = []
    for key in specs:
        for scenario in SCENARIOS:
            for level, arrays in (("slope", grids), ("road", scores)):
                ref, alt = arrays[f"central__{scenario}"], arrays[f"{key}__{scenario}"]
                support = np.isfinite(ref) & np.isfinite(alt) & ((ref > 0) | (alt > 0))
                x, y = ref[support], alt[support]
                top_x, top_y = x >= np.quantile(x, .99), y >= np.quantile(y, .99)
                rows.append(dict(specification=key, scenario=scenario, level=level,
                                 support_count=int(support.sum()), rho=float(spearmanr(x, y).statistic),
                                 top_one_percent_overlap=float(np.sum(top_x & top_y) / min(top_x.sum(), top_y.sum()))))
    pd.DataFrame(rows).to_csv(OUT / "score_diagnostics.csv", index=False)
    write_json(OUT / "central_score_reproduction.json", checks)
    np.savez_compressed(target, **scores)
    print("Central slope/road reconstruction passed", checks, flush=True)
    return scores


def setup_graph(roads, heavy, admin_union):
    lower = isolation.positive_score_quantile(heavy, .85)
    upper = isolation.positive_score_quantile(heavy, .995)
    positions = np.flatnonzero(np.isfinite(heavy) & (heavy >= lower))
    ids = roads.iloc[positions]["Road Section ID"].reset_index(drop=True)
    mapping = pd.Series(np.arange(len(ids), dtype="int32"), index=ids)
    nodes = pd.read_parquet(isolation.NODE_PATH, columns=["Network Node ID", "Network Component ID", "Geometry"])
    node_geometry = road.decode_geometry(nodes.pop("Geometry"))
    node_index = pd.Index(nodes["Network Node ID"])
    edges = pd.read_parquet(isolation.EDGE_PATH, columns=["Road Section ID", "From Node ID", "To Node ID",
        "Network Component ID", "Emergency Route Membership", "Baseline Edge Travel Time (min)", "Network Analysis Eligible"])
    edges = edges.loc[edges["Network Analysis Eligible"]].reset_index(drop=True)
    eu, ev = node_index.get_indexer(edges["From Node ID"]), node_index.get_indexer(edges["To Node ID"])
    assert np.all(eu >= 0) and np.all(ev >= 0)
    candidate = edges["Road Section ID"].isin(ids).to_numpy()
    u, v = eu[~candidate], ev[~candidate]
    graph = coo_matrix((np.ones(len(u)*2, dtype="uint8"),
                       (np.r_[u,v], np.r_[v,u])), shape=(len(nodes),len(nodes))).tocsr()
    root_count, labels = connected_components(graph, directed=False, return_labels=True)
    labels = labels.astype("int32")
    u, v = labels[eu[candidate]], labels[ev[candidate]]
    sections = edges.loc[candidate, "Road Section ID"].map(mapping).to_numpy(dtype="int32")
    mask = u != v
    targets, target_components = isolation.external_target_definitions(nodes,node_geometry,labels,edges,eu,ev,admin_union)
    community, ac, ar, diagnostics, meshes, _ = isolation.build_baseline_communities(nodes,node_geometry,labels,target_components)
    assert abs(community.Total_Population.sum() - meshes["Total Population"].sum()) < 1e-6
    assert abs(community.Population_Age_65.sum() - meshes["Population Age 65+"].sum()) < 1e-6
    result = dict(positions=positions, ids=ids.to_numpy(dtype=str), lower=lower, upper=upper,
                  u=u[mask], v=v[mask], sections=sections[mask], roots=root_count,
                  targets=targets[isolation.PRIMARY_TARGET_NAME], community=community,
                  ac=ac, ar=ar, diagnostics=diagnostics,
                  mesh_ids=meshes["Mesh Code"].to_numpy(dtype=str),
                  propensity=isolation.closure_propensity(heavy[positions],lower,upper))
    assert len(result["targets"]) and not disconnected(result, np.ones(len(ids),dtype=bool)).any()
    return result


def disconnected(g, opened):
    mask = opened[g["sections"]]
    u, v = g["u"][mask], g["v"][mask]
    graph = coo_matrix((np.ones(len(u)*2,dtype="uint8"),(np.r_[u,v],np.r_[v,u])),
                       shape=(g["roots"],g["roots"])).tocsr()
    count, labels = connected_components(graph,directed=False,return_labels=True)
    target = np.zeros(count,dtype=bool)
    target[labels[g["targets"]]] = True
    accessible = np.zeros(len(g["community"]),dtype="uint8")
    np.maximum.at(accessible,g["ac"],target[labels[g["ar"]]].astype("uint8"))
    return accessible == 0


def uniforms(seed, central_count, extra_count, central_index, extra_index):
    central_rng = np.random.default_rng(seed)
    extra_rng = np.random.default_rng(np.random.SeedSequence([seed,3202]))
    shared = central_index >= 0
    for _ in range(1000):
        central, extra = central_rng.random(central_count), extra_rng.random(extra_count)
        values = np.empty(len(central_index))
        values[shared] = central[central_index[shared]]
        values[~shared] = extra[extra_index[~shared]]
        yield values


def simulate(g, seed, central_ids, extra_ids, adjusted=None):
    ci = pd.Index(central_ids).get_indexer(g["ids"])
    ei = pd.Index(extra_ids).get_indexer(g["ids"])
    assert np.all((ci >= 0) | (ei >= 0))
    counts = np.zeros(len(g["community"]),dtype="int32")
    for values in uniforms(seed,len(central_ids),len(extra_ids),ci,ei):
        base = disconnected(g, values >= g["propensity"])
        if adjusted is None:
            counts += base
        else:
            after = disconnected(g, values >= adjusted)
            assert not np.any(after & ~base), "Paired intervention violates monotonicity"
            counts += after
    return counts.astype("float32") / 1000


def priorities(g, roads, heavy, frequency):
    pop = g["community"].Total_Population.to_numpy(dtype=float)
    count = len(g["ids"])
    degree = np.bincount(np.r_[g["u"],g["v"]],minlength=g["roots"]).astype(float)
    burden = intervention.section_burden_from_frequency(frequency,pop,g["ac"],g["ar"],
        g["u"],g["v"],g["sections"],g["roots"],count)
    scarcity = np.zeros(count)
    np.maximum.at(scarcity,g["sections"],1/np.sqrt(np.maximum(np.minimum(degree[g["u"]],degree[g["v"]]),1.)))
    candidate_roads = roads.iloc[g["positions"]]
    emergency = candidate_roads["Emergency Route Membership"].astype("string").ne("None").to_numpy()
    score = heavy[g["positions"]]
    preliminary = score * np.log1p(burden) * (1+scarcity) * np.where(emergency,1.20,1.)
    screen = np.argsort(preliminary)[-1000:]
    single = np.zeros(count)
    for p in screen:
        single[p] = intervention.single_section_closed_population(int(p),g["u"],g["v"],g["sections"],
            g["roots"],g["targets"],g["ac"],g["ar"],pop)
    proxy = single + .15 * burden
    actions = intervention.action_assignment(candidate_roads["Emergency Route Membership"],score,g["upper"],scarcity)
    length = candidate_roads["Road Section Length (m)"].to_numpy(dtype=float)/1000
    costs = np.select([actions=="Temporary reinforcement",actions=="Alternative-route protection"],
                      [3+2*length,2.5+1.2*length],default=1.5+.5*length)
    priority = intervention.assigned_action_priority_score(proxy,actions,costs)
    order = np.argsort(priority)[::-1]
    selected, _ = intervention.select_under_budget(order[:150],costs,BUDGET)
    assert costs[selected].sum() <= BUDGET + 1e-9
    effects = np.array([intervention.ACTION_EFFECT[str(a)]["Central"] for a in actions])
    adjusted = g["propensity"].astype(float).copy()
    adjusted[selected] *= 1-effects[selected]
    assert np.all(adjusted <= g["propensity"])
    table = pd.DataFrame(dict(road_id=g["ids"],score=score,burden=burden,single_close=single,
        action=actions,base_cost=costs,priority=priority,selected=np.isin(np.arange(count),selected)))
    return adjusted,order,selected,table


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest_path = OUT / "input_manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        assert manifest["spec_sha256"] == sha(SPEC)
        check_protected(manifest["protected"])
    else:
        print("Hashing frozen sources, data and protected outputs",flush=True)
        manifest = dict(spec_sha256=sha(SPEC),proposal_sha256=sha(ROOT/"Rev/docs/analysis-proposal-reviewer-3-comment-2.md"),
                        decision="KILA-D-20260905-012",
                        protected={str(p.relative_to(ROOT)):sha(p) for p in protected_paths()})
        write_json(manifest_path,manifest)
    specs = specifications()
    pd.DataFrame([dict(specification=k,**dict(zip(terrain.FEATURE_NAMES,v))) for k,v in specs.items()]).to_csv(OUT/"weight_vectors.csv",index=False)
    scores = prepare_scores(specs)
    roads = pd.read_parquet(road.ROAD_PATH,columns=["Road Section ID","Road Section Length (m)","Emergency Route Membership","Network Analysis Eligible"])
    roads = roads.loc[roads["Network Analysis Eligible"]].reset_index(drop=True)
    assert roads["Road Section ID"].is_unique
    admin_union = shapely.union_all(road.decode_geometry(pd.read_parquet(terrain.ADMIN_PATH,columns=["Geometry"])["Geometry"]))
    ids = {}
    for key in specs:
        heavy = scores[f"{key}__Heavy"]
        threshold = isolation.positive_score_quantile(heavy,.85)
        ids[key] = roads.loc[np.isfinite(heavy)&(heavy>=threshold),"Road Section ID"].to_numpy(dtype=str)
    central_ids = ids["central"]
    extra_ids = np.array(sorted(set(np.concatenate(list(ids.values()))) - set(central_ids)))
    np.savez_compressed(OUT/"random_stream_road_ids.npz",central_ids=central_ids,extra_ids=extra_ids)
    # Verify shared-road identity for first variates, independently of graph simulation.
    shared_checks = {}
    original = np.random.default_rng(isolation.REPLICATE_SEEDS[0]).random(len(central_ids))
    for key in specs:
        ci,ei = pd.Index(central_ids).get_indexer(ids[key]),pd.Index(extra_ids).get_indexer(ids[key])
        actual = next(uniforms(isolation.REPLICATE_SEEDS[0],len(central_ids),len(extra_ids),ci,ei))
        assert np.array_equal(actual[ci>=0],original[ci[ci>=0]])
        shared_checks[key] = int(np.sum(ci>=0))
    summaries,seed_rows=[],[]
    reference = None
    for key in specs:
        print(f"Starting {key}: rebuild graph and Heavy five-seed propagation",flush=True)
        g = setup_graph(roads,scores[f"{key}__Heavy"],admin_union)
        assert np.array_equal(g["ids"],ids[key])
        pop=g["community"].Total_Population.to_numpy(dtype=float)
        older=g["community"].Population_Age_65.to_numpy(dtype=float)
        if reference is not None:
            assert np.array_equal(pop,reference["population"])
            assert np.array_equal(older,reference["older"])
            assert np.array_equal(g["mesh_ids"],reference["mesh_ids"])
            assert np.array_equal(g["community"]["Community ID"],reference["community_ids"])
        path = OUT / f"baseline_{key}.npz"
        if path.exists():
            baseline=dict(np.load(path,allow_pickle=False))
        else:
            baseline={}
            for seed in isolation.REPLICATE_SEEDS:
                baseline[str(seed)]=simulate(g,seed,central_ids,extra_ids)
                print(f"  baseline seed {seed}: {pop @ baseline[str(seed)].astype(float):.6f}",flush=True)
            np.savez_compressed(path,**baseline)
        mean=np.mean(np.vstack([baseline[str(s)].astype(float) for s in isolation.REPLICATE_SEEDS]),axis=0)
        if key=="central":
            assert abs(pop@mean-1063.597598)<.001,("Central disconnection mismatch",pop@mean)
            repeat=simulate(g,isolation.REPLICATE_SEEDS[0],central_ids,extra_ids)
            assert np.array_equal(repeat,baseline[str(isolation.REPLICATE_SEEDS[0])])
            canonical=intervention.quiet_isolation_frequency(g["u"],g["v"],g["sections"],g["propensity"],
                g["roots"],g["targets"],g["ac"],g["ar"],len(pop),isolation.REPLICATE_SEEDS[0])
            assert np.array_equal(canonical,repeat),"Central differs from canonical simulator"
        adjusted,order,selected,table=priorities(g,roads,scores[f"{key}__Heavy"],mean)
        table.to_csv(OUT/f"road_priorities_{key}.csv",index=False)
        path=OUT/f"intervention_{key}.npz"
        if path.exists():
            after=dict(np.load(path,allow_pickle=False))
        else:
            after={}
            for seed in isolation.REPLICATE_SEEDS:
                after[str(seed)]=simulate(g,seed,central_ids,extra_ids,adjusted)
                print(f"  intervention seed {seed} finished",flush=True)
            np.savez_compressed(path,**after)
        protected=[]
        isolated=[]
        for seed in isolation.REPLICATE_SEEDS:
            b,a=baseline[str(seed)].astype(float),after[str(seed)].astype(float)
            assert np.all(a<=b)
            gain=float(pop@(b-a))
            protected.append(gain)
            isolated.append(float(pop@b))
            seed_rows.append(dict(specification=key,seed=seed,isolated_population=float(pop@b),
                older_isolated_population=float(older@b),protected_population=gain))
        community_top=np.argsort(pop*mean)[-30:]
        road_top=g["ids"][order[:30]]
        portfolio=g["ids"][selected]
        if key=="central":
            assert abs(np.mean(protected)-62.31300017163157)<.001,("Central protection mismatch",np.mean(protected))
            reference=dict(population=pop,older=older,mesh_ids=g["mesh_ids"],
                community_ids=g["community"]["Community ID"].to_numpy(),community_top=community_top,
                road_top=road_top,portfolio=portfolio)
        row=dict(specification=key,candidate_count=len(g["ids"]),
            candidate_overlap_central=len(set(g["ids"])&set(central_ids))/len(central_ids),
            root_count=g["roots"],target_root_count=len(g["targets"]),
            eligible_population=float(pop.sum()),older_population=float(older.sum()),
            isolated_population=float(pop@mean),older_isolated_population=float(older@mean),
            isolated_seed_min=min(isolated),isolated_seed_max=max(isolated),isolated_seed_sd=float(np.std(isolated,ddof=1)),
            community_top30_overlap=len(set(community_top)&set(reference["community_top"]))/30,
            intervention_top30_overlap=len(set(road_top)&set(reference["road_top"]))/30,
            portfolio_overlap_central=len(set(portfolio)&set(reference["portfolio"]))/len(reference["portfolio"]),
            portfolio_count=len(selected),budget_used=float(table.base_cost.to_numpy()[selected].sum()),
            protected_population=float(np.mean(protected)),protected_seed_min=min(protected),
            protected_seed_max=max(protected),protected_seed_sd=float(np.std(protected,ddof=1)))
        summaries.append(row)
        c=g["community"].copy()
        c["Heavy disconnection frequency"]=mean
        c["Expected disconnected population"]=pop*mean
        c.to_csv(OUT/f"community_{key}.csv",index=False)
        pd.DataFrame(summaries).to_csv(OUT/"terrain_weight_summary.csv",index=False)
        pd.DataFrame(seed_rows).to_csv(OUT/"terrain_weight_by_seed.csv",index=False)
        print("Completed",row,flush=True)
    check_protected(manifest["protected"])
    write_json(OUT/"decision.json",dict(status="validated",decision="KILA-D-20260905-012",
        specification_sha256=sha(SPEC),source_sha256=sha(Path(__file__)),specifications=9,
        rainfall_scenarios=3,seeds=list(isolation.REPLICATE_SEEDS),draws_per_seed=1000,
        shared_road_identity_checks=shared_checks,central_reproduction=True,
        central_repeat_and_canonical_comparison="exact",paired_draw_monotonicity=True,
        eligible_mesh_and_population_identity=True,protected_inputs_unchanged=True,
        scope="Staged parameter sensitivity; no cross-family probability interval; no service endpoint propagation"))
    print("ALL NINE SPECIFICATIONS VALIDATED",flush=True)


if __name__ == "__main__":
    main()
