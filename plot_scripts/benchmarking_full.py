import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# /////////////////////////////////////////////////////// TIME ///////////////
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
data["res"] = (data["res"] / 1000).astype(int).astype(str)
data["res"] = data["res"] + "kb"
data["filt_pix_num"] /= 100_000_000

times = pd.read_csv(TIME_PATH, sep="\t", index_col=0)
merge = data.merge(times, on=["distance_thr", "counts_thr", "file", "res"])
merge["distance_thr"] = (merge["distance_thr"] / 1_000_000).astype(int).astype(
    str
) + " Mb"
merge = merge[~merge["file"].str.contains("bio")]

merge.query("counts_thr < 0.05", inplace=True)
DIST = ["100 Mb", "50 Mb"]
merge.query(f"distance_thr in {DIST} ", inplace=True)


# Retrieve dataframe rows from the log file
with open("reduced.dat", "r", encoding="utf-8") as handle:
    funcs = []
    memos = []
    for line in handle.readlines():
        if line.startswith("MEM"):
            memos.append(line.strip().split(" "))
        elif line.startswith("FUNC"):
            funcs.append(line.strip().split(" "))
        else:
            continue

# //////////////////////////////////////// MEMORY ////////////////////////////
# Create the dataframes
memos = pd.DataFrame(memos, columns=["mode", "memory", "time"])
funcs = pd.DataFrame(
    funcs,
    columns=[
        "mode",
        "func_name",
        "mem_start",
        "time_start",
        "mem_end",
        "time_end",
        "exist_code",
    ],
)

# Adjust column datatypes
memos["memory"] = memos["memory"].astype(float)
memos["time"] = memos["time"].astype(float)
for col in funcs.columns:
    if col not in ["mode", "func_name"]:
        funcs[col] = funcs[col].astype(float)

# Set starting time to zero
start_time = memos.iloc[0]["time"]
memos["time"] -= start_time
funcs["time_start"] -= start_time
funcs["time_end"] -= start_time

# //////////////////////////////////////// PLOT //////////////////////////////

# Setup main plot

sns.set_style(style="ticks")
CM = 1 / 2.54
fig, axes = plt.subplots(
    1,
    2,
    figsize=(17 * CM, 8.5 * CM),
    gridspec_kw={"width_ratios": [0.35, 0.65]},
)

# fig.supxlabel("Number of pixels ($10^8$)", fontsize=10, va="baseline", ha="center")
# fig.tight_layout()

sns.scatterplot(merge, x="filt_pix_num", y="time (s)", ax=axes[0])
# axes[0].legend(title="Cell Type", fontsize=8, title_fontsize=10, loc=2)
axes[0].tick_params(axis="both", labelsize=10)
axes[0].set_xlabel("Number of pixels ($10^8$)", fontsize=12)
axes[0].set_ylabel("Time (s)", fontsize=12)
axes[0].ticklabel_format(style="plain", axis="x")
axes[0].set_title("Runtime", fontsize=14)

sns.lineplot(memos, x="time", y="memory", ax=axes[1], linewidth=1)  # color="blue", )
for _, row in funcs.iterrows():
    plt.axvline(x=row["time_start"], linestyle="dashed", color="red", linewidth=1)
axes[1].set(ylim=[0, 650])
axes[1].set_xlabel("Runtime (s)", fontsize=12)
axes[1].set_ylabel("RAM (MiB)", fontsize=12)
axes[1].tick_params(axis="both", labelsize=10)
axes[1].set_title("Memory usage", fontsize=14)


axes[1].text(19, 20, "chr1", fontsize=10, color="black")
axes[1].text(126, 60, "chr2", fontsize=10, color="black")
axes[1].text(223, 20, "chr3", fontsize=10, color="black")
axes[1].text(309, 60, "chr4", fontsize=10, color="black")
axes[1].text(391, 20, "chr5", fontsize=10, color="black")
axes[1].text(468, 60, "chr6", fontsize=10, color="black")
axes[1].text(547, 20, "chr7", fontsize=10, color="black")
axes[1].text(632, 60, "chr8", fontsize=10, color="black")

plt.subplots_adjust(wspace=3)
plt.tight_layout()
plt.savefig("test.png", dpi=600, bbox_inches="tight")
