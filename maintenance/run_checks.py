"""Fast checks shared by the VS Code task and the quality CI job."""

import subprocess
import sys

from project_environment import ROOT, environment, python_executable


def main():
    commands = [
        ["uv", "lock", "--check"],
        [str(python_executable()), "-m", "ruff", "check", "."],
        [str(python_executable()), "-m", "ruff", "format", "--check", "."],
        [str(python_executable()), "-m", "pytest"],
    ]
    for command in commands:
        print(f"Checking: {' '.join(command)}", flush=True)
        result = subprocess.run(command, cwd=ROOT, env=environment())
        if result.returncode:
            print(
                "Checks failed. Read the message above; ask the maintainer if unsure."
            )
            return result.returncode
    print("All project checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
