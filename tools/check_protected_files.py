"""Guard exact paths using the staged diff or a PR's trusted base policy.

This file intentionally uses only the standard library so CI can execute a copy
from the trusted base commit without importing feature-branch Python modules.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath

POLICY = ".github/protected-paths.txt"
SETTINGS = ".vscode/settings.json"


def git(*args):
    return subprocess.check_output(["git", *args])


def policy_paths(content):
    paths = set()
    for number, line in enumerate(content.splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        path = json.loads(line) if line.startswith('"') else line
        if (
            not isinstance(path, str)
            or not path
            or "\x00" in path
            or "\\" in path
            or PurePosixPath(path).is_absolute()
            or any(part in ("", ".", "..") for part in path.split("/"))
            or (len(path) > 1 and path[1] == ":")
        ):
            raise ValueError(f"Invalid exact repository-relative path at line {number}")
        paths.add(path)
    return paths


def committed_policy(ref):
    # ls-tree distinguishes a missing policy (allowed on initial setup) from a
    # broken revision or Git error (must fail closed).
    if not git("ls-tree", "--name-only", "-z", ref, "--", POLICY):
        return set()
    return policy_paths(git("show", f"{ref}:{POLICY}").decode("utf-8"))


def staged_policy():
    if not git("ls-files", "--cached", "-z", "--", POLICY):
        return set()
    return policy_paths(git("show", f":{POLICY}").decode("utf-8"))


def changed_paths(*diff_args):
    # --no-renames represents a rename as deletion + addition, checking both ends.
    # NUL delimiters preserve spaces, tabs, quotes, Unicode and embedded newlines.
    output = git(
        "diff", "--no-ext-diff", "--no-renames", "--name-only", "-z", *diff_args
    )
    return {os.fsdecode(path) for path in output.split(b"\0") if path}


def readonly_settings(paths):
    # VS Code consumes glob patterns, while our manifest uses literal paths.
    escapes = {char: f"[{char}]" for char in "*?[]{}"}
    return {
        "".join(escapes.get(char, char) for char in path): True
        for path in sorted(paths)
    }


def settings_check(update=False):
    paths = policy_paths(Path(POLICY).read_text(encoding="utf-8"))
    tracked = {os.fsdecode(path) for path in git("ls-files", "-z").split(b"\0") if path}
    untracked = paths - tracked
    if untracked:
        raise ValueError(
            f"Protection entries must already be tracked files: {untracked!r}"
        )
    settings_path = Path(SETTINGS)
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    expected = readonly_settings(paths)
    if update:
        settings["files.readonlyInclude"] = expected
        settings_path.write_text(
            json.dumps(settings, indent=2) + "\n", encoding="utf-8"
        )
        print(
            "Updated workspace read-only paths. Review and commit both policy and settings."
        )
    elif settings.get("files.readonlyInclude", {}) != expected:
        raise ValueError(
            "Read-only settings differ from the manifest. Maintainer: run "
            "uv run --locked python tools/check_protected_files.py --update-readonly"
        )
    else:
        print("Workspace read-only paths match the manifest.")
    if not paths:
        print(
            "No immutable paths configured; maintainer must populate the protection policy."
        )
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base", help="Trusted PR base commit; reads policy from this commit"
    )
    parser.add_argument("--head", default="HEAD", help="PR head commit (default: HEAD)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check-settings", action="store_true")
    mode.add_argument("--update-readonly", action="store_true")
    args = parser.parse_args(argv)
    try:
        os.chdir(os.fsdecode(git("rev-parse", "--show-toplevel")).strip())
        if args.check_settings or args.update_readonly:
            return settings_check(args.update_readonly)
        if args.base:
            base = (
                git("rev-parse", "--verify", f"{args.base}^{{commit}}").decode().strip()
            )
            head = (
                git("rev-parse", "--verify", f"{args.head}^{{commit}}").decode().strip()
            )
            protected = committed_policy(base)
            changed = changed_paths(f"{base}...{head}")
        else:
            head = subprocess.run(
                ["git", "rev-parse", "--verify", "HEAD"], capture_output=True
            )
            protected = committed_policy("HEAD") if head.returncode == 0 else set()
            protected |= staged_policy()
            changed = changed_paths("--cached")
        violations = sorted(changed & protected)
        if violations:
            print(
                "Commit or pull request stopped: protected files changed:",
                file=sys.stderr,
            )
            for path in violations:
                print(f"  {path!r}", file=sys.stderr)
            print(
                "If these edits are unwanted: Source Control → right-click that file → "
                "Discard Changes. For staged changes, unstage with '-' first. "
                "Discard only unwanted work. If intentional, contact the maintainer; "
                "do not bypass the guard.",
                file=sys.stderr,
            )
            return 1
        print("Protected-file check passed.")
        if not protected:
            print("No immutable paths configured; maintainer action still required.")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Protected-file check could not complete: {error}", file=sys.stderr)
        print(
            "Commit/PR must wait. Share this message with the maintainer.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
