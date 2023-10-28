#!/bin/bash

#PBS -N an_IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_5kb
#PBS -o an_IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_5kb.out 
#PBS -e an_IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_5kb.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=30gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/anno_IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_5kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref=IMR90_set1_bio1_tec5_4DNFIAAUZ7EP_5kb

python ./04_runs_anno_edges_${pref}.py ${pref}.cool

conda deactivate



