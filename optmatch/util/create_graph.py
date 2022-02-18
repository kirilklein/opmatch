from typing import List, Union
import networkx as nx
import pandas as pd

def create_source_unexp_edges(unexp_ids:List[int])->List[tuple]:
    """Create edges between source node and unexposed patients 
    with capacity 1 and no weight (fully connected)"""
    edge_list = [('source', unexp_id, {'capacity':1, 'weight':0})\
         for unexp_id in unexp_ids]
    return edge_list

def append_case_sink_edges(edge_list:List[tuple], exposed_ids:List[int], 
                        k:int)->List[tuple]:
    """Append edges to edge_list which the exposed to the sink, 
    with capacities that result in 1:k matching."""
    append_list = [(exp_id, 'sink', {'capacity':k, 'weight':0})\
        for exp_id in exposed_ids]
    return edge_list + append_list

def create_initial_edge_list(unexp_ids:List[int], 
                        exposed_ids:List[int], k:int)->List[tuple]:
    """Create initial edge list, without connections between exposed and unexposed."""
    edge_list = create_source_unexp_edges(unexp_ids)
    return append_case_sink_edges(edge_list, exposed_ids, k)

#def create_distance_edge_list(data:Union[pd.DataFrame, None],
#    X:Union[List[str], np.array, None], 
#    y:Union[List[str], np.array, None]):
#    edge_list = create_initial_edge_list()
def create_distance_edge_list(treatment, ps): 
    """treatment: boolean np.array (treatment/no treatment)
       ps: float np.array propensity scores"""
    pd.Dataframe(np.concatenate(treatment, ps), columns = ['ps', 'treatment'])
def create_di_graph(edge_list:List[tuple])->nx.DiGraph:
    G = nx.DiGraph()
    G.add_edges_from(edge_list)
    return G
