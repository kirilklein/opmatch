from opmatch.tutorial import example_data
from opmatch.matcher import Matcher
import numpy as np


n_cases = 5
n_control_pool = 30
df = example_data.generate(n_control_pool, n_cases)


def test_dist_mat_expansion(n_controls=15, min_mr=1, max_mr=3):
    """Check whether the distance matrix is expanded correctly"""
    matcher = Matcher(df, var_cols=['age', 'bmi'], matching_type='var', n_controls=n_controls, min_mr=min_mr, max_mr=max_mr) 
    case_control_dist_mat = np.random.uniform(size=(matcher.M, matcher.n)) # n_control_pool x n_cases
    expanded_dist_mat = matcher.case_control_dist_mat(case_control_dist_mat)
    K = matcher.n * matcher.beta - matcher.m
    assert expanded_dist_mat.shape[0]==matcher.n*matcher.beta, f'expanded_dist_mat.shape[0]={expanded_dist_mat.shape[0]}!=n_cases*beta={matcher.n*matcher.beta}'
    assert expanded_dist_mat.shape[1]==matcher.M+K, f'expanded_dist_mat.shape[1]={expanded_dist_mat.shape[1]}!=M+K={matcher.M+K}'
    