import numpy as np
import pandas as pd
from scipy.stats import truncnorm

def convert_scale(clip_a, clip_b, loc, scale):
    a, b = (clip_a - loc) / scale, (clip_b - loc) / scale
    return a, b
    
def generate(num_patients, num_cases):    
    age_loc, age_scale = 50, 30
    bmi_loc, bmi_scale = 20, 10
    age_clip_a, age_clip_b = 0, 100
    bmi_clip_a, bmi_clip_b = 0, 50
    age_a, age_b = convert_scale(age_clip_a, age_clip_b, age_loc, age_scale)
    bmi_a, bmi_b = convert_scale(bmi_clip_a, bmi_clip_b, bmi_loc, bmi_scale)
    age = truncnorm.rvs(a=age_a, b=age_b, loc=age_loc, scale=age_scale, size=num_patients)
    bmi = truncnorm.rvs(a=bmi_a, b=bmi_b, loc=bmi_loc, scale=bmi_scale, size=num_patients)
    cases_ids = np.random.choice(num_patients, num_cases, replace=False,)
    case = np.zeros(num_patients)
    case[cases_ids] = 1
    return pd.DataFrame({'age':age, 'bmi':bmi, 'case':case})
