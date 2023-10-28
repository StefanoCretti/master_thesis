import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


TIME_PATH, DATA_PATH = sys.argv[1], sys.argv[2]

COLS_TO_KEEP = [
    "dist_thr",
    "perc_thr",
    "filt_pix_num",
    "experiment",
    "resolution",
    "intra_pix_num",
]

data = pd.read_csv(DATA_PATH, sep="\t", index_col=0)
data = data[COLS_TO_KEEP]
data.drop_duplicates(inplace=True)
data.columns = [
    "distance_thr",
    "counts_thr",
    "filt_pix_num",
    "file",
    "res",
    "intra_pix_num",
]
data["cell_type"] = data["file"].str.split("_", expand=True)[0]
# data["cell_type"] += " "
# data["cell_type"] += data["file"].str.split("_", expand=True)[2]
# data["cell_type"] = data["cell_type"].str.replace("combined", "MboI")
data["res"] = (data["res"] / 1000).astype(int).astype(str)
data["res"] = data["res"] + "kb"
data["filt_pix_num"] /= 100_000_000

times = pd.read_csv(TIME_PATH, sep="\t", index_col=0)
merge = data.merge(times, on=["distance_thr", "counts_thr", "file", "res"])
merge["distance_thr"] = (merge["distance_thr"] / 1_000_000).astype(int).astype(
    str
) + " Mb"
print(merge)
merge = merge[~merge["file"].str.contains("bio")]

print(merge)

# Setup main plot

sns.set_style(style="ticks")
CM = 1 / 2.54
fig, axes = plt.subplots(1, 2, sharey=True, figsize=(17 * CM, 10 * CM))

fig.add_subplot(111, frame_on=False)
plt.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)
plt.grid(False)
plt.xlabel("Number of pixels ($10^8$)", fontsize=10, labelpad=5)
# fig.supxlabel("Number of pixels ($10^8$)", fontsize=10, va="baseline", ha="center")
# fig.tight_layout()

sns.scatterplot(merge, x="filt_pix_num", y="time (s)", hue="cell_type", ax=axes[0])
axes[0].legend(title="Cell Type", fontsize=8, title_fontsize=10, loc=4)
axes[0].tick_params(axis="both", labelsize=8)
axes[0].set_xlabel("")
axes[0].ticklabel_format(style="plain", axis="x")


sns.scatterplot(
    merge,
    x="filt_pix_num",
    y="time (s)",
    hue="distance_thr",
    ax=axes[1],
    hue_order=["5 Mb", "10 Mb", "25 Mb", "50 Mb", "100 Mb"],
)
axes[1].legend(title="Distance", fontsize=8, title_fontsize=10, loc=4)
axes[1].tick_params(axis="both", labelsize=8)
axes[1].set_ylabel("")
axes[1].set_xlabel("")

# plt.yscale("log")
# plt.xscale("log")
plt.tight_layout()
plt.savefig("test.png", dpi=600, bbox_inches="tight")
