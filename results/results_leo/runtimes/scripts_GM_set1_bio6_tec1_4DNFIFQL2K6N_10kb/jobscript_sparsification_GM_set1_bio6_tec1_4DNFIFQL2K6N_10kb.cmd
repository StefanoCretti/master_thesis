#!/bin/bash

#PBS -N sp_GM_set1_bio6_tec1_4DNFIFQL2K6N_10kb
#PBS -o sp_GM_set1_bio6_tec1_4DNFIFQL2K6N_10kb.out 
#PBS -e sp_GM_set1_bio6_tec1_4DNFIFQL2K6N_10kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=15gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/scripts_GM_set1_bio6_tec1_4DNFIFQL2K6N_10kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=GM_set1_bio6_tec1_4DNFIFQL2K6N_10kb

python ./01_runs_sparsification_${pref}.py

conda deactivate



