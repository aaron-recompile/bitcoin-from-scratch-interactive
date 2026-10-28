// Run every code cell of each notebook in a fresh Pyodide, the same Python the
// site uses in the reader's browser. Exits non-zero if any cell raises.
//
// Usage: node tools/pyodide_test.mjs book/*.ipynb
import { loadPyodide } from "pyodide";
import fs from "fs";
import path from "path";

let failed = 0;
for (const file of process.argv.slice(2)) {
  const py = await loadPyodide();
  py.setStdout({ batched: () => {} });
  const cells = JSON.parse(fs.readFileSync(file)).cells.filter((c) => c.cell_type === "code");
  const t0 = Date.now();
  let error = null;
  for (let i = 0; i < cells.length && !error; i++) {
    try {
      await py.runPythonAsync([].concat(cells[i].source).join(""));
    } catch (e) {
      error = `code cell ${i + 1}: ${String(e.message).trim().split("\n").slice(-1)[0]}`;
    }
  }
  const secs = ((Date.now() - t0) / 1000).toFixed(1);
  console.log(`${error ? "FAIL" : "ok  "}  ${path.basename(file)}  ${cells.length} cells  ${secs}s${error ? "  " + error : ""}`);
  if (error) failed++;
}
process.exit(failed ? 1 : 0);
