import os, sys
from os.path import join
import pickle
ROOT_DIR = os.path.abspath(os.curdir)
opmatch_dir = join(ROOT_DIR, 'opmatch')
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(opmatch_dir)
import subprocess as sp
import numpy as np
import tempfile
import warnings
match_script = join(opmatch_dir, 'util', 'match_par.py')

def match(ps:np.array, treatment:np.array, k:int):
    """
    Input:
        ps: propensity scores ()
        treatment: boolean array 
        k: matching coefficient
    Returns:
        exp_nexp_dic: keys-exposed patients
                      values-corresponding matched unexposed patients
    """
    assert len(ps)==len(treatment), "len(ps)!=len(treatment)"
    assert isinstance(k, int), "k must be an integer"
    num_treated = np.sum(treatment)
    num_untreated = len(treatment)-num_treated
    if k>=(num_untreated/num_treated):
        warnings.warn(
        "matching ratio too high, not enough untreated per treated subjects" , 
        stacklevel=1)
    ps_handle, ps_path = tempfile.mkstemp(suffix='.npy')
    trt_handle, trt_path = tempfile.mkstemp(suffix='.npy')
    np.save(ps_path, ps)
    os.close(ps_handle)
    np.save(trt_path, treatment)
    os.close(trt_handle)
    dic_path = sp.check_output(['python', match_script, ps_path,
                    trt_path, str(k)],stderr=sp.STDOUT).decode(encoding="utf-8")
    dic_path = dic_path[:-2]
    with open(dic_path, 'rb') as f:
        exp_nexp_dic = pickle.load(f)
    os.remove(dic_path)
    return exp_nexp_dic