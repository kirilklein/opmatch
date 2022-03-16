import numpy as np

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