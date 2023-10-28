#!/bin/bash

#PBS -N sp_IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_10kb
#PBS -o sp_IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_10kb.out 
#PBS -e sp_IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_10kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=30gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/stats_0_IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_10kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_10kb

python ./02_runs_get_sparsification_statistics_${pref}.py ${pref}.cool

conda deactivate



