"""Given a sparsified file compute its sparsification statistics."""

import sys
import time

from hicona import HiconaCooler
import numpy as np
import pandas as pd


# Setting defaults within file to avoid passing them with argv
OUTPUT_FOLD = "results"
ALPHA_MODS = ["min", "max"]
DIST_THRESHOLDS = [10000000, 100000000, 25000000, 5000000, 50000000]
#PERC_THRESHOLDS = [0, 0.01, 0.05, 0.1, 0.25]
PERC_THRESHOLDS = [0]
ALPHA_THRESHOLDS = ["optimal", 0.05]
CHROMS = [f"chr{n}" for n in range(1, 23)] + ["chrX", "chrY"]


def get_intra(fhandle, chroms):
    """Retrieve a table containing only intra-chromosomal pixels."""
    intra_pix = []

    for chrom in chroms:
        chrom_chunk = fhandle.pixels().fetch(chrom)
        upper_bin = fhandle.extent(chrom)[1]
        chrom_chunk = chrom_chunk[chrom_chunk["bin2_id"] < upper_bin]
        intra_pix.append(chrom_chunk)

    return pd.concat(intra_pix, ignore_index=True)


def dist_stats(dataf, resolution):
    """Return distance statistics."""
    distances = (dataf["bin2_id"] - dataf["bin1_id"]) * resolution
    return np.mean(distances), np.median(distances)


def compute_stats(fhandle, modality, distance, percentile, alpha_thr):
    """Given a file and a set of parameters, compute sparsification stats."""

    # Containers to merge chromosome level-tables
    filt_tabs = []
    spar_tabs = []

    # Iterate through all pixel tables
    tables = fhandle.tables(CHROMS, dist_thr=distance, quant_thr=percentile)
    for pix_tab in tables:
        pix_tab.alpha_column = f"alpha_{modality}"  # Set min/max

        # Compute optimal sparsification alpha if required
        if alpha_thr == "optimal":
            pix_tab.compute_opt_alpha(decimals=2, num_pts=11)

        # Save both the filtered and non filtered tables
        filt_tabs.append(pix_tab.data)
        spar_tabs.append(pix_tab.filter_alpha(alpha=alpha_thr))

    # Merge the tables
    filt_tabs = pd.concat(filt_tabs, ignore_index=True)
    spar_tabs = pd.concat(spar_tabs, ignore_index=True)

    # Compute distance statistics
    resolution = fhandle.info["bin-size"]
    filt_mean, filt_median = dist_stats(filt_tabs, resolution)
    spar_mean, spar_median = dist_stats(spar_tabs, resolution)

    # Create and return partial results dict
    res_dict = {
        "dist_thr": distance,
        "perc_thr": percentile,
        "alpha_mod": modality,
        "alpha_thr": alpha_thr,
        "filt_pix_num": len(filt_tabs),
        "spar_pix_num": len(spar_tabs),
        "mean_dist_filt": filt_mean,
        "mean_dist_spar": spar_mean,
        "median_dist_filt": filt_median,
        "median_dist_spar": spar_median,
    }

    return res_dict


if __name__ == "__main__":
    # Create handle
    FILE_PATH = sys.argv[1]
    name_root = FILE_PATH.split(".", maxsplit=1)[0]
    handle = HiconaCooler(FILE_PATH)

    # Compute distance statistics on the entire table
    full_table = handle.pixels()[:]
    init_mean, init_median = dist_stats(full_table, handle.info["bin-size"])
    del full_table

    intra_table = get_intra(handle, CHROMS)
    intra_pix_num = len(intra_table)
    intra_mean, intra_median = dist_stats(intra_table, handle.info["bin-size"])
    del intra_table

    # Store raw table stats which are the same for all params
    full_info = {
        "experiment": name_root,
        "resolution": handle.info["bin-size"],
        "init_pix_num": handle.info["nnz"],
        "mean_dist_init": init_mean,
        "median_dist_init": init_median,
        "intra_pix_num": intra_pix_num,
        "mean_intra_init": intra_mean,
        "median_intra_init": intra_median,
    }

    # Iterate parameter grid and store the results
    results = []
    for mod in ALPHA_MODS:
        for dist in DIST_THRESHOLDS:
            for perc in PERC_THRESHOLDS:
                for alpha in ALPHA_THRESHOLDS:
                    res = compute_stats(handle, mod, dist, perc, alpha)
                    res.update(full_info)
                    results.append(res)

    results = pd.DataFrame(results)
    results.to_csv(f"{name_root}_spar_stats.tsv", sep="\t", index=None)

