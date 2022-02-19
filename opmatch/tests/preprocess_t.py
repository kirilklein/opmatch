import os, sys
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from opmatch.util import preprocess
import create_test_data
import numpy as np

data0 = create_test_data.get_test_data()
#data0['score'] = np.arange(len(data0))
print(data0)
X,y = preprocess.get_X_y(data0)
print(X, y)