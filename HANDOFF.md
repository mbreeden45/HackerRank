# Handoff: Builder Prep offline study app

Read this first, then `DECISIONS.md`. Phase 1 is built, committed and verified. Phase 2 and Phase 3 are not started.

## Goal
A local, offline study app that prepares a complete beginner (no coding background, Python 3) for the HackerRank Builder assessment. Passing bar: 60 percent (draw one line at 60, no 70 line).

## Learner rules (apply to ALL content)
- Plain English first, then code. Define every symbol the first time it appears. One new idea at a time.
- Always show a worked example before asking the learner to try one.
- Use the same words as the question when answering.
- Encouraging, never condescending. No exclamation marks (verify.py enforces this in prose).
- Shaky areas: for loops over values vs positions, indexing and slicing, off-by-one (len vs last position vs range), %, == vs =, sliding window, two pointers, 2D grids.

## Hard requirements
- Fully offline. No build step, no frameworks, no accounts. Launch with `start.command` (python3 http.server on 127.0.0.1:8765, opens Chrome).
- Everything vendored in `vendor/` (Pyodide 0.26.4, sql.js 1.10.3, CodeMirror 5).
- Progress is saved in localStorage key `builderPrep.v1`.

## Current state (branch `cursor/offline-study-app-vendor`)
```
start.command  index.html  DECISIONS.md  HANDOFF.md
css/app.css
js/  storage.js runner.js worker.js visuals.js explain.js lesson.js practice.js diagnostic.js app.js
content/  lessons.json diagnostic.json problems.json errors.json   (GENERATED, do not hand-edit)
tools/  c_lessons.py c_problems1.py build_content.py verify.py node_check.js
vendor/  pyodide/ sqljs/ codemirror/
```
- Content is authored in `tools/c_*.py` and built with `python3 tools/build_content.py`. Sample outputs are hand-written. Hidden outputs come from running the reference solution.
- Python runs in a Web Worker (Pyodide) with a timeout and auto-restart. Lesson trace tables come from real execution with `sys.settrace` (`bp_trace` in `js/worker.js`).
- `app.js` has a hook `BP.extraRoute(r, main, C)` for new routes, and `build_content.py` already looks for optional modules `c_problems2.py`, `c_quiz2.py` (exposes `FILES` dict name -> json), `c_cards3.py` (exposes `CARDS`).
- `verify.py` already handles optional files: `quiz_bigo.json`, `quiz_prompt.json` (MC items), `sql_problems.json` + `sql_tables.json`, `flashcards.json`, `mock_exam.json`. Match those names and shapes, or extend verify.py.

## Verification (run at the end of every phase and show the output)
```
python3 tools/build_content.py && python3 tools/verify.py
node tools/node_check.js all        # every solution through the shipped Pyodide
```
Last result: 1220 checks, 0 failed. 44 coding problems, 14 lessons, 27 multiple-choice items.
verify.py fails on: duplicate option text, fewer than 3 options, not exactly one correct answer, predict answers that differ from what the code really prints, exclamation marks in prose, starting stubs that already pass, solutions that fail their own tests.

## Known lessons learned
- The macOS python3 is 3.9, the browser's is 3.12. Avoid version-specific features. Error messages differ (see LITERALS in verify.py).
- Multiple-choice options must render with `white-space: pre-wrap` and a monospace font (already in css `.opt`). Anything new that shows code or output must do the same.
- Browser testing: serve with `python3 -m http.server 8765 --bind 127.0.0.1` and drive the page. After CSS changes, reload.
- Project sits under `~/.cursor`, which some sandboxes cannot write to.

## Remaining build (in this order). Do NOT build: SQL Advanced, System Design, Stakeholder Communication, heaps, greedy, dashboard or scores chart, printable cheat sheet, export/import backup.

### Phase 2
1. Python patterns lessons, each with visuals and a trace: hashmaps (dict, counting), sorting (`sorted`, `key=`), two pointers, sliding window, 2D grid traversal. Use `lesson.window = ['left','right']` and grid `r`,`c` support in `visuals.js`. About 8 problems per pattern, labelled Easy/Medium/Hard, 4 hints each, plus 2 to 3 lessons on strings and parsing.
2. Big O: 1 lesson and about 15 multiple-choice questions (`quiz_bigo.json`).
3. Prompt Engineering (highest weighted): 3 lessons, about 30 items (`quiz_prompt.json`). Multiple choice (pick the better prompt) plus short written answers graded by a checklist rubric: the learner sees a model answer and ticks the key points covered, with a keyword auto-check as a hint only.
4. SQL Foundations with sql.js: `js/sql-runner.js`, 4 lessons (SELECT/WHERE, ORDER BY, JOIN, GROUP BY/HAVING), about 30 problems, sample tables (employees, orders, customers, accounts) in `sql_tables.json`. A SQL practice screen mirroring the Python one (editor, Run, results grid, expected vs actual, hints). `verify.py` runs every SQL solution with Python's sqlite3.
5. Adaptive practice: pick the next problem from the weakest topic, one level above current success, and bring missed items back after 1, 3 and 7 days.

### Phase 3
1. Mock exam: timed (90 minutes), mixed sections weighted by priority (Prompt Engineering, Problem Solving, SQL Foundations high), no hints, score report by topic, a line at 60 percent, recommended next focus. No 15-minute sprint.
2. Flashcards with spaced repetition, about 80 cards worded "I want to... so I write...". Cards with code get an executed `check`.

Stop after each phase for review. Commit on the existing branch.

## Prompts to paste into Claude Code

### Prompt 0: orient (use first)
```
Read HANDOFF.md and DECISIONS.md in this repo, then skim js/ and tools/. Do not change anything yet. Run `python3 tools/build_content.py && python3 tools/verify.py` and tell me the result, then summarise in 10 lines what is built and what Phase 2 involves. Ask me nothing unless you are blocked.
```

### Prompt 1: Phase 2 part A, patterns and Big O
```
Follow HANDOFF.md. Build Phase 2 part A only: the lessons (hashmaps, sorting, two pointers, sliding window, 2D grids, strings and parsing, Big O) and their problems, plus quiz_bigo.json with about 15 multiple-choice questions. Author content in new tools/c_*.py modules so build_content.py picks it up. Match the learner rules exactly: plain English, define every symbol, worked example before a try, no exclamation marks. Every problem needs 4 hints and a hand-written sample output. Add a multiple-choice quiz screen to the app (route via BP.extraRoute) that renders options with pre-wrap monospace. Run build_content.py, verify.py and node_check.js and show me the full output. Fix any failure before stopping. Commit.
```

### Prompt 2: Phase 2 part B, Prompt Engineering
```
Follow HANDOFF.md. Build Prompt Engineering: 3 lessons and about 30 items in quiz_prompt.json (extraction and summarization, completeness validation, structured output). Include multiple choice (choose the better prompt) and short written answers with a model answer and a checklist rubric the learner ticks, with a keyword auto-check as a hint only. Each written item needs 4 to 6 rubric points. Extend verify.py to check rubrics are non-empty and multiple-choice items follow the existing rules. Show the full verify output and commit.
```

### Prompt 3: Phase 2 part C, SQL Foundations
```
Follow HANDOFF.md. Build SQL Foundations with sql.js (already in vendor/sqljs). Create js/sql-runner.js, a SQL practice screen with a CodeMirror editor, Run and Check buttons, a results table, expected vs actual, and the 4-step hint ladder. Write sql_tables.json (employees, orders, customers, accounts) and about 30 problems with 4 lessons (SELECT and WHERE, ORDER BY, JOIN, GROUP BY and HAVING). verify.py must run every SQL solution with Python sqlite3, and add a browser-side check that sql.js gives the same rows. Show the full verify output, test the screen in a real browser, and commit.
```

### Prompt 4: adaptive practice
```
Follow HANDOFF.md. Add adaptive practice: a "Next best question" button on Home that picks from the weakest topic using stored accuracy and hint use, one difficulty above recent success, and re-queues missed items after 1, 3 and 7 days. Keep state in the existing localStorage key. Add a small unit test script under tools/ that simulates answer histories and checks the picker's choices. Commit.
```

### Prompt 5: Phase 3, mock exam
```
Follow HANDOFF.md. Build the mock exam: 90-minute timer, mixed sections weighted by priority, no hints, a Submit button, then a score report by topic with one line drawn at 60 percent, a clear above or below statement, and a recommended next focus. Save results in localStorage. Write mock_exam.json referencing existing item ids, and make verify.py fail on unknown ids. Test the whole flow in a real browser, including a timer expiry using a short debug override. Commit.
```

### Prompt 6: Phase 3, flashcards
```
Follow HANDOFF.md. Build flashcards: about 80 cards worded "I want to... so I write...", spaced repetition with Again, Hard, Good and Easy buttons and stored due dates. Cards with code include a `check` that verify.py executes and compares. Show the full verify output and commit.
```

### Prompt 7: final audit
```
Audit everything before you tell me it is done. Run build_content.py, verify.py and node_check.js. Open the app in a real browser and click through: the diagnostic, one lesson trace, one Python problem (Run Code, Run all test cases, Custom Input, hints), one SQL problem, a quiz, a short mock exam, and flashcards. Confirm no multiple-choice option text collapses, offline mode works (no external URLs: grep for http), and the 60 percent line shows. Report counts per content file and anything you could not test.
```

## Open points to tell the user
- Offline use was not tested in real airplane mode. Check by running one problem with Wi-Fi off after the first load.
- Phase 1 has 44 problems, not about 50.
