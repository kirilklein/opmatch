import numpy as np
import pandas as pd
from scipy.stats import truncnorm

np.random.seed(0)
def convert_scale(clip_a, clip_b, loc, scale):
    a, b = (clip_a - loc) / scale, (clip_b - loc) / scale
    return a, b
    
def simulate_age(n, age_loc, age_scale):
    age_clip_a, age_clip_b = 0, 100
    age_a_con, age_b_con = convert_scale(age_clip_a, age_clip_b, age_loc, age_scale)
    return truncnorm.rvs(a=age_a_con, b=age_b_con, loc=age_loc, scale=age_scale, size=n)
def simulate_bmi(n, bmi_loc, bmi_scale):
    bmi_clip_a, bmi_clip_b = 0, 50
    bmi_a_con, bmi_b_con = convert_scale(bmi_clip_a, bmi_clip_b, bmi_loc, bmi_scale)
    return truncnorm.rvs(a=bmi_a_con, b=bmi_b_con, loc=bmi_loc, scale=bmi_scale, size=n)

def generate(num_patients, num_cases):    
    age_loc_con, age_loc_case = 40, 60
    bmi_loc_con, bmi_loc_case = 18, 25
    age_scale = 20
    bmi_scale = 10
    age_controls = simulate_age(num_patients-num_cases, age_loc_con, age_scale)
    age_cases = simulate_age(num_cases, age_loc_case, age_scale)
    bmi_controls = simulate_bmi(num_patients-num_cases, bmi_loc_con, bmi_scale)
    bmi_cases = simulate_bmi(num_cases, bmi_loc_case, bmi_scale)
    data = {'age': np.concatenate((age_controls, age_cases)), 
            'bmi': np.concatenate((bmi_controls, bmi_cases)), 
            'case': np.concatenate((np.zeros(num_patients-num_cases), np.ones(num_cases)))}
    return pd.DataFrame(data)
