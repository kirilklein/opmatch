import numpy as np

def standardized_difference_bin(p_t:float, p_c:float):
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

