import numpy as np
from numpy import linalg as la
from typing import Union


def mahalanobis_dist(data, x):
    """Compute mahalanobis distance of point x to data."""
    C = np.cov(data.T)
    mu = np.mean(data, axis=0)
    IC = la.inv(C)
    dx = x - mu
    return np.sqrt(dx.T@IC@dx)

def mahalanobis_cont(d1, d2):
    """Compute mahalanobis distance for continuous variables."""
    mu1 = np.mean(d1, axis=0)
    mu2 = np.mean(d2, axis=0)
    C = np.cov(np.concatenate([d1, d2]).T)
    IC = la.inv(C)
    dmu = mu1-mu2
    return np.sqrt(dmu.T@IC@dmu)

def mahalanobis_bin(d1, d2):
    """Compute mahalanobis distance for binary variables.
    If for one of the groups the estimated probabilitiy is zero
        result is the absolute difference between probabilities,
    if both est. probs are zero result is zero,
    else: result is given by (p1-p2)*np.log(p1/p2)
    in the last step we sum over variables.
        """
    d1 = d1.to_numpy()
    d2 = d2.to_numpy()
    p1 = np.sum(d1, axis=0)/len(d1)
    p2 = np.sum(d2, axis=0)/len(d2)
    logarg = np.divide(p1, p2, out=np.ones_like(p1), where=((p1!=0) & (p2!=0)))
    result = (p1-p2)*np.log(logarg,out=np.zeros_like(p1), 
                            where=((p1!=0) & (p2!=0)))
    zero_one_mask = np.logical_xor(p1==0, p2==0)
    result[zero_one_mask] = np.abs(p1[zero_one_mask]-p2[zero_one_mask])
    return np.sum(result)


def gen_mahalanobis(df, g1:Union[None, list]=None, g2:Union[None, list]=None)->float:
    """Takes dataframe and computes generalised mahalanobis distance between the two groups. 
    Given in the paper:
        Barhen, Avner, and J. J. Daudin. 
        "Generalization of the Mahalanobis distance in the mixed case." 
        Journal of Multivariate Analysis 53.2 (1995): 332-342.
    By default the two groups are case==1 and case==0
    Optinally one can pass two lists of indices g1 and g2.
    """
    bin_var_cols = [k for k in df.keys() if k.startswith('b')]
    cont_var_cols = [k for k in df.keys() if k.startswith('x')]
    if isinstance(g1, type(None)) or isinstance(g2, type(None)):    
        df1_c = df[cont_var_cols][df.case==0]
        df2_c = df[cont_var_cols][df.case==1]
        df1_b = df[bin_var_cols][df.case==0]
        df2_b = df[bin_var_cols][df.case==1]        
    else:
        df1_c = df.loc[g1][cont_var_cols]
        df2_c = df.loc[g2][cont_var_cols]
        df1_b = df.loc[g1][bin_var_cols]
        df2_b = df.loc[g2][bin_var_cols]   
    Jc = mahalanobis_cont(df1_c, df2_c)
    Jb = mahalanobis_bin(df1_b, df2_b)
    return Jb + Jc
