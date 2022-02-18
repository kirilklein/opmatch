from util import fit_ps, create_graph, preprocess
import networkx as nx
import numpy as np
import pandas as pd
from typing import Union, List


def match(ps:np.array[float], treatment:np.array[bool], k:int):
    """Input:
    ps: propensity scores ()
    treatment: boolean array 
    k: matching coefficient
    """
    assert len(ps)==len(treatment), "len(ps)!=len(treatment)"
    edge_list = create_graph.create_distance_edge_list_parallel(
        treatment, ps, k)
    G = create_graph.create_di_graph(edge_list)
    mincostFlow_dic = nx.max_flow_min_cost(G, 'source', 'sink')
    return mincostFlow_dic

if __name__ == '__main__':
    print('hi')