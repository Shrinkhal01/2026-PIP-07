#!/usr/bin/env python3
"""
start_browser.py - Cross-platform helper to launch Google Chrome with remote debugging.
Supports macOS, Linux, and Windows.
"""

import argparse
import sys
from orchestrator.config import DEFAULT_PORT, DEFAULT_PROFILE_DIR
from orchestrator.browser.launcher import launch_chrome, is_port_listening, find_chrome


def main():
    parser = argparse.ArgumentParser(description="Launch Chrome with CDP remote debugging")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"CDP port (default: {DEFAULT_PORT})")
    parser.add_argument("--profile-dir", type=str, default=DEFAULT_PROFILE_DIR, help=f"Profile directory (default: {DEFAULT_PROFILE_DIR})")
    args = parser.parse_args()

    return launch_chrome(port=args.port, profile_dir=args.profile_dir)


if __name__ == "__main__":
    sys.exit(main())
