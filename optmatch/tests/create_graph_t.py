import os, sys
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from optmatch.util import create_graph
import create_test_data
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

X, y, ps = create_test_data.get_test_data(False, 500, 3)

ids = np.arange(len(y))
unexp_ids = ids[y==0]
exp_ids = ids[y==1]

#fig, ax = plt.subplots()
#BG = nx.DiGraph()
#BG.add_edges_from(edges)
#nx.draw_networkx(BG,  ax=ax, with_labels=False,
#    )
#fig.savefig('graph.png')
if __name__ == '__main__':
    out_ = create_graph.create_distance_edge_list_parallel(y, ps, 2)
    print(len(out_[0]))