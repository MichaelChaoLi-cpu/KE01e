#!/usr/bin/env python3
"""Audit service-destination estimands for Reviewer 2 Comment 8.

The production analysis already recalculates reachability to every facility in a
service class after each disruption draw.  This revision-only audit reproduces that
any-same-class estimand and compares it, using identical closure draws, with a
restrictive fixed-baseline-destination continuity estimand.

No production figure, table, cache, manuscript, or Appendix file is overwritten.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import warnings

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import numpy as np
import pandas as pd
from rasterio.transform import from_bounds
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
import shapely

import figure_basic_service_reachability_loss as service
import figure_community_isolation_frequency_and_exposed_population as isolation
import figure_road_disruption_exposure_and_observed_restriction_evidence as road_exposure
import table_municipality_isolation_and_service_loss_summary as municipality_table
import table_priority_road_sections as priority_roads


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
OUT_DIR = ROOT / "data/exp/revision/reviewer-2-comment-8"
SUMMARY_PATH = OUT_DIR / "service_destination_estimand_summary.csv"
MUNICIPALITY_PATH = OUT_DIR / "service_destination_estimand_municipality.csv"
DECISION_PATH = OUT_DIR / "decision.json"
REPORT_PATH = OUT_DIR / "audit_report.md"
PRODUCTION_SCRIPT_PATH = Path(service.__file__).resolve()

ADMIN_PATH = PROCESSED / "administrative_areas_preprocessed.parquet"
ROAD_PATH = PROCESSED / "road_sections_preprocessed.parquet"
EDGE_PATH = PROCESSED / "road_edges_preprocessed.parquet"
NODE_PATH = PROCESSED / "road_nodes_preprocessed.parquet"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_context() -> dict[str, object]:
    """Build the frozen Heavy-scenario network, communities, and services."""
    admin = pd.read_parquet(
        ADMIN_PATH,
        columns=["Municipality Code", "Municipality Label", "Municipality Name", "Geometry"],
    )
    admin_geometry = road_exposure.decode_geometry(admin.pop("Geometry"))
    admin_union = shapely.union_all(admin_geometry)
    min_x, min_y, max_x, max_y = shapely.bounds(admin_union)
    pad_x = (max_x - min_x) * 0.025
    pad_y = (max_y - min_y) * 0.025
    extent = (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)
    west, east, south, north = extent
    display_height = max(
        650,
        round(road_exposure.DISPLAY_WIDTH * (north - south) / (east - west)),
    )
    display_shape = (display_height, road_exposure.DISPLAY_WIDTH)
    display_transform = from_bounds(
        west,
        south,
        east,
        north,
        road_exposure.DISPLAY_WIDTH,
        display_height,
    )

    terrain_scores, _, model_mode, elevation_grid = road_exposure.load_or_build_landslide_scores(
        admin,
        admin_geometry,
        admin_union,
        extent,
        display_shape,
        display_transform,
    )
    roads = pd.read_parquet(
        ROAD_PATH,
        columns=[
            "Road Section ID",
            "Emergency Route Membership",
            "Network Analysis Eligible",
            "Geometry",
        ],
    )
    roads = roads.loc[roads["Network Analysis Eligible"]].reset_index(drop=True)
    road_geometry = road_exposure.decode_geometry(roads.pop("Geometry"))
    road_scores = road_exposure.load_or_build_road_scores(
        road_geometry,
        terrain_scores,
        extent,
        elevation_grid,
    )
    heavy_lower = isolation.positive_score_quantile(
        road_scores["Heavy"], isolation.CANDIDATE_QUANTILE
    )
    heavy_upper = isolation.positive_score_quantile(
        road_scores["Heavy"], isolation.UPPER_MAPPING_QUANTILE
    )
    candidate = np.isfinite(road_scores["Heavy"]) & (road_scores["Heavy"] >= heavy_lower)
    candidate_ids = roads.loc[candidate, "Road Section ID"].reset_index(drop=True)
    candidate_position = pd.Series(
        np.arange(len(candidate_ids), dtype="int32"),
        index=candidate_ids,
    )
    candidate_scores = (
        pd.Series(road_scores["Heavy"], index=roads["Road Section ID"])
        .reindex(candidate_ids)
        .to_numpy(dtype="float32")
    )
    section_propensity = isolation.closure_propensity(
        candidate_scores,
        heavy_lower,
        heavy_upper,
    )

    nodes = pd.read_parquet(
        NODE_PATH,
        columns=["Network Node ID", "Network Component ID", "Geometry"],
    )
    node_geometry = road_exposure.decode_geometry(nodes.pop("Geometry"))
    node_index = pd.Index(nodes["Network Node ID"])
    edges = pd.read_parquet(
        EDGE_PATH,
        columns=[
            "Road Section ID",
            "From Node ID",
            "To Node ID",
            "Network Component ID",
            "Emergency Route Membership",
            "Baseline Edge Travel Time (min)",
            "Network Analysis Eligible",
        ],
    )
    edges = edges.loc[edges["Network Analysis Eligible"]].reset_index(drop=True)
    edge_u = node_index.get_indexer(edges["From Node ID"])
    edge_v = node_index.get_indexer(edges["To Node ID"])
    if np.any(edge_u < 0) or np.any(edge_v < 0):
        raise RuntimeError("Road edges reference missing network nodes.")
    edge_candidate = edges["Road Section ID"].isin(candidate_ids).to_numpy()

    stable_u = edge_u[~edge_candidate]
    stable_v = edge_v[~edge_candidate]
    stable_graph = coo_matrix(
        (
            np.ones(len(stable_u) * 2, dtype="uint8"),
            (np.concatenate([stable_u, stable_v]), np.concatenate([stable_v, stable_u])),
        ),
        shape=(len(nodes), len(nodes)),
    ).tocsr()
    root_count, stable_labels = connected_components(
        stable_graph,
        directed=False,
        return_labels=True,
    )
    stable_labels = stable_labels.astype("int32")

    candidate_u = stable_labels[edge_u[edge_candidate]]
    candidate_v = stable_labels[edge_v[edge_candidate]]
    candidate_edge_section = (
        edges.loc[edge_candidate, "Road Section ID"]
        .map(candidate_position)
        .to_numpy(dtype="int32")
    )
    candidate_edge_time = edges.loc[
        edge_candidate, "Baseline Edge Travel Time (min)"
    ].to_numpy(dtype="float64")
    between_root = candidate_u != candidate_v
    candidate_u = candidate_u[between_root]
    candidate_v = candidate_v[between_root]
    candidate_edge_section = candidate_edge_section[between_root]
    candidate_edge_time = candidate_edge_time[between_root]
    pair_reduction = service.prepare_pair_reduction(
        candidate_u,
        candidate_v,
        candidate_edge_section,
        candidate_edge_time,
        root_count,
    )

    target_definitions, target_components = isolation.external_target_definitions(
        nodes,
        node_geometry,
        stable_labels,
        edges,
        edge_u,
        edge_v,
        admin_union,
    )
    (
        community,
        attachment_community,
        attachment_root,
        community_diagnostics,
        selected_mesh,
        selected_mesh_geometry,
    ) = isolation.build_baseline_communities(
        nodes,
        node_geometry,
        stable_labels,
        target_components,
    )

    geometries, source_counts = service.service_geometries()
    service_roots, _, attached_counts = service.attach_services_to_roots(
        geometries,
        node_geometry,
        stable_labels,
    )
    for name in service.SERVICE_CLASSES:
        if not len(service_roots[name]):
            raise RuntimeError(f"No {name} facilities attach to the road network.")

    return {
        "admin": admin,
        "admin_geometry": admin_geometry,
        "community": community,
        "attachment_community": attachment_community,
        "attachment_root": attachment_root,
        "selected_mesh": selected_mesh,
        "selected_mesh_geometry": selected_mesh_geometry,
        "pair_reduction": pair_reduction,
        "candidate_u": candidate_u,
        "candidate_v": candidate_v,
        "candidate_edge_section": candidate_edge_section,
        "root_count": root_count,
        "target_roots": target_definitions[isolation.PRIMARY_TARGET_NAME],
        "section_propensity": section_propensity,
        "service_roots": service_roots,
        "source_counts": source_counts,
        "attached_counts": attached_counts,
        "community_diagnostics": community_diagnostics,
        "candidate_count": len(candidate_ids),
        "model_mode": model_mode,
    }


def baseline_assignments(
    baseline_graph: object,
    service_roots: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return baseline nearest-service distance and its source root per community."""
    root_distance, _, root_source = dijkstra(
        baseline_graph,
        directed=False,
        indices=service_roots,
        min_only=True,
        return_predecessors=True,
    )
    distance = np.full(community_count, np.inf, dtype="float64")
    assigned = np.full(community_count, -1, dtype="int32")
    for community_position, root in zip(attachment_community, attachment_root, strict=True):
        candidate_distance = float(root_distance[root])
        candidate_source = int(root_source[root])
        if not np.isfinite(candidate_distance) or candidate_source < 0:
            continue
        if (
            candidate_distance < distance[community_position]
            or (
                candidate_distance == distance[community_position]
                and (assigned[community_position] < 0 or candidate_source < assigned[community_position])
            )
        ):
            distance[community_position] = candidate_distance
            assigned[community_position] = candidate_source
    return distance, assigned


def reachable_by_component(
    component_labels: np.ndarray,
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
    service_roots: np.ndarray | None = None,
    assigned_root: np.ndarray | None = None,
) -> np.ndarray:
    """Evaluate any-class or fixed-destination reachability from components."""
    if (service_roots is None) == (assigned_root is None):
        raise ValueError("Provide exactly one of service_roots or assigned_root.")
    attachment_components = component_labels[attachment_root]
    if service_roots is not None:
        target_components = np.unique(component_labels[service_roots])
        attachment_reachable = np.isin(attachment_components, target_components)
    else:
        valid_community = assigned_root >= 0
        destination_component = np.full(community_count, -1, dtype="int32")
        destination_component[valid_community] = component_labels[
            assigned_root[valid_community]
        ]
        attachment_reachable = (
            valid_community[attachment_community]
            & (attachment_components == destination_component[attachment_community])
        )
    reachable = np.zeros(community_count, dtype=bool)
    np.logical_or.at(reachable, attachment_community, attachment_reachable)
    return reachable


def simulate_seed(
    section_propensity: np.ndarray,
    pair_reduction: dict[str, np.ndarray],
    root_count: int,
    service_roots: dict[str, np.ndarray],
    attachment_community: np.ndarray,
    attachment_root: np.ndarray,
    community_count: int,
    seed: int,
) -> dict[str, dict[str, np.ndarray]]:
    """Run paired any-class and fixed-destination indicators for one seed."""
    baseline_graph = service.weighted_draw_graph(
        np.ones(len(section_propensity), dtype=bool),
        pair_reduction,
        root_count,
    )
    baseline: dict[str, np.ndarray] = {}
    assigned: dict[str, np.ndarray] = {}
    for name in service.SERVICE_CLASSES:
        baseline[name], assigned[name] = baseline_assignments(
            baseline_graph,
            service_roots[name],
            attachment_community,
            attachment_root,
            community_count,
        )

    any_count = {name: np.zeros(community_count, dtype="int32") for name in service.SERVICE_CLASSES}
    fixed_count = {name: np.zeros(community_count, dtype="int32") for name in service.SERVICE_CLASSES}
    reroute_count = {name: np.zeros(community_count, dtype="int32") for name in service.SERVICE_CLASSES}
    random = np.random.default_rng(seed)
    for draw in range(isolation.MONTE_CARLO_DRAWS):
        section_open = random.random(len(section_propensity)) >= section_propensity
        graph = service.weighted_draw_graph(section_open, pair_reduction, root_count)
        _, labels = connected_components(graph, directed=False, return_labels=True)
        labels = labels.astype("int32", copy=False)
        for name in service.SERVICE_CLASSES:
            eligible = np.isfinite(baseline[name])
            any_reachable = reachable_by_component(
                labels,
                attachment_community,
                attachment_root,
                community_count,
                service_roots=service_roots[name],
            )
            fixed_reachable = reachable_by_component(
                labels,
                attachment_community,
                attachment_root,
                community_count,
                assigned_root=assigned[name],
            )
            any_loss = eligible & ~any_reachable
            fixed_loss = eligible & ~fixed_reachable
            if np.any(any_loss & ~fixed_loss):
                raise RuntimeError(
                    f"Fixed-destination ordering violated for {name}, seed {seed}, draw {draw}."
                )
            rerouted = fixed_loss & any_reachable
            any_count[name] += any_loss
            fixed_count[name] += fixed_loss
            reroute_count[name] += rerouted
        if (draw + 1) % 250 == 0:
            print(f"  seed {seed}: completed {draw + 1:,}/{isolation.MONTE_CARLO_DRAWS:,} paired draws")

    result: dict[str, dict[str, np.ndarray]] = {
        "any": {},
        "fixed": {},
        "reroute": {},
        "baseline": baseline,
        "assigned": assigned,
    }
    for name in service.SERVICE_CLASSES:
        eligible = np.isfinite(baseline[name])
        for key, counts in (
            ("any", any_count[name]),
            ("fixed", fixed_count[name]),
            ("reroute", reroute_count[name]),
        ):
            frequency = np.full(community_count, np.nan, dtype="float32")
            frequency[eligible] = (
                counts[eligible].astype("float32") / isolation.MONTE_CARLO_DRAWS
            )
            result[key][name] = frequency
        if not np.allclose(
            result["fixed"][name] - result["any"][name],
            result["reroute"][name],
            atol=1e-7,
            rtol=0,
            equal_nan=True,
        ):
            raise RuntimeError(f"Rerouting identity failed for {name}, seed {seed}.")
    return result


def population_totals(
    results: list[dict[str, dict[str, np.ndarray]]],
    population: np.ndarray,
) -> dict[str, dict[str, np.ndarray]]:
    totals: dict[str, dict[str, np.ndarray]] = {key: {} for key in ("any", "fixed", "reroute")}
    for key in totals:
        for name in service.SERVICE_CLASSES:
            totals[key][name] = np.asarray(
                [float(np.nansum(item[key][name] * population)) for item in results],
                dtype="float64",
            )
    return totals


def build_summary(
    context: dict[str, object],
    results: list[dict[str, dict[str, np.ndarray]]],
    totals: dict[str, dict[str, np.ndarray]],
) -> pd.DataFrame:
    community = context["community"]
    population = community["Total_Population"].to_numpy(dtype="float64")
    rows: list[dict[str, object]] = []
    for name in service.SERVICE_CLASSES:
        baseline = results[0]["baseline"][name]
        eligible = np.isfinite(baseline)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mean_reroute = np.nanmean(
                np.stack([item["reroute"][name] for item in results]), axis=0
            )
        fixed_mean = float(totals["fixed"][name].mean())
        reroute_mean = float(totals["reroute"][name].mean())
        any_mean = float(totals["any"][name].mean())
        rows.append(
            {
                "Service Class": name,
                "Resolved Source Facilities": int(context["source_counts"][name][0]),
                "Source Facilities Total": int(context["source_counts"][name][1]),
                "Road-Attached Facilities": int(context["attached_counts"][name]),
                "Baseline-Eligible Communities": int(eligible.sum()),
                "Baseline-Eligible Population": float(population[eligible].sum()),
                "Any-Same-Class Loss Population Mean": any_mean,
                "Any-Same-Class Loss Population Min": float(totals["any"][name].min()),
                "Any-Same-Class Loss Population Max": float(totals["any"][name].max()),
                "Fixed-Destination Loss Population Mean": fixed_mean,
                "Fixed-Destination Loss Population Min": float(totals["fixed"][name].min()),
                "Fixed-Destination Loss Population Max": float(totals["fixed"][name].max()),
                "Rerouting Benefit Population Mean": reroute_mean,
                "Rerouting Benefit Population Min": float(totals["reroute"][name].min()),
                "Rerouting Benefit Population Max": float(totals["reroute"][name].max()),
                "Rerouting Benefit Share of Fixed Loss": (
                    reroute_mean / fixed_mean if fixed_mean > 0 else np.nan
                ),
                "Fixed-to-Any Loss Ratio": fixed_mean / any_mean if any_mean > 0 else np.nan,
                "Communities with Positive Rerouting Benefit": int(
                    np.count_nonzero(np.isfinite(mean_reroute) & (mean_reroute > 0))
                ),
            }
        )
    return pd.DataFrame(rows)


def build_municipality_table(
    context: dict[str, object],
    results: list[dict[str, dict[str, np.ndarray]]],
) -> pd.DataFrame:
    admin = context["admin"].reset_index(drop=True)
    selected_mesh = context["selected_mesh"]
    admin_position = municipality_table.administrative_positions(
        context["selected_mesh_geometry"], context["admin_geometry"]
    )
    community_position = selected_mesh["Community Position"].to_numpy(dtype="int32")
    mesh_population = selected_mesh["Total Population"].to_numpy(dtype="float64")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        mean_frequency = {
            key: {
                name: np.nanmean(np.stack([item[key][name] for item in results]), axis=0)
                for name in service.SERVICE_CLASSES
            }
            for key in ("any", "fixed", "reroute")
        }
    rows: list[dict[str, object]] = []
    for position, admin_row in admin.iterrows():
        mask = admin_position == position
        for name in service.SERVICE_CLASSES:
            community_frequency = {
                key: mean_frequency[key][name][community_position[mask]]
                for key in mean_frequency
            }
            evaluable = np.isfinite(community_frequency["any"])
            rows.append(
                {
                    "Admin Area Code": str(admin_row["Municipality Code"]),
                    "Municipality / Ward": priority_roads.MUNICIPALITY_ENGLISH_BY_CODE[
                        str(admin_row["Municipality Code"])
                    ],
                    "Service Class": name,
                    "Baseline-Eligible Population": float(mesh_population[mask][evaluable].sum()),
                    "Any-Same-Class Loss Population": float(
                        np.sum(mesh_population[mask][evaluable] * community_frequency["any"][evaluable])
                    ),
                    "Fixed-Destination Loss Population": float(
                        np.sum(mesh_population[mask][evaluable] * community_frequency["fixed"][evaluable])
                    ),
                    "Rerouting Benefit Population": float(
                        np.sum(mesh_population[mask][evaluable] * community_frequency["reroute"][evaluable])
                    ),
                }
            )
    table = pd.DataFrame(rows).sort_values(
        ["Service Class", "Admin Area Code"], kind="stable"
    ).reset_index(drop=True)
    if table.shape != (len(admin) * len(service.SERVICE_CLASSES), 7):
        raise RuntimeError(f"Unexpected municipality table shape: {table.shape}.")
    return table


def verify_reference(
    context: dict[str, object],
    results: list[dict[str, dict[str, np.ndarray]]],
) -> dict[str, bool]:
    checks: dict[str, bool] = {}
    for item, seed in zip(results, isolation.REPLICATE_SEEDS, strict=True):
        reference, _, _ = service.simulate_service_loss(
            context["section_propensity"],
            context["pair_reduction"],
            context["root_count"],
            context["service_roots"],
            context["attachment_community"],
            context["attachment_root"],
            len(context["community"]),
            seed,
        )
        for name in service.SERVICE_CLASSES:
            key = f"seed_{seed}_{name.lower().replace(' ', '_')}_exact_reproduction"
            checks[key] = bool(
                np.array_equal(
                    item["any"][name],
                    reference[name],
                    equal_nan=True,
                )
            )
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise RuntimeError(f"Existing service-loss reproduction failed: {failed}")
    return checks


def write_report(summary: pd.DataFrame, validation: dict[str, object]) -> None:
    lines = [
        "# Reviewer 2 Comment 8 service-destination audit",
        "",
        "## Conclusion",
        "",
        "The production service-loss results already use post-disruption rerouting to any reachable facility in the same service class. The clean manuscript's fixed-destination wording is therefore inaccurate. The paired comparator below quantifies how much larger the loss would be if the baseline-nearest destination were truly held fixed.",
        "",
        "## Heavy-scenario paired results",
        "",
        "| Service class | Any same class | Fixed destination | Rerouting benefit | Benefit share of fixed loss |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in summary.to_dict("records"):
        lines.append(
            f"| {row['Service Class']} | {row['Any-Same-Class Loss Population Mean']:,.1f} | "
            f"{row['Fixed-Destination Loss Population Mean']:,.1f} | "
            f"{row['Rerouting Benefit Population Mean']:,.1f} | "
            f"{row['Rerouting Benefit Share of Fixed Loss']:.1%} |"
        )
    lines.extend(
        [
            "",
            "All values are five-seed means under the frozen central Heavy scenario. Emergency-water results remain conditional on the resolved 10-of-36 destination subset.",
            "",
            "## Validation",
            "",
            f"- Exact reproduction checks passed: {validation['exact_reproduction_checks_passed']}/{validation['exact_reproduction_checks_total']}.",
            "- Fixed-destination loss was never smaller than any-same-class loss.",
            "- The fixed-minus-any identity equalled the rerouting-benefit result within floating-point tolerance.",
            "- Baseline-unreachable communities remained non-evaluable.",
            "",
            "## Interpretation boundary",
            "",
            "Any-same-class reachability measures whether the road network retains access to at least one mapped, resolved, and attached facility of the class. It does not establish facility operability, staffing, capacity, admission, supplies, or realized emergency response.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    context = build_context()
    print(
        f"Built context: {len(context['community']):,} communities, "
        f"{context['candidate_count']:,} candidate road sections."
    )
    results = [
        simulate_seed(
            context["section_propensity"],
            context["pair_reduction"],
            context["root_count"],
            context["service_roots"],
            context["attachment_community"],
            context["attachment_root"],
            len(context["community"]),
            seed,
        )
        for seed in isolation.REPLICATE_SEEDS
    ]
    reproduction = verify_reference(context, results)
    population = context["community"]["Total_Population"].to_numpy(dtype="float64")
    totals = population_totals(results, population)
    summary = build_summary(context, results, totals)
    municipality = build_municipality_table(context, results)

    output_paths = (SUMMARY_PATH, MUNICIPALITY_PATH, REPORT_PATH)
    previous_output_hashes = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in output_paths
        if path.exists()
    }
    summary.to_csv(SUMMARY_PATH, index=False, float_format="%.10g", lineterminator="\n")
    municipality.to_csv(
        MUNICIPALITY_PATH,
        index=False,
        float_format="%.10g",
        lineterminator="\n",
    )
    baseline_nonevaluable = all(
        np.all(np.isnan(item[key][name][~np.isfinite(item["baseline"][name])]))
        for item in results
        for key in ("any", "fixed", "reroute")
        for name in service.SERVICE_CLASSES
    )
    municipality_reconciles = all(
        np.isclose(
            municipality.loc[municipality["Service Class"] == name, column].sum(),
            summary.loc[summary["Service Class"] == name, summary_column].iloc[0],
            rtol=0,
            atol=1e-3,
        )
        for name in service.SERVICE_CLASSES
        for column, summary_column in (
            ("Any-Same-Class Loss Population", "Any-Same-Class Loss Population Mean"),
            ("Fixed-Destination Loss Population", "Fixed-Destination Loss Population Mean"),
            ("Rerouting Benefit Population", "Rerouting Benefit Population Mean"),
        )
    )
    if not baseline_nonevaluable:
        raise RuntimeError("Baseline-unreachable communities were not consistently non-evaluable.")
    if not municipality_reconciles:
        raise RuntimeError("Municipality service totals do not reconcile to prefecture totals.")
    validation: dict[str, object] = {
        "exact_reproduction_checks_passed": int(sum(reproduction.values())),
        "exact_reproduction_checks_total": int(len(reproduction)),
        "all_exact_reproduction_checks_passed": bool(all(reproduction.values())),
        "fixed_loss_never_below_any_loss": True,
        "rerouting_identity_passed": True,
        "baseline_unreachable_remained_nonevaluable": bool(baseline_nonevaluable),
        "municipality_totals_reconciled": bool(municipality_reconciles),
        "scenario": "Heavy",
        "seed_count": len(isolation.REPLICATE_SEEDS),
        "draws_per_seed": isolation.MONTE_CARLO_DRAWS,
        "primary_estimand": "any-same-class facility reachability",
        "comparator_estimand": "fixed baseline destination continuity",
        "emergency_water_boundary": "conditional on 10 of 36 geolocated destinations",
    }
    write_report(summary, validation)
    current_output_hashes = {
        str(path.relative_to(ROOT)): sha256(path) for path in output_paths
    }
    validation["byte_identical_rerun_passed"] = bool(
        len(previous_output_hashes) == len(output_paths)
        and previous_output_hashes == current_output_hashes
    )
    decision = {
        "reviewer": "reviewer-2",
        "comment": "comment-8",
        "decision": "retain any-same-class reachability as primary; use fixed baseline destination as restrictive comparator",
        "kila_record": "KILA-D-20260904-003",
        "validation": validation,
        "service_summary": summary.to_dict(orient="records"),
        "input_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                ADMIN_PATH,
                ROAD_PATH,
                EDGE_PATH,
                NODE_PATH,
                PRODUCTION_SCRIPT_PATH,
            )
        },
        "output_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (SUMMARY_PATH, MUNICIPALITY_PATH, REPORT_PATH)
        },
    }
    DECISION_PATH.write_text(
        json.dumps(decision, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Saved: {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Saved: {MUNICIPALITY_PATH.relative_to(ROOT)}")
    print(f"Saved: {REPORT_PATH.relative_to(ROOT)}")
    print(f"Saved: {DECISION_PATH.relative_to(ROOT)}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
