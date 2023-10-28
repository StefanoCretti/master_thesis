"""Given a sparsified file compute its sparsification statistics."""

import sys
import time
import cooler
from hicona import HiconaCooler
import numpy as np
import pandas as pd


# Setting defaults within file to avoid passing them with argv
OUTPUT_FOLD = "results"
ALPHA_MODS = ["min", "max"]
DIST_THRESHOLDS = [100000000, 25000000, 50000000]
PERC_THRESHOLDS = [0, 0.01]
ALPHA_THRESHOLDS = ["optimal"]
CHROMS = [f"chr{n}" for n in range(1, 23)] + ["chrX", "chrY"]


def return_tabs(fhandle, modality, distance, percentile, alpha_thr):
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

    return filt_tabs , spar_tabs


if __name__ == "__main__":
    # Create handle
    FILE_PATH = sys.argv[1]
    name_root = FILE_PATH.split(".", maxsplit=1)[0]
    handle = HiconaCooler(FILE_PATH)
    bins=handle.bins()[:]

    # Compute anno enrichment on the entire table
    pix = handle.pixels()[:]
    anno=cooler.annotate(pix,bins)
    anno_edges=anno.groupby(['chromhmm_state1','chromhmm_state2']).count()['count']
    anno_edges.to_csv(f'{name_root}_annotations_edges_tot.tsv',sep='\t')

    # Iterate parameter grid and store the results
  
    for mod in ALPHA_MODS:
        for dist in DIST_THRESHOLDS:
            for perc in PERC_THRESHOLDS:
                for alpha in ALPHA_THRESHOLDS:
                    pix_filt,pix_spar=return_tabs(handle, mod, dist, perc, alpha)

                    anno_f=cooler.annotate(pix_filt,bins)
                    anno_edges_f=anno_f.groupby(['chromhmm_state1','chromhmm_state2']).count()['count']
                    anno_edges_f.to_csv(f'{name_root}_annotations_edges_filter_alpha_{mod}_{dist}bp_{perc}thr.tsv',sep='\t')


                    anno_s=cooler.annotate(pix_spar,bins)
                    anno_edges_s=anno_s.groupby(['chromhmm_state1','chromhmm_state2']).count()['count']
                    anno_edges_s.to_csv(f'{name_root}_annotations_edges_spar_alpha_{mod}_{dist}bp_{perc}thr.tsv',sep='\t')
