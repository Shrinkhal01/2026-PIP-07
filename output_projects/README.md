# 📂 Generated Projects & Artifacts (`output_projects/`)

This directory is the output destination for all pipeline runs. Each project is placed inside its own dedicated subfolder named after the sanitized project idea slug.

---

## 📁 Project Folder Layout

Whenever a pipeline run executes, a folder such as `output_projects/<project_slug>/` is created containing:

```text
output_projects/<project_slug>/
├── phase_1_prompt.txt     # Formatted prompt sent to ChatGPT (Chief Architect)
├── phase_1_output.txt     # Raw meta-prompt produced by ChatGPT
├── phase_2_prompt.txt     # Formatted prompt sent to Claude 3.5 Sonnet
├── phase_2_output.json    # Complete JSON system architecture blueprint from Claude
├── phase_3_prompt.txt     # Formatted prompt sent to ChatGPT (Synthesizer)
├── phase_3_output.md      # Actionable implementation specification for Antigravity
└── <project_codebase>/    # Fully generated, compiling codebase (Phases 4–7)
```

---

## 🔍 Artifact Descriptions

1. **`phase_1_output.txt`**: Architectural guidelines and constraint specifications crafted for Claude.
2. **`phase_2_output.json`**: Machine-readable JSON blueprint detailing:
   * `system_overview`: Architectural style, design principles, non-goals.
   * `folder_structure`: Complete expected directory and file tree.
   * `components`: Individual components, responsibilities, and interface signatures.
   * `dependencies`: Required runtime and dev packages with rationale.
   * `data_flow`: Detailed end-to-end execution flows and error flows.
3. **`phase_3_output.md`**: Step-by-step developer guide consumed by Google Antigravity to write the code.
4. **Project Codebase**: The actual project (e.g., Rust, Python, Go, TypeScript) created by Antigravity CLI.
