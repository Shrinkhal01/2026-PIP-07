import os

DEFAULT_PORT = 9222
DEFAULT_CDP_URL = f"http://127.0.0.1:{DEFAULT_PORT}"
DEFAULT_PROFILE_DIR = os.path.expanduser("~/.chrome-dev-profile")
DEFAULT_PROMPTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts.json")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output_projects")
