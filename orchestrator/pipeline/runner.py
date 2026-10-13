import json
import os
from typing import Dict, Optional

from orchestrator.config import DEFAULT_OUTPUT_DIR, load_prompts
from orchestrator.browser.chatgpt import run_chatgpt_prompt
from orchestrator.browser.claude import run_claude_prompt
from orchestrator.execution.antigravity import run_antigravity_cli


def slugify_idea(idea: str) -> str:
    """Generate a clean filesystem slug from the project idea string."""
    slug = "".join(c if c.isalnum() else "_" for c in idea.lower())[:30].strip("_")
    return slug or "generated_project"


async def run_pipeline(
    idea: str,
    skip_antigravity: bool = False,
    output_dir: Optional[str] = None,
    prompts_path: Optional[str] = None,
) -> str:
    """
    Execute the full 7-Phase Multi-Model Pipeline:
      - Phase 1: ChatGPT generates architecture meta-prompt
      - Phase 2: Claude 3.5 Sonnet generates structured JSON blueprint
      - Phase 3: ChatGPT synthesizes actionable Antigravity specification
      - Phases 4–7: Google Antigravity builds and verifies codebase
    """
    prompts = load_prompts(prompts_path)
    base_output = output_dir or DEFAULT_OUTPUT_DIR
    project_slug = slugify_idea(idea)
    workspace = os.path.abspath(os.path.join(base_output, project_slug))
    os.makedirs(workspace, exist_ok=True)

    print(f"\n=======================================================")
    print(f"  Starting 7-Phase Pipeline for: '{idea}'")
    print(f"  Output Workspace: {workspace}")
    print(f"=======================================================\n")

    # Phase 1: ChatGPT Architecture Meta-Prompt
    print("[Phase 1/7] Generating Architecture Meta-Prompt via ChatGPT...")
    p1_prompt = prompts["phase_1_chatgpt"].format(user_idea=idea)
    p1_prompt_file = os.path.join(workspace, "phase_1_prompt.txt")
    with open(p1_prompt_file, "w", encoding="utf-8") as f:
        f.write(p1_prompt)

    p1_output = await run_chatgpt_prompt(p1_prompt)
    p1_output_file = os.path.join(workspace, "phase_1_output.txt")
    with open(p1_output_file, "w", encoding="utf-8") as f:
        f.write(p1_output)
    print(f"  ✓ Phase 1 Output Received ({len(p1_output)} chars) -> saved to phase_1_output.txt")

    # Phase 2: Claude Architecture Blueprint
    print("\n[Phase 2/7] Generating Architecture Blueprint via Claude 3.5 Sonnet...")
    p2_prompt = prompts["phase_2_claude"].format(phase_1_output=p1_output)
    p2_prompt_file = os.path.join(workspace, "phase_2_prompt.txt")
    with open(p2_prompt_file, "w", encoding="utf-8") as f:
        f.write(p2_prompt)

    p2_output = await run_claude_prompt(p2_prompt)
    p2_output_file = os.path.join(workspace, "phase_2_output.json")
    with open(p2_output_file, "w", encoding="utf-8") as f:
        f.write(p2_output)
    print(f"  ✓ Phase 2 Output Received ({len(p2_output)} chars) -> saved to phase_2_output.json")

    # Phase 3: ChatGPT Implementation Specification
    print("\n[Phase 3/7] Assembling Antigravity Execution Spec via ChatGPT...")
    p3_prompt = prompts["phase_3_chatgpt"].format(phase_2_output=p2_output)
    p3_prompt_file = os.path.join(workspace, "phase_3_prompt.txt")
    with open(p3_prompt_file, "w", encoding="utf-8") as f:
        f.write(p3_prompt)

    p3_output = await run_chatgpt_prompt(p3_prompt)
    p3_output_file = os.path.join(workspace, "phase_3_output.md")
    with open(p3_output_file, "w", encoding="utf-8") as f:
        f.write(p3_output)
    print(f"  ✓ Phase 3 Output Received ({len(p3_output)} chars) -> saved to phase_3_output.md")
    print(f"  ✓ Intermediate artifacts ready in: {workspace}")

    # Phases 4 to 7: Antigravity Autonomous Code Generation
    if skip_antigravity:
        print("\n[--skip-antigravity flag set: Skipping local CLI code generation.]")
        print(f"Specification markdown ready for review at:\n  {p3_output_file}\n")
    else:
        run_antigravity_cli(workspace, p3_output)

    return workspace
