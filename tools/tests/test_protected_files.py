"""Use disposable Git repositories; never modify the user's index or history."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

CHECKER = Path(__file__).resolve().parents[2] / "tools/check_protected_files.py"
POLICY = ".github/protected-paths.txt"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def write(repo, name, text):
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def check(repo, *args):
    return subprocess.run(
        [sys.executable, str(CHECKER), *args],
        cwd=repo,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-b", "main")
    git(tmp_path, "config", "user.name", "Workflow test")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    # Keep fixture commits independent of any machine-wide hooks or signing.
    git(tmp_path, "config", "core.hooksPath", str(tmp_path / "unused-hooks"))
    git(tmp_path, "config", "commit.gpgsign", "false")
    write(tmp_path, "reference data.txt", "original\n")
    write(tmp_path, "ordinary.py", "value = 1\n")
    write(tmp_path, POLICY, "# Fixture policy\nreference data.txt\n")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "Fixture baseline")
    return tmp_path


def change(repo, kind):
    if kind == "modify":
        write(repo, "reference data.txt", "changed\n")
    elif kind == "delete":
        (repo / "reference data.txt").unlink()
    elif kind == "rename-away":
        (repo / "reference data.txt").rename(repo / "renamed.txt")
    elif kind == "rename-into":
        (repo / "reference data.txt").unlink()
        (repo / "ordinary.py").rename(repo / "reference data.txt")
    elif kind == "remove-policy":
        write(repo, POLICY, "# Entry removed by feature branch\n")
        write(repo, "reference data.txt", "changed despite policy removal\n")
    elif kind == "delete-policy":
        (repo / POLICY).unlink()
        (repo / "reference data.txt").unlink()
    git(repo, "add", "-A")


@pytest.mark.parametrize(
    "kind",
    [
        "modify",
        "delete",
        "rename-away",
        "rename-into",
        "remove-policy",
        "delete-policy",
    ],
)
@pytest.mark.parametrize("mode", ["staged", "ci"])
def test_protected_changes_blocked(repo, kind, mode):
    base = git(repo, "rev-parse", "HEAD").decode().strip()
    change(repo, kind)
    args = []
    if mode == "ci":
        git(repo, "commit", "-m", "Simulate a bypassed local hook")
        args = ["--base", base]
    result = check(repo, *args)
    assert result.returncode == 1
    assert "reference data.txt" in result.stderr
    assert "Discard Changes" in result.stderr
    assert "contact the maintainer" in result.stderr


@pytest.mark.parametrize("mode", ["staged", "ci"])
def test_ordinary_changes_pass(repo, mode):
    base = git(repo, "rev-parse", "HEAD").decode().strip()
    write(repo, "ordinary.py", "value = 2\n")
    git(repo, "add", "ordinary.py")
    if mode == "ci":
        git(repo, "commit", "-m", "Ordinary change")
    assert check(repo, *(["--base", base] if mode == "ci" else [])).returncode == 0


def test_worktree_is_not_the_staged_diff(repo):
    write(repo, "reference data.txt", "unstaged edit\n")
    write(repo, "ordinary.py", "value = 3\n")
    git(repo, "add", "ordinary.py")
    assert check(repo).returncode == 0
    git(repo, "add", "reference data.txt")
    write(repo, "reference data.txt", "original\n")
    assert (
        check(repo).returncode == 1
    )  # Staged edit remains, even with worktree restored.


def test_new_staged_protection_cannot_be_ignored(repo):
    write(repo, POLICY, "reference data.txt\nordinary.py\n")
    write(repo, "ordinary.py", "value = 4\n")
    git(repo, "add", "-A")
    result = check(repo)
    assert result.returncode == 1
    assert "ordinary.py" in result.stderr


@pytest.mark.parametrize("mode", ["staged", "ci"])
def test_addition_of_protected_path_blocked(repo, mode):
    # Reintroduction of an absent path that the committed policy still names.
    (repo / "reference data.txt").unlink()
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "Fixture with reserved protected path")
    base = git(repo, "rev-parse", "HEAD").decode().strip()
    write(repo, "reference data.txt", "reintroduced\n")
    git(repo, "add", "-A")
    if mode == "ci":
        git(repo, "commit", "-m", "Bypassed addition")
    assert check(repo, *(["--base", base] if mode == "ci" else [])).returncode == 1


def test_policy_only_edit_requires_review_but_is_not_immutable(repo):
    write(repo, POLICY, "# Maintainer-controlled policy-only change\n")
    git(repo, "add", POLICY)
    assert check(repo).returncode == 0


@pytest.mark.parametrize(
    "name", ["space and é.txt", "-leading.txt", "literal [1].txt", "#hash.txt"]
)
def test_literal_names(repo, name):
    write(repo, name, "original\n")
    write(repo, POLICY, json.dumps(name) + "\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "Protect unusual filename")
    write(repo, name, "changed\n")
    git(repo, "add", "-A")
    assert check(repo).returncode == 1


@pytest.mark.skipif(
    os.name == "nt", reason="Windows filenames cannot contain tabs/newlines"
)
def test_nul_diff_preserves_tabs_quotes_and_newlines(repo):
    name = 'tab\tquote"line\n.txt'
    write(repo, name, "original\n")
    write(repo, POLICY, json.dumps(name) + "\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "Protect unusual POSIX filename")
    write(repo, name, "changed\n")
    git(repo, "add", "-A")
    result = check(repo)
    assert result.returncode == 1
    assert repr(name) in result.stderr


def test_ci_reads_base_policy_even_when_worktree_policy_is_empty(repo):
    base = git(repo, "rev-parse", "HEAD").decode().strip()
    change(repo, "remove-policy")
    git(repo, "commit", "-m", "Remove policy and edit protected file")
    assert check(repo, "--base", base).returncode == 1


def test_bad_base_fails_closed(repo):
    assert check(repo, "--base", "nonexistent-branch").returncode == 1


def test_readonly_update_and_drift_check(repo):
    write(repo, ".vscode/settings.json", '{"editor.fontSize": 14}\n')
    assert check(repo, "--check-settings").returncode == 1
    assert check(repo, "--update-readonly").returncode == 0
    settings = json.loads((repo / ".vscode/settings.json").read_text())
    assert settings["files.readonlyInclude"] == {"reference data.txt": True}
    assert settings["editor.fontSize"] == 14
    assert check(repo, "--check-settings").returncode == 0


def test_untracked_policy_entry_rejected_by_settings_check(repo):
    write(repo, POLICY, "does-not-exist.txt\n")
    write(repo, ".vscode/settings.json", "{}\n")
    assert check(repo, "--check-settings").returncode == 1


def test_initial_commit_can_use_staged_policy(tmp_path):
    git(tmp_path, "init", "-b", "main")
    write(tmp_path, POLICY, "new.txt\n")
    write(tmp_path, "new.txt", "initial content\n")
    git(tmp_path, "add", "-A")
    assert check(tmp_path).returncode == 1
