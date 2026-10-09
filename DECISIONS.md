# Decisions

- Passing line is 60 percent (official Deployment Strategist bar). There is no 70 percent line.
- Launch with `start.command` (runs `python3 -m http.server` on 127.0.0.1:8765 and opens Chrome). A server is needed because Chrome will not load Pyodide from a double-clicked file.
- Editor: CodeMirror 5 (plain script files, no build step). CodeMirror 6 needs a bundler, which breaks the "no build step" rule.
- Python in the browser: Pyodide 0.26.4 (Python 3.12), core files only (about 13 MB), run in a Web Worker. Endless loops are stopped by a timeout and the worker restarts.
- SQL: sql.js 1.10.3 is already vendored in `vendor/sqljs/` for Phase 2.
- Lesson trace tables are produced by really running the lesson code with `sys.settrace`, so they cannot disagree with Python.
- Content is written in `tools/c_*.py` and built into `content/*.json` with `python3 tools/build_content.py`. Sample outputs are written by hand. Hidden-test outputs are produced by running the reference solution.
- `python3 tools/verify.py` checks every reference solution against its tests, that the starting stub does not already pass, that lesson "predict" answers match real output, that diagnostic answers match real output, that error translations match real Python errors, and that prose has no exclamation marks.
- `node tools/node_check.js all` runs every reference solution through the same Pyodide files the app ships, to prove the browser engine agrees with python3.
- Phase 1 has 44 problems (not about 50), 14 lessons, 13 diagnostic questions and 30 error patterns.
- The macOS system Python is 3.9, the browser's is 3.12. Problems avoid features that differ.
- Progress is saved in the browser's localStorage under `builderPrep.v1`. localStorage belongs to the address `127.0.0.1:8765`, so always use the same address (start.command does).
