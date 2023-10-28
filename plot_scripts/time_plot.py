import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Plot execution time as function of filtered pixels, as well as full pixels maybe


# Load datasets with times
TIME_PATH = "results/runtimes_tot_new.txt"
times = pd.read_csv(TIME_PATH, sep="\t", index_col=0)
# Fix column names for convenience

times["dist_thr"] = times["distance_thr"]
times["perc_thr"] = times["counts_thr"]
times["time"] = times["time (s)"]
times["dist_thr"] = times["dist_thr"].astype(int)
times.drop(["distance_thr", "counts_thr", "time (s)"], axis=1, inplace=True)

"""
TIME_PATH = "rerun.csv"
times = pd.read_csv(TIME_PATH, index_col=0)
print(times)
times["dist_thr"] = times["dist"]
times["perc_thr"] = times["perc"]
times["file"] = "IMR90_set1_bio1_tec4_4DNFIMU9T2QI_10kb"
"""

DATA_PATH = "full_stats.tsv"
data = pd.read_csv(DATA_PATH, sep="\t", index_col=0)
data["file"] = data["experiment"]
data.drop("experiment", axis=1, inplace=True)
data = data[data["alpha_mod"] == "min"]  # "max" is the same
print(data)
# print(data.columns)

# print(data.groupby(["file", "dist_thr", "perc_thr"]).sum())

# print(data["file"])
merged = times.merge(data, how="inner", on=["file", "dist_thr", "perc_thr"])
# merged = merged[merged[""]]
merged["id"] = merged["file"].str.extract(r"(4DN[A-Za-z0-9]+)_")
print(merged[["file", "time", "dist_thr", "perc_thr", "id"]])

print(merged)

merged = merged[merged["perc_thr"] == 0.25]
# merged = merged[merged["res"] == "10kb"]

print(merged["file"].unique())

sns.scatterplot(
    merged,
    x="filt_pix_num",
    y="time",
    hue=(merged["file"] == "GM_HiC_combined_4DNFIYECESRC_5kb"),
    size=None,
    style="perc_thr",
    palette=None,
    hue_order=None,
    hue_norm=None,
    sizes=None,
    size_order=None,
    size_norm=None,
    markers=True,
)
# plt.title(idx)
plt.yscale("log")
plt.xscale("log")
plt.show()
