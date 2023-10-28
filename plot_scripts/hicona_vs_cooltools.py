"""Plot comparison of expected counts using HiCONA and cooltools."""

import sys
import time

import cooltools
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import hicona


def get_chrom_view(cool_obj, chrom_name):
    """Get chromosome view for cooltools."""

    interval = pd.DataFrame(
        data=[[chrom_name, 0, cool_obj.chromsizes[chrom_name], chrom_name]],
        columns=["chrom", "start", "end", "name"],
    )

    return interval


def get_cooltool_curve(cool_obj, chrom_name, max_bin_diff):
    """Get chromsome expected counts according to cooltools."""

    start_cooltools = time.time()
    cvd = cooltools.expected_cis(
        clr=cool_obj,
        view_df=get_chrom_view(cool_obj, chrom_name),
        smooth=False,
        aggregate_smoothed=False,
        nproc=4,
    )
    cooltools_time = time.time() - start_cooltools
    cvd.query(f"dist < {max_bin_diff}", inplace=True)
    cvd["dist"] *= cool_obj.binsize

    return cvd, cooltools_time


def merge_frames(hico_df, cool_df):
    """Merge expected counts obtained through different methods for plotting purposes."""

    hico_df = pd.DataFrame(hico_df, columns=["Hicona"])
    merged = cool_df.merge(hico_df, left_index=True, right_index=True)
    merged.rename(columns={"count.avg": "Cooltools"}, inplace=True)
    merged = pd.melt(merged[["Cooltools", "Hicona", "dist"]], id_vars=["dist"])
    merged.rename(columns={"variable": "method", "value": "exp_count"}, inplace=True)

    return merged


def comparison_plot(merged, out_path):
    """Plot both with y axis both in log and in linear scale, side by side."""

    sns.set_style(style="ticks")

    CM = 1 / 2.54
    _, axes = plt.subplots(1, 2, figsize=(17 * CM, 8.5 * CM))

    # TODO: Uncomment for title
    # fig.suptitle(f"name", fontsize=20, fontweight=10)
    # fig.tight_layout(rect=[0, 0, 1, 1])

    sns.scatterplot(
        data=merged,
        x="dist",
        y="exp_count",
        hue="method",
        s=10,
        linewidth=0.01,
        ax=axes[0],
        palette="tab10",
    )
    axes[0].set_xlabel("Genomic distance (bp)", fontsize=10)
    axes[0].set_ylabel("Summary statistic", fontsize=10)
    axes[0].set(xscale="log", yscale="log")
    axes[0].get_legend().remove()
    axes[0].axhline(1, color="grey", linestyle="--", zorder=0)
    axes[0].tick_params(axis="both", labelsize=8)
    axes[0].spines[["right", "top"]].set_visible(False)

    sns.scatterplot(
        data=merged,
        x="dist",
        y="exp_count",
        hue="method",
        s=10,
        linewidth=0.01,
        ax=axes[1],
        palette="tab10",
    )
    axes[1].set_xlabel("Genomic distance (bp)", fontsize=10)
    axes[1].set_ylabel(None)
    axes[1].legend(title="Method", fontsize=8, title_fontsize=10)
    axes[1].set(xscale="log", yscale="linear")
    axes[1].axhline(1, color="grey", linestyle="--", zorder=0)
    axes[1].tick_params(axis="both", labelsize=8)
    axes[1].spines[["right", "top"]].set_visible(False)

    # TODO: uncomment to set y axis ticks to multiples of 2 + 1
    # max_pos = np.nanmax(merged["exp_count"])
    # max_tick = int(max_pos // 2 * 2)  # Round to closest smaller even number
    # axes[1].set_yticks([n for n in range(0,max_tick+1,2)] + [1])

    plt.savefig(out_path, dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    OUT_FOLDER = "plots/hicona_vs_cooltools"
    FILE_PATH = sys.argv[1]
    if not FILE_PATH:
        raise ValueError("File to process not provided")
    FILE_ROOT = FILE_PATH.split("/")[-1].split(".")[0]

    handle = hicona.HiconaCooler(FILE_PATH)
    FILT_OPTS = {"dist_thr": 200_000_000, "count_thr": 0}

    for chrom_id in ["chr20", "chr10"]:  # handle.chromnames:
        print(f"Starting to work on {chrom_id}")

        hico_curve = handle._get_norm_curve(chrom_id, FILT_OPTS)
        bin_diff = FILT_OPTS["dist_thr"] / handle.binsize
        cool_curve, cool_time = get_cooltool_curve(handle, chrom_id, bin_diff)
        data = merge_frames(hico_curve, cool_curve)

        img_path = OUT_FOLDER + "/" + FILE_ROOT + f"_{chrom_id}.png"
        comparison_plot(data, img_path)
