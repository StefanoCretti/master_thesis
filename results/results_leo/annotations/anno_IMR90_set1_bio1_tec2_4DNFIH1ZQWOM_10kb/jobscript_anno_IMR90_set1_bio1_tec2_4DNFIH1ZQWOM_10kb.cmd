#!/bin/bash

#PBS -N an_IMR90_set1_bio1_tec2_4DNFIH1ZQWOM_10kb
#PBS -o an_IMR90_set1_bio1_tec2_4DNFIH1ZQWOM_10kb.out 
#PBS -e an_IMR90_set1_bio1_tec2_4DNFIH1ZQWOM_10kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=30gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/anno_IMR90_set1_bio1_tec2_4DNFIH1ZQWOM_10kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=IMR90_set1_bio1_tec2_4DNFIH1ZQWOM_10kb

python ./04_runs_anno_edges_${pref}.py ${pref}.cool

conda deactivate



