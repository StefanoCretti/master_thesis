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
    data["pix_reduction"] = data["spar_pix_num"] / data["filt_pix_num"]

    # Sort filtering parameters and create categorical column for param combination
    data.sort_values(["dist_thr", "perc_thr"], ascending=[False, True], inplace=True)
    data["params"] = data["dist_thr"].astype(int).astype(str) + " Mb"
    data["params"] = data["params"] + ", " + data["perc_thr"].astype(str)
    data["dist_thr"] = data["dist_thr"].astype(int).astype(str)

    data["mean_reduction"] = data["mean_dist_spar"] / data["mean_dist_filt"]
    data["median_reduction"] = data["median_dist_spar"] / data["median_dist_filt"]

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
        figsize=(9 * CM, 11 * CM),
        gridspec_kw={"height_ratios": [1, 1, 1]},
    )

    flierprops = {"marker": "o", "markersize": 3}
    sns.boxplot(
        data,
        x="alpha_mod",
        y="pix_reduction",
        hue="params",
        ax=axes[0],
        flierprops=flierprops,
    )
    axes[0].tick_params(axis="both", labelsize=8)
    axes[0].set(xlabel=None)
    axes[0].set_ylabel("Edge Fraction", fontsize=10)
    axes[0].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4])

    sns.boxplot(
        data,
        x="alpha_mod",
        y="mean_reduction",
        hue="params",
        ax=axes[1],
        flierprops=flierprops,
    )
    axes[1].tick_params(axis="both", labelsize=8)
    axes[1].set(xlabel=None)
    axes[1].get_legend().remove()
    axes[1].set_ylabel("Mean Distance\nFold Change", fontsize=10)
    axes[1].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4])

    sns.boxplot(
        data,
        x="alpha_mod",
        y="median_reduction",
        hue="params",
        ax=axes[2],
        flierprops=flierprops,
    )
    axes[2].tick_params(axis="both", labelsize=8)
    axes[2].set_xlabel("Distance Threshold (Mb)", fontsize=10)
    axes[2].set_ylabel("Median Distance\nFold Change", fontsize=10)
    axes[2].get_legend().remove()
    axes[2].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4])

    # Move the legend outside of the plot area
    axes[0].legend(
        title="Parameters", fontsize=8, title_fontsize=10, ncol=2, loc="upper center"
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    OUT_FOLDER = "plots/sparsified_pixels_reduced"
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
        "spar_pix_num",
        "mean_dist_spar",
        "median_dist_spar",
        "alpha_mod",
    ]

    data = pd.read_csv(FILE_PATH, sep="\t", index_col=0)
    print(data.columns)
    data = data[COLS_TO_KEEP]
    data = prepare_data(data)
    print(data.dtypes)
    data.query("perc_thr < 0.05", inplace=True)
    DIST = ["100", "50"]
    data.query(f"dist_thr in {DIST} ", inplace=True)
    data.sort_values("pix_reduction", inplace=True)
    print(data[["mean_dist_spar", "median_dist_spar"]])
    print(data["mean_dist_spar"].median())
    print(data["mean_dist_spar"].min())
    print(data["median_dist_spar"].median())
    print(data["median_dist_spar"].min())

    for res in (5000, 10000):
        img_path = OUT_FOLDER + "/" + FILE_ROOT + f"_{res}.png"
        stat_boxplots(data, res, img_path)
