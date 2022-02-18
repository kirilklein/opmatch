from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from typing import Union, List
#https://towardsdatascience.com/how-to-open-source-your-first-python-package-e717444e1da0
def run_logistic_regression(data:Union[list, tuple, pd.DataFrame], 
                            covariates_cols:Union[List[str], None]=None, 
                            treatment_col:Union[str, None]=None, 
                            random_state:Union[int, None]=0, 
                            *args, **kwargs,)->Union[pd.DataFrame, np.array]:
    """Run logistic regression on data.
        covariates_cols: boolean of float columns that contain the variables (X) 
        treatment_col: boolean column that contains the exposure/treatment or outcome
        *args and **kwargs are passed to sklearn.linear_model.LogisticRegression
    """
    nantype = type(None)
    df = isinstance(data, pd.DataFrame)
    tup = isinstance(data, tuple)
    ls = isinstance(data, list)
    cov_none = isinstance(covariates_cols, nantype)
    treat_none = isinstance(treatment_col, nantype)
    if df and cov_none and treat_none:
        print("treatment_col and covariates_cols are not specified.")
        print("By default, interpret last column as treatment and all other columns as covariates.")
        X = data.iloc[:,:-1]
        y = data.iloc[:,-1]
    if df:
        if cov_none:
            print("covariates_cols not specified, use all cols as covariates except treatment_col")
            X = data.drop([treatment_col], axis=1)
            y = data[treatment_col]
        if treat_none:
            if len(data.keys()==(len(covariates_cols)+1)):
                print("treatment_col is not specified")
                print("Use all cols as covariates cols and the remaining one as treatment_col")
            else:
                assert False, "Multiple options for treatment col, either specify or remove all cols except treatment and covariates"
    elif (tup or ls) and (len(data)==2):
        X = data[0]
        y = data[1]
        assert len(X)==len(y), "data[0] and data[1] must have the same length!"
    else:
        assert False, "data must be either df or tuple/list of length 2."

    if isinstance(random_state, int):
        LR = LogisticRegression(*args, **kwargs, random_state=random_state).fit(X, y)
    else:
        LR = LogisticRegression(*args, **kwargs).fit(X, y)

    if df:
        data['P_'+treatment_col] = LR.predict_proba(X)[:,1]
        return data
    elif (tup or ls) and (len(data)==2):
        prob = LR.predict_proba(X)[:,1]
        return prob
