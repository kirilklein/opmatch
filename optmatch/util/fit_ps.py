import preprocess
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from typing import Union, List
#https://towardsdatascience.com/how-to-open-source-your-first-python-package-e717444e1da0
def run_logistic_regression(data:Union[pd.DataFrame, None]=None, 
                            X:Union[List[str], np.array, None]=None, 
                            y:Union[List[str], np.array, None]=None,
                            random_state:Union[int, None]=0, 
                            *args, **kwargs,)->Union[pd.DataFrame, np.array]:
    """Run logistic regression on data.
        If data not provided, provide X (covariates) and y (treatment) as np.array
        If DataFrame passed to data: provide the covariates columns and treatment column
        by default the last column will be used as treatment col, and the rest as covariates cols
        *args and **kwargs are passed to sklearn.linear_model.LogisticRegression
    """
    X, y = preprocess.get_X_y_ls(data, X, y)
    if isinstance(random_state, int):
        LR = LogisticRegression(*args, **kwargs, random_state=random_state).fit(X, y)
    else:
        LR = LogisticRegression(*args, **kwargs).fit(X, y)
    prob = LR.predict_proba(X)[:,1]
    return prob
