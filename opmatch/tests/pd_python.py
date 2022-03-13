import numpy as np
from time import time
import itertools
import networkx as nx
import timeit

exp_ps = np.arange(1,3)*.1
nexp_ps = np.arange(4,7)*.1

exp_ids = exp_ps.astype(str)#['1', '2', '3']
nexp_ids = nexp_ps.astype(str)#['5','6',]

s = time()
def pairwise_abs_dist(a, b):
    """Compute absolute distance matrix
    Input: 1d arrays a and b
    Returns: len(a)xlen(b) distance matrix
    """
    return np.ndarray.astype(np.abs(a[np.newaxis,:] - b[:, np.newaxis])*1e1, int)
print(pairwise_abs_dist(exp_ps, nexp_ps))
def create_exp_nexp_edge_ls(exp_ids, nexp_ids, exp_ps, nexp_ps):
    
    pdist_mat = pairwise_abs_dist(nexp_ps, exp_ps)
    pdist = np.ndarray.flatten(pdist_mat)
    cap_weight_ls = [{'capacity':1, 'weight':dist} for dist in pdist]
    exp_ids_comb, nexp_ids_comb= zip(*itertools.product(exp_ids, nexp_ids))
    exp_nexp_edge_ls = list(zip(exp_ids_comb,nexp_ids_comb, cap_weight_ls))
    return exp_nexp_edge_ls
exp_nexp_edge_ls = create_exp_nexp_edge_ls(exp_ids, nexp_ids, exp_ps, nexp_ps)
#print(exp_nexp_edge_ls)
G = nx.DiGraph()
G.add_edges_from(exp_nexp_edge_ls)
print(time()-s)
