import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def prepare_data(data):
    """Manipulate data to prepare it for the plots."""

    # Convert dist thr in megabases
    data["dist_thr"] = data["dist_thr"] / 1000000
    # Remove biological replicates replicates
    data = data[~data["experiment"].str.contains("bio")]
    # Remove duplicate rows due to sparsification params ignored
    data.drop_duplicates(inplace=True, ignore_index=True)

    # Add experiment cell type
    data["cell_type"] = data["experiment"].str.split("_", expand=True)[0]
    data["cell_type"] += " "
    data["cell_type"] += data["experiment"].str.split("_", expand=True)[2]
    data["cell_type"] = data["cell_type"].str.replace("combined", "MboI")

    # Compute percentage reductions
    data["pix_reduction"] = data["filt_pix_num"] / data["intra_pix_num"]

    # Reduce for more clarity in plotting
    data.query("dist_thr > 10", inplace=True)
    data.query("perc_thr > 0", inplace=True)
    data.query("perc_thr < 0.25", inplace=True)

    # Sort filtering parameters and create categorical column for param combination
    data.sort_values(["dist_thr", "perc_thr"], ascending=[False, True], inplace=True)
    data["params"] = data["dist_thr"].astype(int).astype(str) + " Mb"
    data["params"] = data["params"] + ", " + data["perc_thr"].astype(str)
    data["dist_thr"] = data["dist_thr"].astype(int).astype(str)

    data["mean_reduction"] = data["mean_dist_filt"] / data["mean_intra_init"]
    data["median_reduction"] = data["median_dist_filt"] / data["median_intra_init"]

    return data


def stat_boxplots(dataf, resolution, out_path):
    """Create the boxplots with edge fraction, mean fold and median fold."""

    # Filter by resolution
    data = dataf.query(f"resolution == {resolution}")

    # Setup main plot
    sns.set_style(style="ticks")
    CM = 1 / 2.54
    _, axes = plt.subplots(
        3,
        1,
        sharex=True,
        figsize=(14 * CM, 14 * CM),
        gridspec_kw={"height_ratios": [1, 1, 1]},
    )

    flierprops = {"marker": "o", "markersize": 3}
    sns.boxplot(
        data,
        x="dist_thr",
        y="pix_reduction",
        hue="perc_thr",
        ax=axes[0],
        flierprops=flierprops,
    )
    axes[0].tick_params(axis="both", labelsize=10)
    axes[0].set(xlabel=None)
    axes[0].set_ylabel("Edge Fraction", fontsize=12)
    axes[0].get_legend().remove()
    axes[0].set_yticks([0.0, 0.3, 0.6, 0.9, 1.2])
    axes[0].axhline(1, linestyle="dashed", color="grey")

    sns.boxplot(
        data,
        x="dist_thr",
        y="mean_reduction",
        hue="perc_thr",
        ax=axes[1],
        flierprops=flierprops,
    )
    axes[1].tick_params(axis="both", labelsize=10)
    axes[1].set(xlabel=None)
    axes[1].set_ylabel("Mean Distance\nFold Change", fontsize=12)
    axes[1].set_yticks([0.0, 0.3, 0.6, 0.9, 1.2])
    axes[1].axhline(1, linestyle="dashed", color="grey")

    sns.boxplot(
        data,
        x="dist_thr",
        y="median_reduction",
        hue="perc_thr",
        ax=axes[2],
        flierprops=flierprops,
    )
    axes[2].tick_params(axis="both", labelsize=10)
    axes[2].set_xlabel("Distance Threshold (Mb)", fontsize=12)
    axes[2].set_ylabel("Median Distance\nFold Change", fontsize=12)
    axes[2].get_legend().remove()
    axes[2].set_yticks([0.0, 0.3, 0.6, 0.9, 1.2])
    axes[2].axhline(1, linestyle="dashed", color="grey")

    # Move the legend outside of the plot area
    # axes[1].legend(title="Quantile Threshold", fontsize=10, title_fontsize=12, ncol=3)
    axes[1].legend(
        title="Quantile\nThreshold",
        fontsize=10,
        title_fontsize=12,
        ncol=1,
        # loc="upper left",
        bbox_to_anchor=(1, 1),
        # title_align="center",
    )

    plt.tight_layout()
    plt.savefig(out_path, dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    OUT_FOLDER = "plots/retained_pixels_reduced"
    FILE_PATH = sys.argv[1]
    if not FILE_PATH:
        raise ValueError("File to process not provided")
    FILE_ROOT = FILE_PATH.split("/")[-1].split(".")[0]
    COLS_TO_KEEP = [
        "dist_thr",
        "perc_thr",
        "filt_pix_num",
        "mean_dist_filt",
        "median_dist_filt",
        "experiment",
        "resolution",
        "intra_pix_num",
        "mean_intra_init",
        "median_intra_init",
    ]

    data = pd.read_csv(FILE_PATH, sep="\t", index_col=0)
    data = data[COLS_TO_KEEP]
    data = prepare_data(data)
    for res in (5000, 10000):
        img_path = OUT_FOLDER + "/" + FILE_ROOT + f"_{res}.png"
        stat_boxplots(data, res, img_path)
