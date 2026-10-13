#!/usr/bin/env python3
"""
controller.py - CLI Entrypoint for the 7-Phase Multi-Model Pipeline Orchestrator.
Orchestrates ChatGPT, Claude 3.5 Sonnet, and Google Antigravity to turn ideas into code.
"""

import argparse
import asyncio
import sys
from orchestrator.pipeline import run_pipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="7-Phase Multi-Model Pipeline Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run the full 7-phase pipeline end-to-end:
  python controller.py --idea "Build a CLI file manager in Rust"

  # Stop after Phase 3 to inspect the architecture prompt and blueprint:
  python controller.py --idea "Build a real-time markdown editor in Go" --skip-antigravity
        """,
    )
    parser.add_argument(
        "--idea",
        type=str,
        required=True,
        help="High-level project idea description to design and generate",
    )
    parser.add_argument(
        "--skip-antigravity",
        action="store_true",
        help="Skip Phases 4-7 (stops after producing Phase 3 architecture spec)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Optional custom output directory (defaults to ./output_projects)",
    )
    parser.add_argument(
        "--prompts",
        type=str,
        default=None,
        help="Optional path to custom prompts.json file",
    )
    return parser.parse_args()


async def main():
    args = parse_args()
    try:
        await run_pipeline(
            idea=args.idea,
            skip_antigravity=args.skip_antigravity,
            output_dir=args.output_dir,
            prompts_path=args.prompts,
        )
    except KeyboardInterrupt:
        print("\n[!] Execution cancelled by user.")
        sys.exit(130)


if __name__ == "__main__":
    asyncio.run(main())