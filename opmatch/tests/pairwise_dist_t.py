import numpy as np
import random
import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'opmatch'))
import pyximport
pyximport.install()
from util.pairwise_dist_cython import pairwise_distance

#r = np.array([random.randrange(1, 1000) for _ in range(0, 1000)], dtype=float)
r = np.array([1, 0, 3.])
lr = len(r)
pd = pairwise_distance(r)
ind = np.triu_indices(lr)
values = np.arange(lr**2).reshape(lr,lr)[ind]
result = np.zeros((lr,lr),int)
result[ind]=pd
print(result)