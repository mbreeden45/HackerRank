#!/bin/bash
# Double-click to start Builder Prep. Needs python3 (built into macOS once Command Line Tools are installed).
cd "$(dirname "$0")"
PORT=8765
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 was not found."
  echo "Fix: open Terminal and run:  xcode-select --install   (then double-click this file again)"
  echo "Or install Python from https://www.python.org/downloads/ once."
  read -n 1 -s -r -p "Press any key to close."
  exit 1
fi
echo "Builder Prep is starting at http://localhost:$PORT"
echo "Leave this window open while you study. Close it to stop."
(sleep 1; open -a "Google Chrome" "http://localhost:$PORT" 2>/dev/null || open "http://localhost:$PORT") &
python3 -m http.server $PORT --bind 127.0.0.1
