import os, sys
from re import L
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'opmatch'))
from util import create_graph, utils
import networkx as nx
import numpy as np
from typing import Dict, List, Union
import pandas as pd


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

def matching_dic_from_df(df:pd.DataFrame, matching_ratio:Union[int,str],
                        matching_ratio_dic:Union[dict, None]):
    edge_ls, exp_ids, _ = create_graph.create_distance_edge_list_parallel(
                                        df, matching_ratio, matching_ratio_dic)
    mincostFlow_dic = get_min_cost_flow_dic(edge_ls, exp_ids)
    exp_nexp_dic = get_exp_nexp_dic(mincostFlow_dic)
    return exp_nexp_dic

def get_matching_ratio_dic(df, matching_ratio:str, 
                        min_matching_ratio:Union[int, None],
                        max_matching_ratio:Union[int, None]):
    df_exp = df[df.exposed==1]
    if matching_ratio=='entire_number':
        df_exp['matching_ratio'] = df_exp.ps.map(lambda x: int((1-x)/x))
    else:
        assert False, f'{matching_ratio} matching not implemented yet'
    df_exp.matching_ratio = df_exp.matching_ratio.clip(
        upper=max_matching_ratio, lower=min_matching_ratio) 
    matching_ratio_dic = pd.Series(
        df_exp.matching_ratio.values, index=df_exp.index).to_dict()
    return matching_ratio_dic


def variable_matching(df):
    """Variable matching, match until some criterion is met (mean distance increases)"""
    avg_dist0 = np.ones(len(df[df.exposed==1]))*np.inf
    final_exp_nexp_dic = {}
    i = 0
    while len(df[(df.exposed==1) & (df.matched==0)])!=0:
        if i==10:
            print('reached max num of iterations')
            break
        exp_nexp_dic = matching_dic_from_df(df, matching_ratio=1)
        
        exp_ids = np.array(list(exp_nexp_dic.keys()))
        matched_nexp = utils.flatten(list(exp_nexp_dic.values()))
        avg_dist = utils.compute_avg_dist(df, exp_nexp_dic)
        matched_mask = avg_dist>avg_dist0
        if i!=0:
            unmatched_inds = np.argwhere(~matched_mask)
            print('include indices:', unmatched_inds)
            print(matched_mask)
            exp_nexp_dic = {k:v for k,v in exp_nexp_dic.items() if k in list(unmatched_inds)}
        final_exp_nexp_dic = utils.combine_dicts(final_exp_nexp_dic, exp_nexp_dic)
        matched_exp = exp_ids[matched_mask]
        df.matched[matched_exp] = 1
        df.matched[matched_nexp] = 1
        avg_dist0 = avg_dist
        i+=1
    return final_exp_nexp_dic
    

def match_parallel(ps:np.array, treatment:np.array, matching_ratio:Union[int,str],
    min_matching_ratio:Union[int, None]=None,
    max_matching_ratio:Union[int, None]=None):
    """
    Input:
        ps: propensity scores ()
        treatment: boolean array 
        matching ratio: matching coefficient, or matching_type
            pair, full, entire_number, fine_balance
    Returns:
        exp_nexp_dic: keys-exposed patients
                      values-corresponding matched unexposed patients
    """
    assert len(ps)==len(treatment), "len(ps)!=len(treatment)"
    matched = np.zeros(len(ps))
    df = pd.DataFrame(np.transpose(np.stack([ps, treatment, matched])), 
                    columns = ['ps', 'exposed', 'matched'])
    if isinstance(matching_ratio, int):
        exp_nexp_dic = matching_dic_from_df(df, matching_ratio)
        return exp_nexp_dic
    elif matching_ratio=='pair':
        matching_ratio=1  
        exp_nexp_dic = matching_dic_from_df(df, matching_ratio)
        return exp_nexp_dic
    elif matching_ratio=='variable':
        print("Ubiquitous implementation, mean distance will always increase")
        final_exp_nexp_dic = variable_matching(df)
        return final_exp_nexp_dic
    elif matching_ratio=='entire_number':
        "https://sci-hub.mksa.top/https://doi.org/10.1002/sim.6593"
        matching_ratio_dic = get_matching_ratio_dic(df, 
            matching_ratio, min_matching_ratio, max_matching_ratio)
        exp_nexp_dic = matching_dic_from_df(df, 
            matching_ratio, matching_ratio_dic)
        return exp_nexp_dic
    elif matching_ratio=='fine_balance':
        pass
    elif matching_ratio=='full':
        pass
        
