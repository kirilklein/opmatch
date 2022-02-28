import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'opmatch'))

from util import match_utils
import numpy as np
from typing import Dict, List
import pickle
import tempfile


    
def main():
    ps_path = sys.argv[1]
    trt_path = sys.argv[2]
    k = int(sys.argv[3])
    ps = np.load(ps_path)
    trt = np.load(trt_path)
    exp_nexp_dic = match_utils.match_parallel(ps, trt, k)
    if os.path.exists(ps_path):
        os.remove(ps_path)
    if os.path.exists(trt_path):
        os.remove(trt_path)
    dic_handle, dic_path = tempfile.mkstemp(suffix='.pkl')
    os.close(dic_handle)
    with open(dic_path, 'wb') as f:
        pickle.dump(exp_nexp_dic, f)
    return dic_path
if __name__ == '__main__':
    print(main())