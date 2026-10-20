# End-to-end example

Open `example.py`, select the project's `.venv`, and choose **Run Python File in
Terminal**, or run this command from the repository root:

```sh
uv run --locked python scripts/personal/colin/example.py
```

The script:

1. Imports `calculate_mean` from `src/tools/tools_example.py`.
2. Reads `data/random_numbers.csv`: 20 sample values generated once with Python's
   `random.Random(440).uniform(0, 10)`, rounded to three decimal places.
3. Calculates their mean and saves a plot to `figures/example.png`.
4. Writes the sample count and mean to `outputs/example.txt`.

Edit the CSV and rerun to see the outputs change. Each run replaces these two
output files. Paths are based on `example.py`'s location, so it also runs from
other working directories. No `sys.path` changes or extra setup are needed after
the normal environment sync; NumPy and Matplotlib are shared project dependencies.

The script, shared tool, and CSV can be committed. Generated files in `figures/`
and `outputs/` are ignored by Git.
