#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import {
  SpreadsheetFile,
  Workbook,
} from "/Users/lichao/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const root = process.cwd();
const outDir = path.join(root, "data/exp/revision/reviewer-2-comment-6");
const csvPath = path.join(outDir, "intervention_parameter_sensitivity.csv");
const xlsxPath = path.join(outDir, "Table_intervention_parameter_sensitivity.xlsx");
const pngPath = path.join(outDir, "Table_intervention_parameter_sensitivity.png");

const imported = await Workbook.fromCSV(await fs.readFile(csvPath, "utf8"), {
  sheetName: "Imported",
});
const source = imported.worksheets.getItem("Imported").getUsedRange(true).values;
const header = source[0];
const index = Object.fromEntries(header.map((value, position) => [value, position]));
const rows = source.slice(1).map((row) => {
  const minimum = Number(row[index["Protected Population Seed Minimum"]]);
  const maximum = Number(row[index["Protected Population Seed Maximum"]]);
  return [
    row[index["Parameter Family"]],
    row[index.Setting],
    Number(row[index["Attachment Coefficient"]]),
    Number(row[index["Positive Score Road Count"]]),
    Number(row[index["Score Spearman vs Central"]]),
    Number(row[index["Top-30 Overlap vs Central"]]),
    Number(row[index["Selected Road Count"]]),
    Number(row[index["Selected-Portfolio Overlap vs Central"]]),
    Number(row[index["Realized Planning Cost"]]),
    `${row[index["Temporary Reinforcement Count"]]}/${row[index["Clearance Pre-positioning Count"]]}/${row[index["Alternative-route Protection Count"]]}`,
    `${Number(row[index["Protected Population"]]).toFixed(1)} [${minimum.toFixed(1)}–${maximum.toFixed(1)}]`,
    Number(row[index["Protected Population Change vs Central"]]),
  ];
});

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Intervention sensitivity");
sheet.showGridLines = false;
sheet.tabColor = "#2F6F73";
sheet.getRange("A1:L1").merge();
sheet.getRange("A1").values = [[
  "Table B13. One-family-at-a-time sensitivity of intervention screening assumptions",
]];
sheet.getRange("A2:L2").values = [[
  "Parameter family",
  "Setting",
  "Attachment coefficient (λ)",
  "Roads with positive score",
  "Score Spearman vs Central",
  "Top-30 overlap vs Central",
  "Selected roads",
  "Portfolio overlap vs Central",
  "Realized planning cost",
  "Action mix (R/C/A)",
  "Protected population, mean [seed range]",
  "Change vs Central",
]];
sheet.getRange(`A3:L${rows.length + 2}`).values = rows;
const noteRow = rows.length + 4;
sheet.getRange(`A${noteRow}:L${noteRow}`).merge();
sheet.getRange(`A${noteRow}`).values = [[
  "Notes: Heavy rainfall, Primary Emergency Road backbone, five prespecified seeds, and 1,000 draws per seed. The fixed budget is 269.131 relative planning units. R/C/A denotes temporary reinforcement, clearance pre-positioning, and alternative-route protection. The λ = 0 Spearman value is tie-sensitive because only 216 roads retain a positive score. All parameter values are declared planning stress assumptions, not locally calibrated engineering estimates.",
]];

sheet.getRange("A1:L1").format = {
  fill: "#215A5E",
  font: { bold: true, color: "#FFFFFF", size: 14 },
  horizontalAlignment: "left",
  verticalAlignment: "center",
};
sheet.getRange("A1:L1").format.rowHeight = 30;
sheet.getRange("A2:L2").format = {
  fill: "#DDECEF",
  font: { bold: true, color: "#173F42", size: 9 },
  wrapText: true,
  horizontalAlignment: "center",
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#B8CDD0" },
};
sheet.getRange("A2:L2").format.rowHeight = 46;
sheet.getRange(`A3:L${rows.length + 2}`).format = {
  font: { color: "#1F2933", size: 9 },
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#D8E2E4" },
};
sheet.getRange(`A3:L${rows.length + 2}`).format.rowHeight = 23;
for (let row = 3; row <= rows.length + 2; row += 1) {
  if (row % 2 === 0) sheet.getRange(`A${row}:L${row}`).format.fill = "#F7FAFA";
  if (sheet.getRange(`B${row}`).values[0][0] === "Central reference") {
    sheet.getRange(`A${row}:L${row}`).format.fill = "#EEF6F7";
    sheet.getRange(`A${row}:L${row}`).format.font = {
      bold: true,
      color: "#173F42",
      size: 9,
    };
  }
}
sheet.getRange(`A${noteRow}:L${noteRow}`).format = {
  fill: "#F4F7F8",
  font: { italic: true, color: "#52646A", size: 9 },
  wrapText: true,
  verticalAlignment: "center",
};
sheet.getRange(`A${noteRow}:L${noteRow}`).format.rowHeight = 58;

sheet.getRange(`C3:C${rows.length + 2}`).setNumberFormat("0.000");
sheet.getRange(`D3:D${rows.length + 2}`).setNumberFormat("0");
sheet.getRange(`E3:E${rows.length + 2}`).setNumberFormat("0.000");
sheet.getRange(`F3:F${rows.length + 2}`).setNumberFormat("0.0%");
sheet.getRange(`G3:G${rows.length + 2}`).setNumberFormat("0");
sheet.getRange(`H3:H${rows.length + 2}`).setNumberFormat("0.0%");
sheet.getRange(`I3:I${rows.length + 2}`).setNumberFormat("0.0");
sheet.getRange(`L3:L${rows.length + 2}`).setNumberFormat("+0.0%;-0.0%;0.0%");
sheet.getRange(`A3:B${rows.length + 2}`).format.horizontalAlignment = "left";
sheet.getRange(`C3:L${rows.length + 2}`).format.horizontalAlignment = "right";

const widths = [20, 20, 14, 14, 14, 14, 11, 14, 13, 13, 22, 13];
widths.forEach((width, column) => {
  sheet.getRangeByIndexes(0, column, noteRow, 1).format.columnWidth = width;
});
sheet.getRange(`A1:L${noteRow}`).format.wrapText = true;
sheet.freezePanes.freezeRows(2);

const inspection = await workbook.inspect({
  kind: "region",
  sheetId: "Intervention sensitivity",
  range: `A1:L${noteRow}`,
  maxChars: 14000,
});
console.log(inspection.ndjson);

await fs.mkdir(outDir, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(xlsxPath);
const preview = await workbook.render({
  sheetName: "Intervention sensitivity",
  range: `A1:L${noteRow}`,
  scale: 1.25,
  format: "png",
});
await fs.writeFile(pngPath, new Uint8Array(await preview.arrayBuffer()));
console.log(JSON.stringify({ xlsxPath, pngPath }));
