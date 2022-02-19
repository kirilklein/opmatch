import os, sys
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from opmatch.util import create_graph
import create_test_data

X, y, ps = create_test_data.get_test_data(False, 2000, 3)

if __name__ == '__main__':
    out_ = create_graph.create_distance_edge_list_parallel(y, ps, 2)
    print(len(out_[0]))