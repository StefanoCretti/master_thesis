"""Plot time comparison among tools."""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

TIME = "times_tools.tsv"
FILE = "runtimes_tot_new.txt"

# Found A5 corresponds to IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_5kb by:
# A5 to SRA in paper
# SRA on 4DN gives BAM
# BAM on 4DN gives pairs
hico = pd.read_csv(FILE, sep="\t", index_col=0)
hico.query("file == 'IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_5kb'", inplace=True)
hico.query("counts_thr == 0.01", inplace=True)
hico.query("distance_thr == 100000000.0", inplace=True)
print(hico)
# Added 810 to file by hand

tool = pd.read_csv(TIME, sep="\t")
print(tool)

CM = 1 / 2.54
ORDER = ["HiCONA", "diffHic", "Fit-Hi-C", "GOTHiC", "HiCCUPS", "HIPPIE", "HOMER"]

sns.set_style(style="ticks")
fig, axes = plt.subplots(1, 1, figsize=(11 * CM, 8.5 * CM))
sns.barplot(tool, x="Method", y="Time", order=ORDER)
axes.set(yscale="log")
axes.tick_params(axis="both", labelsize=8)
axes.set_xlabel("Tool", fontsize=10)
axes.set_ylabel("Jaccard Index", fontsize=10)
plt.savefig("test.png", dpi=600, bbox_inches="tight")
