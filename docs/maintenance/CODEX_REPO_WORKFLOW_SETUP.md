# Codex implementation brief: low-maintenance Python modelling repository

> **Audience:** A Codex agent working **inside the actual Git repository**.  
> **Objective:** Implement a reliable, repository-local collaboration workflow for contributors with little Git, command-line, or Python packaging experience. **Do the implementation**, test it, and write the three short guides specified below. Do not merely propose a solution.

## 1. Working principles

1. **Inspect before changing anything.** Determine the existing default branch, Python version, project/package structure, dependencies, tests, notebooks, VS Code settings, GitHub workflows, and Git ignore rules. Preserve working conventions and avoid replacing existing configurations wholesale. Do not rename or reorganize modelling code just to fit a template.
2. Optimize for **VS Code's built-in Source Control interface**. Normal contributors should be able to write, save, stage, commit, pull, publish/push, and switch branches without entering Git commands.
3. One-time local setup is acceptable; **no routine manual formatting, linting, installation of already-declared dependencies, or Git-hook commands** should be required. Failures should be understandable to beginners.
4. All project-specific changes must be **repository-local**: project `.venv`, repo Git hooks, `.vscode/` workspace settings, `pyproject.toml`, and workflows. Do **not** alter `git config --global`, global VS Code settings, system Python packages, or other repos.
5. Prefer **uv + Ruff + pre-commit + pytest + GitHub Actions**. If an existing package manager or project constraints conflict, preserve the working project, adapt minimally, and explicitly explain any deviation in the maintainer guide. Do not create redundant package managers/lockfiles.
6. Keep the solution small and robust. Avoid additional services, bots, heavyweight frameworks, auto-generated commit messages, or continuously running daemons. Do not silently run destructive Git operations, force-push, stash, reset, rewrite history, or merge for anyone.

## 2. Intended division of work

| Owner | One-time or automatic responsibility |
|---|---|
| Codex / tracked repo | Configure project environment, formatter, VS Code tasks/settings, Git hooks, CI, and documentation |
| Maintainer on GitHub | Review CI runs and PRs; configure squash merges where desired |
| Contributor once | Install Git, VS Code, uv and recommended extensions; clone/open repo; run **one clearly labelled VS Code setup task**; select the project's Python interpreter/notebook kernel |
| Contributor routinely | Edit/save code; add a new package through a prompted VS Code task when necessary; use VS Code Source Control to branch, stage, commit, push/pull, and open a PR |

## 3. Implement the project environment and editor experience

- Use/adapt `pyproject.toml` and commit `uv.lock` as the authoritative project dependency definitions. Put `ruff`, `pre-commit`, and `pytest` in the dev group. Use the project's **existing** supported Python version; do not force Python 3.12 or a new source layout if inappropriate. Keep the project importable from its actual modules/package; only introduce editable package installation if warranted.
- Ensure `.venv/`, caches, local secrets, generated results, and other appropriate artifacts are ignored. **Do not indiscriminately ignore or delete existing research data or notebooks.**
- Configure Ruff in `pyproject.toml` for conservative formatting, import organization, and basic safe lint rules. Avoid enabling dozens of disruptive rules in an established modelling repo. When first applying formatting, keep unrelated code churn minimal.
- Commit `.vscode/settings.json` and `.vscode/extensions.json` so Python code is **formatted and imports organized on save** using Ruff, with Python/Jupyter extensions recommended. Apply notebook-on-save settings only if supported and tested. Settings must apply to this workspace, not VS Code globally.
- Commit `.vscode/tasks.json` with plain-language names:
  - **Project: First-time setup** — uses `uv` to run a cross-platform Python bootstrap script that installs the locked environment, installs local Git hooks, and prints a short success/failure message.
  - **Project: Add Python package** — prompts for one package/distribution name and runs `uv add <name>` as an argument list (**process task, not shell string interpolation**). It must update `pyproject.toml`, `uv.lock`, and `.venv` together.
  - **Project: Sync Python environment** — runs `uv sync --locked` for recovery.
  - Optional only if useful: **Project: Run checks** — invokes the same fast local checks as CI.
- The bootstrap script belongs under `maintenance/` and must run on Windows, macOS, and Linux without Bash/PowerShell-specific assumptions. It should detect missing tools with clear installation guidance, operate from the repo root, be safe to run repeatedly, and avoid changing global settings. A contributor should not have to type a sequence of terminal commands.
- Document the difference between **an import statement** and **installing a new external package**. Existing project dependencies work immediately; new dependencies require the *Add Python package* task. `import sklearn` may correspond to a differently named distribution (`scikit-learn`), so **never auto-install arbitrary missing imports**. Project-local imports should resolve from the configured project environment.

## 4. Commit and environment synchronization behavior

- Install **repository-local** `pre-commit` hooks during bootstrap. VS Code's **Commit** button must trigger them because it invokes Git normally.
- Prefer **check-only** Ruff hooks at commit time (no unexpected edits to staged files); normal code fixes should already happen on save. Check staged Python files with Ruff lint and format checks. CI runs equivalent checks across the applicable project paths.
- Configure a light, idempotent post-checkout/post-merge hook to run `uv sync --locked` when switching branches or pulling/merging code. Use pre-commit's supported hook stages or equivalent repository-local hooks; verify VS Code triggers them. Skip unnecessary file-only checkouts where possible. Fail gracefully if offline or package synchronization fails: explain how to run **Project: Sync Python environment**; do not pretend a checkout or pull was undone. The sync must affect **only** this repo's `.venv`.
- Do not require strict Conventional Commit syntax for every local commit: it is unnecessary friction for novices. Encourage ordinary useful commit descriptions. Instead, if structured final history is desired, implement a **small PR-title check** (e.g., `feat: ...`, `fix: ...`, `docs: ...`) in CI and explain that titles can be edited on GitHub. Configure squash merges so the PR title becomes the final main-branch commit message. Avoid adding Commitizen by default.
- Do not add automatic commits, pushes, pull requests, merges, branch switches, or package upgrades. These must remain deliberate actions.

## 5. GitHub Actions: automatic checks, no hidden server setup

Implement one straightforward workflow under `.github/workflows/`, triggered on pull requests to the default branch (including PR-title edits if title linting is enabled) and on pushes to the default branch.

It should:
1. Check out the repository.
2. Install uv and the project's supported Python version; install dependencies reproducibly using `uv sync --locked`.
3. Check lockfile consistency, Ruff lint/format, a basic project import or smoke test if applicable, and **fast/offline** pytest tests. Do not execute expensive model training or require private datasets/secrets.
4. Optionally validate the pull-request title using a short, documented convention.
5. Produce clear named check results and useful failure messages. Use least-privilege GitHub Actions permissions; pin actions to appropriate stable releases/SHAs; avoid untrusted PR code running with write tokens or secrets.

CI reports check results for contributors and reviewers.

## 6. Three finished guides Codex must write

Create these files, with short sentences, exact VS Code menu labels where reliable, and very little jargon. Prefer numbered actions over conceptual explanations. Include screenshots **only if already available in the repo**; do not require screenshots or browser automation.

### `docs/CONTRIBUTOR_SETUP.md` — first time, 5–10 minutes of reading

Include:
- Clearly separated **Windows / macOS / Linux** installation links for Git, VS Code, uv; what editor extensions to install; GitHub sign-in if necessary.
- **Clone Repository** using VS Code → open the project folder → **Terminal → Run Task → Project: First-time setup** → select the `.venv` Python interpreter; for notebooks select its kernel and restart kernels after dependency updates.
- A **visible success check**: expected setup completion message and one simple import or check command through a task, if available.
- A tiny troubleshooting section covering `uv not found`, extension missing, wrong interpreter/kernel, failed sync, hook installation error. Escalation guidance: ask the maintainer and share the message; no global `pip install`, Git reset, or force-push advice.
- Explicitly say these changes are **local to this repository**, aside from installing standard applications/extensions.

### `docs/CONTRIBUTOR_DAILY_USE.md` — one-screen quick reference

Make this the primary non-programmer-facing guide. Include this **exact logical journey**, using VS Code GUI actions rather than shell commands:

1. **Start work:** switch to `main` using the branch indicator; use **Source Control → ... → Pull**. Verify that local uncommitted work has been saved to its own branch first.
2. **Make a branch:** branch indicator → **Create New Branch**; use simple names like `feat/baseline-model` or `fix/missing-values`. One short-lived branch per task; **do not commit directly to main**.
3. **Work:** edit and **Save** (formatting/import organization happens automatically). If a new library is needed, **Terminal → Run Task → Project: Add Python package**, then enter its distribution name. Do not use `pip install` for shared dependencies.
4. **Commit:** Source Control icon → review diffs → stage relevant files using `+` → enter a plain-language description → **Commit**. Explain in one sentence what to do when checks fail.
5. **Upload:** choose **Publish Branch** on first upload or **Push** thereafter; explain clearly that **Commit is local, Push uploads, and neither merges into `main`**.
6. **Finish:** open PR against `main` (GitHub website is an acceptable easy route; optionally use VS Code's PR extension) → complete a simple title/description → wait for green CI → request teammate review → **Squash and merge**. If CI fails or GitHub says there is a conflict, contact the maintainer rather than using complicated Git commands.
7. **Next task:** switch to `main` and **Pull** again; branch for next task. Automatic dependency synchronization may run; restart an open notebook kernel if libraries changed.

**Add a tiny separate paragraph titled “Working on someone else's branch”:** first **commit and push or otherwise safely save your own branch's work**; use VS Code's Fetch and branch picker to switch to their remote branch; pulling first is essential; work on the shared branch **only with the owner's agreement**. If merely testing/reviewing, do not push. If collaborating on the same branch, coordinate ownership of files, **Pull before editing and again before Push if others have contributed**, and stop/ask for help if Git reports a conflict. Never force-push. Mention that uncommitted changes can follow the user across branches; do not switch while unsure about uncommitted files. If simultaneous editing is common, recommend separate branches/PRs instead.

End with a **tiny “If something goes wrong” panel**: commit blocked → read message; new import missing → Add package task; behind remote → Pull before Push; merge conflict → stop and ask maintainer. Avoid teaching rebase, stash, cherry-pick, or command-line Git in this daily guide.

### `docs/MAINTAINER_SETUP.md` — manual GitHub and upkeep checklist

Include:
1. Run setup and the checks; confirm the GitHub Actions workflow runs after upload.
2. Explain how to enable Actions if disabled and name the `Quality` check exactly.
3. In **Settings → General → Pull Requests**, allow/prefer **squash merging** and
   enable automatic deletion of merged branches where appropriate.
4. Verify repeatable setup, formatting, Git hooks, package addition, and dependency
   synchronization with a disposable clone and feature branch.
5. Explain routine upkeep: review PRs and dependency additions; update pinned tools
   occasionally; keep guides aligned with task labels and repository layout.
6. Distinguish local automation from GitHub settings that have not been configured.

Add a short link to both contributor guides in the root README without replacing existing project information.

## 7. Branch and PR policy to implement (keep it simple)

- Stable default branch (`main` if that is already the default; otherwise use the **real** branch name).
- Short-lived task branches (`feat/...`, `fix/...`, `docs/...`). Do not create a permanent `develop` branch.
- Contributors may share a branch with coordination; **separate branches are preferred** if working on the same files simultaneously.
- PR + automated CI + teammate review + squash merge. Do not automatically create PRs or merge anything.
- No forced pushes, global Git hooks, mandatory command-line Git workflow, or strict local conventional-commit requirement.

## 8. Verification before declaring the work complete

Run, and fix failures in, the equivalent of these scenarios (adapt commands to the actual repo):

- Fresh setup on a clean clone is idempotent; dependencies install into project `.venv`; the correct Python interpreter/import works.
- Saving a Python file triggers workspace-only Ruff formatting/import sorting. Confirm notebook behavior where supported.
- Commit via Git with a valid source change runs the hooks and succeeds. Invalid formatting or lint errors fail with a useful message.
- Switching branches or merging/pulling changed dependency declarations synchronizes the project environment; sync errors are clearly explained.
- Adding a dependency through the VS Code task modifies both `pyproject.toml` and `uv.lock`, and is importable thereafter.
- Workflow syntax, action pinning, PR-title validation if chosen, and CI checks are sound; tests do not need proprietary data or long-running training.
- Windows-safe paths/quoting and cross-platform bootstrap invocation are checked, even if the current execution environment permits testing only one OS.
- Daily guide matches **actual** tasks, hook behavior, branch names, repo structure, and GitHub check names; no impossible “one click” promises.

## 9. Final handoff Codex must provide

After implementing, give the maintainer a compact report containing:

- **Created/modified files**, grouped by tooling vs. documentation.
- **What works automatically now**, and any limitations.
- **Manual GitHub actions still required**, prominently listed in the order they should be performed.
- **Tests run and results**, plus untested platform-specific behavior.
- One-line pointers to `docs/CONTRIBUTOR_SETUP.md`, `docs/CONTRIBUTOR_DAILY_USE.md`, and `docs/MAINTAINER_SETUP.md`.

**Success criterion:** After one-time setup, a novice normally needs only **Save → Stage → Commit → Push → Open PR**, with occasional **Add Python package**, while the repository automatically checks quality and synchronizes declared packages.

---

### Primary implementation references

- [VS Code Source Control](https://code.visualstudio.com/docs/sourcecontrol/overview)
- [VS Code Python formatting and import organization](https://code.visualstudio.com/docs/python/formatting)
- [uv projects: locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv and pre-commit](https://docs.astral.sh/uv/guides/integration/pre-commit/)
- [pre-commit hook stages](https://pre-commit.com/#confining-hooks-to-run-at-certain-stages)
