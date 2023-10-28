#!/bin/bash

#PBS -N sp_GM_set1_bio7_tec2_4DNFIXR9BRGT_5kb
#PBS -o sp_GM_set1_bio7_tec2_4DNFIXR9BRGT_5kb.out 
#PBS -e sp_GM_set1_bio7_tec2_4DNFIXR9BRGT_5kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=15gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/scripts_GM_set1_bio7_tec2_4DNFIXR9BRGT_5kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=GM_set1_bio7_tec2_4DNFIXR9BRGT_5kb

python ./01_runs_sparsification_${pref}.py

conda deactivate



