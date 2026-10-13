import os

# Chrome DevTools Protocol configuration
DEFAULT_PORT: int = 9222
DEFAULT_CDP_URL: str = f"http://127.0.0.1:{DEFAULT_PORT}"
DEFAULT_PROFILE_DIR: str = os.path.expanduser("~/.chrome-dev-profile")

# Paths and directories
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Prefer prompts/prompts.json if present, fallback to prompts.json at root
_PROMPTS_SUBDIR = os.path.join(_REPO_ROOT, "prompts", "prompts.json")
_PROMPTS_ROOT = os.path.join(_REPO_ROOT, "prompts.json")
DEFAULT_PROMPTS_FILE: str = _PROMPTS_SUBDIR if os.path.exists(_PROMPTS_SUBDIR) else _PROMPTS_ROOT

DEFAULT_OUTPUT_DIR: str = os.path.join(_REPO_ROOT, "output_projects")

# Automation timeouts (in milliseconds)
BROWSER_WAIT_TIMEOUT_MS: int = 30000
STREAM_TIMEOUT_MS: int = 180000
