import numpy as np
from numpy import linalg as la

def mahalanobis_dist(data, x):
    C = np.cov(data.T)
    mu = np.mean(data, axis=0)
    IC = la.inv(C)
    dx = x - mu
    return np.sqrt(dx.T@IC@dx)

def generalized_mahalanobis_dist():
    pass
