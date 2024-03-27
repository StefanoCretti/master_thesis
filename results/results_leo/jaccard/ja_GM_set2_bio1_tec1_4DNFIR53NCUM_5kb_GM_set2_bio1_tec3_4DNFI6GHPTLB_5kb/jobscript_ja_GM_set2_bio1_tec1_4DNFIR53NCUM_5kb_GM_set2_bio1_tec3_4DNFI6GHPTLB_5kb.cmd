#!/bin/bash

#PBS -N ja_XXXprefXXX
#PBS -o ja_XXXprefXXX.out 
#PBS -e ja_XXXprefXXX.err
#PBS -q CIBIO_cpuQ 
#PBS -l select=1:mem=30gb 

cd /shares/CIBIO-Storage/GROUPS/sharedCE/Leonardo/HiCONA/articolo/ja_GM_set2_bio1_tec1_4DNFIR53NCUM_5kb_GM_set2_bio1_tec3_4DNFI6GHPTLB_5kb
export PATH=$HOME/miniconda3/bin:$PATH

source activate hicona
# Run 

pref1=GM_set2_bio1_tec1_4DNFIR53NCUM_5kb
pref2=GM_set2_bio1_tec3_4DNFI6GHPTLB_5kb

python ./03_runs_get_pair_jaccards_${pref1}_${pref2}.py ${pref1}.cool ${pref2}.cool

conda deactivate


