"""
Trading-Technical-Indicators (tti) python library

File name: example_data_preprocessing.py
    Example code for the Fill Missing Values function.
"""

import pandas as pd
import matplotlib.pyplot as plt

from tti.utils import fillMissingValues

for data_file in [
    "example_data_missing_1.csv",
    "example_data_missing_2.csv",
    "example_data_missing_3.csv",
]:
    # Read data from csv file. Set the index to the correct column
    df = pd.read_csv("./data/" + data_file, parse_dates=True, index_col=0)

    # Create a dataframe with original and modified values, for plotting
    df = pd.concat([fillMissingValues(df), df], axis=1)
    df.columns = ["After", "Before"]

    fig, ax = plt.subplots(figsize=(8.5, 4.5))

    fig.suptitle("Fill Missing Values", fontsize=13, fontweight="bold", y=0.97)

    ax.plot(
        df.index,
        df["After"],
        label="Filled Values",
        color="tomato",
        linestyle="--",
        linewidth=1.8,
        alpha=1.0,
    )
    ax.plot(
        df.index,
        df["Before"],
        label="Before",
        color="limegreen",
        linestyle="-",
        linewidth=1.8,
        alpha=1.0,
    )

    ax.set_facecolor("#ffffff")
    ax.grid(True, which="major", axis="both", linestyle="--", alpha=0.25, linewidth=0.7)
    ax.minorticks_on()
    ax.grid(True, which="minor", axis="y", linestyle=":", alpha=0.12, linewidth=0.6)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_alpha(0.4)

    ax.margins(x=0.01, y=0.10)

    ax.set_xlabel("Date", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Price", fontsize=11, fontweight="bold")

    fig.autofmt_xdate()

    ax.legend(
        loc="upper left",
        frameon=False,
        fontsize=9,
        handlelength=1.6,
        columnspacing=1.2,
        handletextpad=0.8,
        labelspacing=0.5,
        borderpad=0.4,
    )

    fig.subplots_adjust(
        top=0.90,
        bottom=0.18,
        left=0.08,
        right=0.95,
    )

    outfile = "./figures/" + data_file.split(".")[0] + ".png"
    plt.savefig(outfile, dpi=120)
    plt.close(fig)

    print("- Graph", outfile, "saved.")
