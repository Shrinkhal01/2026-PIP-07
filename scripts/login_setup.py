#!/usr/bin/env python3
"""
scripts/login_setup.py - Guided first-time login setup script.
Opens Chrome on port 9222 with persistent profile directory (~/.chrome-dev-profile).
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.browser.launcher import launch_chrome

if __name__ == "__main__":
    print("=" * 68)
    print("  Pipeline Orchestrator - First-Time Login Setup")
    print("=" * 68)
    print("1. Chrome will open with remote debugging on port 9222.")
    print("2. Navigate to https://chatgpt.com and sign in.")
    print("3. Navigate to https://claude.ai and sign in.")
    print("4. Sessions will persist securely in ~/.chrome-dev-profile (0700).")
    print("-" * 68)
    print("  [!] SECURITY NOTICE:")
    print("  This browser instance has remote debugging enabled for automation.")
    print("  Do NOT use this browser instance for general web browsing, banking,")
    print("  or sensitive personal accounts. Keep it dedicated to pipeline LLMs.")
    print("=" * 68 + "\n")
    sys.exit(launch_chrome())
