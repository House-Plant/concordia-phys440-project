# Maintainer setup and upkeep

The tracked workflow is implemented. This clone has `.venv` and local hooks.
GitHub settings have **not** been changed or verified. Work remains in this checklist.
The actual default branch is `main` (`origin/HEAD` was inspected).

## Initial setup

1. Follow [contributor setup](CONTRIBUTOR_SETUP.md) for VS Code, Spyder, or PyCharm.
   Run bootstrap and the checks using that editor's route.
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
  `src/tools/` is the scientific package, installed editably during sync with
  the pinned lightweight `uv_build` backend. Only scientific code is packaged;
  standalone `scripts/`, `maintenance/`, repository guides, and workflow tests stay
  outside the package.
  Setup runs `uv sync --locked` and installs repository-local pre-commit,
  post-checkout, and post-merge hooks. It is safe to repeat. It refuses an existing
  custom `core.hooksPath` instead of changing that setting. Resolve any hook conflict
  deliberately; do not change global Git configuration as part of this project.
- **[x] Editor:** workspace Ruff formatting/import sorting on explicit Python Save.
  `scripts/personal/` is excluded from Ruff linting, formatting, and import sorting.
  Contributor setup includes installing Python/Ruff extensions and enabling Ruff
  for this workspace. The setup task installs the command-line tool; editor extension
  installation is a separate one-time step. Jupyter is recommended for notebooks.
  Python environment selection uses VS Code's discovery of the root `.venv`.
  Do not set `python.defaultInterpreterPath` to the `.venv` directory: Python
  Environments 1.20.1 resolves that directory but then uses it as the executable,
  overriding a valid selection on startup. This causes Run, import analysis, and
  editor test discovery to fail. An explicit executable path differs across OSes;
  automatic `.venv` discovery avoids that shared-setting problem.
  Notebook save automation is
  deliberately omitted because it has not been tested in VS Code here; Ruff CLI and
  commit/CI checks include notebooks. Select `.venv` and restart kernels after updates.
- **[x] Commits:** check-only Ruff lint/format on staged Python/notebook files.
  Personal files under `scripts/personal/` are excluded. `force-exclude = true`
  in `pyproject.toml` enforces the exclusion even for explicit hook filenames;
  the same configuration applies to the editor and CI.
  Unused imports (`F401`) are allowed for exploratory work; import sorting and
  the other configured checks still apply. This setting also applies in the editor
  and CI through `pyproject.toml`.
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
   Verify **Run Python File in Terminal** uses `.venv/bin/python` on macOS/Linux
   or `.venv\Scripts\python.exe` on Windows. Close and reopen the workspace and
   repeat without reselecting the interpreter. **Project: Run checks** invokes
   Python directly and cannot establish that the editor's interpreter is correct.
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
  `src/tools/` and are imported as `tools`. The editable install is automatic
  through `uv sync --locked`; no contributor `pip install` step is required. Run
  a runnable module with **Project: Run Python module**, entering `tools.MODULE`,
  or from the root with `uv run --locked python -m tools.MODULE`.
  Tasks and VS Code notebook kernels start at the root; use `data/` and `results/`
  paths. Other notebook launchers may choose a different working directory.
- Standalone scientific runs belong in `scripts/`; informal manual investigations
  belong in `scripts/testing/`. Neither needs `__init__.py`. Run a script with
  VS Code's **Run Python File in Terminal** using `.venv`, or from the repository
  root with `uv run --locked python scripts/PATH.py`. Scripts can import `tools`.
  Ruff covers shared scripts, with `scripts/personal/` excluded; the default
  pytest suite does not execute standalone scripts.
  Keep slow simulations and visual investigations here; move reusable functions
  into `src/tools/` and fast automated correctness checks into `tests/`.
- Personal workspaces use `scripts/personal/<name>/`, with folders for Colin,
  Naomi, Sabrina, Jaeden, and Eshaal. When onboarding someone else, copy an
  existing folder's empty structure. Keep scripts directly in each person's folder
  and datasets in its `data/` directory; both can be committed and shared.
  `.gitignore` excludes every person's `figures/` and
  `outputs/` contents, except `.gitkeep` files.
  These local files are not backed up by Git. Personal folders are a team convention;
  contributors coordinate before editing another person's work. Keep these rules
  aligned with the [personal-folder instructions](../../scripts/personal/README.md).
- Repository automation and **all its tests** live in `maintenance/` and `maintenance/tests/`.
  Reserve `tests/` for scientific tests; keep scientific reports in `reports/`
  and repository guides in `docs/`. The implementation brief is kept in
  `docs/maintenance/`; use the contributor guides for current paths and commands.
  Pytest discovers `tests/` and `maintenance/tests/` separately with importlib mode.
  Once scientific tests exist, run only those with `uv run --locked pytest tests`;
  run infrastructure tests with `uv run --locked pytest maintenance/tests`.
- Shared scientific dependencies include NumPy, Matplotlib, SciPy, pandas, SymPy, Seaborn,
  and MOCAT-pySSEM, whose distribution and import name is `pyssem`. Keep these in
  `pyproject.toml` and `uv.lock`; do not copy third-party packages into `src/`.
  `pyssem` is pinned to the published prerelease `0.1.dev465`. Review upstream
  release changes before upgrading it; verify `from pyssem.model import Model`
  as well as the repository checks after dependency changes. Model simulations
  may need additional configuration and data; package installation does not run them.
  Seaborn is declared directly because this pySSEM release imports it without
  declaring it in its package dependencies. Keep the isolated Model import check
  when updating either package.
- Spyder 6.1.x: `spyder-kernels>=3.1.6,<3.2` is a default dev dependency;
  setup/sync also installs its `ipykernel` dependency for consoles/notebooks.
  Keeping this in the default dev group prevents ordinary `uv sync --locked`
  calls (including branch/pull hooks) from removing console support. The Spyder
  application stays outside the project environment. Before adopting another
  Spyder release, check its required kernel range, update the shared dependency
  and lock together, and test a real console launch. Do not document a one-off
  `pip install` or optional group that normal hooks would remove.
  Scientific dependencies above are also installed by setup/sync; select `.venv`
  in each IDE and notebook kernel. The contributor guide includes a Run/reopen
  check; automated CLI checks cannot verify the editor's selected interpreter.
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
- The dev tools are Ruff, pre-commit, pytest, Spyder console support, and PyYAML for workflow
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

The Spyder/PyCharm routes were researched against upstream documentation on
2026-11-18. Spyder 6.1.8 requires `spyder-kernels>=3.1.6,<3.2` (verified against
its published package metadata). PyCharm's built-in Ruff settings vary by release;
the targeted Ruff commands are the common fallback. GitHub Desktop 3.5.5+ has
shell-aware hook support; PyCharm's **Run Git hooks** must remain enabled.

On macOS, the updated lock, Ruff checks, and all 12 pytest cases passed. Repeat
locked sync retained console support; a real `spyder_kernels.console` process
accepted a client execution request and imported NumPy, Matplotlib, and this
clone's editable `tools` through `.venv`. Existing locked package versions and
the scientific runtime requirements were preserved.
In a disposable clone, setup succeeded twice with the printed interpreter path;
Git hooks rejected an unsorted/unformatted shared file, accepted it after the
documented formatting commands, and preserved kernel/scientific imports after
a branch switch and its sync hook.

For onboarding acceptance, exercise each contributor's real GUI: run the
setup-check file, reopen and run again, confirm formatting, commit a shared Python
edit with hook output, switch branches and Pull, then confirm sync and restart
consoles. Spyder/PyCharm/GitHub Desktop GUI flows have not been exercised locally;
documentation review and terminal checks are not a substitute for that check.

Contributor links: [Setup](CONTRIBUTOR_SETUP.md) · [Daily use](CONTRIBUTOR_DAILY_USE.md).
