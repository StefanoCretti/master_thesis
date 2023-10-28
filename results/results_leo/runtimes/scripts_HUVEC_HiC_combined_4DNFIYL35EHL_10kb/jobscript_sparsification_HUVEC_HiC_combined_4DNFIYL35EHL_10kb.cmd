#!/bin/bash

#PBS -N sp_HUVEC_HiC_combined_4DNFIYL35EHL_10kb
#PBS -o sp_HUVEC_HiC_combined_4DNFIYL35EHL_10kb.out 
#PBS -e sp_HUVEC_HiC_combined_4DNFIYL35EHL_10kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=15gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/scripts_HUVEC_HiC_combined_4DNFIYL35EHL_10kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=HUVEC_HiC_combined_4DNFIYL35EHL_10kb

python ./01_runs_sparsification_${pref}.py

conda deactivate



