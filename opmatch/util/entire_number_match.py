import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from collections import defaultdict
from scipy.spatial.distance import cdist
from opmatch.util import metrics


def caseand_dist_mat(dist_mat:np.ndarray, min_mr:int, 
                max_mr:int, n_case:int, n_ncase:int, 
                n_controls:int):
    case_ncase_dmat = np.tile(dist_mat, max_mr)
    case_ncase_dmat = np.reshape(case_ncase_dmat, 
                newshape=(n_case*max_mr, n_ncase))
    K = n_case * max_mr - n_controls
    assert isinstance(K, int), 'make sure that max_mr and n_controls are integers'
    case_inf = np.ones(shape=(min_mr, K))*np.inf
    if (max_mr-min_mr)>=1:
        case_zeros = np.zeros(shape=(max_mr-min_mr, K))
        case_mat = np.concatenate([case_inf, case_zeros],  axis=0)
    else:
        case_mat = case_inf
    case_mat = np.tile(case_mat, (n_case,1))
    case_mat = np.reshape(case_mat, newshape=(max_mr*n_case, K))
    final_dist_mat = np.concatenate([case_ncase_dmat, case_mat], axis=1)
    return final_dist_mat

def get_case_ncase_dic(match_result:tuple, case_ids:list, 
        ncase_ids:list, max_mr:int)->dict:
    rep_case_ids = np.repeat(case_ids, max_mr)
    case_nums, ncase_nums = match_result
    mask = ncase_nums<len(ncase_ids) # remove sinks
    case_nums = case_nums[mask]
    ncase_nums = ncase_nums[mask]

    ncase_case_dic = {ncase_ids[ncase_num]:rep_case_ids[case_num] for ncase_num, case_num in \
        zip(ncase_nums, case_nums) if ncase_num<len(ncase_ids)}
    case_ncase_dic = defaultdict(list)
    for key, value in ncase_case_dic.items():
        case_ncase_dic[value].append(key)
    return case_ncase_dic


def match(df:pd.DataFrame)->dict:
    """
    df: has to contain 'case' column, 
        matching dictionary will be returned with dataframe indices
   
    """
    assert False, 'This function is not ready yet'
    df_case = df[(df.case==1)]
    df_ncase = df[(df.case==0)]
    case_ids = df_case.index
    ncase_ids = df_ncase.index
    
    n_case = len(case_ids)
    n_ncase = len(ncase_ids)
    matching_ratio = np.ceil(((1-df_case.ps)/df_case.ps)).astype(int)
    
    print(matching_ratio)
    assert np.sum(matching_ratio)<=n_ncase, f'n_controls>n_ncase={n_ncase}'
    
    assert False
    if metric=='PS':
        case_ps = df_case.ps.to_numpy()
        ncase_ps = df_ncase.ps.to_numpy()
        dist_mat = metrics.create_ps_dist_matrix(case_ps, ncase_ps,n_case, n_ncase, 
                                min_mr, max_mr, n_controls)
    else:
        assert not isinstance(var_cols, type(None)), 'You need to specify var_cols in order to use Mahalanobis as a metric.'
        X_case = df_case[var_cols]
        X_ncase = df_ncase[var_cols]
        dist_mat = cdist(X_ncase, X_case, metric=metric)
    case_ncase_dmat = caseand_dist_mat(
            dist_mat, min_mr, 
            max_mr, n_case, n_ncase,
            n_controls)

    match_result = linear_sum_assignment(case_ncase_dmat)
    case_ncase_dic = get_case_ncase_dic(match_result, case_ids, ncase_ids, max_mr)
    return case_ncase_dic

