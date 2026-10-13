#!/usr/bin/env python3
"""
login_setup.py - Quick launcher for initial session authentication.
Opens Chrome on port 9222 with persistent profile directory (~/.chrome-dev-profile).
"""

import sys
from orchestrator.browser.launcher import launch_chrome

if __name__ == "__main__":
    print("=" * 60)
    print("  Pipeline Orchestrator - First-Time Login Setup")
    print("=" * 60)
    print("1. Chrome will open with remote debugging enabled.")
    print("2. Navigate to https://chatgpt.com and sign in.")
    print("3. Navigate to https://claude.ai and sign in.")
    print("4. Sessions will persist across runs in ~/.chrome-dev-profile.")
    print("=" * 60 + "\n")
    sys.exit(launch_chrome())