import hicona
import sys

sys.setrecursionlimit(10000)

FILE_PATH = "4DNFIIFAUT24_10000.cool"
CHROMS = [f"chr{n}" for n in range(1,9)]
handle = hicona.HiconaCooler(FILE_PATH)
handle.create_tables(CHROMS, quant_thr=0.01, dist_thr=100_000_000)
