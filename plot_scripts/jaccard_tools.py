"""Convert .xlsx into .tsv ready for analysis."""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
FILE_PATH = "jaccards_tools.tsv"
HICO_PATH = "jaccard_stats.tsv"
data = pd.read_csv(FILE_PATH, sep="\t")
hico = pd.read_csv(HICO_PATH, sep="\t")
print(hico.columns)

# Remove undesired rows and merge
data = data[data["Interaction type"] == "cis"]
data = data[~(data["Cell line"] == "H1-hESC")]
data = data[~(data["Cell line"] == "GM06990")]
data = data[data["Dataset"] == "Rao"]
data.drop(["Dataset", "Interaction type"], axis=1, inplace=True)
data.columns = ["cell", "method", "jaccard"]
print(data)
print(data["method"].unique())

TO_DROP = [
    "file_a",
    "file_b",
    "rep_type",
    "resolution",
    "size_a_filt",
    "size_b_filt",
    "size_overlap_filt",
    "jacc_value_filt",
    "size_a_spar",
    "size_b_spar",
    "size_overlap_spar",
    "dist_thr",
    "perc_thr",
    "alpha_thr",
]
hico = hico[hico["alpha_thr"] == "optimal"]
hico = hico[hico["perc_thr"] == 0.01]
hico = hico[hico["dist_thr"] == 100_000_000]
hico["alpha_mod"] = "Hicona\n(" + hico["alpha_mod"] + ")"
hico["cell_type"].loc[hico["cell_type"] == "GM"] = "GM12878"
hico.drop(TO_DROP, axis=1, inplace=True)
hico.columns = ["cell", "method", "jaccard"]

data = pd.concat([data, hico], ignore_index=True)

# Plot data
CM = 1 / 2.54
FLIERS = {"marker": "o", "markersize": 3}
ORDER = [
    "HiCONA\n(min)",
    "HiCONA\n(max)",
    "diffHic",
    "Fit-Hi-C",
    "GOTHiC",
    "HiCCUPS",
    "HIPPIE",
    "HOMER",
]

sns.set_style(style="ticks")
fig, axes = plt.subplots(1, 1, figsize=(17 * CM, 8.5 * CM))
sns.boxplot(data, x="method", y="jaccard", hue="cell", order=ORDER, flierprops=FLIERS)
axes.tick_params(axis="both", labelsize=8)
axes.set_xlabel("Method", fontsize=10)
axes.set_ylabel("Jaccard Index", fontsize=10)
axes.legend(title="Cell Line", fontsize=8, title_fontsize=10)
plt.savefig("test.png", dpi=600, bbox_inches="tight")
