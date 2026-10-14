import os
import platform
import shutil
import socket
import subprocess
import time
from typing import Optional

from orchestrator.config import DEFAULT_PORT, DEFAULT_PROFILE_DIR


def is_port_listening(port: int = DEFAULT_PORT, host: str = "127.0.0.1") -> bool:
    """Check if the debugging port is already bound and listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def find_chrome() -> Optional[str]:
    """Detect the Google Chrome binary path across macOS, Linux, and Windows."""
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


def launch_chrome(port: int = DEFAULT_PORT, profile_dir: str = DEFAULT_PROFILE_DIR) -> int:
    """
    Launch Google Chrome with remote debugging on the specified port.
    Reuses an existing instance if port is already listening.
    """
    if is_port_listening(port):
        print(f"[✓] Chrome is already running with remote debugging on http://127.0.0.1:{port}")
        return 0

    chrome_bin = find_chrome()
    if not chrome_bin:
        print("[!] Error: Could not automatically locate Google Chrome on this system.")
        print("Please start Chrome manually with:")
        print(f'  <chrome-executable> --remote-debugging-port={port} --user-data-dir="{profile_dir}" --remote-allow-origins="*"')
        return 1

    os.makedirs(profile_dir, exist_ok=True)
    if platform.system() != "Windows":
        try:
            os.chmod(profile_dir, 0o700)
        except OSError:
            pass

    print(f"[*] Starting Chrome from: {chrome_bin}")
    print(f"[*] Profile directory: {profile_dir} (permissions restricted to 0700)")

    cmd = [
        chrome_bin,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_dir}",
        f"--remote-allow-origins=http://127.0.0.1:{port},http://localhost:{port}",
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
        if is_port_listening(port):
            print(f"[✓] Google Chrome connected successfully on http://127.0.0.1:{port}")
            return 0

    print(f"[!] Chrome process launched, waiting for port {port}...")
    return 0
