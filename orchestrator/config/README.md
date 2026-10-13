# ⚙️ Configuration Module (`orchestrator/config/`)

This module manages all runtime settings, default ports, filesystem paths, timeouts, and prompt loading utilities.

---

## 📄 Files in this Folder

| File | Purpose |
| :--- | :--- |
| **[`settings.py`](settings.py)** | Declares centralized constants: CDP port (`9222`), profile path (`~/.chrome-dev-profile`), output paths, and browser timeouts. |
| **[`prompt_loader.py`](prompt_loader.py)** | Provides `load_prompts()` to load and parse prompt templates from `prompts.json`. |
| **[`__init__.py`](__init__.py)** | Re-exports all settings and loaders for clean external imports (`from orchestrator.config import ...`). |

---

## 🔍 How this Module Works

1. **Centralized Defaults**: All constants such as ports and directories are defined in one place rather than being hardcoded across multiple files.
2. **Path Discovery**: Dynamically resolves project root and prioritizes `prompts/prompts.json` with a transparent fallback to `./prompts.json`.
3. **Safe Imports**: Exposes clean interface without leaking internal path resolution logic.
