import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'opmatch'))
import match
import create_test_data
import numpy as np
from util import vis

X, y, ps = create_test_data.get_test_data(False, 30, 1, .15)
print(np.sum(y), 'case')
print(len(y)-np.sum(y), 'control')
case_control_dic = match.match(ps, y, 'variable')
vis.plot_matching(ps, case_control_dic, save=True)