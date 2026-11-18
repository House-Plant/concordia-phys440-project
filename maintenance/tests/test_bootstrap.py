"""Exercise setup's Git defaults with two contributors and an offline remote."""

import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_setup_allows_divergent_pulls_without_changing_other_clones(
    tmp_path, monkeypatch
):
    global_config = tmp_path / "global.gitconfig"
    global_settings = "[pull]\n\trebase = true\n\tff = only\n"
    global_config.write_text(global_settings)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for role in ("AUTHOR", "COMMITTER"):
        monkeypatch.setenv(f"GIT_{role}_NAME", "Workflow test")
        monkeypatch.setenv(f"GIT_{role}_EMAIL", "workflow@example.invalid")

    real_run = subprocess.run

    def git(*args, cwd=tmp_path, check=True):
        return real_run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, check=check
        )

    remote = tmp_path / "remote.git"
    alice = (tmp_path / "alice").resolve()
    bob = (tmp_path / "bob").resolve()
    git("init", "--bare", "--initial-branch=working", str(remote))
    git("clone", str(remote), str(alice))
    (alice / "shared.txt").write_text("Initial shared content\n")
    git("add", ".", cwd=alice)
    git("commit", "-m", "Initial content", cwd=alice)
    git("push", cwd=alice)
    git("clone", str(remote), str(bob))

    monkeypatch.syspath_prepend(str(ROOT / "maintenance"))
    spec = importlib.util.spec_from_file_location(
        "bootstrap_under_test", ROOT / "maintenance/bootstrap.py"
    )
    bootstrap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bootstrap)
    monkeypatch.setattr(bootstrap, "ROOT", alice)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: name)

    def setup_run(command, **kwargs):
        if command[0] == "git":
            return real_run(command, **kwargs)
        # Environment installation is covered separately; exercise real Git here.
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(bootstrap.subprocess, "run", setup_run)
    assert bootstrap.main() == 0
    assert bootstrap.main() == 0  # Rerunning setup must be safe.

    (bob / "bob.txt").write_text("Bob's independent change\n")
    git("add", ".", cwd=bob)
    git("commit", "-m", "Bob's change", cwd=bob)
    git("push", cwd=bob)
    (alice / "alice.txt").write_text("Alice's independent change\n")
    git("add", ".", cwd=alice)
    git("commit", "-m", "Alice's change", cwd=alice)
    assert git("push", cwd=alice, check=False).returncode != 0

    # Only suppress the message editor; setup must supply the pull strategy.
    git("pull", "--no-edit", cwd=alice)
    parents = git("rev-list", "--parents", "-n", "1", "HEAD", cwd=alice)
    assert len(parents.stdout.split()) == 3  # A merge with both parents.
    assert (alice / "bob.txt").read_text() == "Bob's independent change\n"
    assert (alice / "alice.txt").read_text() == "Alice's independent change\n"
    git("push", cwd=alice)
    git("pull", "--no-edit", cwd=bob)
    assert (bob / "alice.txt").read_text() == "Alice's independent change\n"

    assert global_config.read_text() == global_settings
    assert git("config", "--get", "pull.rebase", cwd=bob).stdout.strip() == "true"
    assert git("config", "--get", "pull.ff", cwd=bob).stdout.strip() == "only"
