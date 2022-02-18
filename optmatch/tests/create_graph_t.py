import os, sys
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from optmatch.util import create_graph
import create_test_data
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

X, y = create_test_data.get_test_data(False)
ids = np.arange(len(y))
unexp_ids = ids[y==0]
exp_ids = ids[y==1]
edges = create_graph.create_source_unexp_edges(unexp_ids)
edges = create_graph.append_case_sink_edges(edges, exp_ids, 2)

print(edges)
fig, ax = plt.subplots()
#BG = nx.DiGraph()
#BG.add_edges_from(edges)
#nx.draw_networkx(BG,  ax=ax, with_labels=False,
#    )
fig.savefig('graph.png')