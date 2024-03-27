#!/bin/bash

#PBS -N sp_H1hESC_HiC_DdelI_4DNFIPVA6VYB_5kb
#PBS -o sp_H1hESC_HiC_DdelI_4DNFIPVA6VYB_5kb.out 
#PBS -e sp_H1hESC_HiC_DdelI_4DNFIPVA6VYB_5kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=15gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/scripts_H1hESC_HiC_DdelI_4DNFIPVA6VYB_5kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=H1hESC_HiC_DdelI_4DNFIPVA6VYB_5kb

python ./01_runs_sparsification_${pref}.py

conda deactivate


