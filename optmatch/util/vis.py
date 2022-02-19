import matplotlib.pyplot as plt
plt.style.use('ggplot')
colors = plt.rcParams['axes.prop_cycle']
import numpy as np
from matplotlib.ticker import MaxNLocator

def plot_matching(ps, exp_nexp_dic, 
    xlabel='Propensity Score',
    ylabel='Group Number',
    exposed_label='exposed',
    unexposed_label='not exposed',
    show=True,
    save=False,
    figname='optmatch\\tests\\matched_ps.png',
    color=None,
    figsize=(6,4),
    dpi=80):
    
    fig, ax = plt.subplots(figsize=figsize)
    exp_ids = list(exp_nexp_dic.keys())
    for i, exp in enumerate(exp_ids):
        if i==0:
            exp_label = exposed_label
            nexp_label = unexposed_label    
        else:
            exp_label=nexp_label=None
        if isinstance(color, type(None)):
            color = list(plt.rcParams['axes.prop_cycle'])[0]['color']
        ax.scatter(ps[exp], i, marker='x', color=color, label=exp_label)
        nexp_ps = ps[exp_nexp_dic[exp]]
        group_arr = np.ones(len(nexp_ps))*i
        ax.scatter(nexp_ps, group_arr, marker='.', color=color, label=nexp_label)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if show:
        plt.rcParams["figure.dpi"] = dpi
        plt.show(dpi)
    if save:
        fig.savefig(figname, dpi=dpi)
    