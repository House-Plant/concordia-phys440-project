# Daily use

Once per clone: follow [setup](CONTRIBUTOR_SETUP.md) for VS Code, Spyder, or
PyCharm. Save → Stage/select changes → Commit → Push → Open PR is the normal cycle.
The numbered workflow below names VS Code's buttons. Other editors follow the
same branch/review rules using the
[Spyder/PyCharm controls and commands](#spyder-and-pycharm-daily-workflow).
Put reusable scientific code in `src/tools/`, standalone analysis/simulation
scripts in `scripts/`, and informal investigations in `scripts/testing/`.
Use `notebooks/` for interactive exploration, `data/` for inputs, `tests/` for
automated scientific checks, and `reports/` for your write-up. Repository automation
lives in `maintenance/`; see the [directory map](../../README.md#where-to-work).

For a personal workspace, use your named folder under `scripts/personal/`.
Put scripts directly in your personal folder and datasets in its `data/` folder. Stage,
commit, and push these files to save and share them through Git. Put plots and
other generated files in `figures/` and `outputs/`; their contents are ignored.
Ruff linting, formatting, and import sorting are disabled in `scripts/personal/`,
so personal files do not block commits for Ruff issues.
Coordinate before editing someone else's folder. See the
[personal-folder instructions](../../scripts/personal/README.md) for running scripts
and choosing output paths. Continue using the normal task-branch workflow below.

1. **Start work.** First commit and push your current task's work on its own
   branch, or otherwise safely save it. Check Source Control for uncommitted files;
   do not switch branches if unsure. Use the bottom-left branch indicator to
   switch to `main`, then **Source Control → … → Pull**.
2. **Make a branch.** Branch indicator → **Create New Branch**. Use a name such as
   `feat/baseline-model` or `fix/missing-values`. Keep one short-lived branch per
   task. Do not commit directly to `main`.
3. **Work.** Edit and **Save** Python files; Ruff formats and organizes imports
   outside `scripts/personal/`.
   Select `.venv` first. Open a standalone script from `scripts/` or
   `scripts/testing/` and use the Python extension's **Run Python File in
   Terminal** button, with the terminal at the repository root. These scripts need
   no `__init__.py` and can import shared code from `tools`. For runnable package
   modules, use
   **Terminal → Run Task → Project: Run Python module** and enter the module's
   name, such as `tools.simulation`. For notebooks in `notebooks/`,
   select `.venv` under **Select Kernel** and import reusable code from `tools`,
   then run cells; notebook formatting on save is not enabled. Run **Terminal →
   Run Task → Project: Run checks** before uploading.
   An `import` statement uses a package; it does not install one. Already-declared
   packages are installed automatically. For a new external package, run **Terminal
   → Run Task → Project: Add Python package**, enter one distribution name, then
   include **both `pyproject.toml` and `uv.lock`** in your commit. For example,
   `import sklearn` needs distribution `scikit-learn`. Do not use `pip install`
   for shared dependencies or install a project-local module from PyPI. Restart
   notebook kernels after package changes. Keep generated output in `results/`;
   it is ignored, while data and notebooks are not broadly ignored. Tasks and
   VS Code notebook kernels use root-relative paths such as `data/raw/...`.
4. **Commit.** Source Control icon → review each diff → stage relevant files with
   **+** → enter a useful plain-language description → **Commit**. If checks fail,
   read the message, fix/Save, review and stage again, then retry; ask the maintainer
   if unsure.
5. **Upload.** Choose **Publish Branch** on the first upload, or **… → Push** later.
   **Commit is local. Push uploads. Neither merges into `main`.**
6. **Finish.** On GitHub, open **Pull requests → New pull request**, with base
   `main` and your branch as compare. Add a short title and explain the change
   and how you checked it. Wait for the green **Quality** check, request teammate
   review, then **Squash and merge** when approved.
   If CI fails or GitHub reports a conflict, contact the maintainer.
7. **Next task.** Switch to `main` and **Pull** again; create the next task branch.
   Dependencies sync automatically after branch switches and pulls that update
   files. Restart an open notebook kernel if libraries changed.

**Working on someone else's branch:** First commit and push, or otherwise safely
save, your own branch's work. Uncommitted changes can follow you across branches;
do not switch while unsure. Use **Source Control → … → Fetch**, then the branch
picker to select their remote branch, and **Pull before editing**. Work there only
with the owner's agreement. If testing/reviewing, do not push. If sharing the branch,
coordinate file ownership, Pull before editing and again before Push if others
contributed. Stop and ask for help on conflicts. Never force-push. Prefer separate
branches/PRs when simultaneous editing is common.

**If something goes wrong:** Commit blocked → read its message. New external import
missing → **Add Python package** task; check `.venv` first. Behind remote → **Pull**
before **Push**. Sync failed → **Sync Python environment** task. Merge conflict or
an unresolved error → stop and ask the maintainer.

## Spyder and PyCharm daily workflow

Complete [your editor's setup](CONTRIBUTOR_SETUP.md#7-use-spyder-or-pycharm) once
per clone. Open the same repo root in your IDE and Git GUI. Work on a task branch;
the `src/tools/`, personal-folder, data, and generated-output rules above apply
in every editor. `.vscode` settings do not configure Spyder or PyCharm.

### Run code and manage packages

Use the clone's `.venv` interpreter and the repo root as the working directory:

| Action | Spyder | PyCharm |
| --- | --- | --- |
| Run a `.py` script | Open file → **Run / F5**; set root in **Run → Configuration per file** | Right-click file → **Run**; set root and project interpreter in **Run → Edit Configurations** |
| Run an interactive cell | **Run cell** for `# %%` cells in `.py` files | Use the Python Console or supported notebook/cell runner; select the project interpreter |
| Pick/check Python | **Preferences → Python interpreter**, then restart the kernel | Project **Python Interpreter** settings; check run configurations and Python Console too |
| After changing packages or branches | Restart the IPython kernel before running again | Restart Python Console and any notebook kernels; rerun scripts in a fresh process |

For a process that should start cleanly each time, the terminal script/module
commands below work in either editor. Spyder keeps a live console: old variables
and imports can otherwise outlast a run or branch change. Save files before
running terminal commands, and reload them if the IDE reports an external edit.

The **Project:** task names in the VS Code instructions have these equivalents.
Run commands in PyCharm's Terminal pane or a system terminal **at the repo root**,
not in Spyder's IPython Console. Activation is not required.

| VS Code task / action | Command in another editor |
| --- | --- |
| First-time setup | `uv run --no-project --python 3.12 maintenance/bootstrap.py` |
| Sync Python environment | `uv sync --locked` |
| Add Python package | `uv add -- scikit-learn` (example; replace with the requested distribution) |
| Run Python module | `uv run --locked python -m tools.simulation` (after creating that module) |
| Run checks | `uv run --locked python maintenance/run_checks.py` |
| Run a standalone script | `uv run --locked python scripts/personal/colin/example.py` (a working example that writes ignored plots/results) |

Add a new shared dependency with **uv add**, not the IDE's package browser,
`pip install`, Conda, or Spyder's automatic kernel installer. Review and commit
**both `pyproject.toml` and `uv.lock`**. An `import` uses an installed package;
`from tools...` imports this repo's editable scientific package and needs no new
PyPI dependency. Setup already includes the scientific libraries listed in the
[README](../../README.md#scientific-packages), plus development tools and Spyder
6.1 console support. A newer Spyder release requesting another kernel range
needs a coordinated lock update rather than a local workaround.

After **every pull/branch switch**, wait for the environment-sync hook. If the
GUI does not show **Environment ready**, run `uv sync --locked` before running
code. If sync fails, the Git operation may already have completed: check the
current branch and keep the error message. Restart live consoles after sync.
Do not resolve an environment error by recloning over your work or bypassing hooks.

### Format shared files in any editor

VS Code's Save automation is not inherited by other IDEs. Configure Ruff as in
the setup guide, or use these commands after saving and **before selecting files
for a commit**. Replace the quoted example path with each shared file you edited:

```sh
uv run --locked ruff check --select I --fix -- "src/tools/your_module.py"
uv run --locked ruff format -- "src/tools/your_module.py"
uv run --locked python maintenance/run_checks.py
```

The first command sorts imports; the second formats code. The last command
checks the full project and reports other lint/test failures to fix. Inspect
the diff after formatting. These commands respect the shared Ruff configuration
and exclude `scripts/personal/`; personal experiments do not require formatting.
Do not run another automatic formatter or import-removal tool alongside Ruff.
Editor-only inspections may report additional suggestions (including unused
imports allowed here); the repo's checks determine the shared requirements.

### PyCharm Git controls

1. **Start:** in **Commit**, check for unfinished work and save/commit it on its
   existing branch first. From the branch widget, select local **main → Checkout**,
   then **Git → Pull**, selecting `origin` and `main`. Stop on conflicts or if the
   GUI proposes discarding changes; ask the maintainer instead.
2. **Branch:** branch widget → **New Branch** → name it `feat/your-task` or
   `fix/your-task` and check it out. Confirm the widget shows that task branch.
3. **Prepare:** Save, format shared files, and run checks. Open **Commit**, select
   the intended files, and review each diff. PyCharm normally uses selection
   checkboxes/changelists; a separate staging area is optional. Include both
   dependency files when you added a package. Keep `.idea/`, `.venv`, outputs,
   and credentials out of the commit.
4. **Commit:** enter a message, keep **Run Git hooks** enabled in the commit
   options, and choose **Commit**. This repo's **Ruff lint** and **Ruff format**
   checks must pass for shared Python edits. Leave overlapping IDE **Reformat
   code** and **Optimize imports** commit actions off; format with Ruff first.
   If a hook fails, fix the files, review/reselect them, and commit again.
5. **Upload:** **Git → Push**. Check the task branch and destination `origin`;
   create/set its upstream when first prompted. Pushing does not merge the PR.
6. **PR:** open GitHub in a browser → **Pull requests → New pull request**, base
   `main`, compare your branch. Wait for green **Quality** and teammate approval,
   then **Squash and merge**. Return to `main`, Pull, and branch for the next task.

To review a teammate's branch, first save your own work, then **Git → Fetch** and
choose their branch under `origin` in the branch widget; check it out and Pull.
The permissions and coordination rules above still apply. Do not force-push or
use **Amend** to rewrite already-shared commits.
[Branch controls](https://www.jetbrains.com/help/pycharm/manage-branches.html),
[commit, staging, and push](https://www.jetbrains.com/help/pycharm/commit-and-push-changes.html).

### Spyder with GitHub Desktop (macOS/Windows)

Use Desktop for Git and Spyder for code; both must open the same clone. Spyder's
context-menu Git integration is optional and does not replace this full workflow.
Keep Desktop's [hook settings](CONTRIBUTOR_SETUP.md#enable-the-git-gui-hooks-both-routes)
enabled. A checkbox in Desktop selects a change for the next commit; no VS Code
staging button is required.

1. **Start:** select the correct **Current Repository**. Inspect **Changes** for
   unfinished work. Commit/push your current task on its existing branch before
   switching. **Current Branch → main**, then **Fetch origin** and **Pull origin**
   if offered. Fetch alone does not update your local files.
2. **Branch:** **Current Branch → New Branch**, enter a task name, and create it
   from the updated `main`. If asked about moving uncommitted work between
   branches, stop and resolve that work deliberately before continuing.
3. **Prepare:** edit and Save in Spyder, format shared files, and run checks from
   the repo-root system terminal. Return to Desktop → **Changes**. Review diffs
   and check only the files/lines intended for this task.
4. **Commit:** enter a Summary and choose **Commit to your-task-branch**. Confirm
   **Ruff lint** and **Ruff format** pass for shared Python files. Do not select
   **Skip hooks** or **Bypass** when checks fail; fix, Save, review, and retry.
5. **Upload:** **Publish branch** on the first upload, then **Push origin** for
   later commits. On GitHub create the PR with base `main`, wait for green
   **Quality**, request review, and **Squash and merge** after approval. Desktop's
   **Create Pull Request** can open the browser for this step.
6. **Next task:** switch to `main`, Fetch/Pull, sync if no hook success is shown,
   restart Spyder's kernel, then make the next branch. If asked about deleting a
   branch, first confirm its PR was merged and its work is safely on GitHub.

For a teammate's branch, save your work first, **Fetch origin**, select their
branch in **Current Branch**, and Pull. Coordinate before editing/pushing there.
[Desktop branch synchronization](https://docs.github.com/en/desktop/working-with-your-remote-repository-on-github-or-github-enterprise/syncing-your-branch-in-github-desktop),
[hooks and visible output](https://docs.github.com/en/desktop/making-changes-in-a-branch/working-with-git-hooks-in-github-desktop).

### Spyder on Linux: Git GUI and terminal

GitHub Desktop's official installers target macOS/Windows. On Linux, install
`git-gui` and `gitk` using your distribution's package manager. From a repo-root
terminal, `git gui` opens the commit UI; Spyder's project/file context menu can
also invoke Git commit/history when these programs are on PATH.

For an explicit pull-and-branch sequence, first save/commit your current work,
then run these **one at a time**, checking for errors between commands:

```sh
git status
git switch main
git pull --ff-only
git switch -c feat/your-task
uv sync --locked
git gui
```

`git status` must show no unfinished changes before switching. Replace the example
branch name for each task. In Git GUI: **Rescan**, select/review your changed files,
**Commit → Stage to Commit**, enter a message, then **Commit**. Leave commit-hook
verification enabled. If a hook rejects the commit, format/fix and Save, Rescan,
review, stage again, and retry. For the first upload run
`git push -u origin HEAD` while on your task branch; later use **Remote → Push**
or `git push`. Close Git GUI first, or use a second repo-root terminal, if the
terminal that launched the GUI is still waiting. Create/review the PR on GitHub
as above. A failed fast-forward pull needs help rather than a force-push/reset.
[Git GUI](https://git-scm.com/docs/git-gui),
[Spyder version control](https://docs.spyder-ide.org/current/panes/projects.html#working-with-version-control).

### Troubleshooting other IDEs

| Symptom | Check and recovery |
| --- | --- |
| Scientific imports fail | Run the setup guide's `setup_check.py` with the IDE Run button. Select the clone's actual Python executable in `.venv`, then restart the console/kernel. Run `uv sync --locked` if dependencies are missing. |
| Spyder reports missing/incompatible `spyder-kernels` | Use supported Spyder 6.1.x, sync, select `.venv`, and restart the kernel. A different requested range needs a maintainer-reviewed lock change; do not accept an automatic install into `.venv`. |
| `tools` cannot be imported | Confirm setup succeeded and this clone's `.venv` is selected. Sync reinstalls the editable package. Avoid `sys.path` edits or installing a similarly named package from PyPI. |
| Data file not found or results appear in the wrong folder | Set the run configuration's working directory to the repo root. Check `Path.cwd()` in the running script/console. |
| Save does not match the repo's formatting | Configure Ruff, or use the two targeted formatting commands above. Spyder/PyCharm's other formatter settings do not come from `.vscode`. |
| GUI commit reports `uv not found` or cannot launch Python | Restart the Git GUI/IDE and check hook settings. Verify `uv --version` in a system terminal and rerun setup there if a clone was moved. A successful IDE Python run does not verify the GUI's hook environment. Keep the hook output and ask the maintainer if it persists. |
| GUI commit succeeds but shared Python hooks never appear | Confirm setup ran in this clone, hooks were not skipped, and the GUI is using this same repository. Stop before Push and ask the maintainer to check the hook configuration. |
| Packages disappear after a switch/Pull | Sync, restart consoles, and check dependency files. Shared packages must be declared and locked; local ad hoc installs are not preserved. Spyder 6.1 kernel support is already declared. |
| IDE settings are listed as changes | `.idea/` and `.spyproject/` should be ignored. Do not force-add them; share unexpected tracked settings with the maintainer. |
| Merge conflict, failed Pull, or unknown error | Keep the message and ask the maintainer. Avoid **Discard**, **Reset**, force-push, or bypassing checks as a shortcut. |
