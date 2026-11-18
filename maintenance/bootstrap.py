"""One-time, repeatable setup, also used by the VS Code process task."""

import shutil
import subprocess
import sys
from pathlib import Path

from project_environment import ROOT, environment, python_executable


def main():
    for tool, url in (
        ("git", "https://git-scm.com/downloads"),
        ("uv", "https://docs.astral.sh/uv/getting-started/installation/"),
    ):
        if not shutil.which(tool):
            print(f"Setup stopped: {tool} not found. Install it: {url}")
            print("Restart your IDE and terminal, then rerun setup.")
            return 1
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], cwd=ROOT, text=True
        ).strip()
        if ROOT != Path(root).resolve():
            raise RuntimeError("Open the cloned project folder, not its parent folder.")
        hooks_path = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if hooks_path.returncode == 0:
            raise RuntimeError(
                "A custom core.hooksPath is already configured. Ask the maintainer "
                "to resolve it; setup will not replace existing hook settings."
            )
        env = environment()
        subprocess.run(["uv", "sync", "--locked"], cwd=ROOT, env=env, check=True)
        subprocess.run(
            [str(python_executable()), "-m", "pre_commit", "install"],
            cwd=ROOT,
            env=env,
            check=True,
        )
        for key, value in (("pull.rebase", "false"), ("pull.ff", "true")):
            subprocess.run(
                ["git", "config", "--local", key, value],
                cwd=ROOT,
                env=env,
                check=True,
            )
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Setup stopped: {error}")
        print("Keep the message and ask the maintainer. Rerunning setup is safe.")
        return 1
    print("Setup complete: .venv ready; commit and branch/pull hooks installed.")
    print(
        "Git pulls: merge divergent commits; fast-forward when possible (this clone only)."
    )
    print(f"IDE Python interpreter: {python_executable()}")
    print("Editor and Git GUI setup: docs/repo-guides/CONTRIBUTOR_SETUP.md")
    print("VS Code: select .venv in Python: Select Interpreter.")
    print("Checks: uv run --locked python maintenance/run_checks.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
