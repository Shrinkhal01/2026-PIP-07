# 📦 Orchestrator Core Package (`orchestrator/`)

The `orchestrator` package contains the core business logic, browser automation drivers, configuration management, and execution runners for the 7-phase pipeline.

---

## 📁 Submodules in this Package

| Subfolder | What Files Are in Them | Responsibility |
| :--- | :--- | :--- |
| **[`config/`](config/)** | [`settings.py`](config/settings.py), [`prompt_loader.py`](config/prompt_loader.py) | Manages system constants (ports, timeouts, paths) and prompt template parsing. |
| **[`browser/`](browser/)** | [`launcher.py`](browser/launcher.py), [`connection.py`](browser/connection.py), [`chatgpt.py`](browser/chatgpt.py), [`claude.py`](browser/claude.py) | Connects to Chrome via CDP, automates ChatGPT and Claude 3.5 Sonnet tabs, and scrapes stream results. |
| **[`execution/`](execution/)** | [`antigravity.py`](execution/antigravity.py) | Discovers Google Antigravity CLI (`agy`) binary and executes Phases 4–7 code generation. |
| **[`pipeline/`](pipeline/)** | [`runner.py`](pipeline/runner.py) | Central engine coordinating Phase 1 through Phase 7 and writing artifacts. |

---

## 🔍 Architecture & Modularity Principles

1. **High Cohesion**: Every submodule only contains code directly related to its domain (e.g., all browser code lives strictly inside `browser/`).
2. **Explicit Interfaces**: All submodules define strict `__all__` definitions in their `__init__.py`, preventing circular imports or unintended leaking of private helpers.
3. **Transparent Extensibility**: Adding a new model provider (e.g., DeepSeek, Gemini, or local Ollama) only requires adding a new driver under `browser/` and updating the prompt dispatch inside `pipeline/runner.py`.
