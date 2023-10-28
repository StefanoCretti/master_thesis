"""Plot the pixels before and after genomic distance normalization."""

import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import hicona


def count_pixels(pix_df):
    """Compute the number of pixels as a function of distance."""

    all_pix = pix_df.groupby("distance").count()
    all_pix.rename(columns={"count": "all"}, inplace=True)
    one_pix = pix_df[pix_df["count"] == 1].groupby("distance").count()
    one_pix.rename(columns={"count": "ones"}, inplace=True)
    all_pix = all_pix.merge(one_pix, how="left", left_index=True, right_index=True)
    all_pix.reset_index(inplace=True)
    all_pix = pd.melt(all_pix, id_vars=["distance"], value_vars=["all", "ones"])
    all_pix.rename(columns={"variable": "pixels"}, inplace=True)

    return all_pix


def compute_quantiles(pix_df, quantiles, normalized=False):
    """Create dataframe with quantiles values."""

    var_to_grp = "exp_ratio" if normalized else "count"
    quant_df = pd.DataFrame(pix_df["distance"].unique(), columns=["distance"])
    group_filt = pix_df.groupby("distance")[var_to_grp]
    for quant in quantiles:
        quant_df = quant_df.merge(group_filt.quantile(quant), how="left", on="distance")
        quant_df.rename(columns={var_to_grp: quant}, inplace=True)
    quant_df = pd.melt(quant_df, id_vars=["distance"], value_vars=quantiles)
    quant_df.rename(columns={"variable": "quantile", "value": var_to_grp}, inplace=True)
    quant_df.sort_values(["distance", "quantile"], inplace=True)
    quant_df.reset_index(inplace=True)
    quant_df.drop("index", axis=1, inplace=True)

    return quant_df


def create_plot(filt_distr, norm_distr, count_distr, out_path):
    """Given the three dataframes the create and save the plot."""

    sns.set_style(style="ticks")
    CM = 1 / 2.54

    fig, axes = plt.subplots(
        3,
        1,
        sharex=True,
        figsize=(9 * CM, 10 * CM),
        gridspec_kw={"height_ratios": [0.8, 0.8, 0.4]},
    )
    # fig.suptitle(f"{chrom}, res: {res:,} bp, file: {F_NAME}", fontsize=24, fontweight=10)
    # fig.tight_layout()
    # plt.xlim([res, MAX_GEN_DIST])

    sns.lineplot(
        data=filt_distr,
        x="distance",
        y="count",
        hue="quantile",
        palette="tab10",
        ax=axes[0],
    )
    axes[0].set_ylabel("Filtered\nCounts", fontsize=10)
    axes[0].set(xscale="log")
    axes[0].tick_params(axis="both", labelsize=8)
    axes[0].legend(loc="upper right", title="Quantiles", fontsize=8, title_fontsize=10)

    sns.lineplot(
        data=norm_distr,
        x="distance",
        y="exp_ratio",
        hue="quantile",
        palette="tab10",
        ax=axes[1],
    )
    axes[1].set_ylabel("Normalized\nCounts", fontsize=10)
    axes[1].tick_params(axis="both", labelsize=8)
    axes[1].get_legend().remove()

    sns.lineplot(
        data=count_distr,
        x="distance",
        y="value",
        hue="pixels",
        ax=axes[2],
        palette=["purple", "red"],
    )
    axes[2].set_ylabel("Num\nPixels", fontsize=10)
    axes[2].set(yscale="log")
    # axes[2].set_yticks([1, 10, 100, 1000, 10000])
    axes[2].set_yticks([1, 100, 10000])
    axes[2].axhline(10, color="grey", linestyle="--", linewidth=1.5)
    axes[2].get_legend().set_title(None)
    axes[2].tick_params(axis="both", labelsize=8)
    axes[2].legend(fontsize=8, ncol=2)

    axes[2].set_xlabel("Genomic Distance (bp)", fontsize=10)
    plt.savefig(out_path, dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    QUANTS = [0.25, 0.50, 0.75]
    FILT_OPTS = {"dist_thr": 200_000_000, "count_thr": 0, "quant_thr": 0.0}
    OUT_FOLDER = "plots/normalized_counts_reduced"
    FILE_PATH = sys.argv[1]
    if not FILE_PATH:
        raise ValueError("File to process not provided")
    FILE_ROOT = FILE_PATH.split("/")[-1].split(".")[0]

    handle = hicona.HiconaCooler(FILE_PATH)
    for chrom_id in handle.chromnames:
        print(f"Starting to work on {chrom_id}")

        for tab in handle.tables([chrom_id], **FILT_OPTS):
            table = tab.data  # TODO: Not pretty to define variable in loop

        if table is None:
            raise ValueError("No table matching the criteria was found")

        table["distance"] = table["bin2_id"] - table["bin1_id"]
        table["distance"] *= handle.binsize

        num_pix = count_pixels(table)
        filt_qts = compute_quantiles(table, QUANTS)
        norm_qts = compute_quantiles(table, QUANTS, normalized=True)

        img_path = OUT_FOLDER + "/" + FILE_ROOT + f"_{chrom_id}.png"
        create_plot(filt_qts, norm_qts, num_pix, img_path)
        del table, filt_qts, norm_qts
