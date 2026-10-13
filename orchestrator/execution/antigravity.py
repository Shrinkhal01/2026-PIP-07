import os
import shutil
import subprocess
from typing import Optional


def find_agy_binary() -> str:
    """Locate the Google Antigravity CLI binary across standard platform paths."""
    found = shutil.which("agy")
    if found:
        return found
    candidates = [
        os.path.expanduser("~/.local/bin/agy"),
        os.path.expanduser("~/bin/agy"),
        os.path.expandvars(r"%USERPROFILE%\.local\bin\agy.cmd"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\agy\agy.exe"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return "agy"


def run_antigravity_cli(workspace_path: str, task_prompt: str) -> int:
    """
    Invoke Google Antigravity CLI (agy) inside the target workspace.
    Streams output in real-time. Returns the process returncode.
    """
    os.makedirs(workspace_path, exist_ok=True)
    print(f"\n[Phase 4-7] Invoking Google Antigravity CLI in: {workspace_path}\n", flush=True)

    agy_bin = find_agy_binary()
    cmd = [agy_bin, "-p", task_prompt, "--dangerously-skip-permissions"]

    try:
        # Inherit stdout and stderr directly so live animations, colors, and progress stream in real time
        result = subprocess.run(cmd, cwd=workspace_path)
        print(f"\n[✓] Antigravity execution finished with exit code: {result.returncode}\n", flush=True)
        return result.returncode
    except FileNotFoundError:
        print("\n[!] 'agy' command not found in PATH or standard installation paths.", flush=True)
        print("Make sure Google Antigravity CLI is installed and accessible.", flush=True)
        return 1
