# Maintainer setup and upkeep

The tracked workflow is implemented. This clone has `.venv` and local hooks.
GitHub settings have **not** been changed or verified. Work remains in this checklist.
The actual default branch is `main` (`origin/HEAD` was inspected).

## Initial setup

1. Run **Project: First-time setup**, then **Project: Run checks** in VS Code.
2. Publish the reviewed changes through your normal branch/PR process. Under
   **Actions**, confirm the **Project checks** workflow completes successfully.
   It runs on PRs to `main` and pushes to `main`, with one check named **Quality**.
   If Actions is disabled, enable it under **Settings → Actions → General**, allowing
   the pinned `actions/checkout` and `astral-sh/setup-uv` actions.
3. In **Settings → General → Pull Requests**, enable **Allow squash merging**.
   Optionally set its default commit message to **Pull request title** and enable
   **Automatically delete head branches**. Useful plain-language PR titles are fine;
   there is no title linter or local commit-message requirement.
4. Verify the local workflow in a disposable clone before onboarding contributors.
   See the checks below. GitHub settings are manual steps; local setup does not
   change them.

## What runs automatically

- **[x] Environment:** `uv.lock` locks runtime and dev packages; `.venv` is ignored.
  `src/phys440/` is the scientific package, installed editably during sync with
  the pinned lightweight `uv_build` backend. Only scientific code is packaged;
  `tools/`, repository guides, and workflow tests stay outside the package.
  Setup runs `uv sync --locked` and installs repository-local pre-commit,
  post-checkout, and post-merge hooks. It is safe to repeat. It refuses an existing
  custom `core.hooksPath` instead of changing that setting. Resolve any hook conflict
  deliberately; do not change global Git configuration as part of this project.
- **[x] Editor:** workspace Ruff formatting/import sorting on explicit Python Save.
  Python, Ruff, and Jupyter are recommended extensions. Notebook save automation is
  deliberately omitted because it has not been tested in VS Code here; Ruff CLI and
  commit/CI checks include notebooks. Select `.venv` and restart kernels after updates.
- **[x] Commits:** check-only Ruff lint/format on staged Python/notebook files.
  Code fixes happen on Save or through a deliberate edit. Like standard pre-commit,
  the framework temporarily sets aside unstaged edits while checking staged content
  and restores them afterward. The project scripts never discard work.
- **[x] Branch/pull:** `uv sync --locked` on branch checkout or successful merge
  (including an updating Pull). File-only checkouts are skipped. Sync always targets
  this repo's `.venv`, even if another environment is active. It is idempotent and
  bounded to 60 seconds. Offline/failure messages give the recovery task and explain
  that Git's branch switch/pull has already happened. Missing uv or a broken hook
  runner can fail before the script; restart VS Code/rerun setup, then sync manually.
- **[x] CI:** **Quality** checks lock consistency, Ruff, tool/package imports,
  and fast/offline pytest tests. Tokens have read access only, checkout credentials
  are not persisted, and actions are pinned to release SHAs. No private data,
  secrets, or model training is required.

## Verification and recovery

1. On a clean clone, run **Project: First-time setup** twice and **Project: Run checks**.
   Both setup runs should finish successfully, using `.venv` Python 3.12.
2. In VS Code, Save a temporary badly spaced `.py` file with out-of-order imports;
   inspect formatting and import order. Delete it afterward. Select `.venv` for
   script runs and notebook kernels. The GUI Save/Commit buttons use the configured
   formatter and normal Git hooks; actual GUI behavior still needs your local check.
3. On a disposable branch, commit a valid Python edit. Confirm both Ruff checks run.
   Temporarily stage unformatted code to confirm a commit is blocked; Save, review,
   restage, and retry. Commits should not rewrite staged content.
4. Test **Add Python package** with an approved distribution. Review the
   `pyproject.toml`/`uv.lock` changes and verify its import with `.venv`. On a
   disposable clone, test switching/pulling between branches with different
   dependency lists and confirm the package appears/disappears in `.venv`.
5. For a failed environment sync, run **Project: Sync Python environment**; do not
   assume a failed hook reversed the Pull or branch switch. After moving/renaming
   a clone or upgrading Python, rerun setup to refresh hook interpreter paths.

## Occasional upkeep and different project needs

- Review PRs and external dependency additions. Encourage task branches, clear
  descriptions, teammate review and squash merge. Separate branches are preferred
  for simultaneous changes to the same files. Never force-push shared history.
- New runtime library: use **Project: Add Python package**. The import name may
  differ from its distribution name. Reusable scientific modules belong in
  `src/phys440/` and are imported as `phys440`. The editable install is automatic
  through `uv sync --locked`; no contributor `pip install` step is required. Run
  a runnable module with **Project: Run Python module**, entering `phys440.MODULE`,
  or from the root with `uv run --locked python -m phys440.MODULE`.
  Tasks and VS Code notebook kernels start at the root; use `data/` and `results/`
  paths. Other notebook launchers may choose a different working directory.
- Repository automation and **all its tests** live in `tools/` and `tools/tests/`.
  Reserve `tests/` for scientific tests; keep scientific reports in `reports/`
  and repository guides in `docs/`. The implementation brief is kept in
  `docs/maintenance/`; use the contributor guides for current paths and commands.
  Pytest discovers `tests/` and `tools/tests/` separately with importlib mode.
  Once scientific tests exist, run only those with `uv run --locked pytest tests`;
  run infrastructure tests with `uv run --locked pytest tools/tests`.
- First notebooks: add `ipykernel` with that task, then select `.venv`. NumPy,
  SciPy, plotting libraries and model frameworks are intentionally not guessed.
  The contributor guide covers running scripts and notebooks.
- Dev-only dependency (maintainer terminal): `uv add --dev DISTRIBUTION`.
  Remove an unused runtime dependency with `uv remove DISTRIBUTION` (add `--dev`
  for dev tools). Review and commit both dependency files. Contributors normally
  need only the prompted Add task.
- Occasionally update a selected tool with `uv lock --upgrade-package ruff`
  (or another distribution), then `uv sync --locked`, **Run checks**, and review
  the lock diff in a PR. Use `uv lock --upgrade` only for a deliberate broader
  refresh. Keep action SHAs/release comments and the CI uv version reviewed too.
  The initial CI uv pin matches the tested local version, 0.11.19.
- No Python support was declared in the empty starting repo. Python 3.12 was
  selected because it was already available via uv. To change it deliberately,
  update `requires-python`, `.python-version`, Ruff's target, both bootstrap/hook
  `--python` arguments, and the smoke-test assertion; regenerate the lock, sync,
  rerun setup/tests on contributor OSes, and update the guides.
- The initial dev tools are Ruff, pre-commit, pytest and PyYAML for workflow
  validation. PyYAML is also a dependency of pre-commit, so it adds no extra install.
  The pinned `uv_build` build backend installs only the scientific package. There
  is no second package manager, daemon, title linter,
  dependency-upgrade bot, or permanent `develop` branch.
- Keep a clear data/output policy. `results/` is ignored as generated output;
  scientific datasets and notebooks are not broadly ignored.
- Keep these guides aligned with task labels, the default branch, and check names.
  Keep tests in the default suite fast/offline. Run expensive model experiments
  deliberately outside that suite.

## Verification limits at handoff

Verified on macOS on 2026-10-20: 11 pytest cases; lock consistency; Ruff lint and
format checks; pre-commit configuration and VS Code JSON validation. Disposable
clone checks cover repeatable setup, imports from `notebooks/`, the module-run
and package-add tasks, scientific/tooling test discovery, valid/blocked Ruff
commits, branch dependency synchronization, updating Pull, and failed-sync recovery.
Wheel and source archive inspection confirmed that repository scripts, tests,
and guides are excluded from the scientific package. Windows/POSIX interpreter
path selection and package-task argument handling also have automated checks.

Windows and Linux execution, live VS Code Save/notebook/Source Control behavior,
and GitHub Actions runs remain unverified. Process tasks pass package input as one
argument with an option terminator; Python scripts choose Windows
`Scripts/python.exe` or POSIX `bin/python` without shell-specific bootstrap commands.

Contributor links: [Setup](CONTRIBUTOR_SETUP.md) · [Daily use](CONTRIBUTOR_DAILY_USE.md).
