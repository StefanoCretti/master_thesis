import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import pingouin as pg
import scipy.stats as stats

FILE_PATH = "jaccard_stats.tsv"
data = pd.read_csv(FILE_PATH, sep="\t")

print(data.columns)
data.query("alpha_thr == 'optimal'", inplace=True)  # It is fixed 5000
data.query("cell_type == 'GM'", inplace=True)  # TODO: Try IMR90
data["id"] = data["file_a"] + data["file_b"]

print(data.dtypes)
data.query("perc_thr < 0.05", inplace=True)
data.query("dist_thr > 25_000_000", inplace=True)
data.query("alpha_mod == 'max'", inplace=True)
data["fold_change"] = data["jacc_value_spar"] / data["jacc_value_filt"]
data["comb"] = data["perc_thr"].astype(str) + ", " + data["dist_thr"].astype(str)


cond_dfs = [data[data["comb"] == c]["fold_change"] for c in data["comb"].unique()]
average_changes = [d.median() for d in cond_dfs]
print(average_changes)

cond_dfs = [data[data["comb"] == c]["fold_change"] for c in data["comb"].unique()]
statistic, p_value = stats.friedmanchisquare(*cond_dfs)

p_values = []
conditions = list(data["comb"].unique())

for i in range(len(conditions)):
    for j in range(i + 1, len(conditions)):
        condition1 = data[data["comb"] == conditions[i]]["fold_change"]
        condition2 = data[data["comb"] == conditions[j]]["fold_change"]
        diff = [x - y for x, y in zip(condition1, condition2)]
        # print(sum([d > 0 for d in diff]), sum([d < 0 for d in diff]))
        _, p_value = stats.wilcoxon(diff)
        p_values.append((conditions[i], conditions[j], p_value))

# Adjust p-values for multiple comparisons (Bonferroni correction)
adjusted_p_values = [p_value[2] * 24 for p_value in p_values]

# Print results
print(adjusted_p_values)
# for (condition1, condition2, p_value), adj_p_value in zip(p_values, adjusted_p_values):
# print(adj_p_value)
# print(f"{condition1} vs {condition2}: p-value = {p_value}, adjusted p-value = {adj_p_value}")

CM = 1 / 2.54
for col in data.columns:
    if col not in ["id", "fold_change"]:
        sns.set_style(style="ticks")
        _, axes = plt.subplots(1, 1, figsize=(17 * CM, 17 * CM))

        """
        sns.scatterplot(
            data,
            x="id",
            y="fold_change",
            hue=col,  # legend=False
        )
        axes.set_title(col)
        """

        data.sort_values("file_a", inplace=True)
        sns.scatterplot(data, x="id", y="jacc_value_spar", hue=col)
        # sns.scatterplot(data, x="comb", y="fold_change", hue="rep_type")
        # axes.set_ylim([0, 0.30])
        # axes.set_xlim([0, 0.30])

        plt.show()
