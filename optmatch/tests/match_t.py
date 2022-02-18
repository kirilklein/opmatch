import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'optmatch'))
#import match_subjects
import create_test_data
import subprocess as sp
    
X, y, ps = create_test_data.get_test_data(False, 10, 3)
if __name__ == '__main__':
    #dic = match_subjects.match()
    #print(dic)
    output = sp.call([join(ROOT_DIR, 'optmatch', 'match_subjects.py')], shell=True)
