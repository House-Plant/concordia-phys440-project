"""Configuration and post-checkout failure paths need no network or datasets."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def sync_script(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "maintenance"))
    spec = importlib.util.spec_from_file_location(
        "sync_hook", ROOT / "maintenance/sync_environment.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_file_checkout_skips_sync(sync_script, monkeypatch):
    monkeypatch.setenv("PRE_COMMIT_CHECKOUT_TYPE", "0")

    def unexpected(*args, **kwargs):
        pytest.fail("File-only checkout must not run uv sync")

    monkeypatch.setattr(sync_script.subprocess, "run", unexpected)
    assert sync_script.main() == 0


@pytest.mark.parametrize(
    "failure",
    [
        OSError("offline"),
        subprocess.TimeoutExpired("uv", 60),
        subprocess.CalledProcessError(1, "uv"),
    ],
)
def test_sync_failure_explains_recovery(sync_script, monkeypatch, capsys, failure):
    monkeypatch.delenv("PRE_COMMIT_CHECKOUT_TYPE", raising=False)

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(sync_script.subprocess, "run", fail)
    assert sync_script.main() == 0
    output = capsys.readouterr().out
    assert "NOT undone" in output
    assert "Project: Sync Python environment" in output


def test_sync_forces_repo_environment(sync_script, monkeypatch):
    monkeypatch.setenv("UV_PROJECT_ENVIRONMENT", "/unrelated/project")
    monkeypatch.setenv("VIRTUAL_ENV", "/unrelated/project")
    monkeypatch.delenv("PRE_COMMIT_CHECKOUT_TYPE", raising=False)
    calls = []
    monkeypatch.setattr(
        sync_script.subprocess, "run", lambda *a, **kw: calls.append((a, kw))
    )
    assert sync_script.main() == 0
    args, kwargs = calls[0]
    assert args[0] == ["uv", "sync", "--locked"]
    assert kwargs["env"]["UV_PROJECT_ENVIRONMENT"] == str(ROOT / ".venv")
    assert "VIRTUAL_ENV" not in kwargs["env"]
    assert kwargs["cwd"] == ROOT


@pytest.mark.parametrize(
    ("platform", "relative"),
    [("nt", "Scripts/python.exe"), ("posix", "bin/python")],
)
def test_interpreter_path_for_windows_and_posix(
    sync_script, monkeypatch, platform, relative
):
    import project_environment

    monkeypatch.setattr(project_environment, "os", SimpleNamespace(name=platform))
    assert project_environment.python_executable() == ROOT / ".venv" / relative


def test_task_package_input_is_one_process_argument():
    tasks = json.loads((ROOT / ".vscode/tasks.json").read_text())
    task = next(
        t for t in tasks["tasks"] if t["label"] == "Project: Add Python package"
    )
    assert task["type"] == "process"
    assert task["args"] == ["add", "--", "${input:packageName}"]
    assert all(t["type"] == "process" for t in tasks["tasks"])


def test_workflow_has_stable_check_name_and_least_privilege_permissions():
    # BaseLoader preserves GitHub's YAML 1.2 `on` key as a string.
    workflow = yaml.load(
        (ROOT / ".github/workflows/checks.yml").read_text(), Loader=yaml.BaseLoader
    )
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["on"]["pull_request"]["branches"] == ["main"]
    assert workflow["on"]["push"]["branches"] == ["main"]
    assert {job["name"] for job in workflow["jobs"].values()} == {"Quality"}
    for job in workflow["jobs"].values():
        for step in job["steps"]:
            if "uses" in step:
                assert len(step["uses"].split("@")[1]) == 40


def test_setup_python_and_tool_imports():
    import pre_commit
    import ruff

    assert sys.version_info[:2] == (3, 12)
    assert pre_commit.__file__
    assert ruff.__file__


def test_scientific_package_imports_away_from_root_without_tooling(tmp_path):
    # Isolated mode excludes the working directory and PYTHONPATH; the editable
    # install must make the scientific package available by itself.
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "import importlib.util, tools; "
            "assert importlib.util.find_spec('project_environment') is None; "
            "print(tools.__file__)",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert Path(result.stdout.strip()).resolve() == ROOT / "src/tools/__init__.py"


def test_pyssem_model_imports_away_from_root(tmp_path):
    # Import the public entry point, not just distribution metadata: pySSEM
    # imports Seaborn without declaring it as a package dependency.
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "from pyssem.model import Model; print(Model.__module__)",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "pyssem.model"
