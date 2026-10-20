"""Git post-checkout/post-merge hook. Git has already changed the files."""

import os
import subprocess

from project_environment import ROOT, environment


def main():
    if os.environ.get("PRE_COMMIT_CHECKOUT_TYPE") == "0":
        return 0  # A file checkout, not a branch switch.
    try:
        subprocess.run(
            ["uv", "sync", "--locked"],
            cwd=ROOT,
            env=environment(),
            check=True,
            timeout=60,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        print(f"Environment sync did not finish: {error}")
        print("Your branch switch or pull has already happened; it was NOT undone.")
        print("Reconnect if offline, then run Project: Sync Python environment.")
        print(
            "If that fails, share the message with the maintainer before running code."
        )
    else:
        print("Environment ready. Restart open notebook kernels if libraries changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
