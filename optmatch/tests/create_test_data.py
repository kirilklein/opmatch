import pandas as pd
import numpy as np
from scipy.stats import norm, bernoulli




def get_test_data(df=True, num_pat = 10, num_var = 3):
    X = norm.rvs(size=(num_pat, num_var))
    y = bernoulli.rvs(p =.3 , size=num_pat)
    if df:
        x_cols = ['x' + str(i) for i in range(num_var)]
        return pd.DataFrame(np.concatenate([X,y.reshape(-1,1)], axis=1), columns = x_cols + ['y'])
    else:
        return [X, y]
