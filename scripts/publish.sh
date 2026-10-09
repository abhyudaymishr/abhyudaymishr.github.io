#!/usr/bin/env bash
# Quick launcher for Mac Shortcut / Terminal
set -e

# Resolve repository directory reliably
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "/Users/abhyuday/abhyudaymishr.github.io/scripts")"
REPO_DIR="$(cd "$SCRIPT_DIR/.." 2>/dev/null && pwd || echo "/Users/abhyuday/abhyudaymishr.github.io")"

if [ ! -f "$REPO_DIR/scripts/publish_note.py" ]; then
  REPO_DIR="/Users/abhyuday/abhyudaymishr.github.io"
fi

/usr/bin/python3 "$REPO_DIR/scripts/publish_note.py" "$@"

