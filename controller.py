import argparse
import asyncio
import json
import os
import shutil
import subprocess
from browser_driver import run_chatgpt_prompt, run_claude_prompt

def load_prompts():
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts.json")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_agy_binary():
    """Locate the Google Antigravity CLI binary across platforms."""
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

def run_antigravity_cli(workspace_path: str, task_prompt: str):
    os.makedirs(workspace_path, exist_ok=True)
    print(f"\n[Phase 4-7] Invoking Google Antigravity CLI in: {workspace_path}\n", flush=True)
    
    agy_bin = find_agy_binary()
    cmd = [agy_bin, "-p", task_prompt, "--dangerously-skip-permissions"]
    
    try:
        # Inherit stdout and stderr directly so live animations, colors, and progress stream in real time
        result = subprocess.run(cmd, cwd=workspace_path)
        print(f"\n[✓] Antigravity execution finished with exit code: {result.returncode}\n", flush=True)
    except FileNotFoundError:
        print("\n[!] 'agy' command not found in PATH or standard installation paths.", flush=True)
        print("Make sure Google Antigravity CLI is installed and accessible.", flush=True)

async def main():
    parser = argparse.ArgumentParser(description="7-Phase Pipeline Orchestrator")
    parser.add_argument("--idea", type=str, required=True, help="Project idea description")
    parser.add_argument("--skip-antigravity", action="store_true", help="Stop after Phase 3 (prompt assembly)")
    args = parser.parse_args()
    
    prompts = load_prompts()
    print(f"=== Starting 7-Phase Pipeline for: '{args.idea}' ===\n")
    
    project_slug = "".join(c if c.isalnum() else "_" for c in args.idea.lower())[:30].strip("_")
    workspace = os.path.abspath(os.path.join(".", "output_projects", project_slug))
    os.makedirs(workspace, exist_ok=True)
    
    # Phase 1: ChatGPT Architecture Meta-Prompt
    print("[Phase 1] Generating Architecture Meta-Prompt via ChatGPT...")
    p1_prompt = prompts["phase_1_chatgpt"].format(user_idea=args.idea)
    with open(os.path.join(workspace, "phase_1_prompt.txt"), "w", encoding="utf-8") as f:
        f.write(p1_prompt)
        
    p1_output = await run_chatgpt_prompt(p1_prompt)
    with open(os.path.join(workspace, "phase_1_output.txt"), "w", encoding="utf-8") as f:
        f.write(p1_output)
    print(f"-> Phase 1 Output Received ({len(p1_output)} chars)")
    
    # Phase 2: Claude Architecture Blueprint
    print("\n[Phase 2] Generating Architecture Blueprint via Claude...")
    p2_prompt = prompts["phase_2_claude"].format(phase_1_output=p1_output)
    with open(os.path.join(workspace, "phase_2_prompt.txt"), "w", encoding="utf-8") as f:
        f.write(p2_prompt)
        
    p2_output = await run_claude_prompt(p2_prompt)
    with open(os.path.join(workspace, "phase_2_output.json"), "w", encoding="utf-8") as f:
        f.write(p2_output)
    print(f"-> Phase 2 Output Received ({len(p2_output)} chars)")
    
    # Phase 3: ChatGPT Implementation Specification
    print("\n[Phase 3] Assembling Antigravity Execution Spec via ChatGPT...")
    p3_prompt = prompts["phase_3_chatgpt"].format(phase_2_output=p2_output)
    with open(os.path.join(workspace, "phase_3_prompt.txt"), "w", encoding="utf-8") as f:
        f.write(p3_prompt)
        
    p3_output = await run_chatgpt_prompt(p3_prompt)
    with open(os.path.join(workspace, "phase_3_output.md"), "w", encoding="utf-8") as f:
        f.write(p3_output)
    print(f"-> Phase 3 Output Received ({len(p3_output)} chars)")
    print(f"-> Intermediate artifacts saved to: {workspace}")
    
    # Phases 4 to 7: Antigravity Autonomous Code Generation
    if args.skip_antigravity:
        print("\n[--skip-antigravity flag set: Skipping local CLI code generation.]")
    else:
        run_antigravity_cli(workspace, p3_output)

if __name__ == "__main__":
    asyncio.run(main())