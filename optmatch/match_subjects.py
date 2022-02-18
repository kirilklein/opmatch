from util import fit_ps, create_graph, preprocess
import networkx as nx
import numpy as np
import pandas as pd
from typing import Union, List


def match(scores:Union[str, np.array[float], None]=None,):
    """Input:
    data: pd.DataFrame, 
    X[n_subject, n_covariates], y[n_subj], score[n_subj], ids[n_subj]: 
                        If data provided: 
                            columns specifying the covariates, treatment, 
                            scores (e.g. propensity score), ids
                        else: arrays containing the corresponding data
                        if ids==None: enumerate patients starting from 0
                        if score==None: perform logistic regression"""
    
    edge_list = create_graph.create_distance_edge_list()
    G = create_graph.create_digraph(edge_list)
    mincostFlow_dic = nx.max_flow_min_cost(G, 'source', 'sink')
    return mincostFlow_dic