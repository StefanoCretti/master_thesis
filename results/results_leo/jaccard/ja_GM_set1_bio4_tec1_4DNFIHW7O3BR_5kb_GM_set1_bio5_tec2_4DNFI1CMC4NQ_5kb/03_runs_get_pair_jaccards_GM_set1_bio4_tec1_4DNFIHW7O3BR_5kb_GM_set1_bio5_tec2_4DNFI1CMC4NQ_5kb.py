"""Compute jaccard indexes at different steps on a pair of sparsified files"""

import sys
import time

from hicona import HiconaCooler
import pandas as pd

ALPHA_MODS = ["min", "max"]
DIST_THRESHOLDS = [10000000, 100000000, 25000000, 5000000, 50000000]
PERC_THRESHOLDS = [0, 0.01, 0.05, 0.1, 0.25]
ALPHA_THRESHOLDS = ["optimal", 0.05]
CHROMS = [f"chr{n}" for n in range(1, 23)] + ["chrX", "chrY"]


def replicate_type(name_a, name_b):
    """Given file names, define which type of replicate they are."""
    root_a = name_a.split(".", maxsplit=1)[0]
    root_b = name_b.split(".", maxsplit=1)[0]

    _, _, bio_a, tec_a, _, _ = root_a.split("_")
    _, _, bio_b, tec_b, _, _ = root_b.split("_")

    rep_type = None
    if bio_a != bio_b:
        rep_type = "bio"
    elif tec_a != tec_b:
        rep_type = "tec"

    if not rep_type:
        raise RuntimeError("Unable to define replicate type")

    return rep_type


def compute_jaccard(table_a, table_b, step_name):
    """Given two pixel tables, return jaccard index and stats."""
    shared = table_a.merge(table_b, on=["bin1_id", "bin2_id"], how="inner")
    jaccard = len(shared) / ((len(table_a) + len(table_b)) - len(shared))

    res_dict = {
        f"size_a_{step_name}": len(table_a),
        f"size_b_{step_name}": len(table_b),
        f"size_overlap_{step_name}": len(shared),
        f"jacc_value_{step_name}": jaccard,
    }

    return res_dict


def full_table_jacc(file_a, file_b):
    """Compute jaccard index on the two complete pixel tables."""
    table_a = file_a.pixels()[:]
    table_b = file_b.pixels()[:]
    return compute_jaccard(table_a, table_b, "full")


def intra_table_jacc(file_a, file_b):
    """Compute jaccard index using only intra-chromosomal pixels."""

    def get_intra(fhandle, chroms):
        """Retrieve a table containing only intra-chromosomal pixels."""
        intra_pix = []

        for chrom in chroms:
            chrom_chunk = fhandle.pixels().fetch(chrom)
            upper_bin = fhandle.extent(chrom)[1]
            chrom_chunk = chrom_chunk[chrom_chunk["bin2_id"] < upper_bin]
            intra_pix.append(chrom_chunk)

        return pd.concat(intra_pix, ignore_index=True)

    table_a = get_intra(file_a, CHROMS)
    table_b = get_intra(file_b, CHROMS)
    return compute_jaccard(table_a, table_b, "intra")


def filt_table_jacc(files, distance, percent):
    """Compute jaccard on a filtered pair of tables."""

    def get_filt_tab(file, distance, percent):
        """Retrieve filtered and sparsified table for a file."""

        # Containers to merge chromosome level-tables
        filt_tabs = []

        # Iterate through all pixel tables
        tables = file.tables(CHROMS, dist_thr=distance, quant_thr=percent)
        for pix_tab in tables:
            filt_tabs.append(pix_tab.data)

        # Merge the tables
        filt_tabs = pd.concat(filt_tabs, ignore_index=True)

        return filt_tabs

    # Get the filterd and sparsified tables for both files
    file_a, file_b = files
    filt_a = get_filt_tab(file_a, distance, percent)
    filt_b = get_filt_tab(file_b, distance, percent)

    # Compute jaccards on both filtered and sparsified tables
    filt_dict = compute_jaccard(filt_a, filt_b, "filt")

    return filt_dict


def spar_table_jacc(files, modality, distance, percent, alpha_thr):
    """Compute jaccard on a sparsified pair of tables."""

    def get_spar_tab(file, modality, distance, percent, alpha_thr):
        """Retrieve filtered and sparsified table for a file."""

        # Containers to merge chromosome level-tables
        spar_tabs = []

        # Iterate through all pixel tables
        tables = file.tables(CHROMS, dist_thr=distance, quant_thr=percent)
        for pix_tab in tables:
            pix_tab.alpha_column = f"alpha_{modality}"  # Set min/max

            # Compute optimal sparsification alpha if required
            if alpha_thr == "optimal":
                pix_tab.compute_opt_alpha(decimals=2, num_pts=11)

            # Save sparsified table
            spar_tabs.append(pix_tab.filter_alpha(alpha=alpha_thr))

        # Merge the tables
        spar_tabs = pd.concat(spar_tabs, ignore_index=True)

        return spar_tabs

    # Get the sparsified tables for both files and compute jaccard
    file_a, file_b = files
    spar_a = get_spar_tab(file_a, modality, distance, percent, alpha_thr)
    spar_b = get_spar_tab(file_b, modality, distance, percent, alpha_thr)
    spar_dict = compute_jaccard(spar_a, spar_b, "spar")

    return spar_dict


if __name__ == "__main__":
    # Create file handles

    start = time.time()

    FILE_A, FILE_B = sys.argv[1], sys.argv[2]
    handle_a = HiconaCooler(FILE_A)
    handle_b = HiconaCooler(FILE_B)
    handles = [handle_a, handle_b]

    # Define information shared by all results
    base_info = {
        "file_a": FILE_A.split("/")[-1],
        "file_b": FILE_B.split("/")[-1],
        "rep_type": replicate_type(FILE_A, FILE_B),
        "cell_type": FILE_A.split("_", maxsplit=1)[0].split("/")[-1],
        "resolution": handle_a.info["bin-size"],
    }
    # base_info.update(full_table_jacc(handle_a, handle_b))
    # base_info.update(intra_table_jacc(handle_a, handle_b))

    # Iterate parameter grid and store the results
    results = []
    for mod in ALPHA_MODS:
        for dist in DIST_THRESHOLDS:
            for perc in PERC_THRESHOLDS:
                for alpha in ALPHA_THRESHOLDS:
                    # Compute jaccards for filtered and sparsified files
                    filt = filt_table_jacc(handles, dist, perc)
                    spar = spar_table_jacc(handles, mod, dist, perc, alpha)

                    # Create a dictionary with the parameters used
                    params_dict = {
                        "dist_thr": dist,
                        "perc_thr": perc,
                        "alpha_mod": mod,
                        "alpha_thr": alpha,
                    }

                    # Merge all informations to create the individual row
                    res = dict(base_info)  # To make deep copy
                    res.update(params_dict)
                    res.update(filt)
                    res.update(spar)
                    results.append(res)

    # Save results
    root = FILE_A.split(".", maxsplit=1)[0]
    root += "_"
    root += FILE_A.split(".", maxsplit=1)[0].split("/")[-1]
    results = pd.DataFrame(results)
    results.to_csv(f"{root}_spar_stats.tsv", sep="\t", index=None)

    print(time.time() - start)
