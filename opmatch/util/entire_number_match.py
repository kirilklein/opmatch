import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from collections import defaultdict
from scipy.spatial.distance import cdist
from opmatch.util import metrics


def caseand_dist_mat(dist_mat:np.ndarray, min_mr:int, 
                max_mr:int, n_case:int, n_control:int, 
                n_controls:int):
    case_control_dmat = np.tile(dist_mat, max_mr)
    case_control_dmat = np.reshape(case_control_dmat, 
                newshape=(n_case*max_mr, n_control))
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
    final_dist_mat = np.concatenate([case_control_dmat, case_mat], axis=1)
    return final_dist_mat

def get_case_control_dic(match_result:tuple, case_ids:list, 
        control_ids:list, max_mr:int)->dict:
    rep_case_ids = np.repeat(case_ids, max_mr)
    case_nums, control_nums = match_result
    mask = control_nums<len(control_ids) # remove sinks
    case_nums = case_nums[mask]
    control_nums = control_nums[mask]

    control_case_dic = {control_ids[control_num]:rep_case_ids[case_num] for control_num, case_num in \
        zip(control_nums, case_nums) if control_num<len(control_ids)}
    case_control_dic = defaultdict(list)
    for key, value in control_case_dic.items():
        case_control_dic[value].append(key)
    return case_control_dic


def match(df:pd.DataFrame)->dict:
    """
    df: has to contain 'case' column, 
        matching dictionary will be returned with dataframe indices
   
    """
    assert False, 'This function is not ready yet'
    df_case = df[(df.case==1)]
    df_control = df[(df.case==0)]
    case_ids = df_case.index
    control_ids = df_control.index
    
    n_case = len(case_ids)
    n_control = len(control_ids)
    matching_ratio = np.ceil(((1-df_case.ps)/df_case.ps)).astype(int)
    
    print(matching_ratio)
    assert np.sum(matching_ratio)<=n_control, f'n_controls>n_control={n_control}'
    
    assert False
    if metric=='PS':
        case_ps = df_case.ps.to_numpy()
        control_ps = df_control.ps.to_numpy()
        dist_mat = metrics.create_ps_dist_matrix(case_ps, control_ps,n_case, n_control, 
                                min_mr, max_mr, n_controls)
    else:
        assert not isinstance(var_cols, type(None)), 'You need to specify var_cols in order to use Mahalanobis as a metric.'
        X_case = df_case[var_cols]
        X_control = df_control[var_cols]
        dist_mat = cdist(X_control, X_case, metric=metric)
    case_control_dmat = caseand_dist_mat(
            dist_mat, min_mr, 
            max_mr, n_case, n_control,
            n_controls)

    match_result = linear_sum_assignment(case_control_dmat)
    case_control_dic = get_case_control_dic(match_result, case_ids, control_ids, max_mr)
    return case_control_dic

