"""Shared environment handling; never sync into a different project's venv."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def environment():
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    env["UV_PROJECT_ENVIRONMENT"] = str(ROOT / ".venv")
    return env


def python_executable():
    folder = "Scripts" if os.name == "nt" else "bin"
    executable = "python.exe" if os.name == "nt" else "python"
    return ROOT / ".venv" / folder / executable
