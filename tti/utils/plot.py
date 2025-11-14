"""
Trading-Technical-Indicators (tti) python library

File name: plot.py
    Plotting methods defined under the tti.utils package.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math


def linesGraph(data, y_label, title, lines_color, alpha_values, areas, x_label="Date"):
    """
    Returns a lines graph of type matplotlib.pyplot. The graph can be either
    a figure with a single plot, or a figure containing two vertical subplots.
    """
    if type(data) != list:
        data = [data]

    for df in data:
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                "Invalid input_data type. It was expected "
                + "`pd.DataFrame` but `"
                + str(type(df).__name__)
                + "` was found."
            )

        if not isinstance(df.index, pd.DatetimeIndex):
            raise TypeError(
                "Invalid input_data index type. It was expected "
                + "`pd.DatetimeIndex` but `"
                + str(type(df.index).__name__)
                + "` was found."
            )

    nrows = len(data)
    base_h = 3.2
    fig_h = max(5.0, nrows * base_h)
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=1,
        sharex=True,
        figsize=(8.5, fig_h),
    )
    if nrows == 1:
        axes = [axes]

    fig.suptitle(title, fontsize=13, fontweight="bold", y=0.97)

    for ax in axes:
        ax.set_facecolor("#ffffff")
        ax.grid(True, which="major", axis="both", linestyle="--", alpha=0.25, linewidth=0.7)
        ax.minorticks_on()
        ax.grid(True, which="minor", axis="y", linestyle=":", alpha=0.12, linewidth=0.6)
        # De-emphasize spines
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        for spine in ("left", "bottom"):
            ax.spines[spine].set_alpha(0.4)

    j = 0
    for i, df in enumerate(data):
        ax = axes[i]

        _locator = mdates.AutoDateLocator()
        ax.xaxis.set_major_locator(_locator)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(_locator))

        for line_name in df.columns.values:
            color = (
                lines_color[j % len(lines_color)] if lines_color and len(lines_color) > 0 else None
            )
            alpha = (
                alpha_values[j % len(alpha_values)]
                if alpha_values and len(alpha_values) > 0
                else 0.9
            )
            ax.plot(
                df.index,
                df[line_name],
                label=line_name,
                color=color,
                alpha=alpha,
                linewidth=1.8,
            )
            j += 1

        ax.margins(x=0.01, y=0.10)

        if i < nrows - 1:
            ax.label_outer()

    axes[-1].set_xlabel(x_label, fontsize=11, fontweight="bold", labelpad=10)
    fig.supylabel(y_label, fontsize=11, fontweight="bold")

    top_ax = axes[0]
    handles_top, labels_top = top_ax.get_legend_handles_labels()
    if handles_top:
        fig.legend(
            handles_top,
            labels_top,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.92),
            bbox_transform=fig.transFigure,
            frameon=False,
            ncol=len(labels_top),
            fontsize=9,
        )

    if nrows >= 2:
        bottom_ax = axes[-1]
        handles_b, labels_b = bottom_ax.get_legend_handles_labels()
        if handles_b and len(axes) >= 2:
            y_mid = (axes[0].get_position().y0 + axes[1].get_position().y1) / 2
            fig.legend(
                handles_b,
                labels_b,
                loc="center",
                bbox_to_anchor=(0.5, y_mid),
                bbox_transform=fig.transFigure,
                frameon=False,
                ncol=len(labels_b),
                fontsize=9,
            )

    fig.subplots_adjust(top=0.90, bottom=0.12, left=0.12, right=0.95, hspace=0.25)

    if areas is not None:
        areas_objects = []

        for a in areas:
            areas_objects.append({})

            for area_key, area_value in a.items():
                if type(area_value) == list:
                    areas_objects[-1][area_key] = data[area_value[0]][area_value[2]].to_list()

                elif area_value == "ti_index":
                    areas_objects[-1][area_key] = data[0].index
                else:
                    areas_objects[-1][area_key] = a[area_key]

        target_ax = axes[-1]
        for a in areas_objects:
            target_ax.fill_between(
                x=a["x"], y1=a["y1"], y2=a["y2"], color=a.get("color", "#cccccc"), alpha=0.15
            )

    return plt
