#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = process.cwd();
const sourcePath = path.join(
  root,
  "data/exp/revision/reviewer-3-comment-5/spatially_correlated_closure_summary.csv",
);
const referencePath = path.join(
  root,
  "data/results/tables/Table_threshold_baseline_and_rainfall_parameter_sensitivity.xlsx",
);
const outputPath = path.join(
  root,
  "data/results/tables/Table_spatial_closure_dependence_sensitivity.xlsx",
);
const previewPath = path.join(
  root,
  "data/exp/revision/reviewer-3-comment-5/Table_spatial_closure_dependence_sensitivity.png",
);
const referencePreviewPath = "/private/tmp/ke01e-r3c5-reference-table.png";

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') {
        field += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        field += char;
      }
    } else if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n") {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += char;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ""));
    rows.push(row);
  }
  return rows;
}

function asNumber(record, key) {
  const value = Number(record[key]);
  if (!Number.isFinite(value)) {
    throw new Error(`Non-numeric ${key}: ${record[key]}`);
  }
  return value;
}

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(path.dirname(previewPath), { recursive: true });

// Render and inspect an existing project table before authoring so the new
// workbook follows the established restrained blue-gray visual language.
const referenceBlob = await FileBlob.load(referencePath);
const referenceWorkbook = await SpreadsheetFile.importXlsx(referenceBlob);
const referenceInspection = await referenceWorkbook.inspect({
  kind: "workbook,sheet,region,computedStyle",
  range: "A1:G10",
  maxChars: 5000,
  tableMaxRows: 10,
  tableMaxCols: 7,
});
const referencePreview = await referenceWorkbook.render({
  sheetName: referenceWorkbook.worksheets.getItemAt(0).name,
  autoCrop: "all",
  scale: 1.5,
  format: "png",
});
await fs.writeFile(
  referencePreviewPath,
  new Uint8Array(await referencePreview.arrayBuffer()),
);

const csvRows = parseCsv(await fs.readFile(sourcePath, "utf8"));
const headers = csvRows[0];
const records = csvRows.slice(1).filter((row) => row.some((value) => value !== "")).map((row) =>
  Object.fromEntries(headers.map((header, index) => [header, row[index]])),
);
if (records.length !== 15) {
  throw new Error(`Expected 15 sensitivity rows, found ${records.length}.`);
}

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Spatial dependence");
sheet.showGridLines = false;
sheet.mergeCells("A1:L1");
sheet.getRange("A1").values = [["Table B8. Spatial Closure-Dependence Sensitivity"]];
sheet.getRange("A2:L2").values = [[
  "Rainfall scenario",
  "Dependence setting",
  "Cluster scale (km)",
  "ρ",
  "Expected isolated population",
  "Expected isolated population age 65+",
  "Mean change vs independent",
  "Per-draw P95",
  "P95 change vs independent",
  "Community-frequency Spearman correlation",
  "Top-30 burden overlap",
  "Communities with |Δfrequency| ≥ 0.05",
]];

const dataValues = records.map((record) => [
  record.scenario,
  record.dependence_setting,
  asNumber(record, "cluster_scale_km"),
  asNumber(record, "rho"),
  asNumber(record, "expected_isolated_population_mean"),
  asNumber(record, "expected_isolated_older_population_mean"),
  null,
  asNumber(record, "draw_isolated_population_p95"),
  null,
  asNumber(record, "community_frequency_spearman_vs_independent"),
  asNumber(record, "top30_burden_overlap_vs_independent"),
  asNumber(record, "communities_abs_frequency_change_ge_0_05"),
]);
sheet.getRange("A3:L17").values = dataValues;

const baseRows = { Moderate: 3, Heavy: 8, Extreme: 13 };
for (let row = 3; row <= 17; row += 1) {
  const scenario = dataValues[row - 3][0];
  const baseRow = baseRows[scenario];
  sheet.getRange(`G${row}`).formulas = [[`=E${row}/$E$${baseRow}-1`]];
  sheet.getRange(`I${row}`).formulas = [[`=H${row}/$H$${baseRow}-1`]];
}

sheet.mergeCells("A19:L19");
sheet.getRange("A19").values = [[
  "Interpretation: dependence settings preserve section-level marginal closure propensities and are uncalibrated sensitivity bounds, not alternative failure forecasts.",
]];
sheet.mergeCells("A20:L20");
sheet.getRange("A20").values = [[
  "Design: independent reference; 1 km and 3 km square clusters at ρ = 0.25 and 0.50; five seeds and 1,000 draws per seed for each rainfall scenario.",
]];

sheet.getRange("A1:L1").format = {
  fill: "#D9EAF7",
  font: { bold: true, color: "#17365D", size: 15 },
  horizontalAlignment: "left",
  verticalAlignment: "center",
};
sheet.getRange("A2:L2").format = {
  fill: "#17365D",
  font: { bold: true, color: "#FFFFFF", size: 9 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: "#A6B7C8" },
};
sheet.getRange("A3:L17").format = {
  font: { color: "#1F1F1F", size: 10 },
  verticalAlignment: "center",
  borders: {
    insideHorizontal: { style: "thin", color: "#D9E2F3" },
    bottom: { style: "thin", color: "#A6B7C8" },
  },
};
sheet.getRange("A3:B17").format.horizontalAlignment = "left";
sheet.getRange("C3:L17").format.horizontalAlignment = "right";
sheet.getRange("A19:L20").format = {
  fill: "#F3F6F8",
  font: { italic: true, color: "#4F5B66", size: 9 },
  horizontalAlignment: "left",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "outside", style: "thin", color: "#D5DCE3" },
};

sheet.getRange("A1:L1").format.rowHeight = 28;
sheet.getRange("A2:L2").format.rowHeight = 46;
sheet.getRange("A3:L17").format.rowHeight = 22;
sheet.getRange("A19:L20").format.rowHeight = 34;
sheet.getRange("A:A").format.columnWidth = 15;
sheet.getRange("B:B").format.columnWidth = 17;
sheet.getRange("C:C").format.columnWidth = 13;
sheet.getRange("D:D").format.columnWidth = 7;
sheet.getRange("E:F").format.columnWidth = 17;
sheet.getRange("G:G").format.columnWidth = 15;
sheet.getRange("H:H").format.columnWidth = 12;
sheet.getRange("I:I").format.columnWidth = 14;
sheet.getRange("J:J").format.columnWidth = 17;
sheet.getRange("K:K").format.columnWidth = 14;
sheet.getRange("L:L").format.columnWidth = 18;

sheet.getRange("C3:C17").format.numberFormat = "0.0";
sheet.getRange("D3:D17").format.numberFormat = "0.00";
sheet.getRange("E3:F17").format.numberFormat = "#,##0.0";
sheet.getRange("G3:G17").format.numberFormat = "+0.0%;-0.0%;0.0%";
sheet.getRange("H3:H17").format.numberFormat = "#,##0.0";
sheet.getRange("I3:I17").format.numberFormat = "+0.0%;-0.0%;0.0%";
sheet.getRange("J3:J17").format.numberFormat = "0.000";
sheet.getRange("K3:K17").format.numberFormat = "0.0%";
sheet.getRange("L3:L17").format.numberFormat = "#,##0";

for (const row of [3, 8, 13]) {
  sheet.getRange(`A${row}:L${row}`).format.fill = "#EDF4FA";
  sheet.getRange(`A${row}:L${row}`).format.font = {
    bold: true,
    color: "#17365D",
    size: 10,
  };
}
sheet.freezePanes.freezeRows(2);

const inspection = await workbook.inspect({
  kind: "sheet,region,formula",
  sheetId: sheet.name,
  range: "A1:L20",
  include: "values,formulas",
  maxChars: 12000,
  tableMaxRows: 20,
  tableMaxCols: 12,
});
const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
const preview = await workbook.render({
  sheetName: sheet.name,
  range: "A1:L20",
  scale: 1.5,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);

console.log(JSON.stringify({
  referenceInspection: referenceInspection.ndjson,
  inspection: inspection.ndjson,
  formulaErrors: errors.ndjson,
  outputPath,
  previewPath,
  referencePreviewPath,
}, null, 2));
