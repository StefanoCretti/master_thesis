#!/bin/bash

#PBS -N sp_GM_set2_bio1_tec3_4DNFI6GHPTLB_5kb
#PBS -o sp_GM_set2_bio1_tec3_4DNFI6GHPTLB_5kb.out 
#PBS -e sp_GM_set2_bio1_tec3_4DNFI6GHPTLB_5kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=30gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/stats_0_GM_set2_bio1_tec3_4DNFI6GHPTLB_5kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=GM_set2_bio1_tec3_4DNFI6GHPTLB_5kb

python ./02_runs_get_sparsification_statistics_${pref}.py ${pref}.cool

conda deactivate



