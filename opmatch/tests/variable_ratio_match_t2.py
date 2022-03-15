import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'opmatch'))
from util import variable_ratio_match
import create_test_data

df = create_test_data.get_test_data(True, 30, 3, .2)
df['exposed'] = df.y
n_exp = (df.exposed==1).sum()
print('n_exp =',n_exp)
mr = variable_ratio_match.match(df, 3,3, int(3*n_exp))
print(mr)