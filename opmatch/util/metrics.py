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
    assert n_controls<=n_nexp, f'n_controls>n_nexp={n_nexp}'
    assert max_mr<=(n_controls-n_exp+1), f'max_mr>(total_controls-n_exp+1)={n_controls-n_exp+1}'
    assert max_mr>=np.ceil(n_controls/n_exp), f'max_mr<np.ceil(total_controls/n_exp)={np.ceil(n_controls/n_exp)}'
    assert min_mr<=np.floor(n_controls/n_exp), f'min_mr>np.floor(n_controls/n_exp)={np.floor(n_controls/n_exp)}'
    assert min_mr>=1, 'min_mr<1'
    K = n_exp * max_mr - n_controls
    assert isinstance(K, int), 'make sure that max_mr and n_controls are integers'
    dist_mat = pairwise_abs_dist(exp_ps, nexp_ps)
    return dist_mat