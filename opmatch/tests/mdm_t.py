import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'opmatch'))
from util import mdm
import pandas as pd
import create_test_data
import matplotlib.pyplot as plt 
df = create_test_data.get_test_data(True, 10, num_var=2,num_bin_var=1, pexp=.4,random_state=3)
df['exposed'] = df.y
print(df)
n_exp = (df.exposed==1).sum()
n_nexp = (df.exposed==0).sum()
print('n_exp =',n_exp)
print('n_nexp =',n_nexp)

cols = ['x0', 'b0']


def test_mahalanobis_dist():
    dists = []
    data = df[cols]
    for i in range(len(data)):
        x = data.iloc[i,:].to_numpy()
        md = mdm.mahalanobis_dist(data.to_numpy(), x)
        dists.append(md)
    fig, ax = plt.subplots()
    ax.scatter(data.iloc[:,0], data.iloc[:,1])
    for i, d in enumerate(dists):
        ax.text(data.iloc[i,0], data.iloc[i,1], str(round(d,3)))
    plt.show()

pdist = mdm.match(df, cols)
print(pdist)
