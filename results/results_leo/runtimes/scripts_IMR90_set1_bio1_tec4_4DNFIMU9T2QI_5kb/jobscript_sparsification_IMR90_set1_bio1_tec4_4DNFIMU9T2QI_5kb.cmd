#!/bin/bash

#PBS -N sp_IMR90_set1_bio1_tec4_4DNFIMU9T2QI_5kb
#PBS -o sp_IMR90_set1_bio1_tec4_4DNFIMU9T2QI_5kb.out 
#PBS -e sp_IMR90_set1_bio1_tec4_4DNFIMU9T2QI_5kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=15gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/scripts_IMR90_set1_bio1_tec4_4DNFIMU9T2QI_5kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=IMR90_set1_bio1_tec4_4DNFIMU9T2QI_5kb

python ./01_runs_sparsification_${pref}.py

conda deactivate



