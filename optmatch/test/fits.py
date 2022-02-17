import os, sys
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from optmatch import fit_ps
import pandas as pd
import numpy as np
from scipy.stats import norm, bernoulli


num_pat = 8
num_var = 5
X = norm.rvs(size=(num_pat, num_var))
y = bernoulli.rvs(p =.3 , size=num_pat)
x_cols = ['x' + str(i) for i in range(num_var)]
data0 = pd.DataFrame(np.concatenate([X,y.reshape(-1,1)], axis=1), columns = x_cols + ['y'])
data1 = [X, y]
#data0_out = fit_ps.run_logistic_regression(data0, treatment_col='y')
data1_out = fit_ps.run_logistic_regression(data1, {'penalty':'l1'}, random_state=1, )
print(data1_out)
