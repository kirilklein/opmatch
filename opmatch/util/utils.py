from collections import defaultdict
import numpy as np
import pandas as pd
from typing import List

def combine_dicts(d1:dict, d2:dict)->dict:
    """Combines two dictionaries,
    values from same keys are stored in a list"""
    dd = defaultdict(list)
    for d in (d1, d2): # you can list as many input dicts as you want here
        for key, value in d.items():
            if isinstance(value, list):
                dd[key] = dd[key] + value
            else:
                dd[key].append(value)
    return dd
    
def compute_avg_dist(df:pd.DataFrame, case_control_dic:dict)->np.array:
    """Computes the absolute average distance between the case and 
    matched control."""
    keys = np.array(list(case_control_dic.keys()))
    values = np.array(list(case_control_dic.values()))
    ps = df.ps.to_numpy()
    abs_avg_dist = np.average(np.abs(ps[keys, np.newaxis] - ps[values]), axis=1)
    return abs_avg_dist

def flatten(ls_of_ls:List[List]):
    """Flatten list of lists"""
    return [item for sublist in ls_of_ls for item in sublist]