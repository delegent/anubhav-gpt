"""Compatibility entrypoint for running the AnubhavGPT API locally.

Prefer `make dev` or:

    uvicorn app.main:app --reload
"""

from app.main import app
