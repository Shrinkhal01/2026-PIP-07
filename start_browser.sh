#!/bin/bash
# Shell wrapper around cross-platform start_browser.py
python3 start_browser.py 2>/dev/null || python start_browser.py
