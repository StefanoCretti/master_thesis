import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def retain_by_param(dataf):
    # data = dataf[dataf["resolution"] == 10000]

    grid = sns.FacetGrid(data, col="perc_thr", row="dist_thr")
    grid.map_dataframe(
        sns.lineplot,
        x="step",
        y="pix_num",
        hue="cell_type",
    )

    grid.add_legend()
    plt.yscale("log")
    plt.yticks([10**i for i in range(5, 10)], [f"10^{i}" for i in range(5, 10)])
    plt.show()


if __name__ == "__main__":
    OUT_FOLDER = "plots/retained_pixels"
    FILE_PATH = sys.argv[1]
    if not FILE_PATH:
        raise ValueError("File to process not provided")
    FILE_ROOT = FILE_PATH.split("/")[-1].split(".")[0]

    COLS_TO_KEEP = [
        "dist_thr",
        "perc_thr",
        "alpha_mod",
        "alpha_thr",
        "experiment",
        "resolution",
        "filt_pix_num",
        "spar_pix_num",
        "init_pix_num",
        "intra_pix_num",
    ]

    data = pd.read_csv(FILE_PATH, sep="\t", index_col=0)
    data = data[COLS_TO_KEEP]
    data["dist_thr"] = data["dist_thr"] / 1000000
    data["cell_type"] = data["experiment"].str.split("_", expand=True)[0]
    data["enzyme"] = data["experiment"].str.split("_", expand=True)[2]
    data["enzyme"] = data["enzyme"].str.replace("combined", "MboI")
    data["enzyme"] = data["enzyme"].str.replace(r"bio\d", "MboI", regex=True)
    data["cell_type"] = data["cell_type"] + " " + data["enzyme"]
    data["is_replicate"] = data["experiment"].str.contains("bio")

    data = data[data["alpha_thr"] == "optimal"]
    data = data[data["alpha_mod"] == "max"]
    data = data[data["resolution"] == 10000]

    # data["is_replicate"] = data["experiment"].str.contains("bio")
    # print(data[data["is_replicate"] == True][["experiment"]].nunique())

    data = pd.melt(
        data,
        id_vars=[v for v in data.columns if not v.endswith("pix_num")],
        var_name="step",
        value_name="pix_num",
    )
    data["step"] = data["step"].str.replace("_pix_num", "", regex=True)
    STEP_ORDER = ("init", "intra", "filt", "spar")
    data = data[data["step"].isin(STEP_ORDER)].sort_values(
        by=["step"], key=lambda x: x.map({v: i for i, v in enumerate(STEP_ORDER)})
    )
    data.query("is_replicate == False", inplace=True)

    print(data)
    sys.exit()
    retain_by_param(data)
