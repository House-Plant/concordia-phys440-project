# First-time contributor setup

Allow 5–10 minutes to read this guide, plus download time. Repeat it on each
computer or new clone. Project settings, hooks, and packages stay local to this
repository. Installing standard applications and editor extensions is the exception.

## 1. Install the applications for your system

| System | Git | VS Code | uv |
| --- | --- | --- | --- |
| Windows | [Git for Windows](https://git-scm.com/downloads/win) | [Windows setup](https://code.visualstudio.com/docs/setup/windows) | [uv installer: Windows PowerShell instructions](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) |
| macOS | [Git for macOS](https://git-scm.com/downloads/mac) | [macOS setup](https://code.visualstudio.com/docs/setup/mac) | [uv installer: macOS instructions](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) |
| Linux | [Git for Linux](https://git-scm.com/downloads/linux) | [Linux setup](https://code.visualstudio.com/docs/setup/linux) | [uv installer: Linux instructions](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) |

Follow your system's installation instructions. Use uv 0.11.19 or newer. Close
and reopen VS Code after installation so it can find Git and uv. You do not need
to install Python packages globally; uv finds or downloads Python 3.12 for you.
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

3. Open the Command Palette → **Python: Select Interpreter**. Choose the Python
   inside this folder's `.venv`. If it is missing, use **Enter interpreter path**:
   `.venv\Scripts\python.exe` on Windows, `.venv/bin/python` on macOS/Linux.
4. Choose **Terminal → Run Task → Project: Run checks**. Success ends with
   **All project checks passed.** This verifies Python, tool imports, formatting,
   and the fast tests.
5. Confirm **Ruff formatting on Save** once: create a temporary `.py` file at the
   repository root (outside `scripts/personal/`) containing `x=1`,
   then **Save**. It should become `x = 1`. Remove this temporary file afterward.
   If it stays unchanged, check that Ruff is enabled and this workspace is trusted.

If Git later asks for your name/email at your first commit, use **Terminal → New
Terminal** for this one-time repository-local configuration. Replace the values
with your name and your GitHub email (a GitHub no-reply email is fine):

```text
git config --local user.name "Your Name"
git config --local user.email "YOUR_GITHUB_EMAIL"
```

These settings affect only this clone. Existing Git identity settings are preserved
by setup. Ask the maintainer for help if you are unsure which email to use.

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
already declared in `pyproject.toml`, including NumPy.
Before the first notebook, run **Project: Add Python package**, enter `ipykernel`,
and include the resulting dependency files in your PR. If already declared, it
is installed by setup and does not need adding again. No Jupyter server package
or global kernel registration is required.

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
| Download or sync fails | Reconnect, then run **Project: Sync Python environment**. Share persistent lock/version errors with the maintainer. |
| Hook installation fails or `core.hooksPath` is configured | Share the full message with the maintainer. Setup leaves existing hook configuration alone. |
| Commit cannot find `uv` after setup | Restart VS Code so its Git process inherits the updated application path. |

Keep the error text and ask the maintainer. Do not try global `pip install` or
force-pushing as a repair. You may safely repeat **Project: First-time setup**.
Next: [Daily use](CONTRIBUTOR_DAILY_USE.md).
