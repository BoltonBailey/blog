# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "pandas",
# ]
# ///

"""Analyze CSV files in data/ and produce overlaid line plots."""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = pathlib.Path(__file__).parent / "data"


def read_data_file(path: pathlib.Path) -> pd.DataFrame:
    """Read a fixed-width/space-separated data file exported from Stack Exchange Data Explorer."""
    rows = []
    with open(path) as f:
        lines = f.readlines()
    # Skip header (line 0) and separator (line 1)
    for line in lines[2:]:
        parts = line.split()
        if len(parts) >= 2:
            date_str = parts[0]  # e.g. "2009-09-01"
            value = int(parts[-1])
            rows.append({"date": pd.to_datetime(date_str), "value": value})
    return pd.DataFrame(rows)


def main():
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        print("No CSV files found in", DATA_DIR)
        return

    datasets = {}
    for csv_file in csv_files:
        label = csv_file.stem.removeprefix("QueryResults")
        datasets[label] = read_data_file(csv_file)

    for label, df in datasets.items():
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df["date"], df["value"], label=label)
        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        ax.set_title(f"Monthly Post Counts – {label}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate()
        fig.tight_layout()
        output_path = pathlib.Path(__file__).parent / "img" / f"plot_{label}.png"
        output_path.parent.mkdir(exist_ok=True)
        fig.savefig(output_path, dpi=150)
        print(f"Saved plot to {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
