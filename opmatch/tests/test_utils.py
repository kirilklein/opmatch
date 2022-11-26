import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(join(ROOT_DIR,'opmatch'))
from util import utils
import numpy as np
from tests import create_test_data
d1 = {'a': [1,3]}
d2 = {'a':2, 'b':2}
d = utils.combine_dicts(d1,d2)
print(d)
print('first func tested')
df = create_test_data.get_test_data(True, 30, 3, .3)

case_control_dic = {0:[1,2], 3:[4,5], 6:[7,8] }
avg_dist = utils.compute_avg_dist(df, case_control_dic)
print(avg_dist)