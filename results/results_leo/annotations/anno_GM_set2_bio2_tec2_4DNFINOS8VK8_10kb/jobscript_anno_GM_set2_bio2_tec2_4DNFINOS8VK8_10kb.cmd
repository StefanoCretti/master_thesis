#!/bin/bash

#PBS -N an_GM_set2_bio2_tec2_4DNFINOS8VK8_10kb
#PBS -o an_GM_set2_bio2_tec2_4DNFINOS8VK8_10kb.out 
#PBS -e an_GM_set2_bio2_tec2_4DNFINOS8VK8_10kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=30gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/anno_GM_set2_bio2_tec2_4DNFINOS8VK8_10kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=GM_set2_bio2_tec2_4DNFINOS8VK8_10kb

python ./04_runs_anno_edges_${pref}.py ${pref}.cool

conda deactivate



