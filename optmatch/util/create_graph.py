from typing import List, Union
import networkx as nx
import pandas as pd
import numpy as np
import itertools
import multiprocessing as mp
import time

def create_source_unexp_edges(unexp_ids:List[int])->List[tuple]:
    """Create edges between source node and unexposed patients 
    with capacity 1 and no weight (fully connected)"""
    edge_list = [('source', unexp_id, {'capacity':1, 'weight':0})\
         for unexp_id in unexp_ids]
    return edge_list

def append_case_sink_edges(edge_list:List[tuple], exposed_ids:List[int], 
                        k:int)->List[tuple]:
    """Append edges to edge_list which the exposed to the sink, 
    with capacities that result in 1:k matching."""
    append_list = [(exp_id, 'sink', {'capacity':k, 'weight':0})\
        for exp_id in exposed_ids]
    return edge_list + append_list

def create_initial_edge_list(unexp_ids:List[int], 
                        exposed_ids:List[int], k:int)->List[tuple]:
    """Create initial edge list, without connections between exposed and unexposed."""
    edge_list = create_source_unexp_edges(unexp_ids)
    return append_case_sink_edges(edge_list, exposed_ids, k)

def compute_ps_abs_dist(exp_row, exp_id, nexp_row, nexp_id, dist_multiplier=1e5):
    """Helper function for create_distance_edge_list_parallel"""
    ps_abs_dist_int = int(np.abs(exp_row.ps-nexp_row.ps)*dist_multiplier)
    return (nexp_id, exp_id, {'capacity':1, 'weight':ps_abs_dist_int})

def create_distance_edge_list_parallel(treatment:np.array, ps:np.array, k:int): 
    """treatment: boolean np.array (treatment/no treatment)
       ps: float np.array propensity scores"""
    df = pd.DataFrame(np.transpose(np.stack([ps, treatment])), 
                    columns = ['ps', 'exposed'])
    df_exp = df[df['exposed']==1]
    df_nexp = df[df['exposed']==0]
    exp_ids = df_exp.index
    nexp_ids = df_nexp.index
    init_edge_ls = create_initial_edge_list(nexp_ids, exp_ids, k)
    exp_list = [(exp_row, exp_id) for exp_id, exp_row in df_exp.iterrows()]
    nexp_list = [(nexp_row, nexp_id) for nexp_id, nexp_row in df_nexp.iterrows()]
    exp_nexp_comb_ls = list(itertools.product(exp_list, nexp_list))
    mp_input = [(exp_row, exp_id, nexp_row, nexp_id) \
        for ((exp_row, exp_id), (nexp_row, nexp_id)) in exp_nexp_comb_ls]
    start = time.time()
    with mp.Pool() as pool:
        edge_list_exp_nexp = pool.starmap(compute_ps_abs_dist, mp_input)
    print(f'{time.time()-start:.2f} s')
    edge_ls = init_edge_ls + edge_list_exp_nexp
    return edge_ls

def create_di_graph(edge_ls:List[tuple])->nx.DiGraph:
    G = nx.DiGraph()
    G.add_edges_from(edge_ls)
    return G
