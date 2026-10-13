# 🛠️ Utility & Setup Scripts (`scripts/`)

This directory contains standalone operational scripts for launching Chrome with debugging capabilities and managing user login sessions.

---

## 📄 Files in this Folder

| File | Purpose | Usage |
| :--- | :--- | :--- |
| **[`start_browser.py`](start_browser.py)** | Cross-platform Python script to launch Chrome with remote debugging on port 9222. | `python3 scripts/start_browser.py [--port 9222]` |
| **[`start_browser.sh`](start_browser.sh)** | Shell wrapper for macOS and Linux users. | `./scripts/start_browser.sh` |
| **[`login_setup.py`](login_setup.py)** | Interactive first-time login helper with instructions for ChatGPT & Claude. | `python3 scripts/login_setup.py` |

---

## 🔍 How These Scripts Work

* **Automatic Detection**: `start_browser.py` scans standard OS locations (`/Applications/Google Chrome.app`, `%ProgramFiles%`, `/usr/bin/google-chrome`) across macOS, Windows, and Linux.
* **Socket Check**: Pure-socket port checking detects whether port `9222` is already open before attempting to launch another instance.
* **Persistent Profile**: All sessions, cookies, and Cloudflare tokens are saved to `~/.chrome-dev-profile`, ensuring you do not have to log in repeatedly.
