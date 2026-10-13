# ⚡ Execution Module (`orchestrator/execution/`)

This module manages the execution of local code generation agents, specifically invoking the **Google Antigravity CLI (`agy`)** to implement, compile, and verify projects.

---

## 📄 Files in this Folder

| File | Purpose | Key Functions |
| :--- | :--- | :--- |
| **[`antigravity.py`](antigravity.py)** | Locates the `agy` executable across platforms and streams live code generation. | `find_agy_binary()`, `run_antigravity_cli()` |
| **[`__init__.py`](__init__.py)** | Package re-exports for easy imports (`from orchestrator.execution import ...`). | `find_agy_binary`, `run_antigravity_cli` |

---

## 🔍 How this Module Works

1. **Binary Auto-Discovery**:
   `find_agy_binary()` checks standard locations in order:
   - System `PATH` via `shutil.which("agy")`
   - `~/.local/bin/agy` (standard macOS/Linux user binary path)
   - `~/bin/agy`
   - `%USERPROFILE%\.local\bin\agy.cmd` (Windows)
   - `%USERPROFILE%\AppData\Local\Programs\agy\agy.exe` (Windows)

2. **Autonomous Execution (`--dangerously-skip-permissions`)**:
   Runs the agent inside the targeted project folder with full terminal output streaming, allowing the user to watch Antigravity create files, run test suites, and repair compilation errors in real-time.
