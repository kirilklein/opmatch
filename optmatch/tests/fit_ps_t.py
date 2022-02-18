import os, sys
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from optmatch.util import fit_ps
import create_test_data

data0 = create_test_data.get_test_data()
data1 = create_test_data.get_test_data(False)
#data0_out = fit_ps.run_logistic_regression(data0, treatment_col='y')
data1_out = fit_ps.run_logistic_regression(data1, {'penalty':'l1'}, random_state=1, )
print(data1_out)
