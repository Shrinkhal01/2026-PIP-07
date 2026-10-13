# 📝 Prompt Templates (`prompts/`)

This directory contains the foundational prompt templates that drive each phase of the multi-model pipeline.

---

## 📄 Files in this Folder

| File | Purpose | Target Model | Template Variables |
| :--- | :--- | :--- | :--- |
| **[`prompts.json`](prompts.json)** | Stores JSON-formatted system prompt templates for Phases 1, 2, and 3. | ChatGPT & Claude | `{user_idea}`, `{phase_1_output}`, `{phase_2_output}` |

---

## 🔍 How Each Prompt Works

1. **`phase_1_chatgpt`**:
   * **Role**: Chief Software Architect
   * **Injected Variable**: `{user_idea}`
   * **Instruction**: Analyzes user's raw idea and generates a tailored meta-prompt for Claude 3.5 Sonnet demanding strict JSON architecture output.

2. **`phase_2_claude`**:
   * **Role**: System Architect
   * **Injected Variable**: `{phase_1_output}`
   * **Instruction**: Produces a comprehensive JSON blueprint with fields: `system_overview`, `folder_structure`, `components`, `dependencies`, and `data_flow`.

3. **`phase_3_chatgpt`**:
   * **Role**: Synthesizer & Specification Writer
   * **Injected Variable**: `{phase_2_output}`
   * **Instruction**: Converts Claude's architecture JSON into a token-efficient, file-by-file execution spec prompt for Google Antigravity.
