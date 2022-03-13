import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

def pairwise_abs_dist(a:np.ndarray, b:np.ndarray):
    """Compute absolute distance matrix.
    Input: 1d arrays a and b
    Returns: len(a)xlen(b) distance matrix
    """
    return np.abs(a[:,np.newaxis] - b[np.newaxis, :])

def create_dist_matrix(exp_ps:np.ndarray, nexp_ps:np.ndarray, 
                    n_exp:int, n_nexp:int, min_mr:int, 
                    max_mr:int, n_controls:int):
    assert n_controls<=n_nexp, f'n_controls>n_nexp={n_nexp}'
    assert max_mr<=(n_controls-n_exp+1), f'max_mr>(total_controls-n_exp+1)={n_controls-n_exp+1}'
    assert max_mr>=np.ceil(n_controls/n_exp), f'max_mr<np.ceil(total_controls/n_exp)={np.ceil(n_controls/n_exp)}'
    assert min_mr<=np.floor(n_controls/n_exp), f'min_mr>np.floor(n_controls/n_exp)={np.floor(n_controls/n_exp)}'
    assert min_mr>=1, 'min_mr<1'
    K = n_exp * max_mr - n_controls
    assert isinstance(K, int), 'make sure that max_mr and n_controls are integers'
    dist_mat = pairwise_abs_dist(exp_ps, nexp_ps)
    return dist_mat

def expand_dist_mat(dist_mat:np.ndarray, min_mr:int, 
                max_mr:int, n_exp:int, n_nexp:int, 
                n_controls:int):
    exp_nexp_dmat = np.tile(dist_mat, max_mr)
    exp_nexp_dmat = np.reshape(exp_nexp_dmat, 
                newshape=(n_exp*max_mr, n_nexp))
    K = n_exp * max_mr - n_controls
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

def get_nexp_exp_dic(match_result):
    row_ind, col_ind = match_result
    pass


def match(df:pd.DataFrame, min_mr:int, 
         max_mr:int, n_controls:int):
    
    df_exp = df[(df.exposed==1)]
    df_nexp = df[(df.exposed==0)]
    exp_ids = df_exp.index
    nexp_ids = df_nexp.index
    exp_ps = df_exp.ps.to_numpy()
    nexp_ps = df_nexp.ps.to_numpy()
    n_exp = len(exp_ids)
    n_nexp = len(nexp_ids)

    dist_mat = create_dist_matrix(exp_ps, nexp_ps,n_exp, n_nexp, 
                                min_mr, max_mr, n_controls)
    exp_nexp_dmat = expand_dist_mat(
            dist_mat, min_mr, 
            max_mr, n_exp, n_nexp,
            n_controls)

    match_result = linear_sum_assignment(exp_nexp_dmat)
    return match_result

