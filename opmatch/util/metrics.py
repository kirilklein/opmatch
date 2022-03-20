import numpy as np
from typing import Union
from scipy.spatial import distance

def pairwise_abs_dist(a:np.ndarray, b:np.ndarray):
    """Compute absolute distance matrix.
    Input: 1d arrays a and b
    Returns: len(a)xlen(b) distance matrix
    """
    return np.abs(a[:,np.newaxis] - b[np.newaxis, :])

def create_ps_dist_matrix(exp_ps:np.ndarray, nexp_ps:np.ndarray, 
                    n_exp:int, n_nexp:int, min_mr:int, 
                    max_mr:int, n_controls:int):
    K = n_exp * max_mr - n_controls
    assert isinstance(K, int), 'make sure that max_mr and n_controls are integers'
    dist_mat = pairwise_abs_dist(exp_ps, nexp_ps)
    return dist_mat

def standardized_difference_bin(p_t:float,p_c:float):
    """p_t, p_c: estimated prevalence in treated and control group"""
    assert (p_t<=1).all() and (0<=p_t).all() and (0<=p_c).all() and (p_c<=1).all(), 'p_t and p_c must be between 0 and 1'
    num = p_t - p_c
    den = np.sqrt((p_t*(1-p_t)+p_c*(1-p_c))/2)
    return np.abs(num/den)

def standardized_difference_con(mu_t:float,mu_c:float, s_t:float, s_c:float):
    """p_t, p_c: estimated prevalence in treated and control group"""
    num = mu_t - mu_c
    den = np.sqrt((s_t**2+s_c**2)/2)
    return np.abs(num/den)

