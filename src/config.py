"""Configuration — loads environment variables and defines constants."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
RUNS_DIR = ROOT_DIR / "runs"
BRAND_DIR = ROOT_DIR / "brand-assets" / "AIwithVishal"
ENV_PATH = ROOT_DIR / ".env"

DATA_DIR.mkdir(exist_ok=True)
RUNS_DIR.mkdir(exist_ok=True)

load_dotenv(ENV_PATH)

# Blotato (YouTube extraction, visual generation, publishing)
BLOTATO_API_KEY = os.getenv("BLOTATO_API_KEY", "")
BLOTATO_BASE_URL = "https://backend.blotato.com/v2"

# LLM (Euri — OpenAI-compatible. 200K free tokens/day on euron.one)
EURI_API_KEY = os.getenv("EURI_API_KEY", "")
EURI_BASE_URL = "https://api.euron.one/api/v1/euri"
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

# Safety switch — when true, run.py skips Blotato calls and uses seed text.
DRY_RUN_DEFAULT = os.getenv("DRY_RUN_DEFAULT", "true").lower() == "true"

PLATFORMS = ["linkedin", "x", "instagram"]

# Polling
EXTRACTION_TIMEOUT = 120
VISUAL_TIMEOUT = 180
PUBLISH_TIMEOUT = 120
POLL_INTERVAL_EXTRACT = 3
POLL_INTERVAL_VISUAL = 5
POLL_INTERVAL_PUBLISH = 3
