import os, sys
from os.path import join, split
ROOT_DIR = split(os.path.dirname(os.path.realpath(__file__)))[0]
print(ROOT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
import create_test_data
from util import match_utils, vis

X, y, ps = create_test_data.get_test_data(df=False, num_pat=30, num_var=3, pexp=0.15)

if __name__ == '__main__':
    exp_nexp_dic = match_utils.match_parallel(ps, treatment=y, matching_ratio='variable')
    vis.plot_matching(ps, exp_nexp_dic, save=True,)
    print(exp_nexp_dic)

