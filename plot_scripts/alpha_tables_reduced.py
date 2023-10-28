"""Create side by side tables of the optimal alpha value."""

import sys

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, InsetPosition, mark_inset
import seaborn as sns

import hicona


def make_alpha_plot(grids, out_path):
    """Plot alpha grids side by side."""

    # Define marker styles
    optim_style = {
        "marker": "o",
        "markersize": 8,
        "markerfacecolor": "tab:orange",
        "markeredgewidth": 0.0,
    }
    other_style = {
        "marker": "o",
        "markersize": 5,
        "markerfacecolor": "tab:blue",
        "markeredgewidth": 0.0,
    }

    # Set up plot grid
    CM = 1 / 2.54
    sns.set_style(style="ticks")
    fig, axes = plt.subplots(1, 1, figsize=(8.5 * CM, 8.5 * CM))

    # ////////////////////////////// MIN ALPHA //////////////////////////////

    first_iter = grids["alpha_min"][0:11]

    # Create min lineplot
    sns.lineplot(first_iter, x="nodes_f", y="edges_f", color="dimgrey", ax=axes)
    axes.set_ylabel("Edge Fraction", fontsize=10)
    axes.set_xlabel("Node Fraction", fontsize=10)
    axes.tick_params(axis="both", labelsize=8)

    # Add markers for all tested points
    for _, pts in first_iter.iterrows():
        axes.plot(pts["nodes_f"], pts["edges_f"], **other_style)

    # Refresh optimal point marker to be on top
    optim = first_iter.iloc[first_iter["eu_dist"].idxmin()]
    axes.plot(optim["nodes_f"], optim["edges_f"], **optim_style)

    # ///////////////////////////// INSET //////////////////////////////////

    second_iter = grids["alpha_min"][11:22]
    print(second_iter)

    # bounds = [0.89, 0.98, 0.01, 0.12]
    # bounds = [0.88, 0.01, 0.99, 0.12]
    axin = plt.axes([0, 0, 1, 1])

    pos = InsetPosition(axes, [0.20, 0.40, 0.5, 0.5])
    axin.set_axes_locator(pos)
    mark_inset(
        axes, axin, loc1=1, loc2=3, fc="none", ec="0.5", linestyle="dashed", zorder=0
    )

    axin.plot(second_iter["nodes_f"], second_iter["edges_f"], "dimgrey")

    for _, pts in second_iter.iterrows():
        axin.plot(pts["nodes_f"], pts["edges_f"], **other_style)

    # Refresh optimal point marker to be on top
    optim = second_iter.iloc[second_iter["eu_dist"].idxmin() - 11]
    axin.plot(optim["nodes_f"], optim["edges_f"], **optim_style)

    axin.set_xlim(0.89, 1)
    axin.set_ylim(0.01, 0.12)
    axin.tick_params(axis="both", labelsize=8)
    axin.set_xticks([0.90, 0.93, 0.96, 0.99])
    axin.set_xticklabels(axin.get_xticks(), backgroundcolor="w")
    axin.set_yticks([0.02, 0.05, 0.08, 0.11])

    # axin.xaxis.tick_top()
    # axin.xaxis.set_label_position("top")
    # axin.tick_params(axis="x", bottom=False, top=True)

    # axin.set_yticks(np.arange(0, 2, 0.4))
    # axin.tick_params(axis="x", which="major")
    # axin.set_yticks(np.arange(0, 2, 0.4))
    # axin.set_xticklabels(axin.get_xticks(), backgroundcolor="w")
    # axin.tick_params(axis="x", which="major", pad=8)

    """


    # Create an inset axes
    axins = inset_axes(axes, width="40%", height="40%", loc="upper left")

    # Plot some data in the inset axes
    axins.plot(second_iter["nodes_f"], second_iter["edges_f"], "dimgrey")

    for _, pts in second_iter.iterrows():
        axins.plot(pts["nodes_f"], pts["edges_f"], **other_style)
    optim = second_iter.iloc[second_iter["eu_dist"].idxmin() - 11]
    axins.plot(optim["nodes_f"], optim["edges_f"], **optim_style)
    axins.tick_params(axis="both", labelsize=8)

    print(second_iter["nodes_f"][21])
    # Set limits of the inset axes
    axins.set_xlim(second_iter["nodes_f"][21] - 0.01, second_iter["nodes_f"][11] + 0.01)
    axins.set_ylim(second_iter["edges_f"][21] - 0.01, second_iter["edges_f"][11] + 0.01)

    # Add a legend to the inset axes
    # axins.legend()
    """

    plt.savefig(out_path, dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    OUT_FOLDER = "plots/alpha_tables_reduced"
    FILE_PATH = sys.argv[1]
    if not FILE_PATH:
        raise ValueError("File to process not provided")
    FILE_ROOT = FILE_PATH.split("/")[-1].split(".")[0]
    FILT_OPTS = {"dist_thr": 200_000_000, "count_thr": 0, "quant_thr": 0.0}

    handle = hicona.HiconaCooler(FILE_PATH)
    for chrom_id in handle.chromnames:
        print(f"Starting to work on {chrom_id}")

        for table in handle.tables([chrom_id], **FILT_OPTS):
            alpha_grids = {}
            for alpha_mod in ["alpha_min"]:
                table.alpha_column = alpha_mod
                table.compute_opt_alpha()
                alpha_grids[alpha_mod] = table._alphas_grid

            img_path = OUT_FOLDER + "/" + FILE_ROOT + f"_{chrom_id}.png"
            make_alpha_plot(alpha_grids, img_path)
