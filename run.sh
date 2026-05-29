#!/bin/bash
# Script to launch the puzzle game in the virtual environment
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
"$DIR/.venv/bin/python3" "$DIR/main.py"
