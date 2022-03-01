import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(join(ROOT_DIR,'opmatch'))
from util import utils
import numpy as np
from tests import create_test_data
d1 = {'a': 1}
d2 = {'a':2, 'b':2}
d = utils.combine_dicts(d1,d2)
print(d)
print('first func tested')
df = create_test_data.get_test_data(True, 30, 3, .3)
avg_dist = np.array([1, 5, 1.4])
exp_nexp_dic = {0:[1,2], 3:[4,5], 6:[7,8] }
keys = np.array(list(exp_nexp_dic.keys()))
values = np.array(list(exp_nexp_dic.values()))
ps = np.array([0,1,2,3,10,5,6,7,8])
abs_diff = np.average(np.abs(ps[keys,np.newaxis] - ps[values]), axis=1)
print(abs_diff)
#ps_exp = df.iloc[keys]
keep_mask = avg_dist>=abs_diff
print(keys[keep_mask])
for key in exp_nexp_dic.keys():
    pass
