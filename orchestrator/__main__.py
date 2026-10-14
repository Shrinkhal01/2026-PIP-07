#!/usr/bin/env python3
"""
orchestrator.__main__ - Module execution entrypoint for the 7-Phase Multi-Model Pipeline.
Allows running the orchestrator via:
    python -m orchestrator --idea "Your project idea"
"""

import argparse
import asyncio
import sys
from orchestrator.pipeline import run_pipeline


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        prog="python -m orchestrator",
        description="7-Phase Multi-Model Pipeline Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run the full 7-phase pipeline end-to-end:
  python controller.py --idea "Build a CLI file manager in Rust"
  # Or run via Python module:
  python -m orchestrator --idea "Build a CLI file manager in Rust"

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
        help="Optional path to custom prompts.json file (defaults to prompts/prompts.json)",
    )
    return parser.parse_args(args)


async def main(args=None):
    parsed = parse_args(args)
    try:
        await run_pipeline(
            idea=parsed.idea,
            skip_antigravity=parsed.skip_antigravity,
            output_dir=parsed.output_dir,
            prompts_path=parsed.prompts,
        )
    except KeyboardInterrupt:
        print("\n[!] Execution cancelled by user.")
        sys.exit(130)


if __name__ == "__main__":
    asyncio.run(main())
