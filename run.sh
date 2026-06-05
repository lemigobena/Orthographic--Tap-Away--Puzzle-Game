#!/bin/bash
set -e
# Script to launch the puzzle game from the virtual environment if available.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON="$DIR/.venv/bin/python3"
if [ ! -x "$PYTHON" ]; then
  PYTHON="$(command -v python3 || command -v python)"
fi
exec "$PYTHON" "$DIR/main.py"
