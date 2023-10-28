#!/bin/bash

#PBS -N sp_IMR90_set1_bio1_tec1_4DNFIW2BKSNF_10kb
#PBS -o sp_IMR90_set1_bio1_tec1_4DNFIW2BKSNF_10kb.out 
#PBS -e sp_IMR90_set1_bio1_tec1_4DNFIW2BKSNF_10kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=15gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/scripts_IMR90_set1_bio1_tec1_4DNFIW2BKSNF_10kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=IMR90_set1_bio1_tec1_4DNFIW2BKSNF_10kb

python ./01_runs_sparsification_${pref}.py

conda deactivate



