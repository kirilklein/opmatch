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


def get_min_cost_flow_dic(edge_ls:List, case_ids:List):
    """Create a digraph from edge_ls and run max_flow_min_cost algorithm.
    Returns a dictionary for every connection between case and not case,
    with a 0 (no flow) or 1 (1 flow), we will interpret the 1 flow connection as a match."""
    G = create_graph.create_di_graph(edge_ls)
    mincostFlow_dic = nx.max_flow_min_cost(G, 'source', 'sink')
    # remove all but the case-control edges
    del mincostFlow_dic['source']
    del mincostFlow_dic['sink']
    for case_id in case_ids:
        del mincostFlow_dic[case_id]
    return mincostFlow_dic

def get_case_control_dic(mincostFlow_dic:Dict):
    """From mincostFlow_dic creates a dictionary with case patients as keys
    and corresponding matched control patients as values."""
    case_control_dic = dict()
    for control in list(mincostFlow_dic.keys()):
        for case in list(mincostFlow_dic[control].keys()):
            if case not in case_control_dic.keys():
                case_control_dic[case] = []
            if mincostFlow_dic[control][case]==1:
                case_control_dic[case] = case_control_dic[case]+[control]
    return case_control_dic

def matching_dic_from_df(df:pd.DataFrame, matching_ratio:Union[int,str],
                        matching_ratio_dic:Union[dict, None]):
    edge_ls, case_ids, _ = create_graph.create_distance_edge_list_parallel(
                                        df, matching_ratio, matching_ratio_dic)
    mincostFlow_dic = get_min_cost_flow_dic(edge_ls, case_ids)
    case_control_dic = get_case_control_dic(mincostFlow_dic)
    return case_control_dic

def get_matching_ratio_dic(df, matching_ratio:str, 
                        min_matching_ratio:Union[int, None],
                        max_matching_ratio:Union[int, None]):
    df_case = df[df.case==1]
    if matching_ratio=='entire_number':
        df_case['matching_ratio'] = df_case.ps.map(lambda x: int((1-x)/x))
    else:
        assert False, f'{matching_ratio} matching not implemented yet'
    df_case.matching_ratio = df_case.matching_ratio.clip(
        upper=max_matching_ratio, lower=min_matching_ratio) 
    matching_ratio_dic = pd.Series(
        df_case.matching_ratio.values, index=df_case.index).to_dict()
    return matching_ratio_dic


def variable_matching(df):
    """Variable matching, match until some criterion is met (mean distance increases)"""
    avg_dist0 = np.ones(len(df[df.case==1]))*np.inf
    final_case_control_dic = {}
    i = 0
    while len(df[(df.case==1) & (df.matched==0)])!=0:
        if i==10:
            print('reached max num of iterations')
            break
        case_control_dic = matching_dic_from_df(df, matching_ratio=1)
        
        case_ids = np.array(list(case_control_dic.keys()))
        matched_control = utils.flatten(list(case_control_dic.values()))
        avg_dist = utils.compute_avg_dist(df, case_control_dic)
        matched_mask = avg_dist>avg_dist0
        if i!=0:
            unmatched_inds = np.argwhere(~matched_mask)
            print('include indices:', unmatched_inds)
            print(matched_mask)
            case_control_dic = {k:v for k,v in case_control_dic.items() if k in list(unmatched_inds)}
        final_case_control_dic = utils.combine_dicts(final_case_control_dic, case_control_dic)
        matched_case = case_ids[matched_mask]
        df.matched[matched_case] = 1
        df.matched[matched_control] = 1
        avg_dist0 = avg_dist
        i+=1
    return final_case_control_dic
    

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
        case_control_dic: keys-case patients
                      values-corresponding matched control patients
    """
    assert len(ps)==len(treatment), "len(ps)!=len(treatment)"
    matched = np.zeros(len(ps))
    df = pd.DataFrame(np.transpose(np.stack([ps, treatment, matched])), 
                    columns = ['ps', 'case', 'matched'])
    if isinstance(matching_ratio, int):
        case_control_dic = matching_dic_from_df(df, matching_ratio)
        return case_control_dic
    elif matching_ratio=='pair':
        matching_ratio=1  
        case_control_dic = matching_dic_from_df(df, matching_ratio)
        return case_control_dic
    elif matching_ratio=='variable':
        print("Ubiquitous implementation, mean distance will always increase")
        final_case_control_dic = variable_matching(df)
        return final_case_control_dic
    elif matching_ratio=='entire_number':
        "https://sci-hub.mksa.top/https://doi.org/10.1002/sim.6593"
        matching_ratio_dic = get_matching_ratio_dic(df, 
            matching_ratio, min_matching_ratio, max_matching_ratio)
        case_control_dic = matching_dic_from_df(df, 
            matching_ratio, matching_ratio_dic)
        return case_control_dic
    elif matching_ratio=='fine_balance':
        pass
    elif matching_ratio=='full':
        pass
        
