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
from typing import Union


def match(ps:np.array, treatment:np.array, matching_ratio:Union[int, str]):
    """
    Input:
        ps: propensity scores ()
        treatment: boolean array 
        matching ratio: 
            if integer: matching_ratio controls per positive 
            elif: str:variable, Controls are matched until average distance stops decreasing
            elif: str:full, at least one control for every positive and at least one positive for every control
    Returns:
        exp_nexp_dic: keys-exposed patients
                      values-corresponding matched unexposed patients
    """
    assert len(ps)==len(treatment), "len(ps)!=len(treatment)"
    num_treated = np.sum(treatment)
    num_untreated = len(treatment)-num_treated
    if isinstance(matching_ratio, int):
        if matching_ratio>=(num_untreated/num_treated):
            warnings.warn(
            "matching ratio too high, not enough untreated per treated subjects" , 
            stacklevel=1)
    elif matching_ratio=='variable':
        assert False, f'{matching_ratio} matching_ratio not available right now'
        #print("Variable matching ratio: Additional controls are matched until some criterion is met")
    elif matching_ratio=='full':
        assert False, "Full matching not implemented yet"
    elif matching_ratio=='entire_number':
        print("Matching ratio based on entire number")
    else:
        assert False, "Matching ratio should be integer, 'variable' or 'full' "
    ps_handle, ps_path = tempfile.mkstemp(suffix='.npy')
    trt_handle, trt_path = tempfile.mkstemp(suffix='.npy')
    np.save(ps_path, ps)
    os.close(ps_handle)
    np.save(trt_path, treatment)
    os.close(trt_handle)
    match_script = join(opmatch_dir, 'util', 'match_par.py')
    dic_path = sp.check_output(['python', match_script, ps_path,
                    trt_path, str(matching_ratio)],stderr=sp.STDOUT).decode(encoding="utf-8")
    dic_path = dic_path[:-2]
    with open(dic_path, 'rb') as f:
        exp_nexp_dic = pickle.load(f)
    os.remove(dic_path)
    return exp_nexp_dic