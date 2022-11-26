import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'opmatch'))
from opmatch.util import preprocess
import multiprocessing as mp
import numpy as np

def quad(x):
    return x**2
def mp_func(arg):
    x = np.arange(arg)
    with mp.Pool() as pool:
        result_ = pool.map(quad, x)
    print(result_)
if __name__=='__main__':
        arg = int(sys.argv[1])
        mp_func(arg)