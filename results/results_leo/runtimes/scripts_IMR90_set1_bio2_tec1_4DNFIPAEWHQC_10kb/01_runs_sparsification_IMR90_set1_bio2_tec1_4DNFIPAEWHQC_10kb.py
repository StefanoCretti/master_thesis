from hicona import hicona_cooler
import time
import pandas as pd

pref='IMR90_set1_bio2_tec1_4DNFIPAEWHQC_10kb'

cell=f'{pref}.cool'




c=hicona_cooler.HiconaCooler(f'{cell}')

dist_thr=[5e6,10e6,25e6,50e6,100e6]
quant_thr=[0,0.01,0.05,0.1,0.25]

DF=pd.DataFrame()

for d in dist_thr:
    d=int(d)
    for n in quant_thr:
        t0=time.time()
        print('distance threshold =',d,'\n'+'counts threshold =',n)
        c.create_tables(quant_thr=n, dist_thr=d)
        t=time.time()-t0
        print('''\n \n ''',  t)
        df=pd.DataFrame([d,n,t],index=['distance_thr','counts_thr','time (s)']).T
        DF=pd.concat([DF,df])

DF.to_csv(f'{cell}_sparsification_stats.txt',sep='\t')
