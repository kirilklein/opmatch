import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'optmatch'))
from util import create_graph
import networkx as nx
import numpy as np
from typing import Dict, List
import pickle
import tempfile

def get_min_cost_flow_dic(edge_ls:List, exp_ids:List):
    """Create a digraph from edge_ls and run max_flow_min_cost algorithm.
    Returns a dictionary for every connection between exposed and not exposed,
    with a 0 (no flow) or 1 (1 flow), we will interpret the 1 flow connection as a match."""
    G = create_graph.create_di_graph(edge_ls)
    mincostFlow_dic = nx.max_flow_min_cost(G, 'source', 'sink')
    # remove all but the exp-nexp edges
    del mincostFlow_dic['source']
    del mincostFlow_dic['sink']
    for exp_id in exp_ids:
        del mincostFlow_dic[exp_id]
    return mincostFlow_dic

def get_exp_nexp_dic(mincostFlow_dic:Dict):
    """From mincostFlow_dic creates a dictionary with exposed patients as keys
    and corresponding matched unexposed patients as values."""
    exp_nexp_dic = dict()
    for nexp in list(mincostFlow_dic.keys()):
        for exp in list(mincostFlow_dic[nexp].keys()):
            if exp not in exp_nexp_dic.keys():
                exp_nexp_dic[exp] = []
            if mincostFlow_dic[nexp][exp]==1:
                exp_nexp_dic[exp] = exp_nexp_dic[exp]+[nexp]
    return exp_nexp_dic

def match_parallel(ps:np.array, treatment:np.array, k:int):
    """
    Input:
        ps: propensity scores ()
        treatment: boolean array 
        k: matching coefficient
    Returns:
        exp_nexp_dic: keys-exposed patients
                      values-corresponding matched unexposed patients
    """
    assert len(ps)==len(treatment), "len(ps)!=len(treatment)"
    edge_ls, exp_ids, nexp_ids = create_graph.create_distance_edge_list_parallel(
                                    treatment, ps, k)
    mincostFlow_dic = get_min_cost_flow_dic(edge_ls, exp_ids)
    exp_nexp_dic = get_exp_nexp_dic(mincostFlow_dic)
    return exp_nexp_dic
    
def main():
    ps_path = sys.argv[1]
    trt_path = sys.argv[2]
    k = int(sys.argv[3])
    ps = np.load(ps_path)
    trt = np.load(trt_path)
    exp_nexp_dic = match_parallel(ps, trt, k)
    if os.path.exists(ps_path):
        os.remove(ps_path)
    if os.path.exists(trt_path):
        os.remove(trt_path)
    dic_handle, dic_path = tempfile.mkstemp(suffix='.pkl')
    os.close(dic_handle)
    with open(dic_path, 'wb') as f:
        pickle.dump(exp_nexp_dic, f)
    return dic_path
if __name__ == '__main__':
    print(main())