"""Better plotting of memory_profiler results."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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


# Plot
CM = 1 / 2.54
sns.set_style(style="ticks")
_, axes = plt.subplots(1, 1, figsize=(17 * CM, 8.5 * CM))

sns.lineplot(memos, x="time", y="memory", ax=axes, color="black", linewidth=1)
for _, row in funcs.iterrows():
    plt.axvline(x=row["time_start"], linestyle="dashed", color="red", linewidth=1)

axes.set(ylim=[0, 650])
axes.set_xlabel("Runtime (s)", fontsize=10)
axes.set_ylabel("RAM usage (MiB)", fontsize=10)
axes.tick_params(axis="both", labelsize=8)

plt.tight_layout()
plt.savefig("test.png", dpi=600, bbox_inches="tight")
