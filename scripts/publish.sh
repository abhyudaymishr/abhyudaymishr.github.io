#!/usr/bin/env bash
# Quick launcher for Mac Shortcut / Terminal
set -e
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$REPO_DIR/scripts/publish_note.py" "$@"
