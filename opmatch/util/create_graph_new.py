from typing import List, Union
import networkx as nx
import pandas as pd
import numpy as np
import itertools


def create_source_unexp_edges(unexp_ids:List[int])->List[tuple]:
    """Create edges between source node and unexposed patients 
    with capacity 1 and no weight (fully connected)"""
    edge_list = [('source', unexp_id, {'capacity':1, 'weight':0})\
         for unexp_id in unexp_ids]
    return edge_list

def append_case_sink_edges(edge_list:List[tuple], exposed_ids:List[int], 
                        matching_ratio:Union[int, str], 
                        matching_ratio_dic:Union[dict, None])->List[tuple]:
    """Append edges to edge_list which the exposed to the sink, 
    with capacities that result in constant 1:k matching or entire number matching."""
    if isinstance(matching_ratio, int):
        append_list = [(exp_id, 'sink', {'capacity':matching_ratio, 'weight':0})\
            for exp_id in exposed_ids]
    elif matching_ratio=='entire_number':
        assert isinstance(matching_ratio_dic, dict), 'entire_number_dic is not a dictionary'
        append_list = [(exp_id, 'sink', {'capacity':matching_ratio_dic[exp_id], 'weight':0})\
            for exp_id in exposed_ids]
    else:
        assert False, f'{matching_ratio} not implemented yet'
    return edge_list + append_list

def create_initial_edge_list(unexp_ids:List[int], 
                        exposed_ids:List[int], 
                        matching_ratio:Union[int, str],
                        matching_ratio_dic:Union[dict, None],
                        )->List[tuple]:
    """Create initial edge list, without connections between exposed and unexposed."""
    edge_list = create_source_unexp_edges(unexp_ids)
    edge_list = append_case_sink_edges(edge_list, exposed_ids, matching_ratio,
                                    matching_ratio_dic)
    return edge_list


def pairwise_abs_dist(a, b, dist_multiplier=1e3):
    """Compute absolute distance matrix
    Input: 1d arrays a and b
    Returns: len(a)xlen(b) distance matrix
    """
    return np.ndarray.astype(np.abs(a[np.newaxis,:] - b[:, np.newaxis])*dist_multiplier, int)

def create_exp_nexp_edge_ls(exp_ids, nexp_ids, exp_ps, nexp_ps):
    
    pdist_mat = pairwise_abs_dist(nexp_ps, exp_ps)
    pdist = np.ndarray.flatten(pdist_mat)
    cap_weight_ls = [{'capacity':1, 'weight':dist} for dist in pdist]
    exp_ids_comb, nexp_ids_comb= zip(*itertools.product(exp_ids, nexp_ids))
    exp_nexp_edge_ls = list(zip(exp_ids_comb,nexp_ids_comb, cap_weight_ls))
    return exp_nexp_edge_ls


def create_distance_edge_list_parallel(df:pd.DataFrame, 
    matching_ratio:Union[int, str],
    matching_ratio_dic:Union[dict, None]=None)->tuple: 
    """df: pd.DataFram
    treatment: boolean np.array (treatment/no treatment)
       ps: float np.array propensity scores"""
    df_exp = df[(df.exposed==1) & (df.matched==0)]
    df_nexp = df[(df.exposed==0) & (df.matched==0)]
    exp_ids = df_exp.index
    nexp_ids = df_nexp.index
    exp_ps = df_exp.ps.to_numpy()
    nexp_ps = df_nexp.ps.to_numpy()
    init_edge_ls = create_initial_edge_list(nexp_ids, exp_ids, matching_ratio,
                        matching_ratio_dic)
    edge_list_exp_nexp = create_exp_nexp_edge_ls(exp_ids, nexp_ids, exp_ps, nexp_ps)   
    edge_ls = init_edge_ls + edge_list_exp_nexp
    return edge_ls, exp_ids, nexp_ids

def create_di_graph(edge_ls:List[tuple])->nx.DiGraph:
    G = nx.DiGraph()
    G.add_edges_from(edge_ls)
    return G
