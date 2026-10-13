# 🔄 Pipeline Orchestration Module (`orchestrator/pipeline/`)

This module houses the central execution engine that sequences the 7 distinct phases of the code generation pipeline.

---

## 📄 Files in this Folder

| File | Purpose | Key Functions |
| :--- | :--- | :--- |
| **[`runner.py`](runner.py)** | Coordinates prompt dispatch, artifact saving, model handoffs, and CLI code generation. | `run_pipeline()`, `slugify_idea()` |
| **[`__init__.py`](__init__.py)** | Package exports (`from orchestrator.pipeline import run_pipeline`). | `run_pipeline`, `slugify_idea` |

---

## 🔍 How this Module Works

```text
User Idea
   │
   ▼
[Phase 1] ──> ChatGPT ──> phase_1_output.txt
                              │
                              ▼
[Phase 2] ────────────> Claude 3.5 Sonnet ──> phase_2_output.json
                                                    │
                                                    ▼
[Phase 3] ────────────────────────────────────> ChatGPT ──> phase_3_output.md
                                                                │
                                                                ▼
[Phases 4-7] ─────────────────────────────────────────────> Google Antigravity (agy)
                                                                │
                                                                ▼
                                                            Working Codebase
```

1. **Artifact Persistence**: Every intermediate prompt and response is persisted to disk under `output_projects/<project_slug>/`, providing total auditability of every decision made by each model.
2. **Graceful Degeneration**: Passing `--skip-antigravity` halts the pipeline cleanly at Phase 3, enabling human inspection and editing of the architectural specification before code generation begins.
