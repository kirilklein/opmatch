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
df = create_test_data.get_test_data(True, 30, 3, .3)
#print(df)
exp_nexp_dic = {0:[1,2,3], }
