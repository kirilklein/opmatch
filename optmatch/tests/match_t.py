import os, sys
from os.path import join

from matplotlib.markers import MarkerStyle
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'optmatch'))
#import match_subjects
from util import match
import create_test_data
import subprocess as sp
import matplotlib.pyplot as plt
import numpy as np

X, y, ps = create_test_data.get_test_data(False, 15, 3, .2)
#script = join(ROOT_DIR, 'optmatch', 'match_subjects.py')
#output = sp.call(['python', script, 'hallo'], shell=True)
def plot_matching(ps, exp_nexp_dic):
    fig, ax = plt.subplots()
    exp_ids = list(exp_nexp_dic.keys())
    for i, exp in enumerate(exp_ids):
        ax.scatter(ps[exp], i, marker='x', color='k')
        print(exp_nexp_dic[exp])
        nexp_ps = ps[exp_nexp_dic[exp]]
        group_arr = np.ones(len(nexp_ps))*i
        ax.scatter(nexp_ps, group_arr, marker='.', color='k')
    fig.savefig('optmatch\\tests\\matched_ps.png')


if __name__ == '__main__':
    exp_nexp_dic = match.match_parallel(ps, y, 2)
    print(exp_nexp_dic)
    plot_matching(ps, exp_nexp_dic)
    