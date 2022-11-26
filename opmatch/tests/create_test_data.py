from matplotlib.pyplot import get
import pandas as pd
import numpy as np
from scipy.stats import norm, bernoulli, uniform, binom




def get_test_data(df=True, num_pat = 10, num_var = 3, num_bin_var =0, 
    pcase=.5, random_state=None):
    if not isinstance(random_state, type(None)):
        np.random.seed(random_state)
    X = norm.rvs(size=(num_pat, num_var))
    if num_bin_var>0:
        B = np.random.randint(0,2, (num_pat, num_bin_var))
    y = bernoulli.rvs(p=pcase , size=num_pat)
    ps = uniform.rvs(size=num_pat)
    if df:
        x_cols = ['x' + str(i) for i in range(num_var)]
        if num_bin_var>0:
            b_cols = ['b' + str(i) for i in range(num_bin_var)]
            df_out = pd.DataFrame(
            np.concatenate([X, B, y.reshape(-1,1), ps.reshape(-1,1)], axis=1), 
            columns = x_cols + b_cols + ['y']+['ps'])    
        else:
            df_out = pd.DataFrame(
                np.concatenate([X, y.reshape(-1,1), ps.reshape(-1,1)], axis=1), 
                columns = x_cols + ['y']+['ps'])
        return df_out 
    else:
        return [X, B, y, ps]

if __name__ == '__main__':
    df = get_test_data()