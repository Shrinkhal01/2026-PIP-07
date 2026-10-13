import json
from typing import Dict, Optional
from orchestrator.config.settings import DEFAULT_PROMPTS_FILE


def load_prompts(prompts_path: Optional[str] = None) -> Dict[str, str]:
    """
    Load prompt templates from a JSON file.
    Falls back to the configured DEFAULT_PROMPTS_FILE.
    """
    path = prompts_path or DEFAULT_PROMPTS_FILE
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
