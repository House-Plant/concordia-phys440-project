# Personal experiments

Use your folder under `scripts/personal/` for your own investigations. Folders
are provided for `colin`, `naomi`, `sabrina`, `jaeden`, and `eshaal`, each with
the same structure:

```text
scripts/personal/<your-name>/
    your_script.py  # Put scripts directly in your personal folder
    data/           # Datasets you can commit and share
    figures/        # Generated plots and images (ignored)
    outputs/        # Other generated files (ignored)
```

- Create, edit, and delete your own experiments freely. Coordinate before changing
  another person's folder. This is a team convention, not an access restriction.
- Scripts and notes in your personal folder, and datasets in `data/`, can be committed and
  shared. Ruff linting, formatting, and import sorting are disabled throughout
  `scripts/personal/`, including the editor and commit/CI checks. Personal scripts
  are not automatically executed by the project's test suite.
- Contents of each person's `figures/` and `outputs/` directories are
  ignored by Git, except their `.gitkeep` placeholders. These files stay local;
  pushing your branch does not back them up or share them. Do not force-add them.
- Keep reproducible, shareable inputs in the root `data/` directory when needed.
  Preserve selected scientific findings in `reports/`. Put reusable functions in
  `src/tools/` so other scripts can import them.

Select the project's `.venv`, open your script, and choose **Run Python File in
Terminal**. Keep the terminal at the repository root. Use output paths such as
`scripts/personal/colin/figures/comparison.png`, replacing `colin` with your name;
plots and datasets are only saved there if your script writes to those paths.
These folders need no `__init__.py`. Use the normal task-branch and PR workflow
when sharing your scripts and data. Files are saved to Git when you stage and
commit them; push those commits to share them on GitHub.

See the [daily-use guide](../../docs/repo-guides/CONTRIBUTOR_DAILY_USE.md).

For a runnable example that imports a shared tool, reads a CSV, and saves a plot
and text result, see [Colin's example](colin/README.md).
