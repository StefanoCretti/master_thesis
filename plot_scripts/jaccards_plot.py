import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
FILE_PATH = "jaccard_stats.tsv"
data = pd.read_csv(FILE_PATH, sep="\t")

# Remove unnecessary columns
data.query("alpha_thr == 'optimal'", inplace=True)
data.query("perc_thr < 0.05", inplace=True)
data.query("dist_thr > 25_000_000", inplace=True)
# Resolution is only 5000

# Compute new necessary columns
data["id"] = data["file_a"] + data["file_b"]
data["fold_change"] = data["jacc_value_spar"] / data["jacc_value_filt"]

# Adjust columns for plotting purposes
data["dist_thr"] = (data["dist_thr"] / 1_000_000).astype(int).astype(str)
data["comb"] = data["perc_thr"].astype(str) + "\n" + data["dist_thr"]

# Set plot basics
CM = 1 / 2.54
sns.set_style(style="ticks")
fig, axes = plt.subplots(1, 2, sharex=True, figsize=(17 * CM, 8.5 * CM))

fig.add_subplot(111, frame_on=False)
plt.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)
plt.grid(False)
plt.xlabel("Parameter combination", fontsize=10, labelpad=10)

cell_types = ["GM", "IMR90"]
for ind, cell in enumerate(cell_types):
    print(cell, ind)
    tmp_data = data.query(f"cell_type == '{cell}'")
    print(tmp_data)

    sns.boxplot(
        tmp_data,
        x="comb",
        y="fold_change",
        hue="alpha_mod",
        palette={"min": "skyblue", "max": "darkorange"},
        ax=axes[ind],
        showfliers=False,
    )
    sns.stripplot(
        tmp_data,
        x="comb",
        y="fold_change",
        hue="alpha_mod",
        dodge=True,
        palette={"min": "dimgrey", "max": "dimgrey"},
        size=2.5,
        jitter=0.2,
        legend=None,
        ax=axes[ind],
    )

    axes[ind].set_title(f"{cell} cells")
    axes[ind].set_ylim([0.5, 1.25])
    axes[ind].set_yticks([0.1 * n for n in range(6, 13)])
    axes[ind].set_xlabel("")
    # axes.set_xlim([0, 0.30])

    axes[ind].tick_params(axis="both", labelsize=8)

axes[0].set_ylabel("Fold Change", size=10)
axes[0].legend().remove()
axes[1].legend(
    title="Alpha modality",
    fontsize=8,
    title_fontsize=10,
)
axes[1].set_ylabel("")
axes[1].set_yticklabels([])

plt.text(
    -0.05,
    -0.11,
    "Quantile\nDistance (Mb)",
    fontsize=8,
    ha="center",
    va="center",
)
plt.tight_layout()
plt.savefig("fold_changes.png", dpi=600, bbox_inches="tight")