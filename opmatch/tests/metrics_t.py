import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'opmatch'))
from util import metrics
from tests import create_test_data
import numpy as np
import matplotlib.pyplot as plt



def test_std_diff_bin():
    x = np.linspace(0,1, 90)
    y = np.linspace(0,1, 90)
    xx, yy = np.meshgrid(x, y)
    zz = metrics.standardized_difference_bin(xx, yy)
    plt.contourf(xx, yy, zz)
    plt.colorbar()
    plt.show()
def test_std_diff_cont():
    x = np.linspace(-10,10, 90)
    y = np.linspace(-10,10, 90)
    s_c=s_t = 1
    xx, yy = np.meshgrid(x, y)
    zz = metrics.standardized_difference_con(xx, yy,s_c,s_t)
    plt.contourf(xx, yy, zz)
    plt.colorbar()
    plt.show()
df = create_test_data.get_test_data(True, 100, 2, 2,pexp=.1, random_state=2)
df['exposed'] = df.y
print(df.head())
#test_std_diff_cont()