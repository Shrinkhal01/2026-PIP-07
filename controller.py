#!/usr/bin/env python3
"""
controller.py - CLI Entrypoint for the 7-Phase Multi-Model Pipeline Orchestrator.
Orchestrates ChatGPT, Claude 3.5 Sonnet, and Google Antigravity to turn ideas into code.
"""

import asyncio
import sys
from orchestrator.__main__ import main

if __name__ == "__main__":
    asyncio.run(main())