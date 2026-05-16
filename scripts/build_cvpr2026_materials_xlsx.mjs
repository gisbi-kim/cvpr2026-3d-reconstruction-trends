import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = process.cwd();
const outDir = path.join(root, "output");

async function readText(file) {
  return fs.readFile(path.join(outDir, file), "utf8");
}

function stripBom(text) {
  return text.replace(/^\uFEFF/, "");
}

function parseCsv(text) {
  text = stripBom(text);
  const rows = [];
  let row = [];
  let field = "";
  let inQuotes = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (inQuotes) {
      if (ch === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ",") {
      row.push(field);
      field = "";
    } else if (ch === "\n") {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ""));
    rows.push(row);
  }
  return rows.filter((r) => r.some((v) => String(v).trim() !== ""));
}

function countRowsBy(rows, headerName) {
  const header = rows[0];
  const idx = header.indexOf(headerName);
  const counts = new Map();
  for (const row of rows.slice(1)) {
    const key = row[idx] || "(blank)";
    counts.set(key, (counts.get(key) || 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1]);
}

function writeBlock(sheet, startCell, matrix, header = true) {
  const range = sheet.getRange(startCell).resize(matrix.length, matrix[0].length);
  range.values = matrix;
  if (header) {
    const headerRange = range.getRow(0);
    headerRange.format.fill = { color: "#235789" };
    headerRange.format.font = { color: "#FFFFFF", bold: true };
  }
  range.format.wrapText = true;
  range.format.autofitColumns();
  range.format.autofitRows();
}

function writeSheetFromRows(workbook, name, rows) {
  const sheet = workbook.worksheets.add(name);
  const rowCount = rows.length;
  const colCount = Math.max(...rows.map((r) => r.length));
  const normalized = rows.map((r) => {
    const row = [...r];
    while (row.length < colCount) row.push("");
    return row;
  });
  sheet.getRangeByIndexes(0, 0, rowCount, colCount).values = normalized;
  const headerRange = sheet.getRangeByIndexes(0, 0, 1, colCount);
  headerRange.format.fill = { color: "#235789" };
  headerRange.format.font = { color: "#FFFFFF", bold: true };
  return sheet;
}

function styleUsed(sheet) {
  const used = sheet.getUsedRange();
  if (!used) return;
  used.format.font = { name: "Arial", size: 10 };
  used.format.wrapText = true;
  used.format.autofitColumns();
  used.format.autofitRows();
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
}

async function main() {
  const seedCsv = await readText("cvpr2026_3d_recon_blog_seed_list.csv");
  const strictCsv = await readText("cvpr2026_3d_recon_strict_reading_list.csv");
  const broadCsv = await readText("cvpr2026_3d_recon_broad_candidates.csv");
  const summaryCsv = await readText("cvpr2026_3d_recon_cluster_summary.csv");

  const seedRows = parseCsv(seedCsv);
  const strictRows = parseCsv(strictCsv);
  const broadRows = parseCsv(broadCsv);
  const summaryRows = parseCsv(summaryCsv);

  const workbook = Workbook.create();
  const summary = workbook.worksheets.add("Summary");
  summary.showGridLines = false;
  summary.mergeCells("A1:F1");
  summary.getRange("A1").values = [["CVPR 2026 3D Reconstruction Materials"]];
  summary.getRange("A1").format.font = { bold: true, size: 18, color: "#171717" };
  summary.getRange("A1:F1").format.rowHeightPx = 34;
  summary.getRange("A3:B7").values = [
    ["Metric", "Value"],
    ["Explorer papers parsed", 4070],
    ["Broad candidates", broadRows.length - 1],
    ["Strict reading candidates", strictRows.length - 1],
    ["Blog seed papers", seedRows.length - 1],
  ];
  summary.getRange("A3:B3").format.fill = { color: "#235789" };
  summary.getRange("A3:B3").format.font = { color: "#FFFFFF", bold: true };

  const clusters = summaryRows
    .filter((r) => r[0] === "cluster")
    .map((r) => [r[3], Number(r[2])]);
  writeBlock(summary, "D3", [["Cluster", "Count"], ...clusters], true);
  const clusterChart = summary.charts.add("bar", summary.getRange(`D3:E${clusters.length + 3}`));
  clusterChart.title = "Strict Candidate Cluster Counts";
  clusterChart.hasLegend = false;
  clusterChart.xAxis = { axisType: "textAxis" };
  clusterChart.setPosition("G3", "N18");

  const bucketCounts = countRowsBy(seedRows, "editorial_bucket");
  writeBlock(summary, "A10", [["Seed editorial bucket", "Count"], ...bucketCounts], true);
  const bucketChart = summary.charts.add("bar", summary.getRange(`A10:B${bucketCounts.length + 10}`));
  bucketChart.title = "Blog Seed Papers by Editorial Bucket";
  bucketChart.hasLegend = false;
  bucketChart.xAxis = { axisType: "textAxis" };
  bucketChart.setPosition("G20", "N34");

  const cross = summaryRows
    .filter((r) => r[0] === "cross_cluster")
    .slice(0, 15)
    .map((r) => [r[1], Number(r[2]), r[3]]);
  writeBlock(summary, "D20", [["Cross-cluster signal", "Count", "Label"], ...cross], true);
  styleUsed(summary);
  summary.getRange("A:A").format.columnWidthPx = 330;
  summary.getRange("B:B").format.columnWidthPx = 80;
  summary.getRange("D:D").format.columnWidthPx = 360;
  summary.getRange("E:E").format.columnWidthPx = 70;
  summary.getRange("F:F").format.columnWidthPx = 460;
  summary.getRange("A10:B17").format.rowHeightPx = 32;
  summary.getRange("D20:F35").format.rowHeightPx = 34;

  writeSheetFromRows(workbook, "SeedList", seedRows);
  writeSheetFromRows(workbook, "StrictReadingList", strictRows);
  writeSheetFromRows(workbook, "BroadCandidates", broadRows);
  writeSheetFromRows(workbook, "ClusterSummary", summaryRows);

  for (const name of ["SeedList", "StrictReadingList", "BroadCandidates", "ClusterSummary"]) {
    const sheet = workbook.worksheets.getItem(name);
    styleUsed(sheet);
    sheet.getRange("A:A").format.columnWidthPx = 46;
    sheet.getRange("D:D").format.columnWidthPx = 340;
    sheet.getRange("K:K").format.columnWidthPx = 360;
    sheet.getRange("N:N").format.columnWidthPx = 520;
  }

  const inspect = await workbook.inspect({
    kind: "sheet,table",
    maxChars: 5000,
    tableMaxRows: 4,
    tableMaxCols: 8,
  });
  console.log(inspect.ndjson);

  const errors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 20 },
    summary: "formula error scan",
  });
  console.log(errors.ndjson);

  const preview = await workbook.render({
    sheetName: "Summary",
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  await fs.writeFile(
    path.join(outDir, "cvpr2026_3d_recon_materials_preview.png"),
    new Uint8Array(await preview.arrayBuffer()),
  );

  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(path.join(outDir, "cvpr2026_3d_recon_materials.xlsx"));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
