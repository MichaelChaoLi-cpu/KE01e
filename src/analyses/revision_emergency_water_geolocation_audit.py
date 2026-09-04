#!/usr/bin/env python3
"""Audit emergency-water geolocation support for Reviewer 1 Comment 1.

This revision-only analysis is descriptive. It never imputes coordinates and
does not modify production results, figures, tables, manuscripts, or Appendix.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data/processed/emergency_water_points_preprocessed.parquet"
OUT = ROOT / "data/exp/revision/reviewer-1-comment-1"

MUNICIPALITY_ENGLISH = {
    "八代市": "Yatsushiro City",
    "宇城市": "Uki City",
    "氷川町": "Hikawa Town",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def facility_class(name: str) -> str:
    if "学校" in name:
        return "school"
    if "コミセン" in name or "公民館" in name:
        return "community_center"
    if "役所" in name or "振興局" in name or "防災拠点" in name:
        return "government_or_disaster_center"
    return "other"


def summarize(frame: pd.DataFrame, group: str) -> pd.DataFrame:
    result = (
        frame.groupby(group, observed=True, sort=True)["Resolved"]
        .agg(Resolved="sum", Announced="count")
        .reset_index()
    )
    result["Resolved"] = result["Resolved"].astype(int)
    result["Announced"] = result["Announced"].astype(int)
    result["Unresolved"] = result["Announced"] - result["Resolved"]
    result["Resolution Percent"] = 100.0 * result["Resolved"] / result["Announced"]
    return result


def main() -> None:
    source = pd.read_parquet(INPUT)
    required = {
        "Municipality",
        "Water Point Name",
        "Latitude",
        "Longitude",
        "Location Resolution Status",
        "Source URL",
        "Source Status Time",
    }
    missing = required.difference(source.columns)
    if missing:
        raise RuntimeError(f"Missing required columns: {sorted(missing)}")

    latitude_present = source["Latitude"].notna()
    longitude_present = source["Longitude"].notna()
    if not latitude_present.equals(longitude_present):
        raise RuntimeError("At least one record has only one coordinate.")

    audit = source[
        [
            "Municipality",
            "Water Point Name",
            "Latitude",
            "Longitude",
            "Location Resolution Status",
            "Source URL",
            "Source Status Time",
        ]
    ].copy()
    audit["Municipality English"] = audit["Municipality"].map(MUNICIPALITY_ENGLISH)
    if audit["Municipality English"].isna().any():
        unknown = sorted(audit.loc[audit["Municipality English"].isna(), "Municipality"].unique())
        raise RuntimeError(f"Unmapped municipality labels: {unknown}")
    audit["Facility Name Class"] = audit["Water Point Name"].astype(str).map(facility_class)
    audit["Resolved"] = latitude_present.to_numpy()

    if len(audit) != 36:
        raise RuntimeError(f"Expected 36 announcements, found {len(audit)}.")
    if int(audit["Resolved"].sum()) != 10:
        raise RuntimeError(f"Expected 10 resolved announcements, found {int(audit['Resolved'].sum())}.")
    resolved_status = audit.loc[audit["Resolved"], "Location Resolution Status"].astype(str)
    unresolved_status = audit.loc[~audit["Resolved"], "Location Resolution Status"].astype(str)
    if not resolved_status.eq("matched_exact_2012_facility").all():
        raise RuntimeError("A resolved record lacks the expected exact-register-match status.")
    if not unresolved_status.eq("unmatched").all():
        raise RuntimeError("An unresolved record lacks the expected unmatched status.")

    municipality = summarize(audit, "Municipality English")
    facility = summarize(audit, "Facility Name Class")
    if int(municipality["Announced"].sum()) != 36 or int(facility["Announced"].sum()) != 36:
        raise RuntimeError("Grouped totals do not reconcile to the source total.")

    overall = {
        "announced": int(len(audit)),
        "resolved": int(audit["Resolved"].sum()),
        "unresolved": int((~audit["Resolved"]).sum()),
        "resolution_percent": round(100.0 * float(audit["Resolved"].mean()), 1),
        "source_municipalities": int(audit["Municipality English"].nunique()),
        "municipalities_with_resolved_destination": int(
            audit.loc[audit["Resolved"], "Municipality English"].nunique()
        ),
        "municipality_representation_percent": round(
            100.0
            * audit.loc[audit["Resolved"], "Municipality English"].nunique()
            / audit["Municipality English"].nunique(),
            1,
        ),
        "resolved_are_exact_2012_register_matches": True,
        "urban_rural_missingness_identifiable": False,
    }

    decision = {
        "reviewer_id": "reviewer-1",
        "comment_id": "comment-1",
        "analysis_type": "descriptive_geolocation_support_audit",
        "overall": overall,
        "gates": {
            "source_count_36": len(audit) == 36,
            "resolved_count_10": int(audit["Resolved"].sum()) == 10,
            "unresolved_count_26": int((~audit["Resolved"]).sum()) == 26,
            "coordinate_pairs_complete": bool(latitude_present.equals(longitude_present)),
            "status_consistent": True,
            "group_totals_reconcile": True,
        },
        "interpretation": {
            "municipality_and_name_class_concentration_present": True,
            "uniform_or_random_missingness_supported": False,
            "prefecture_wide_operational_water_access_supported": False,
            "resolved_subset_connectivity_supported": True,
        },
    }

    OUT.mkdir(parents=True, exist_ok=True)
    audit.sort_values(
        ["Municipality English", "Facility Name Class", "Water Point Name"],
        kind="mergesort",
    ).to_csv(OUT / "record_audit.csv", index=False)
    municipality.to_csv(OUT / "municipality_summary.csv", index=False)
    facility.to_csv(OUT / "facility_class_summary.csv", index=False)
    pd.DataFrame(
        [{"Path": str(INPUT.relative_to(ROOT)), "SHA-256": sha256(INPUT)}]
    ).to_csv(OUT / "input_hashes.csv", index=False)
    (OUT / "decision.json").write_text(
        json.dumps(decision, ensure_ascii=False, indent=2) + "\n"
    )

    municipality_lines = "\n".join(
        f"- {row['Municipality English']}: {int(row['Resolved'])}/{int(row['Announced'])} resolved "
        f"({row['Resolution Percent']:.1f}%); {int(row['Unresolved'])} unresolved."
        for _, row in municipality.iterrows()
    )
    facility_lines = "\n".join(
        f"- {row['Facility Name Class']}: {int(row['Resolved'])}/{int(row['Announced'])} resolved "
        f"({row['Resolution Percent']:.1f}%); {int(row['Unresolved'])} unresolved."
        for _, row in facility.iterrows()
    )
    report = f"""# Reviewer 1 Comment 1 Emergency-Water Geolocation Audit

## Result

- Overall: {overall['resolved']}/{overall['announced']} announcements resolved ({overall['resolution_percent']:.1f}%); {overall['unresolved']} unresolved.
- Municipality representation: {overall['municipalities_with_resolved_destination']}/{overall['source_municipalities']} source municipalities have at least one resolved destination ({overall['municipality_representation_percent']:.1f}%).
- Every resolved point is an exact match to the retained 2012 facility register; every unresolved point is marked unmatched.

## Municipality distribution

{municipality_lines}

## Name-class distribution

{facility_lines}

## Operational interpretation

The resolved subset is concentrated by municipality and facility-name class: all ten resolved destinations are in Yatsushiro City and all are school-named points. Uki City and Hikawa Town have no resolved destination in the routing denominator; community-centre and government/disaster-centre announcements are also entirely unresolved. The missingness therefore cannot be treated as uniform or random from the available evidence.

The current emergency-water output supports only a conditional statement about road-network connectivity to the ten resolved, road-attached destinations. It cannot support prefecture-wide operational deployment, municipality comparisons, water availability, capacity, operating-status, or unmet-demand claims. Because unresolved coordinates are absent, this audit cannot classify the 26 missing points as urban or rural. Completing and validating their coordinates, road attachments, operating status, and capacity is a prerequisite for site-level operational planning.

## Gates

All predeclared consistency and reconciliation gates passed. No coordinates were imputed and no production artifact was modified.
"""
    (OUT / "audit_report.md").write_text(report)

    print(report)


if __name__ == "__main__":
    main()
