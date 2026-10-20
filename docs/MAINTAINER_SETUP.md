# Maintainer setup and upkeep

The tracked workflow is implemented. This clone has `.venv` and local hooks.
GitHub settings have **not** been changed or verified. Work remains in this checklist.
The actual default branch is `main` (`origin/HEAD` was inspected).

## Activate the protections, in this order

1. **[ ] MAINTAINER ACTION REQUIRED: specify actual protected paths.**
   **No actual immutable paths identified; maintainer must populate the protected-file
   list before protection is active.** The original repo had only `.gitignore` and
   `LICENSE`; neither was designated immutable. Do not guess which future data files
   should be frozen. Approve only existing, tracked files with no legitimate routine
   edits. Add exact root-relative paths to `.github/protected-paths.txt`, one per line.
   Spaces are literal; comments start with `#`; there are no globs/directories or
   inline comments. JSON-quoted strings support unusual filenames.
   Run the following from the repo root:

   ```text
   uv run --locked python tools/check_protected_files.py --update-readonly
   uv run --locked python tools/check_protected_files.py --check-settings
   ```

   The first command updates only `files.readonlyInclude` in `.vscode/settings.json`.
   Review and commit **both files together**, with no edits to the newly protected
   files. VS Code makes matching files read-only in editors/Explorer. The second
   command, also in **Project: Run checks** and CI, checks tracking and policy/settings
   agreement. Paths with glob characters are escaped for VS Code; unusual names
   should also be checked manually in the editor on your contributors' OSes.
2. **[ ] Fill in `.github/CODEOWNERS`.** Replace every `@OWNER` with a real account
   or `@organization/team` with explicit write access, then uncomment the rule lines.
   No username has been invented. These entries cover the policy, checker and other
   tooling scripts/tests, guides, workflows, CODEOWNERS itself, editor/task settings,
   and dependency files. They are evolving tooling, not immutable science files. Check GitHub's
   CODEOWNERS error display after upload. [Code-owner requirements and availability](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
3. **[ ] Publish the reviewed implementation and observe Actions.** Commit/push
   intentionally using your normal review process; nothing has been committed or
   pushed by setup. The workflow is `.github/workflows/checks.yml`, named
   **Project checks**, running on PRs to `main` and pushes to `main`. Initial adoption
   must be reviewed manually: the old base has no policy/checker to enforce yet.
   After installation, PR enforcement uses the base commit's checker and policy.
   If Actions is disabled, enable it under **Settings → Actions → General** with
   permission to run the pinned `actions/checkout` and `astral-sh/setup-uv` actions.
4. **[ ] Require the checks and reviews.** After a successful run, go to **Settings
   → Rules → Rulesets → New ruleset → New branch ruleset** (or **Settings → Branches
   → Add branch protection rule**). Target `main`; set enforcement to **Active**.
   Require a pull request, require one approval where feasible, and enable
   **Require review from Code Owners**. Require status checks **`Quality`** and
   **`Protected files`**, from GitHub Actions. The workflow's job `name` fields define
   these exact names; select them from the successful run. Prefer requiring branches
   to be up to date before merging. Block force pushes and branch deletions. Keep
   bypass permissions minimal, including administrator bypass where possible.
   Confirm these rules really block merging a failing test PR. CI alone does not
   prevent a merge. Check your plan: private/free repositories may lack the needed
   branch/review protections; do not assume that a visible workflow means enforcement
   is active. [GitHub rules and availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
5. **[ ] Set merge behavior.** In **Settings → General → Pull Requests**, enable
   **Allow squash merging**. Set its default commit message to **Pull request title**.
   Optionally disable merge commits/rebase merging and enable **Automatically delete
   head branches**. PR titles should describe the resulting change. Structured
   prefixes such as `feat:` or `fix:` are optional; there is no PR-title check or
   local commit-message requirement.
6. **[ ] Optional: add stronger push-time path restrictions if your plan supports
   them.** Under **Settings → Rules → Rulesets**, create a **push ruleset** with
   **Restrict file paths**, using the same approved immutable paths. GitHub interprets
   these as patterns, so check escaping/matches for unusual names. This can reject
   pushes to **feature branches too**. Review who may bypass it. Availability depends
   on plan/repository type; this is not required for the baseline workflow.
   [Push path restrictions](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#restrict-file-paths).
7. **[ ] Verify with a disposable test branch and PR.** See the checks below before
   onboarding contributors. Close the test PR afterward; discard only test edits
   that you have reviewed as unwanted. Do not overwrite real research work.

Hooks, workflows, and CODEOWNERS templates in this repository cannot stop deliberate
tampering by someone who can replace them. Required GitHub reviews, permissions,
and rules are necessary. A policy-only change is a maintainer-reviewed tooling PR;
it is not automatically authorized just because the protected-file checker passes.

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
- **[x] Commits:** check-only Ruff lint/format on staged Python/notebook files; protected
  paths checked against **HEAD plus staged additions** to the policy. A same-commit
  entry removal cannot permit a protected edit. No automatic fixes, commits or pushes.
  Like standard pre-commit, the framework temporarily sets aside unstaged edits while
  checking staged content and restores them; the project scripts never discard work.
- **[x] Branch/pull:** `uv sync --locked` on branch checkout or successful merge
  (including an updating Pull). File-only checkouts are skipped. Sync always targets
  this repo's `.venv`, even if another environment is active. It is idempotent and
  bounded to 60 seconds. Offline/failure messages give the recovery task and explain
  that Git's branch switch/pull has already happened. Missing uv or a broken hook
  runner can fail before the script; restart VS Code/rerun setup, then sync manually.
- **[x] CI:** **Quality** checks lock consistency, Ruff, policy/editor agreement,
  tool-import smoke tests and fast/offline pytest tests. **Protected files** uses
  the trusted base policy and checker against the PR diff; both ends of renames
  are checked. Removing an entry on the PR branch cannot disable base protection.
  Pushes to `main` also compare against their preceding commit. Full history is
  fetched. Tokens are read-only, checkout credentials are not persisted, and actions
  are pinned to release SHAs. No private data, secrets or model training is required.

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
5. After selecting actual immutable paths, simulate a protected edit outside the
   read-only editor. The staged commit must fail and name the path. Test deletion
   and rename too. Only in a disposable clone/test PR, a maintainer may simulate
   skipped local hooks; **Protected files** must still fail on GitHub, including a
   protected edit plus removal of its manifest entry. Confirm required rules prevent
   merge. Close the PR. The automated tests already exercise these cases with
   temporary fixture files, without freezing any invented project data.
6. If a protected edit is unwanted, unstage it with **−**, then **Source Control →
   right-click file → Discard Changes**. Do this only after reviewing what will be
   lost. For intentional changes, contact the policy owner. An approved unfreeze
   needs a separate policy/settings PR and review before an edit can land; update
   any server push restriction deliberately as well.
7. For a failed environment sync, run **Project: Sync Python environment**; do not
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
  and repository guides in `docs/`. The original implementation brief is archived
  in `docs/maintenance/`; it is historical, not the current path reference.
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
- Maintain the protected manifest and editor settings together. CI checks their
  agreement. Protect tooling through owner review rather than declaring it
  immutable. Document any future data/output policy; only `/results/` is newly
  ignored as generated output, not arbitrary datasets/notebooks.
- Keep these guides aligned with task labels, the default branch, and check names.
  Keep tests in the default suite fast/offline. Run expensive model experiments
  deliberately outside that suite.

## Verification limits at handoff

Verified on macOS on 2026-10-20: 40 pytest cases; lock consistency; Ruff lint and
format checks; pre-commit configuration and VS Code JSON validation; Actionlint
v1.7.12 workflow validation. A disposable clean clone with spaces in its path passed
setup twice, imports from `notebooks/`, the exact module-run task, separate scientific
and tooling test discovery, real valid/blocked commits, protected-policy-removal
rejection with a trusted CI checker, the exact package-add task, branch dependency
removal/addition, an updating Pull, and recovery messaging for a failed locked sync.
Wheel and source archive inspection confirmed that tooling, workflow tests, and
guides are excluded from the scientific package; it has no runtime tool dependencies.
The CI shell step was tested with current and legacy base-checker paths, first
installation, and a missing trusted checker. No real project history was changed
by those tests. Python/Windows interpreter path selection and the argument-list
task configuration also have automated checks.

Windows and Linux execution, live VS Code Save/notebook/Source Control behavior, GitHub
Actions runs, repository plan features, and server-side merge blocking must be
verified on those systems. Process tasks pass package input as one argument with
an option terminator; Python scripts choose Windows `Scripts/python.exe` or POSIX
`bin/python` without shell-specific bootstrap commands.

Contributor links: [Setup](CONTRIBUTOR_SETUP.md) · [Daily use](CONTRIBUTOR_DAILY_USE.md).
