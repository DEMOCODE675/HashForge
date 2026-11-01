"""Vercel Serverless Function Entrypoint for HashForge.

Exposes the FastAPI application to Vercel's Python runtime.
All /api/* requests are dispatched through this handler.
"""

import sys
from pathlib import Path

# Ensure root directory is on Python path so core and backend can be imported
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.main import app

