from util import create_graph
import networkx as nx
import numpy as np
import sys
from typing import Dict, List

def get_min_cost_flow_dic(edge_ls:List, exp_ids:List):
    G = create_graph.create_di_graph(edge_ls)
    print(G)
    mincostFlow_dic = nx.max_flow_min_cost(G, 'source', 'sink')
    # remove all but the exp-nexp edges
    del mincostFlow_dic['source']
    del mincostFlow_dic['sink']
    for exp_id in exp_ids:
        del mincostFlow_dic[exp_id]
    return mincostFlow_dic

def get_exp_nexp_dic(mincostFlow_dic:Dict):
    exp_nexp_dic = dict()
    for nexp in list(mincostFlow_dic.keys()):
        for exp in list(mincostFlow_dic[nexp].keys()):
            if exp not in exp_nexp_dic.keys():
                exp_nexp_dic[exp] = []
            if mincostFlow_dic[nexp][exp]==1:
                exp_nexp_dic[exp] = exp_nexp_dic[exp]+[nexp]
    return exp_nexp_dic

def match_parallel(ps:np.array, treatment:np.array, k:int):
    """Input:
    ps: propensity scores ()
    treatment: boolean array 
    k: matching coefficient
    """
    assert len(ps)==len(treatment), "len(ps)!=len(treatment)"
    edge_ls, exp_ids, nexp_ids = create_graph.create_distance_edge_list_parallel(
                                    treatment, ps, k)
    mincostFlow_dic = get_min_cost_flow_dic(edge_ls, exp_ids)
    exp_nexp_dic = get_exp_nexp_dic(mincostFlow_dic)
    return exp_nexp_dic
    
def test_func(x):
    print(x)

if __name__ == '__main__':
    x = sys.argv[1]
    test_func(x)