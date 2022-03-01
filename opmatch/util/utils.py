from collections import defaultdict

def combine_dicts(d1:dict, d2:dict)->dict:
    """Combines two dictionaries,
    values from same keys are stored in a list"""

    dd = defaultdict(list)
    for d in (d1, d2): # you can list as many input dicts as you want here
        for key, value in d.items():
            dd[key].append(value)
    return dd
    
def compute_avg_dist(df, exp_nexp_dic):
    pass