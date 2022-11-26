import os, sys
from os.path import join, split
ROOT_DIR = split(os.path.dirname(os.path.realpath(__file__)))[0]
print(ROOT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
import create_test_data
from util import match_utils, vis
import numpy as np
X, y, ps = create_test_data.get_test_data(df=False, num_pat=50, num_var=3, pcase=0.2)
#y = np.array([1,1,0,0,0,0,0,0])
#ps = np.array([.1, .5, .11, .1101, .51, .51001, .110001, .8])
#print('case: ', np.argwhere(y==1))
if __name__ == '__main__':
    case_control_dic = match_utils.match_parallel(ps, treatment=y, matching_ratio='entire_number',
        min_matching_ratio=1, max_matching_ratio=4)
    vis.plot_matching(ps, case_control_dic, save=True,figname='opmatch\\tests\\test_match_parallel.png',
    show=False)
    print(case_control_dic)

