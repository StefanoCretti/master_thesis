#!/bin/bash

#PBS -N sp_HMEC_HiC_combined_4DNFIIFAUT24_10kb
#PBS -o sp_HMEC_HiC_combined_4DNFIIFAUT24_10kb.out 
#PBS -e sp_HMEC_HiC_combined_4DNFIIFAUT24_10kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=30gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/stats_HMEC_HiC_combined_4DNFIIFAUT24_10kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=HMEC_HiC_combined_4DNFIIFAUT24_10kb

python ./02_runs_get_sparsification_statistics_${pref}.py ${pref}.cool

conda deactivate



