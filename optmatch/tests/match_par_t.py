import os, sys
from os.path import join
import pickle
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'optmatch'))
#import match_subjects
from util import match_par
import create_test_data
import subprocess as sp
import matplotlib.pyplot as plt
import numpy as np

X, y, ps = create_test_data.get_test_data(False, 30, 3, .2)
#script = join(ROOT_DIR, 'optmatch', 'match_subjects.py')
#output = sp.call(['python', script, 'hallo'], shell=True)

if __name__ == '__main__':
    exp_nexp_dic = match_par.match_parallel(ps, y, 2)
    np.save('optmatch\\tests\data\ps', ps)
    with open('optmatch\\tests\data\exp_nexp_dic.pkl', 'wb') as f:
        pickle.dump(exp_nexp_dic, f)
    print(exp_nexp_dic)
