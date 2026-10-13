#!/bin/bash
# scripts/start_browser.sh - Shell shortcut to launch Chrome with remote debugging
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/start_browser.py" 2>/dev/null || python "$DIR/start_browser.py"
