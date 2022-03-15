import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from collections import defaultdict
from scipy.spatial.distance import cdist
from typing import List
import metrics


def expand_dist_mat(dist_mat:np.ndarray, min_mr:int, 
                max_mr:int, n_exp:int, n_nexp:int, 
                n_controls:int):
    exp_nexp_dmat = np.tile(dist_mat, max_mr)
    exp_nexp_dmat = np.reshape(exp_nexp_dmat, 
                newshape=(n_exp*max_mr, n_nexp))
    K = n_exp * max_mr - n_controls
    assert isinstance(K, int), 'make sure that max_mr and n_controls are integers'
    exp_inf = np.ones(shape=(min_mr, K))*np.inf
    if (max_mr-min_mr)>=1:
        exp_zeros = np.zeros(shape=(max_mr-min_mr, K))
        exp_mat = np.concatenate([exp_inf, exp_zeros],  axis=0)
    else:
        exp_mat = exp_inf
    exp_mat = np.tile(exp_mat, (n_exp,1))
    exp_mat = np.reshape(exp_mat, newshape=(max_mr*n_exp, K))
    final_dist_mat = np.concatenate([exp_nexp_dmat, exp_mat], axis=1)
    return final_dist_mat

def get_exp_nexp_dic(match_result:tuple, exp_ids:list, 
        nexp_ids:list, max_mr:int)->dict:
    rep_exp_ids = np.repeat(exp_ids, max_mr)
    exp_nums, nexp_nums = match_result
    mask = nexp_nums<len(nexp_ids) # remove sinks
    exp_nums = exp_nums[mask]
    nexp_nums = nexp_nums[mask]

    nexp_exp_dic = {nexp_ids[nexp_num]:rep_exp_ids[exp_num] for nexp_num, exp_num in \
        zip(nexp_nums, exp_nums) if nexp_num<len(nexp_ids)}
    exp_nexp_dic = defaultdict(list)
    for key, value in nexp_exp_dic.items():
        exp_nexp_dic[value].append(key)
    return exp_nexp_dic


def match(df:pd.DataFrame, min_mr:int, 
         max_mr:int, n_controls:int, metric:str='PS',
         var_cols:List[str]=None)->dict:
    
    df_exp = df[(df.exposed==1)]
    df_nexp = df[(df.exposed==0)]
    exp_ids = df_exp.index
    nexp_ids = df_nexp.index
    
    n_exp = len(exp_ids)
    n_nexp = len(nexp_ids)

    assert n_controls<=n_nexp, f'n_controls>n_nexp={n_nexp}'
    assert max_mr<=(n_controls-n_exp+1), f'max_mr>(total_controls-n_exp+1)={n_controls-n_exp+1}'
    assert max_mr>=np.ceil(n_controls/n_exp), f'max_mr<np.ceil(total_controls/n_exp)={np.ceil(n_controls/n_exp)}'
    assert min_mr<=np.floor(n_controls/n_exp), f'min_mr>np.floor(n_controls/n_exp)={np.floor(n_controls/n_exp)}'
    assert min_mr>=1, 'min_mr<1'
    
    if metric=='PS':
        exp_ps = df_exp.ps.to_numpy()
        nexp_ps = df_nexp.ps.to_numpy()
        dist_mat = metrics.create_ps_dist_matrix(exp_ps, nexp_ps,n_exp, n_nexp, 
                                min_mr, max_mr, n_controls)
    elif metric=='Mahalanobis':
        assert not isinstance(var_cols, type(None)), 'You need to specify var_cols in order to use Mahalanobis as a metric.'
        X_exp = df_exp[var_cols]
        X_nexp = df_nexp[var_cols]
        dist_mat = cdist(X_nexp, X_exp)
    else:
        assert False, f"Metric {metric} not implemented."
    exp_nexp_dmat = expand_dist_mat(
            dist_mat, min_mr, 
            max_mr, n_exp, n_nexp,
            n_controls)

    match_result = linear_sum_assignment(exp_nexp_dmat)
    exp_nexp_dic = get_exp_nexp_dic(match_result, exp_ids, nexp_ids, max_mr)
    return exp_nexp_dic

