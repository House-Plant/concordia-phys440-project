"""Read sample data, use a shared tool, and save a plot and text result.

Run this file using the project's .venv in VS Code, or from the repo root:
    uv run --locked python scripts/personal/colin/example.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from tools.tools_example import calculate_mean


def main():
    # Locate Colin's folders relative to this file, regardless of where you run it.
    personal_folder = Path(__file__).resolve().parent
    data_file = personal_folder / "data" / "random_numbers.csv"
    figures_folder = personal_folder / "figures"
    outputs_folder = personal_folder / "outputs"
    figures_folder.mkdir(exist_ok=True)
    outputs_folder.mkdir(exist_ok=True)

    # CSV data is read from disk; Python functions are imported from tools.
    values = np.loadtxt(data_file, delimiter=",", skiprows=1, ndmin=1)
    mean = calculate_mean(values)

    sample_numbers = np.arange(1, len(values) + 1)
    fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
    ax.plot(sample_numbers, values, "o-", label="Sample values")
    ax.axhline(mean, color="tab:orange", linestyle="--", label=f"Mean = {mean:.3f}")
    ax.set(
        title="Example: random numbers and their mean",
        xlabel="Sample number",
        ylabel="Value",
    )
    ax.grid(alpha=0.25)
    ax.legend()

    plot_file = figures_folder / "example.png"
    fig.savefig(plot_file, dpi=150)
    plt.close(fig)

    result_file = outputs_folder / "example.txt"
    result_file.write_text(
        f"Samples: {len(values)}\nMean: {mean:.6f}\n", encoding="utf-8"
    )

    print(f"Read: {data_file}")
    print(f"Saved plot: {plot_file}")
    print(f"Saved result: {result_file}")


if __name__ == "__main__":
    main()
