#!/bin/bash

#PBS -N sp_GM_set1_bio5_tec2_4DNFI1CMC4NQ_5kb
#PBS -o sp_GM_set1_bio5_tec2_4DNFI1CMC4NQ_5kb.out 
#PBS -e sp_GM_set1_bio5_tec2_4DNFI1CMC4NQ_5kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=30gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/stats_GM_set1_bio5_tec2_4DNFI1CMC4NQ_5kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=GM_set1_bio5_tec2_4DNFI1CMC4NQ_5kb

python ./02_runs_get_sparsification_statistics_${pref}.py ${pref}.cool

conda deactivate



