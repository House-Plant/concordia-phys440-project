# Daily use

Once per clone: follow [setup](CONTRIBUTOR_SETUP.md). Use VS Code with this
repository open. Save → Stage → Commit → Push → Open PR is the normal cycle.
Put reusable scientific code in `src/tools/`, standalone analysis/simulation
scripts in `scripts/`, and informal investigations in `scripts/testing/`.
Use `notebooks/` for interactive exploration, `data/` for inputs, `tests/` for
automated scientific checks, and `reports/` for your write-up. Repository automation
lives in `maintenance/`; see the [directory map](../../README.md#where-to-work).

For a personal workspace, use your named folder under `scripts/personal/`.
Put scripts in its `testing/` folder and datasets in its `data/` folder. Stage,
commit, and push these files to save and share them through Git. Put plots and
other generated files in `figures/` and `outputs/`; their contents are ignored.
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
3. **Work.** Edit and **Save** Python files; Ruff formats and organizes imports.
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
