#!/bin/bash

#PBS -N sp_H1hESC_HiC_HindIII_4DNFIUTE4F4B_5kb
#PBS -o sp_H1hESC_HiC_HindIII_4DNFIUTE4F4B_5kb.out 
#PBS -e sp_H1hESC_HiC_HindIII_4DNFIUTE4F4B_5kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=30gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/stats_H1hESC_HiC_HindIII_4DNFIUTE4F4B_5kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=H1hESC_HiC_HindIII_4DNFIUTE4F4B_5kb

python ./02_runs_get_sparsification_statistics_${pref}.py ${pref}.cool

conda deactivate



