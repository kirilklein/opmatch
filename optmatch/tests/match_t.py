import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'optmatch'))
#import match_subjects
import match
import create_test_data

X, y, ps = create_test_data.get_test_data(False, 30, 3, .2)

if __name__=="__main__":
    match.match(ps, y, 3)