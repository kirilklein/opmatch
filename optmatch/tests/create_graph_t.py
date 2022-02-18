import os, sys
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from optmatch.util import create_graph
import pandas as pd
import numpy as np
from scipy.stats import norm, bernoulli
import matplotlib.pyplot as plt
import networkx as nx


num_pat = 8
num_var = 5
X = norm.rvs(size=(num_pat, num_var))
y = bernoulli.rvs(p =.3 , size=num_pat)
x_cols = ['x' + str(i) for i in range(num_var)]
data0 = pd.DataFrame(np.concatenate([X,y.reshape(-1,1)], axis=1), columns = x_cols + ['y'])
data1 = [X, y]

ids = np.arange(len(y))
unexp_ids = ids[y==0]
exp_ids = ids[y==1]
edges = create_graph.create_source_unexp_edges(unexp_ids)
edges = create_graph.append_case_sink_edges(edges, exp_ids, 2)

print(edges)
"""fig, ax = plt.subplots()
BG = nx.DiGraph()
BG.add_nodes_from(edges)
nx.draw_networkx(BG,  ax=ax, with_labels=False,
    )

fig.savefig('graph.png')
"""