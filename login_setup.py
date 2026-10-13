#!/usr/bin/env python3
"""
login_setup.py - Launcher for initial login.
Delegates to cross-platform start_browser.py to open Chrome with persistent profile on port 9222.
"""
import sys
from start_browser import main

if __name__ == "__main__":
    print("Opening Chrome for login setup...")
    print("Sign into ChatGPT, Claude, and Gemini in the opened browser window.")
    sys.exit(main())