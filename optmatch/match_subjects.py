from util import create_graph
import networkx as nx



def match():
    edge_list = create_graph.create_distance_edge_list()
    G = create_graph.create_digraph(edge_list)
    mincostFlow_dic = nx.max_fl