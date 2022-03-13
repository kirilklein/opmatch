import os, sys
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from opmatch.util import create_graph
from opmatch.util import create_graph_new 
import create_test_data
from time import time

df = create_test_data.get_test_data(True, 10, 3)

if __name__ == '__main__':
    s0 = time()
    out0 = create_graph.create_distance_edge_list_parallel(df, 2)
    print('time for old:', time()-s0)
    s1 = time()
    out1 = create_graph_new.create_distance_edge_list_parallel(df, 2)
    print('time for new:', time()-s1)
    print('checksum: ', all([o0==o1 for o0, o1 in zip(out0, out1)]))
    #print(len(out_[0]))