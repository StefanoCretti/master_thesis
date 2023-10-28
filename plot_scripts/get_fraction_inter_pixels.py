import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

FILE_PATH = sys.argv[1]
if not FILE_PATH:
    raise ValueError("File to process not provided")
FILE_ROOT = FILE_PATH.split("/")[-1].split(".")[0]
COLS_TO_KEEP = [
    "dist_thr",
    "perc_thr",
    "intra_pix_num",
    "experiment",
    "resolution",
    "init_pix_num",
]

data = pd.read_csv(FILE_PATH, sep="\t", index_col=0)
print(data)
data = data[COLS_TO_KEEP]
print(data)

data.drop_duplicates("init_pix_num", inplace=True)
data = data[~data["experiment"].str.contains("bio")]
print(data)

data["removed"] = 1 - data["intra_pix_num"] / data["init_pix_num"]
print(data)
print(data.groupby("resolution")["removed"].mean())
