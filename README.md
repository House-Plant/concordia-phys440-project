# Concordia PHYS 440 project

Python modelling workspace. Scientific models and datasets have not been added yet.
Python 3.12 and a repository-local `.venv` are managed with uv. Shared dependencies
live in `pyproject.toml` and `uv.lock`.

## Where to work

| Directory | Contents |
| --- | --- |
| `src/phys440/` | Scientific Python modules: models, simulation, analysis, and runnable modules |
| `notebooks/` | Exploratory notebooks; select the project's `.venv` kernel |
| `data/raw/` | Original input datasets; small, shareable data can be committed |
| `results/` | Generated outputs; ignored by Git except the empty-directory placeholder |
| `reports/` | Scientific write-up, bibliography, and selected figures/tables worth committing |
| `tests/` | Scientific tests of the code in `src/phys440/` |

Add a module such as `src/phys440/simulation.py` and import it with
`from phys440.simulation import ...`. Setup installs `phys440` into `.venv` in
editable mode, so saved source changes are available without reinstalling.
Once a runnable module exists, use **Terminal → Run Task → Project: Run Python
module** and enter `phys440.simulation`. Notebooks belong in `notebooks/`; the
installed package works there too. Run tasks with the repository root open in
VS Code. Tasks and VS Code notebook kernels use the root as their working
directory, so data/output paths are `data/raw/...` and `results/...`. For notebooks
launched outside VS Code, check their working directory first.

## Repository infrastructure

All setup/check/synchronization scripts and their tests live under `tools/`
and `tools/tests/`. The scientific directories above contain no repository
automation or workflow tests. `docs/` holds repository user guides; scientific
reports belong in `reports/`. `.github/` and `.vscode/` hold platform integration
files. Shared Python, Git, and dependency configuration stays at the root.

Empty content directories use `.gitkeep` placeholders so they appear in a clone.
Remove a placeholder once its directory contains tracked project files.
`results/` stays ignored for generated output. For large or private data, agree
on storage and ignore rules before adding it to Git.

## Guides and setup

- [First-time contributor setup](docs/CONTRIBUTOR_SETUP.md)
- [Daily use: editing, notebooks, packages, branches, and PRs](docs/CONTRIBUTOR_DAILY_USE.md)
- [Maintainer setup, GitHub protections, and upkeep](docs/MAINTAINER_SETUP.md)

Start in VS Code with **Terminal → Run Task → Project: First-time setup**.
Then use **Save → Stage → Commit → Push → Open PR** on a task branch.

GitHub rules and code owners still need maintainer configuration. No actual
immutable paths have been identified; file protection is not active until the
maintainer fills in the policy. See the maintainer checklist before onboarding a team.

The original implementation brief is archived under
[docs/maintenance/](docs/maintenance/CODEX_REPO_WORKFLOW_SETUP.md).
It records the original request; use the current guides for paths and commands.
