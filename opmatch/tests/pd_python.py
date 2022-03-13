import numpy as np
from time import time
import itertools
import networkx as nx
import timeit
def pairwise_numpy(a, b):
    return np.abs(a[np.newaxis,:] - b[:, np.newaxis])
ps_exp = np.arange(1,3)
ps_nexp = np.arange(4,7)

exp_ids = ps_exp.astype(str)#['1', '2', '3']
nexp_ids = ps_nexp.astype(str)#['5','6',]
z_l = [{'capacity':1,}]


s = time()
pd_mat = pairwise_numpy(ps_nexp,ps_exp)
pd = np.ndarray.flatten(pd_mat)
cap_weight_ls = [{'capacity':1, 'weight':d} for d in pd]
#print(a)
#print(np.ndarray.flatten(a)) 
exp_ids_comb, nexp_ids_comb= zip(*itertools.product(exp_ids, nexp_ids))


edge_ls = list(zip(exp_ids_comb,nexp_ids_comb, cap_weight_ls))

print(edge_ls)
G = nx.DiGraph()
G.add_edges_from(edge_ls)
print(time()-s)
