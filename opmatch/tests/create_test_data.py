from matplotlib.pyplot import get
import pandas as pd
import numpy as np
from scipy.stats import norm, bernoulli, uniform




def get_test_data(df=True, num_pat = 10, num_var = 3, pexp=.5, random_state=None):
    if not isinstance(random_state, type(None)):
        np.random.seed(random_state)
    X = norm.rvs(size=(num_pat, num_var))
    y = bernoulli.rvs(p=pexp , size=num_pat)
    ps = uniform.rvs(size=num_pat)
    if df:
        x_cols = ['x' + str(i) for i in range(num_var)]
        df_out = pd.DataFrame(
            np.concatenate([X, y.reshape(-1,1), ps.reshape(-1,1)], axis=1), 
            columns = x_cols + ['y']+['ps'])
        return df_out 
    else:
        return [X, y, ps]

if __name__ == '__main__':
    df = get_test_data()