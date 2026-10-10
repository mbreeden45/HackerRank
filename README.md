# HackerRank Builder Prep

An offline study app that takes a complete beginner (Python 3, no coding background) to the 60 percent pass line on the HackerRank Builder assessment.

## What is in it
- Placement check, then lessons with step-by-step traces: Python basics, patterns (hashmaps, sorting, two pointers, sliding window, 2D grids), strings and parsing, Big O
- 96 Python problems and 32 SQL problems (Easy, Medium, Hard, 4 hints each), run in the browser with Pyodide and sql.js
- Prompt Engineering lessons and 30 questions, including written answers checked against a model answer
- "Next best question" adaptive practice, with missed items coming back after 1, 3 and 7 days
- 90 minute mock exam with a score report and a line at 60 percent
- 88 spaced repetition flashcards ("I want to... so I write...")

## Run it
You need `python3` (built into macOS once the Command Line Tools are installed).

1. Double-click `start.command`, or run `python3 tools/serve.py` from this folder.
2. Open http://localhost:8765 (the port matters: your progress is saved in the browser under that address).
3. Leave the terminal window open while you study.

Everything is vendored in `vendor/`, so it works with no internet after the first load.

## Getting the latest version
```
git pull
```
Then restart `start.command` and reload the page. If a page looks old, hard-refresh with Cmd+Shift+R.

## For contributors
Content is written in `tools/c_*.py` and built into `content/*.json`. Do not edit `content/` by hand.

```
python3 tools/build_content.py && python3 tools/verify.py
node tools/node_check.js all
node tools/node_sql_check.js
node tools/test_adaptive.js && node tools/test_cards.js && node tools/test_explain.js
python3 tools/brute_check.py
```
See `HANDOFF.md` and `DECISIONS.md` for how it is put together and why.
