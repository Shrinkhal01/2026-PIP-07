"""
browser_driver.py - Backwards-compatibility wrapper.
Re-exports run_chatgpt_prompt and run_claude_prompt from orchestrator.browser.
"""

from orchestrator.config import DEFAULT_CDP_URL
from orchestrator.browser.connection import connect_browser as _connect_browser
from orchestrator.browser.chatgpt import run_chatgpt_prompt
from orchestrator.browser.claude import run_claude_prompt

CDP_URL = DEFAULT_CDP_URL

__all__ = [
    "CDP_URL",
    "_connect_browser",
    "run_chatgpt_prompt",
    "run_claude_prompt",
]