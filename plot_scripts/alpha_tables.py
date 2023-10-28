"""Create side by side tables of the optimal alpha value."""

import sys

import matplotlib.pyplot as plt
import seaborn as sns

import hicona


def make_alpha_plot(grids, out_path):
    """Plot alpha grids side by side."""

    # Define marker styles
    optim_style = {
        "marker": "o",
        "markersize": 10,
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
    fig, axes = plt.subplots(1, 2, figsize=(17 * CM, 8.5 * CM))
    fig.supxlabel("Node Fraction", fontsize=10, va="baseline", ha="center")

    # ////////////////////////////// MIN ALPHA //////////////////////////////

    # Create min lineplot
    sns.lineplot(grids["alpha_min"], x="nodes_f", y="edges_f", ax=axes[0])
    axes[0].set_ylabel("Edge Fraction", fontsize=10)
    axes[0].set(xlabel="", aspect="equal")
    axes[0].tick_params(axis="both", labelsize=8)

    # Add markers for all tested points
    for _, pts in grids["alpha_min"].iterrows():
        axes[0].plot(pts["nodes_f"], pts["edges_f"], **other_style)

    # Refresh optimal point marker to be on top
    optim = grids["alpha_min"].iloc[grids["alpha_min"]["eu_dist"].idxmin()]
    axes[0].plot(optim["nodes_f"], optim["edges_f"], **optim_style)

    # Add optimal value text
    axes[0].text(
        0.60,
        0.15,
        rf"$\alpha$ = {optim['alpha']:.3f}",
        transform=axes[0].transAxes,
        fontsize=10,
        va="top",
        ha="left",
    )

    # Add modality text
    axes[0].text(
        0.05,
        0.95,
        r"$\min(\alpha_{ij}, \alpha_{ji})$",
        transform=axes[0].transAxes,
        fontsize=10,
        va="top",
        ha="left",
    )

    # ////////////////////////////// MAX ALPHA //////////////////////////////

    # # Create max lineplot
    sns.lineplot(grids["alpha_max"], x="nodes_f", y="edges_f", ax=axes[1])
    axes[1].set(xlabel="", ylabel="", aspect="equal")
    axes[1].tick_params(axis="both", labelsize=8)

    # Add markers for all tested points
    for _, pts in grids["alpha_max"].iterrows():
        axes[1].plot(pts["nodes_f"], pts["edges_f"], **other_style)

    # Refresh optimal point marker to be on top
    optim = grids["alpha_max"].iloc[grids["alpha_max"]["eu_dist"].idxmin()]
    axes[1].plot(optim["nodes_f"], optim["edges_f"], **optim_style)

    # Add optimal value text
    axes[1].text(
        0.60,
        0.15,
        rf"$\alpha$ = {optim['alpha']:.3f}",
        transform=axes[1].transAxes,
        fontsize=10,
        va="top",
        ha="left",
    )

    # Add modality text
    axes[1].text(
        0.05,
        0.95,
        r"$\max(\alpha_{ij}, \alpha_{ji})$",
        transform=axes[1].transAxes,
        fontsize=10,
        va="top",
        ha="left",
    )

    plt.savefig(out_path, dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    OUT_FOLDER = "plots/alpha_tables"
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
            for alpha_mod in ["alpha_min", "alpha_max"]:
                table.alpha_column = alpha_mod
                table.compute_opt_alpha()
                alpha_grids[alpha_mod] = table._alphas_grid

            img_path = OUT_FOLDER + "/" + FILE_ROOT + f"_{chrom_id}.png"
            make_alpha_plot(alpha_grids, img_path)
