#!/usr/bin/env python3
"""Rainfall and Threshold Scenarios.

Plan: Define the nine combinations of Moderate, Heavy, and Extreme historical
rainfall with baseline, 80 percent, and 70 percent threshold-retention settings.
Framework: AnaSOP Sections 5-7 use station-specific wet-window quantiles and
official area-level retention factors. Values remain at station support and do
not imply fine-resolution rainfall interpolation or a causal earthquake effect.
"""
from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.table import Table, TableStyleInfo
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
RAIN_PATH = PROCESSED / "jma_hourly_rainfall_preprocessed.parquet"
THRESHOLD_PATH = PROCESSED / "official_threshold_factors_preprocessed.parquet"
OUT = ROOT / "data/results/tables/Table_rainfall_and_threshold_scenarios.xlsx"
SHEET_NAME = "Rainfall Scenarios"
TABLE_TITLE = "Rainfall and Threshold Scenarios"

WINDOWS = (1, 3, 24, 72, 168)
SCENARIOS = (
    ("Moderate", 0.75, "M"),
    ("Heavy", 0.90, "H"),
    ("Extreme", 0.99, "E"),
)
RETENTION_SETTINGS = (
    (1.00, "Station-quantile median; baseline threshold. Seven-day rainfall is descriptive only."),
    (0.80, "Station-quantile median; official 80% threshold setting. No fine-grid rainfall inference."),
    (0.70, "Station-quantile median; official 70% threshold setting. No fine-grid rainfall inference."),
)


def station_wet_window_quantiles(rain: pd.DataFrame) -> pd.DataFrame:
    """Compute station-specific rainfall quantiles using complete wet windows."""
    rows: list[dict[str, object]] = []
    for station_id, group in rain.groupby("Station ID", sort=True):
        values = (
            group.sort_values("Observation Time")
            .set_index("Observation Time")["Hourly Rainfall"]
            .astype(float)
        )
        full_index = pd.date_range(
            values.index.min(), values.index.max(), freq="h", tz=values.index.tz
        )
        values = values.reindex(full_index)
        for window in WINDOWS:
            rolling = values if window == 1 else values.rolling(window, min_periods=window).sum()
            wet_windows = rolling.loc[rolling > 0].dropna()
            if wet_windows.empty:
                raise RuntimeError(
                    f"No complete wet windows for station {station_id}, window {window} h."
                )
            for scenario, quantile, _ in SCENARIOS:
                rows.append(
                    {
                        "Station ID": str(station_id),
                        "Rainfall Scenario": scenario,
                        "Historical Quantile": quantile,
                        "Window (h)": window,
                        "Rainfall (mm)": float(wet_windows.quantile(quantile)),
                    }
                )
    return pd.DataFrame(rows)


def build_table() -> pd.DataFrame:
    """Assemble one row per rainfall-severity and retention-factor combination."""
    rain = pd.read_parquet(
        RAIN_PATH,
        columns=["Station ID", "Observation Time", "Hourly Rainfall", "Quality Flag"],
    )
    rain = rain.loc[rain["Hourly Rainfall"].notna()].copy()
    if rain["Station ID"].nunique() < 2:
        raise RuntimeError("Scenario construction requires more than one rainfall station.")

    threshold = pd.read_parquet(
        THRESHOLD_PATH,
        columns=["Rainfall Threshold Retention Factor"],
    )
    observed_factors = set(
        threshold["Rainfall Threshold Retention Factor"].dropna().astype(float).round(2)
    )
    required_factors = {0.70, 0.80}
    if not required_factors.issubset(observed_factors):
        raise RuntimeError(
            f"Official threshold data do not contain required factors {required_factors}; "
            f"found {observed_factors}."
        )

    station_quantiles = station_wet_window_quantiles(rain)
    support = (
        station_quantiles.groupby(
            ["Rainfall Scenario", "Historical Quantile", "Window (h)"],
            as_index=False,
        )["Rainfall (mm)"]
        .median()
        .pivot(
            index=["Rainfall Scenario", "Historical Quantile"],
            columns="Window (h)",
            values="Rainfall (mm)",
        )
    )

    rows: list[dict[str, object]] = []
    for scenario, quantile, code in SCENARIOS:
        scenario_values = support.loc[(scenario, quantile)]
        for factor, factor_boundary in RETENTION_SETTINGS:
            rows.append(
                {
                    "Scenario ID": f"{code}-{int(round(factor * 100)):03d}",
                    "Rainfall Scenario": scenario,
                    "Historical Quantile": quantile,
                    "1 h Rainfall (mm)": float(scenario_values[1]),
                    "3 h Rainfall (mm)": float(scenario_values[3]),
                    "24 h Rainfall (mm)": float(scenario_values[24]),
                    "72 h Rainfall (mm)": float(scenario_values[72]),
                    "7-day Antecedent Rainfall (mm)": float(scenario_values[168]),
                    "Threshold Retention Factor": factor,
                    "Interpretation Boundary": factor_boundary,
                }
            )
    table = pd.DataFrame(rows)
    if table.shape != (9, 10):
        raise RuntimeError(f"Expected a 9 × 10 table, found {table.shape}.")
    if table["Scenario ID"].duplicated().any():
        raise RuntimeError("Scenario identifiers must be unique.")
    return table


def style_workbook(path: Path) -> None:
    """Apply compact scientific-table formatting for screen and A3 review."""
    workbook = load_workbook(path)
    worksheet = workbook[SHEET_NAME]
    worksheet.sheet_view.showGridLines = False
    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = f"A1:J{worksheet.max_row}"
    worksheet.sheet_view.zoomScale = 90
    worksheet.print_area = f"A1:J{worksheet.max_row}"
    worksheet.print_title_rows = "1:1"
    worksheet.page_setup.orientation = "landscape"
    worksheet.page_setup.paperSize = worksheet.PAPERSIZE_A3
    worksheet.page_setup.fitToWidth = 1
    worksheet.page_setup.fitToHeight = 1
    worksheet.sheet_properties.pageSetUpPr.fitToPage = True
    worksheet.page_margins = PageMargins(
        left=0.25, right=0.25, top=0.35, bottom=0.35, header=0.15, footer=0.15
    )

    header_fill = PatternFill("solid", fgColor="17365D")
    header_font = Font(name="Aptos", size=10, bold=True, color="FFFFFF")
    body_font = Font(name="Aptos", size=9.5, color="172033")
    subtle_border = Border(bottom=Side(style="thin", color="D0D5DD"))
    scenario_fills = {
        "Moderate": PatternFill("solid", fgColor="D9EDE9"),
        "Heavy": PatternFill("solid", fgColor="FCE5D4"),
        "Extreme": PatternFill("solid", fgColor="F4D6D3"),
    }

    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    worksheet.row_dimensions[1].height = 38

    for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
        scenario = str(row[1].value)
        for cell in row:
            cell.font = body_font
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = subtle_border
        row[1].fill = scenario_fills[scenario]
        row[2].number_format = "0%"
        for cell in row[3:8]:
            cell.number_format = "0.0"
        row[8].number_format = "0%"
        for cell in row[2:9]:
            cell.alignment = Alignment(horizontal="right", vertical="top")
        worksheet.row_dimensions[row[0].row].height = 34

    widths = {
        "A": 14,
        "B": 18,
        "C": 18,
        "D": 17,
        "E": 17,
        "F": 18,
        "G": 18,
        "H": 25,
        "I": 20,
        "J": 47,
    }
    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width

    worksheet.conditional_formatting.add(
        f"I2:I{worksheet.max_row}",
        ColorScaleRule(
            start_type="num",
            start_value=0.70,
            start_color="F8696B",
            mid_type="num",
            mid_value=0.80,
            mid_color="FFEB84",
            end_type="num",
            end_value=1.00,
            end_color="63BE7B",
        ),
    )
    excel_table = Table(displayName="RainfallThresholdScenarios", ref=f"A1:J{worksheet.max_row}")
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
    """Reopen the workbook and verify structure, values, and error-free cells."""
    workbook = load_workbook(path, data_only=False)
    if workbook.sheetnames != [SHEET_NAME]:
        raise RuntimeError(f"Unexpected workbook sheets: {workbook.sheetnames}")
    worksheet = workbook[SHEET_NAME]
    if worksheet.max_row != 10 or worksheet.max_column != 10:
        raise RuntimeError(
            f"Expected 10 worksheet rows including the header and 10 columns; found "
            f"{worksheet.max_row} × {worksheet.max_column}."
        )
    error_tokens = {"#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"}
    for row in worksheet.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and cell.value in error_tokens:
                raise RuntimeError(f"Spreadsheet error token in {cell.coordinate}: {cell.value}")
    factors = {float(worksheet.cell(row, 9).value) for row in range(2, 11)}
    if factors != {0.70, 0.80, 1.00}:
        raise RuntimeError(f"Unexpected retention-factor set: {factors}")
    for row in range(2, 11):
        for column in range(3, 10):
            value = worksheet.cell(row, column).value
            if not isinstance(value, (int, float)):
                raise RuntimeError(f"Expected numeric value at row {row}, column {column}.")


def main() -> None:
    table = build_table()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    table.to_excel(OUT, index=False, sheet_name=SHEET_NAME, engine="openpyxl")
    style_workbook(OUT)
    verify_workbook(OUT)
    unique_values = table.drop_duplicates("Rainfall Scenario").set_index("Rainfall Scenario")
    print(f"Saved: {OUT.relative_to(ROOT)}")
    print(f"Rows: {len(table):,}; columns: {len(table.columns):,}")
    for scenario, _, _ in SCENARIOS:
        row = unique_values.loc[scenario]
        print(
            f"{scenario}: 1 h={row['1 h Rainfall (mm)']:.1f} mm; "
            f"24 h={row['24 h Rainfall (mm)']:.1f} mm; "
            f"7 day={row['7-day Antecedent Rainfall (mm)']:.1f} mm"
        )
    print("Workbook verification: passed")


if __name__ == "__main__":
    main()
