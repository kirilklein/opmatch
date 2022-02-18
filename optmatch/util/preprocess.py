import pandas as pd
import numpy as np
from typing import Union, List

def get_X_y(data:Union[pd.DataFrame, None],
    X:Union[List[str], np.array, None], 
    y:Union[List[str], np.array, None],)->tuple(np.array,np.array):
    
    df = isinstance(data, pd.DataFrame)
    Xnan = isinstance(X, type(None))
    ynan = isinstance(y, type(None)) 
    if df:
        if Xnan and ynan:
            print("y (treatment_col) and X (covariates_cols) are not specified.")
            print("By default, interpret last column as treatment and all other columns as covariates.")
            X = data.iloc[:,:-1]
            y = data.iloc[:,-1]
        elif Xnan:
            print("X (covariates_cols) not specified, use all cols as covariates except treatment_col")
            X = data.drop([y], axis=1)
            y = data[y]
        elif ynan:
            if len(data.keys()==(len(X)+1)):
                print("y (treatment_col) is not specified")
                print("Use all cols as covariates cols and the remaining one as treatment_col")
            else:
                assert False, "Multiple options for treatment col, either specify or remove all cols except treatment and covariates"
        else:
            X = data[X]
            y = data[y]

    elif isinstance(X, np.array) and isinstance(y, np.array):
        assert len(X)==len(y), "X and y must have the same length!"
    else:
        assert False, "Either pass DataFrame to data or numpy arays to X and y."
    return X, y