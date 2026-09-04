#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = process.cwd();
const outDir = path.join(root, "data/exp/revision/reviewer-4-comment-4");
const csvPath = path.join(outDir, "closure_mapping_summary.csv");
const xlsxPath = path.join(outDir, "Table_closure_mapping_policy_sensitivity.xlsx");
const pngPath = path.join(outDir, "Table_closure_mapping_policy_sensitivity.png");

const csvText = await fs.readFile(csvPath, "utf8");
const imported = await Workbook.fromCSV(csvText, { sheetName: "Imported" });
const importedValues = imported.worksheets.getItem("Imported").getUsedRange(true).values;
const header = importedValues[0];
const numericColumns = new Set(header.slice(1).map((_, index) => index + 1));
const interpretations = {
  Low: "Lower-bound stress check",
  Central: "Transparent reference",
  High: "Capacity stress test",
};
const rows = importedValues.slice(1).map((row) => [
  ...row.map((value, index) =>
    numericColumns.has(index) && value !== "" ? Number(value) : value
  ),
  interpretations[row[0]],
]);

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Closure mapping");
sheet.showGridLines = false;
sheet.tabColor = "#2F6F73";
sheet.getRange("A1:K1").merge();
sheet.getRange("A1").values = [[
  "Table B12. Heavy-scenario closure-mapping sensitivity under matched simulation seeds",
]];
sheet.getRange("A2:K2").values = [[...header, "Planning use"]];
sheet.getRange("A3:K5").values = rows;
sheet.getRange("A7:K7").merge();
sheet.getRange("A7").values = [[
  "Notes: All settings use the same five prespecified seeds and 1,000 draws per seed. Low and High are declared planning stress bounds, not confidence limits. Top-30 communities are ranked by population-weighted disconnection burden.",
]];

sheet.getRange("A1:K1").format = {
  fill: "#215A5E",
  font: { bold: true, color: "#FFFFFF", size: 14 },
  horizontalAlignment: "left",
  verticalAlignment: "center",
};
sheet.getRange("A1:K1").format.rowHeight = 30;
sheet.getRange("A2:K2").format = {
  fill: "#DDECEF",
  font: { bold: true, color: "#173F42", size: 10 },
  wrapText: true,
  horizontalAlignment: "center",
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#B8CDD0" },
};
sheet.getRange("A2:K2").format.rowHeight = 48;
sheet.getRange("A3:K5").format = {
  font: { color: "#1F2933", size: 10 },
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#D8E2E4" },
};
sheet.getRange("A3:K5").format.rowHeight = 25;
sheet.getRange("A4:K4").format.fill = "#EEF6F7";
sheet.getRange("A4:K4").format.font = { bold: true, color: "#173F42", size: 10 };
sheet.getRange("A7:K7").format = {
  fill: "#F4F7F8",
  font: { italic: true, color: "#52646A", size: 9 },
  wrapText: true,
  verticalAlignment: "center",
};
sheet.getRange("A7:K7").format.rowHeight = 42;

sheet.getRange("B3:B5").setNumberFormat("0.00");
sheet.getRange("C3:F5").setNumberFormat("0.0");
sheet.getRange("G3:G5").setNumberFormat("0.0%");
sheet.getRange("H3:I5").setNumberFormat("0.000");
sheet.getRange("J3:J5").setNumberFormat("0");
sheet.getRange("A3:A5").format.horizontalAlignment = "left";
sheet.getRange("B3:J5").format.horizontalAlignment = "right";
sheet.getRange("K3:K5").format.horizontalAlignment = "left";

const widths = [18, 16, 18, 14, 14, 14, 16, 17, 17, 18, 20];
widths.forEach((width, index) => {
  sheet.getRangeByIndexes(0, index, 7, 1).format.columnWidth = width;
});
sheet.getRange("A1:K7").format.wrapText = true;
sheet.freezePanes.freezeRows(2);

const inspection = await workbook.inspect({
  kind: "region",
  sheetId: "Closure mapping",
  range: "A1:K7",
  maxChars: 8000,
});
console.log(inspection.ndjson);

await fs.mkdir(outDir, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(xlsxPath);
const preview = await workbook.render({
  sheetName: "Closure mapping",
  range: "A1:K7",
  scale: 1.35,
  format: "png",
});
await fs.writeFile(pngPath, new Uint8Array(await preview.arrayBuffer()));
console.log(JSON.stringify({ xlsxPath, pngPath }));
