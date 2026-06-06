"""Immutable project-wide constants."""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMPLATE_DIR = PROJECT_ROOT / "src" / "crewai_book" / "latex" / "templates"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Quality Gates
MIN_VERIFIED_SOURCES = 15
MAX_CRITICAL_HALLUCINATIONS = 0
MIN_READABILITY_FLESCH = 60.0
MIN_PDF_PAGES = 20

# Timeouts & Retries
DEFAULT_API_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3

# Document Settings
DEFAULT_DOCUMENT_CLASS = "memoir"
DEFAULT_BIB_STYLE = "apa"
