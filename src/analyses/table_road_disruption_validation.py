#!/usr/bin/env python3
"""Road-Disruption Validation.

Plan: Compare Moderate, Heavy, and Extreme road-disruption rankings with a
warning-zone baseline, road-length baseline, and municipality-wide Yatsushiro
0.70 and 0.80 bounding assignments.
Framework: AnaSOP Sections 5-7 require matching on municipality, road category,
emergency-route membership, and road-length decile. Section-level concordance and its
bootstrap interval support relative ranking only, not closure probabilities.
"""
from __future__ import annotations

import os
from pathlib import Path

os.environ.pop("PROJ_LIB", None)
os.environ.pop("PROJ_DATA", None)

import numpy as np
from openpyxl import load_workbook
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.table import Table, TableStyleInfo
import pandas as pd
from rasterio.features import rasterize
from rasterio.transform import from_bounds
import shapely

import figure_road_disruption_exposure_and_observed_restriction_evidence as road_validation
from cache_fingerprint import cache_matches, content_signature


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
OUT = ROOT / "data/results/tables/Table_road_disruption_validation.xlsx"
SHEET_NAME = "Road Validation"
TABLE_TITLE = "Road-Disruption Validation"
WARNING_SCORE_CACHE = (
    ROOT / "data/results/intermediate/road_warning_zone_scores_normalized_v3.npz"
)


def restriction_sections(roads: pd.DataFrame) -> tuple[pd.Series, int, int]:
    """Return reliable deduplicated restriction-linked road-section identifiers."""
    matches = pd.read_parquet(
        road_validation.MATCH_PATH,
        columns=[
            "Restriction Observation ID",
            "Snapshot Time",
            "Restriction Reason",
            "Matched Road Edge ID",
            "Road Edge Match Distance (m)",
            "Road Edge Match Status",
        ],
    )
    reliable = (
        matches["Restriction Reason"]
        .astype("string")
        .str.contains(road_validation.LANDSLIDE_REASON_PATTERN, na=False)
        & matches["Road Edge Match Status"].eq("matched_primary")
        & matches["Road Edge Match Distance (m)"].le(50)
    )
    evidence = matches.loc[reliable].drop_duplicates(
        ["Restriction Observation ID", "Snapshot Time", "Matched Road Edge ID"]
    )
    observation_count = int(
        len(evidence.drop_duplicates(["Restriction Observation ID", "Snapshot Time"]))
    )
    edges = pd.read_parquet(
        road_validation.EDGE_PATH,
        columns=["Road Edge ID", "Road Section ID"],
    )
    evidence_edges = evidence.merge(
        edges,
        left_on="Matched Road Edge ID",
        right_on="Road Edge ID",
        how="inner",
        validate="many_to_one",
    ).drop_duplicates(["Road Edge ID", "Restriction Reason"])
    evidence_edges = evidence_edges.loc[
        evidence_edges["Road Section ID"].isin(set(roads["Road Section ID"]))
    ]
    edge_count = int(evidence_edges["Road Edge ID"].nunique())
    return evidence_edges["Road Section ID"], observation_count, edge_count


def warning_zone_road_score(
    road_geometry: np.ndarray,
    elevation_grid: np.ndarray,
    extent: tuple[float, float, float, float],
    display_shape: tuple[int, int],
    display_transform: object,
) -> np.ndarray:
    """Build or load normalized directional warning-zone exposure by road section."""
    signature = content_signature(
        "road-warning-zone-score-v3",
        files=(road_validation.WARNING_PATH, road_validation.ROAD_PATH, Path(__file__)),
        arrays={"elevation_grid": elevation_grid},
        parameters={
            "road_count": len(road_geometry),
            "extent": tuple(float(value) for value in extent),
            "display_shape": tuple(int(value) for value in display_shape),
            "sample_fractions": road_validation.SAMPLE_FRACTIONS,
            "upslope_radius_cells": road_validation.UPSLOPE_RADIUS_CELLS,
        },
    )
    if WARNING_SCORE_CACHE.exists():
        cached = np.load(WARNING_SCORE_CACHE, allow_pickle=False)
        if cache_matches(cached, signature):
            return cached["score"].astype("float32")
    warning = pd.read_parquet(road_validation.WARNING_PATH, columns=["Geometry"])
    warning_geometry = road_validation.decode_geometry(warning["Geometry"])
    warning_grid = rasterize(
        ((geometry, 1.0) for geometry in warning_geometry),
        out_shape=display_shape,
        transform=display_transform,
        fill=0.0,
        all_touched=True,
        dtype="float32",
    )
    score = road_validation.road_scores(
        road_geometry,
        {"Warning-zone baseline": warning_grid},
        extent,
        elevation_grid,
    )["Warning-zone baseline"]
    WARNING_SCORE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        WARNING_SCORE_CACHE,
        signature=np.asarray(signature),
        score=score.astype("float32"),
    )
    return score


def build_table() -> pd.DataFrame:
    """Build seven matched-validation rows from the accepted road-score inputs."""
    admin = pd.read_parquet(
        road_validation.ADMIN_PATH,
        columns=["Municipality Name", "Geometry"],
    )
    admin_geometry = road_validation.decode_geometry(admin.pop("Geometry"))
    admin_union = shapely.union_all(admin_geometry)
    min_x, min_y, max_x, max_y = shapely.bounds(admin_union)
    pad_x = (max_x - min_x) * 0.025
    pad_y = (max_y - min_y) * 0.025
    extent = (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)
    west, east, south, north = extent
    display_height = max(
        650,
        round(road_validation.DISPLAY_WIDTH * (north - south) / (east - west)),
    )
    display_shape = (display_height, road_validation.DISPLAY_WIDTH)
    display_transform = from_bounds(
        west,
        south,
        east,
        north,
        road_validation.DISPLAY_WIDTH,
        display_height,
    )

    landslide_scores, _, _, elevation_grid = (
        road_validation.load_or_build_landslide_scores(
            admin,
            admin_geometry,
            admin_union,
            extent,
            display_shape,
            display_transform,
        )
    )
    roads = pd.read_parquet(
        road_validation.ROAD_PATH,
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
    road_geometry = road_validation.decode_geometry(roads.pop("Geometry"))
    scenario_scores = road_validation.load_or_build_road_scores(
        road_geometry,
        landslide_scores,
        extent,
        elevation_grid,
    )
    warning_score = warning_zone_road_score(
        road_geometry,
        elevation_grid,
        extent,
        display_shape,
        display_transform,
    )
    evidence_section_ids, observation_count, edge_count = restriction_sections(roads)
    heavy_score = scenario_scores["Heavy"]
    yatsushiro_bound_scores: dict[str, np.ndarray] = {}
    for bound_factor in (0.70, 0.80):
        bound_landslide_scores, _, _, _ = road_validation.load_or_build_landslide_scores(
            admin,
            admin_geometry,
            admin_union,
            extent,
            display_shape,
            display_transform,
            yatsushiro_factor=bound_factor,
        )
        yatsushiro_bound_scores[f"{bound_factor:.2f}"] = (
            road_validation.load_or_build_road_scores(
                road_geometry,
                bound_landslide_scores,
                extent,
                elevation_grid,
                yatsushiro_factor=bound_factor,
            )["Heavy"]
        )
    specifications = [
        (
            "Road score — Moderate rainfall",
            scenario_scores["Moderate"],
            "Scenario ranking; near-unity rank agreement limits spatial reprioritization claims.",
        ),
        (
            "Road score — Heavy rainfall",
            heavy_score,
            "Primary matched ranking evidence; not a closure probability.",
        ),
        (
            "Road score — Extreme rainfall",
            scenario_scores["Extreme"],
            "Scenario ranking; near-unity rank agreement limits spatial reprioritization claims.",
        ),
        (
            "Road warning-zone exposure baseline",
            warning_score,
            "Official-zone comparator under the same matched-control design.",
        ),
        (
            "Road-length baseline",
            roads["Road Section Length (m)"].to_numpy(dtype=float),
            "Length-only comparator under the same matched-control design.",
        ),
        (
            "Heavy road score — Yatsushiro bound 0.70",
            yatsushiro_bound_scores["0.70"],
            "Municipality-wide analytical bound for unresolved Yatsushiro subareas; not an official municipality value.",
        ),
        (
            "Heavy road score — Yatsushiro bound 0.80",
            yatsushiro_bound_scores["0.80"],
            "Municipality-wide analytical bound for unresolved Yatsushiro subareas; not an official municipality value.",
        ),
    ]

    rows: list[dict[str, object]] = []
    for specification, score, interpretation in specifications:
        metrics = road_validation.matched_road_concordance(
            roads,
            road_geometry,
            np.asarray(score, dtype=float),
            evidence_section_ids,
            admin_geometry,
            display_shape,
            display_transform,
            extent,
        )
        rank_correlation = float(
            pd.Series(score).corr(pd.Series(heavy_score), method="spearman")
        )
        rows.append(
            {
                "Specification": specification,
                "Matched Sample (Matched / Evidence / Controls)": (
                    f"{int(metrics['Matched Evidence Sections']):,}/"
                    f"{int(metrics['Evidence Sections']):,} / "
                    f"{int(metrics['Matched Controls']):,}"
                ),
                "Matched Concordance": metrics["Road Score Concordance"],
                "Section-Bootstrap 95% CI": (
                    f"{metrics['Road Score CI Low']:.3f}–"
                    f"{metrics['Road Score CI High']:.3f}"
                ),
                "Rank Correlation vs Heavy": rank_correlation,
                "Permitted Interpretation": interpretation,
            }
        )
    table = pd.DataFrame(rows)
    if table.shape != (7, 6):
        raise RuntimeError(f"Expected a 7 × 6 table, found {table.shape}.")
    print(
        f"Restriction linkage: {observation_count:,} observations; "
        f"{edge_count:,} reliably matched edges"
    )
    return table


def style_workbook(path: Path) -> None:
    """Apply the accepted compact scientific-table style."""
    workbook = load_workbook(path)
    worksheet = workbook[SHEET_NAME]
    worksheet.sheet_view.showGridLines = False
    worksheet.freeze_panes = "A3"
    worksheet.auto_filter.ref = f"A2:F{worksheet.max_row}"
    worksheet.sheet_view.zoomScale = 95
    worksheet.print_area = f"A1:F{worksheet.max_row}"
    worksheet.print_title_rows = "1:2"
    worksheet.page_setup.orientation = "landscape"
    worksheet.page_setup.paperSize = worksheet.PAPERSIZE_A3
    worksheet.page_setup.fitToWidth = 1
    worksheet.page_setup.fitToHeight = 1
    worksheet.sheet_properties.pageSetUpPr.fitToPage = True
    worksheet.page_margins = PageMargins(
        left=0.25,
        right=0.25,
        top=0.35,
        bottom=0.35,
        header=0.10,
        footer=0.10,
    )

    header_fill = PatternFill("solid", fgColor="17365D")
    header_font = Font(name="Aptos", size=10, bold=True, color="FFFFFF")
    body_font = Font(name="Aptos", size=9.5, color="172033")
    subtle_border = Border(bottom=Side(style="thin", color="D0D5DD"))

    worksheet.merge_cells("A1:F1")
    title_cell = worksheet["A1"]
    title_cell.value = TABLE_TITLE
    title_cell.fill = PatternFill("solid", fgColor="D9EAF7")
    title_cell.font = Font(name="Aptos Display", size=15, bold=True, color="17365D")
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    worksheet.row_dimensions[1].height = 28

    for cell in worksheet[2]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    worksheet.row_dimensions[2].height = 44

    for row in worksheet.iter_rows(min_row=3, max_row=worksheet.max_row):
        for cell in row:
            cell.font = body_font
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = subtle_border
        row[0].fill = PatternFill("solid", fgColor="FCE8D7")
        if row[0].value == "Road score — Heavy rainfall":
            row[0].fill = PatternFill("solid", fgColor="D9EDE9")
        row[2].number_format = "0.0%"
        row[4].number_format = "0.000"
        for cell in row[1:5]:
            cell.alignment = Alignment(horizontal="right", vertical="top", wrap_text=True)
        worksheet.row_dimensions[row[0].row].height = 42

    widths = {
        "A": 39,
        "B": 30,
        "C": 23,
        "D": 25,
        "E": 24,
        "F": 54,
    }
    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width

    for column in ("C", "E"):
        worksheet.conditional_formatting.add(
            f"{column}3:{column}{worksheet.max_row}",
            ColorScaleRule(
                start_type="min",
                start_color="F8696B",
                mid_type="percentile",
                mid_value=50,
                mid_color="FFEB84",
                end_type="max",
                end_color="63BE7B",
            ),
        )
    excel_table = Table(displayName="RoadDisruptionValidation", ref=f"A2:F{worksheet.max_row}")
    excel_table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    worksheet.add_table(excel_table)
    workbook.save(path)


def verify_workbook(path: Path) -> None:
    """Verify dimensions, numeric fields, and absence of spreadsheet errors."""
    workbook = load_workbook(path, data_only=False)
    if workbook.sheetnames != [SHEET_NAME]:
        raise RuntimeError(f"Unexpected workbook sheets: {workbook.sheetnames}")
    worksheet = workbook[SHEET_NAME]
    if worksheet.max_row != 9 or worksheet.max_column != 6:
        raise RuntimeError(
            f"Expected 9 rows including title and header and 6 columns; found "
            f"{worksheet.max_row} × {worksheet.max_column}."
        )
    if worksheet["A1"].value != TABLE_TITLE:
        raise RuntimeError("Workbook title row is missing or incorrect.")
    error_tokens = {"#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"}
    for row in worksheet.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and cell.value in error_tokens:
                raise RuntimeError(f"Spreadsheet error token in {cell.coordinate}: {cell.value}")
    for row in range(3, 10):
        for column in (3, 5):
            if not isinstance(worksheet.cell(row, column).value, (int, float)):
                raise RuntimeError(f"Expected numeric value at row {row}, column {column}.")


def main() -> None:
    table = build_table()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    table.to_excel(
        OUT,
        index=False,
        sheet_name=SHEET_NAME,
        engine="openpyxl",
        startrow=1,
    )
    style_workbook(OUT)
    verify_workbook(OUT)
    print(f"Saved: {OUT.relative_to(ROOT)}")
    print(f"Rows: {len(table):,}; columns: {len(table.columns):,}")
    for row in table.itertuples(index=False):
        print(
            f"{row[0]}: concordance={row[2]:.4f}; CI={row[3]}; "
            f"rho={row[4]:.6f}"
        )
    print("Workbook verification: passed")


if __name__ == "__main__":
    main()
