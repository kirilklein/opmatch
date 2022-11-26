import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'opmatch'))
from util import variable_ratio_match
import create_test_data

df = create_test_data.get_test_data(True, 10, 3, .4,random_state=3)
df['case'] = df.y
print(df)
n_case = (df.case==1).sum()
n_control = (df.case==0).sum()
print('n_case =',n_case)
print('n_control =',n_control)
mr = variable_ratio_match.match(df, 1, 2, 4)
print(mr)