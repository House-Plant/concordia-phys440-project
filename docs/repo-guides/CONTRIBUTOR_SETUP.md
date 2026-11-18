# First-time contributor setup

Read the route for your editor; allow 10–15 minutes plus download time. Repeat it
on each computer or new clone. Project settings, hooks, and packages stay local to this
repository. Installing standard applications and editor extensions is the exception.

Choose one route; VS Code is not required:

| Your editor | Follow these steps |
| --- | --- |
| VS Code | Sections 1–6 below |
| Spyder 6.1.x | Install Git and uv from section 1, then [Spyder/PyCharm setup](#7-use-spyder-or-pycharm) |
| PyCharm | Install Git and uv from section 1, then [Spyder/PyCharm setup](#7-use-spyder-or-pycharm) |

All routes use the same Python 3.12 `.venv`, shared packages, commit hooks, and
GitHub review process. `.vscode` settings and **Project:** tasks apply only in
VS Code; other editors use the equivalent commands listed in this guide.

## 1. Install the applications for your system

| System | Git | VS Code | uv |
| --- | --- | --- | --- |
| Windows | [Git for Windows](https://git-scm.com/downloads/win) | [Windows setup](https://code.visualstudio.com/docs/setup/windows) | [uv installer: Windows PowerShell instructions](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) |
| macOS | [Git for macOS](https://git-scm.com/downloads/mac) | [macOS setup](https://code.visualstudio.com/docs/setup/mac) | [uv installer: macOS instructions](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) |
| Linux | [Git for Linux](https://git-scm.com/downloads/linux) | [Linux setup](https://code.visualstudio.com/docs/setup/linux) | [uv installer: Linux instructions](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) |

The VS Code download column is optional for the Spyder/PyCharm routes.
Follow your system's installation instructions. Use uv 0.11.19 or newer. Close
and reopen your IDE, Git GUI, and terminal after installation so they can find
Git and uv. You do not need to install Python packages globally; uv finds or
downloads Python 3.12 for you.
The first setup needs an internet connection.

## 2. Clone and open this repository

1. Sign in to your GitHub account in your browser. Ask the maintainer for access
   if this is a private repository.
2. Open VS Code. Open the Command Palette with **Ctrl+Shift+P** (Windows/Linux)
   or **Cmd+Shift+P** (macOS). Choose **Git: Clone** (or **Clone Repository** in
   Source Control).
3. Paste `https://github.com/House-Plant/concordia-phys440-project.git`.
   Pick a local parent folder. Complete GitHub sign-in when requested.
4. Choose **Open** when cloning finishes. Open the folder that contains
   `pyproject.toml` and `.vscode`, not its parent. Trust the workspace after
   confirming that it is this repository. If several repositories appear in
   Source Control, select **concordia-phys440-project** before any Git action.

## 3. Set up Python and Ruff in VS Code (once)

1. Open **Extensions** from the left sidebar. Install **Python** by Microsoft
   (`ms-python.python`) if it is not already installed.
2. Find and install **Ruff** (`charliermarsh.ruff`). It is also listed under the
   workspace's recommended extensions. This provides lint highlighting,
   formatting, and import sorting in the editor.
3. To keep a newly installed Ruff extension active only for this repository,
   open its gear menu → **Disable** (globally), then reopen the menu →
   **Enable (Workspace)**. Restart extensions if VS Code prompts you.
   If you already use Ruff in other projects, keep your existing enablement if
   you prefer. [VS Code extension controls](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace#_disable-an-extension).
4. Install **Jupyter** by Microsoft (`ms-toolsai.jupyter`) only if you use notebooks.

The setup task below installs the Ruff command-line tool into this repository's
`.venv`. It does **not** install or enable the VS Code extension. Complete the
editor steps above once; no formatter commands are needed during normal editing.

## 4. Run the one-time setup task

1. Choose **Terminal → Run Task → Project: First-time setup**.
2. Wait for this exact message:

   > Setup complete: .venv ready; commit and branch/pull hooks installed.

3. Open a Python file. VS Code should discover this folder's `.venv` after setup.
   Confirm it with the Command Palette → **Python: Select Interpreter**. If needed,
   choose the discovered `.venv` environment, or use **Enter interpreter path**:
   `.venv\Scripts\python.exe` on Windows, `.venv/bin/python` on macOS/Linux.
   When entering a path, select the Python executable, not the `.venv` folder.
4. Choose **Terminal → Run Task → Project: Run checks**. Success ends with
   **All project checks passed.** This verifies the installed environment, tool
   imports, formatting, and the fast tests. It does not verify VS Code's selected
   interpreter; the task runs the project's Python directly.
   NumPy, Matplotlib, SciPy, pandas, SymPy, Seaborn, and MOCAT-pySSEM are installed by setup;
   see the [package imports](../../README.md#scientific-packages). You do not need
   to add them individually. For an existing clone, **Project: Sync Python
   environment** installs newly declared packages.
   Verify the editor separately: open a runnable Python script and choose
   **Run Python File in Terminal**. The terminal command must use
   `.venv/bin/python` on macOS/Linux or `.venv\Scripts\python.exe` on Windows.
   Close and reopen this workspace and repeat; the environment should remain
   usable without selecting it again.
5. Confirm **Ruff formatting on Save** once: create a temporary `.py` file at the
   repository root (outside `scripts/personal/`) containing `x=1`,
   then **Save**. It should become `x = 1`. Remove this temporary file afterward.
   If it stays unchanged, check that Ruff is enabled and this workspace is trusted.

### Git identity (all editors)

If Git later asks for your name/email at your first commit, use **Terminal → New
Terminal** for this one-time repository-local configuration. Replace the values
with your name and your GitHub email (a GitHub no-reply email is fine):

```text
git config --local user.name "Your Name"
git config --local user.email "YOUR_GITHUB_EMAIL"
```

These settings affect only this clone. Existing Git identity settings are preserved
by setup. In other IDEs, use their Terminal pane or your system terminal at the
repository root. Ask the maintainer for help if you are unsure which email to use.

## 5. Run standalone scripts

Put scripts for simulations, data analysis, and generating figures in `scripts/`.
Use `scripts/testing/` for informal investigations that you run and inspect
yourself. Open a script, select this project's `.venv`, then choose **Run Python
File in Terminal**. Keep the terminal at the repository root so paths such as
`data/raw/...` and `results/...` work. For example, you can run the existing
`scripts/personal/colin/linting-test-1.py` this way.

For your own space, use your named folder under `scripts/personal/`.
Put scripts directly in your personal folder and datasets in its `data/` folder;
both can be committed and shared. `figures/` and `outputs/` hold local files ignored by Git. Follow the
[personal-folder instructions](../../scripts/personal/README.md).
Ruff linting, formatting, and import sorting are disabled throughout
`scripts/personal/`; your personal files can be committed without Ruff checks.

These directories need no `__init__.py`. Scripts can import reusable tools from
`src/tools/`, such as `from tools import analysis` after creating
`src/tools/analysis.py`. Automated scientific checks with pass/fail assertions
belong in `tests/`; see the [repository map](../../README.md#where-to-work).

## 6. If you use notebooks

Put notebooks in `notebooks/`. Scientific Python modules belong in `src/tools/`;
see the [repository map](../../README.md#where-to-work). Setup installs the dependencies
already declared in `pyproject.toml`; see the
[scientific package list](../../README.md#scientific-packages).
Setup also installs the locked development tools, including `spyder-kernels`
and its `ipykernel` dependency for consoles/notebooks. Existing contributors should
sync once to obtain them. No global kernel registration is required for VS Code.

Open an `.ipynb` file → **Select Kernel** (top right) → **Python Environments** →
this project's `.venv`. Use **Restart** in the notebook toolbar after dependency
updates or a branch/pull that changes libraries. Notebook formatting on save is
not enabled; checks still cover Python notebook cells. Setup installs this project
as the editable package `tools`, so notebooks can import its modules directly.
For example, after adding `src/tools/analysis.py`, use `from tools import analysis`.
The workspace starts notebook kernels at the repository root, so paths such as
`data/raw/measurements.csv` and `results/figure.png` work from VS Code notebooks.
Notebooks launched in another editor/server may use a different working directory.
Source edits do not need reinstalling. First-time setup/sync installs the package
automatically. Run a runnable module with **Project: Run Python module** and enter
its import name, such as `tools.simulation`, after creating that module.

## If setup does not work

| Message or symptom | What to do |
| --- | --- |
| `uv not found`, or task cannot launch `uv` | Install uv using the link above; fully quit and reopen VS Code. Rerun setup. |
| Ruff/Python commands missing | Complete section 3; confirm Ruff is enabled for this workspace. Restart extensions if prompted. |
| Saving leaves `x=1` unchanged | This is expected under `scripts/personal/`. Elsewhere, open a saved `.py` file in this trusted repository, enable Ruff for this workspace, and Save explicitly. Ask the maintainer if it still does not format. |
| Imports fail in the editor/notebook | Select this repo's `.venv` interpreter/kernel; restart the kernel. |
| Run reports `permission denied` for `.venv`, or its command starts with the `.venv` folder | Pull the latest repo settings, then use **Developer: Reload Window**. If necessary, select the Python executable from step 4.3; the environment folder itself cannot be run. |
| Download or sync fails | Reconnect, then run **Project: Sync Python environment**. Share persistent lock/version errors with the maintainer. |
| Hook installation fails or `core.hooksPath` is configured | Share the full message with the maintainer. Setup leaves existing hook configuration alone. |
| Commit cannot find `uv` after setup | Restart VS Code so its Git process inherits the updated application path. |

Keep the error text and ask the maintainer. Do not try global `pip install` or
force-pushing as a repair. You may safely repeat **Project: First-time setup**.
Next: [Daily use](CONTRIBUTOR_DAILY_USE.md).

## 7. Use Spyder or PyCharm

### Install your editor and clone the repo

Install Git and uv from section 1 first. Then choose one editor:

- **Spyder:** install the standalone **Spyder 6.1.x** application from the
  [official downloads](https://www.spyder-ide.org/download/). The kernel requirement
  was checked against version 6.1.8's published package metadata. Its console package,
  `spyder-kernels>=3.1.6,<3.2`, is locked in this repo's development dependencies.
  Spyder runs as a separate application; setup installs only its console support
  in `.venv`. Existing Anaconda users can keep their Spyder application and select
  this repo's `.venv` for code execution. A different Spyder release that requests
  another kernel version needs a maintainer-reviewed dependency update; do not
  accept an automatic package replacement or install packages with Conda into
  `.venv`. [Spyder environment guidance](https://docs.spyder-ide.org/current/faq.html).
- **PyCharm:** install a current release from
  [JetBrains](https://www.jetbrains.com/pycharm/download/). Python and Git support
  are built in. On the Welcome screen choose **Clone Repository / Get from VCS**,
  or **Git → Clone** in an open project. Select Git as the version-control system
  and use the URL below. Open the resulting project; defer prompts to create a
  Python environment until after the shared setup below. If the clone already
  exists, choose **Open** instead of cloning it again.

Repository URL:

```text
https://github.com/House-Plant/concordia-phys440-project.git
```

Sign in to GitHub when the cloning tool asks. For a private repo, accept the
maintainer's invitation first. If authentication/access fails, keep that message
and ask for help; creating another empty repository will not fix access.

Spyder has basic Git actions, rather than a complete branch/pull/push interface.
On **macOS/Windows**, install [GitHub Desktop](https://desktop.github.com/), sign
in, and choose **File → Clone Repository → URL** with the URL above. For an
existing clone use **File → Add Local Repository**. Desktop and Spyder must point
to the **same folder**, not two separate clones. On **Linux**, use the system
terminal to clone, then use Git GUI as described in
[daily use](CONTRIBUTOR_DAILY_USE.md#spyder-on-linux-git-gui-and-terminal).

```sh
git clone https://github.com/House-Plant/concordia-phys440-project.git
cd concordia-phys440-project
```

For every route, the repo root is the folder containing `pyproject.toml`, `uv.lock`,
and `maintenance/`. Do not choose its parent or use **New Repository / git init**
inside the clone. [Spyder's Git integration](https://docs.spyder-ide.org/current/panes/projects.html#working-with-version-control),
[Desktop cloning](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop).

### Run the shared setup (both editors)

1. Open PyCharm's **Terminal** pane, or a system terminal (PowerShell on Windows;
   Terminal on macOS/Linux). Spyder's **IPython Console** runs Python code; it is
   not the terminal for these shell commands.
2. Change into the cloned repo root. You can type `cd `, drag the folder from
   your file manager into the terminal, and press Enter. If typing the path,
   put it in quotes when it contains spaces. Run these one at a time:

   ```sh
   git rev-parse --show-toplevel
   uv --version
   uv run --no-project --python 3.12 maintenance/bootstrap.py
   ```

   The first command must show this clone's root; uv must be 0.11.19 or newer.
   Wait for **Setup complete: .venv ready; commit and branch/pull hooks installed.**
   Save the **IDE Python interpreter** path printed underneath it. It points to
   an executable, not just an environment folder. Setup can be repeated safely.
3. Run:

   ```sh
   uv run --locked python maintenance/run_checks.py
   ```

   Wait for **All project checks passed.** This confirms the packages and
   repository checks. It does not check your IDE's interpreter or Git GUI settings.
4. Complete the editor instructions below and the
   [run/reopen check](#verify-the-ide-after-setup). If Git needs an author name or
   email, use [Git identity](#git-identity-all-editors).

No environment activation command is needed for these `uv` commands. Use uv for
package changes; do not use an IDE package-install button or create a second
Conda/virtualenv environment for this project.

### Spyder: interpreter, working directory, and formatting

**Spyder 6.1 uses a global default interpreter, not one saved per project.**
Select this clone's Python once; that preference normally survives restarting
Spyder if the executable still exists. Opening another project does not
automatically select that project's `.venv`. If you change the default for
another project, select this clone's interpreter again when returning and restart
the kernel. A Git branch switch within this clone keeps the same `.venv` path;
wait for sync and restart the kernel to load its updated packages.
[Spyder's project-interpreter tracking issue](https://github.com/spyder-ide/spyder/issues/11362).

1. Choose **Projects → New Project → Existing directory** and select the repo
   root. This creates local Spyder project settings; it does not create another
   Git repository. Later, use **Projects → Open Project** to return to it.
2. Open **Preferences → Python interpreter** (under **Tools** on Windows/Linux,
   or the application menu on macOS). Select **Use the following Python
   interpreter** and browse to the path printed by setup:

   | System | Executable inside this clone |
   | --- | --- |
   | Windows | `.venv\Scripts\python.exe` |
   | macOS/Linux | `.venv/bin/python` |

   Apply the change, then choose **Consoles → Restart kernel** or open a new
   IPython console. The standalone installer's own Python and Anaconda `base`
   will not use this repo's packages. Recheck the interpreter when changing
   projects. [Interpreter instructions](https://docs.spyder-ide.org/current/faq.html).
3. Open a script and choose **Run → Configuration per file**. For the IPython
   Console runner, choose the repo root as its working directory, rather than
   the script's directory. Save the configuration. **Run → Run** / **F5** runs
   the file; **Run cell** runs a `# %%` cell. Restart the kernel after dependency
   updates to discard already-imported library versions.
   [Projects](https://docs.spyder-ide.org/current/panes/projects.html),
   [run configuration](https://docs.spyder-ide.org/current/panes/editor.html#run-configuration).
4. No VS Code extension is needed. Spyder's editor tools and the project's
   execution environment are separate. If **Preferences → Completion and
   linting → Code formatting** offers Ruff, it can be used, but verify the
   result with the repo's checks. Keep other automatic formatters off for this
   project. The reliable, version-independent route is to Save and run the
   [two Ruff commands](CONTRIBUTOR_DAILY_USE.md#format-shared-files-in-any-editor)
   before committing shared files. Installing Ruff in `.venv` alone does not
   configure Spyder's formatter or language server.

Spyder's `.py` cells are not `.ipynb` notebooks. For `.ipynb` files use the VS Code
notebook route in section 6 or PyCharm's notebook support if available in your
installation, selecting the same `.venv` kernel. No Spyder notebook plugin is
required for this project's scripts.

### PyCharm: interpreter, working directory, and formatting

1. Open the cloned root as a project. In **Settings**, search for **Python
   Interpreter** (the location is **Python → Interpreter** or **Project → Python
   Interpreter**, depending on version). Choose **Add Interpreter → Add Local
   Interpreter → Existing**, and browse to `.venv\Scripts\python.exe` on Windows
   or `.venv/bin/python` on macOS/Linux. Select it as this project's interpreter.
   If the dialog offers an existing uv environment, select this same `.venv`;
   do not generate another environment or initialize another project.
   [Interpreter setup](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html),
   [existing uv environments](https://www.jetbrains.com/help/pycharm/uv.html).
2. Right-click a script → **Run**. In **Run → Edit Configurations**, choose that
   Python configuration, select the project interpreter, and set **Working
   directory** to the repo root. Set this in the **Python configuration template**
   too for future scripts; existing configurations need updating individually.
   Use the same interpreter in the **Python Console**, and restart that console
   after package updates. [Run settings](https://www.jetbrains.com/help/pycharm/run-debug-configuration-python.html).
3. Current PyCharm includes Ruff support. In **Settings**, search for **Ruff**;
   recent releases place it under **Python → Tools → External Tools**. Enable
   Ruff and use **Env**, meaning Ruff from this project's interpreter, rather
   than downloading a different version through `uvx` or a global install.
   Enable its **Formatting** and **Sort imports when formatting** options.
   Use Ruff's code fixes on save for import sorting, and the IDE's reformat-on-save
   action with Ruff formatting enabled if you want save automation. Disable
   overlapping Black/autopep8 and PyCharm's own import optimization/reformatting
   commit actions. The shared rules and exclusions come from `pyproject.toml`.
   [Current Ruff integration](https://www.jetbrains.com/help/pycharm/lsp-tools.html#ruff).
4. If your release lacks built-in Ruff support, the
   [Ruff plugin](https://plugins.jetbrains.com/plugin/20574-ruff) is an option;
   do not install a second Ruff integration alongside the built-in one. Select
   the project Ruff executable (`.venv/bin/ruff` or `.venv\Scripts\ruff.exe`).
   The [terminal formatting commands](CONTRIBUTOR_DAILY_USE.md#format-shared-files-in-any-editor)
   work with either version. Prove formatting on a temporary root-level `.py`
   file containing `x=1`: reformat/save should produce `x = 1`. Remove it afterward.
5. For notebooks, open an `.ipynb` under `notebooks/` and use the notebook toolbar
   to choose/configure an **IDE-managed server** with the project's `.venv`
   interpreter/kernel. Current PyCharm can use the installed IPyKernel directly.
   In a cell, check `sys.executable` and `Path.cwd()` as below; the working directory
   should be the repo root. Older releases that ask to install a server package
   need a maintainer-reviewed uv dependency addition, or use the VS Code notebook
   route. [Managed notebook execution](https://www.jetbrains.com/help/pycharm/configuring-jupyter-notebook.html).

If enabling automatic formatting in either editor, also save a temporary file
containing `x=1` in **your own** `scripts/personal/<name>/` folder: the repo's
personal-folder exclusion should leave it unchanged. Remove it afterward. If the
integration ignores that exclusion, leave automatic formatting/import actions off
and use the targeted terminal commands, which honor the shared configuration.

Do not mark extra folders as import roots to hide missing-package errors:
setup installs `tools` editably from `src/tools/`. Verify the selected interpreter
first. Keep `.idea/` and `.spyproject/` local; these IDE settings are ignored by Git.

### Enable the Git GUI hooks (both routes)

The setup script installs real Git hooks. Their formatter checks and environment
sync must also run when commits, branch switches, and pulls come from a GUI.

- **PyCharm:** in **Settings → Version Control → Git**, choose your installed
  Git executable and click **Test**. In the Commit window's options, keep
  **Run Git hooks** checked; leave **Do not run Git commit hooks** off if your
  release exposes it in Advanced Settings. IDE inspections are not a replacement
  for these hooks. [Commit options](https://www.jetbrains.com/help/pycharm/commit-and-push-changes.html).
- **GitHub Desktop:** use **3.5.5 or newer**. In **Settings** (macOS) or **File →
  Options** (Windows) → **Git → Hooks**, enable **Load Git hook environment
  variables from shell**. Keep the commit-message gear option to skip hooks
  off; do not use **Bypass** after a hook fails.
  [Hook environment settings](https://docs.github.com/en/desktop/configuring-and-customizing-github-desktop/configuring-git-for-github-desktop#configuring-your-shell-environment-for-git-hooks),
  [hook support and output](https://docs.github.com/en/desktop/making-changes-in-a-branch/working-with-git-hooks-in-github-desktop).
- **Spyder's Git context menu / Linux Git GUI:** `git gui` and `gitk` must be
  installed and available on PATH for Spyder's commit/history actions. Installing
  Spyder does not install them. Launch `git gui` from the repo-root terminal
  where `uv --version` succeeds; follow the
  [Linux workflow](CONTRIBUTOR_DAILY_USE.md#spyder-on-linux-git-gui-and-terminal).

On your first real task-branch commit of a shared Python file, inspect the GUI's
hook output for **Ruff lint** and **Ruff format**. Both must pass. Open PyCharm's
commit-check details / Git tool window's Console, or Desktop's hook-output panel,
to see the results. If a hook cannot find uv/Python, fully quit and reopen the
Git GUI/IDE after installing uv. A working Python Console does not prove the Git
process can find uv. Share persistent
errors with the maintainer; do not disable hooks to make the Commit button work.
For future branch switches/pulls, run `uv sync --locked` yourself if the GUI does
not report **Environment ready**. Restart open consoles/kernels afterward.

### Verify the IDE after setup

Create a temporary **`setup_check.py` at the repo root** with:

```python
import sys
from pathlib import Path

import matplotlib
import numpy as np

import tools

print("Python:", sys.executable)
print("Working directory:", Path.cwd())
print("Shared tools:", tools.__file__)
print("NumPy:", np.__version__, "Matplotlib:", matplotlib.__version__)
```

Run it using **Spyder F5** or **PyCharm Run**, not the terminal's `uv run` command.
The Python path must be inside this clone's `.venv`, the working directory must
be the repo root, and `tools` must come from this clone's `src/tools/`. There
should be no missing-package error. Close and reopen the project and run it again
without selecting an interpreter. Remove the temporary file afterward. For
Spyder, also confirm that its IPython Console starts successfully.

Follow [the daily-use equivalents](CONTRIBUTOR_DAILY_USE.md#spyder-and-pycharm-daily-workflow)
for formatting, packages, GUI commits, and uploads. If setup fails, check the
troubleshooting section there and keep the full error message for the maintainer.
