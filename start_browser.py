#!/usr/bin/env python3
"""
Cross-platform helper to launch Google Chrome with remote debugging on port 9222.
Supports macOS, Linux, and Windows.
"""

import os
import platform
import shutil
import socket
import subprocess
import sys
import time

PORT = 9222
PROFILE_DIR = os.path.expanduser("~/.chrome-dev-profile")


def is_port_listening(port=PORT, host="127.0.0.1"):
    """Check if port is already listening using pure sockets (cross-platform)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def find_chrome():
    """Detect the Google Chrome binary path on macOS, Linux, or Windows."""
    system = platform.system()

    if system == "Darwin":  # macOS
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            shutil.which("google-chrome"),
        ]
    elif system == "Windows":  # Windows
        candidates = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
            shutil.which("chrome.exe"),
        ]
    else:  # Linux / Unix
        candidates = [
            shutil.which("google-chrome"),
            shutil.which("google-chrome-stable"),
            shutil.which("chromium-browser"),
            shutil.which("chromium"),
        ]

    for path in candidates:
        if path and os.path.exists(path):
            return path

    return None


def main():
    if is_port_listening(PORT):
        print(f"[✓] Chrome is already running with remote debugging on http://127.0.0.1:{PORT}")
        return 0

    chrome_bin = find_chrome()
    if not chrome_bin:
        print("[!] Error: Could not automatically locate Google Chrome on this system.")
        print("Please start Chrome manually with:")
        print(f'  <chrome-executable> --remote-debugging-port={PORT} --user-data-dir="{PROFILE_DIR}" --remote-allow-origins="*"')
        return 1

    os.makedirs(PROFILE_DIR, exist_ok=True)
    print(f"[*] Starting Chrome from: {chrome_bin}")
    print(f"[*] Profile directory: {PROFILE_DIR}")

    cmd = [
        chrome_bin,
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={PROFILE_DIR}",
        "--remote-allow-origins=*",
    ]

    system = platform.system()
    if system == "Windows":
        subprocess.Popen(
            cmd,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
            close_fds=True,
        )
    else:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

    # Wait briefly for port to bind
    for _ in range(10):
        time.sleep(0.5)
        if is_port_listening(PORT):
            print(f"[✓] Google Chrome connected successfully on http://127.0.0.1:{PORT}")
            return 0

    print(f"[!] Chrome process launched, waiting for port {PORT}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
