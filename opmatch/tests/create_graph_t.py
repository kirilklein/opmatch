import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR,'opmatch' ))
from util import create_graph
import create_test_data
from time import time

df = create_test_data.get_test_data(True, 1000, 10, random_seed=0)
df['matched'] = 0
df['exposed'] = df.y

if __name__ == '__main__':
    s = time()
    out = create_graph.create_distance_edge_list_parallel(df, 2)
    print('time:', time()-s)
    s1 = time()
    #print(out[0])
    #print(out[1])
    #print(out[2])
    #print('checksum: ', all([o0==o1 for o0, o1 in zip(out0[0], out1[1])]))
