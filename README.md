# Concordia PHYS 440 project

Python modelling and research workspace: build reusable scientific tools, then use
them in independent scripts and notebooks for simulations, analysis, and visualization.
Python 3.12 and a repository-local `.venv` are managed with uv. Shared dependencies
live in `pyproject.toml` and `uv.lock`.

## Where to work

| Directory | Contents |
| --- | --- |
| `src/tools/` | Reusable scientific Python modules: models, solvers, analysis, and plotting helpers |
| `scripts/` | Standalone scripts for simulations, parameter sweeps, data analysis, and generating figures |
| `scripts/testing/` | Informal scripts for trying ideas or inspecting behaviour manually |
| `scripts/personal/<name>/` | Personal scripts and data you can commit, with ignored figures and outputs; [instructions](scripts/personal/README.md) |
| `notebooks/` | Exploratory notebooks; select the project's `.venv` kernel |
| `data/raw/` | Original input datasets; small, shareable data can be committed |
| `results/` | Generated outputs; ignored by Git except the empty-directory placeholder |
| `reports/` | Scientific write-up, bibliography, and selected figures/tables worth committing |
| `tests/` | Automated scientific checks with definite pass/fail results |

Add a module such as `src/tools/simulation.py` and import it with
`from tools.simulation import ...`. Setup installs `tools` into `.venv` in
editable mode, so saved source changes are available without reinstalling.
Standalone scripts in `scripts/` can import those modules too; they do not need
`__init__.py`. With `.venv` selected, open a script and choose **Run Python File in
Terminal** in VS Code. For example, the existing formatting experiment is
`scripts/personal/colin/linting-test-1.py`. From a terminal at the repository root,
you can also run it with:

```sh
uv run --locked python scripts/personal/colin/linting-test-1.py
```

Use `scripts/testing/` for "run this and inspect the plot"; use `tests/` for
"automatically verify this answer is correct." Scripts and experiments are covered
by Ruff, but are not automatically executed by **Project: Run checks** or CI.
Shared functions that other scripts need belong in `src/tools/`.

Personal experimentation folders are provided under `scripts/personal/` for
`colin`, `naomi`, `sabrina`, `jaeden`, and `eshaal`.
Keep scripts in your `testing/` folder and datasets in your `data/` folder;
both can be committed and shared. Your `figures/` and `outputs/` contents stay
local and are ignored by Git. Coordinate before editing another person's folder.

Once a runnable package module exists, use **Terminal → Run Task → Project: Run
Python module** and enter `tools.simulation`. Notebooks belong in `notebooks/`;
the installed package works there too. Open the repository root in VS Code and
run scripts from a terminal at that root. Tasks and VS Code notebook kernels
start there too, so data/output paths are `data/raw/...` and `results/...`.
If using another launcher or an existing terminal, check its working directory.

## Repository infrastructure

All setup/check/synchronization scripts and their tests live under `maintenance/`
and `maintenance/tests/`. The scientific directories above contain no repository
automation or workflow tests. `docs/` holds repository user guides; scientific
reports belong in `reports/`. `.github/` and `.vscode/` hold platform integration
files. Shared Python, Git, and dependency configuration stays at the root.

Empty content directories use `.gitkeep` placeholders so they appear in a clone.
Remove a placeholder once its directory contains tracked project files.
`results/` and personal figure/output folders stay ignored for generated or
local files. For large or private data, agree on storage and ignore rules before
adding it to Git.

## Guides and setup

- [First-time contributor setup](docs/repo-guides/CONTRIBUTOR_SETUP.md)
- [Daily use: editing, notebooks, packages, branches, and PRs](docs/repo-guides/CONTRIBUTOR_DAILY_USE.md)
- [Maintainer setup and upkeep](docs/repo-guides/MAINTAINER_SETUP.md)

Follow [contributor setup](docs/repo-guides/CONTRIBUTOR_SETUP.md), including the one-time Ruff
extension setup. Then run **Terminal → Run Task → Project: First-time setup**.
Then use **Save → Stage → Commit → Push → Open PR** on a task branch.

The workflow implementation brief is kept under
[docs/maintenance/](docs/maintenance/CODEX_REPO_WORKFLOW_SETUP.md).
Use the contributor and maintainer guides for current paths and commands.
