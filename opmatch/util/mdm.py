import numpy as np
from numpy import linalg as la
from typing import Union


def mahalanobis_dist(data, x):
    C = np.cov(data.T)
    mu = np.mean(data, axis=0)
    IC = la.inv(C)
    dx = x - mu
    return np.sqrt(dx.T@IC@dx)

def mahalanobis_const(d1, d2):
    mu1 = np.mean(d1, axis=0)
    mu2 = np.mean(d2, axis=0)
    C = np.cov(np.concatenate([d1, d2]).T)
    IC = la.inv(C)
    dmu = mu1-mu2
    return np.sqrt(dmu.T@IC@dmu)

def mahalanobis_bin(d1, d2):
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
    """Takes dataframe and computes gowers coefficient between two groups. 
    By default the two groups are exposed==1 and exposed==0
    Optinally one can pass two lists of indices g1 and g2"""
    if isinstance(g1, type(None)) or isinstance(g2, type(None)):
        bin_var_cols = [k for k in df.keys() if k.startswith('b')]
        cont_var_cols = [k for k in df.keys() if k.startswith('x')]
        df1_c = df[cont_var_cols][df.exposed==0]
        df2_c = df[cont_var_cols][df.exposed==1]
        df1_b = df[bin_var_cols][df.exposed==0]
        df2_b = df[bin_var_cols][df.exposed==1]        
    else:
        pass
    Jc = mahalanobis_const(df1_c, df2_c)
    Jb = mahalanobis_bin(df1_b, df2_b)
    return Jb + Jc
