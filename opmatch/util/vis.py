import matplotlib.pyplot as plt
plt.style.use('ggplot')
colors = plt.rcParams['axes.prop_cycle']
import numpy as np
from matplotlib.ticker import MaxNLocator

def plot_matching(ps, exp_nexp_dic,
    title='Optimal PS matching results',
    set_title=True,
    title_fs=18,
    xlabel='Propensity Score',
    xlabel_fs=18,
    ylabel='Group Number',
    ylabel_fs=18,
    exposed_label='exposed',
    unexposed_label='not exposed',
    legend=True,
    legend_fs=18,
    legend_pos=0,
    legend_facecolor='white',
    show=True,
    save=False,
    figname='optmatch\\tests\\matched_ps.png',
    color=None,
    markerstyle_exp='x',
    markersize_exp=60,
    markerstyle_unexp='o',
    markersize_unexp=60,
    xtickparams_ls=14,
    ytickparams_ls=14,
    figsize=(7,5),
    dpi=100):
    
    fig, ax = plt.subplots(figsize=figsize)
    exp_ids = list(exp_nexp_dic.keys())

    for i, exp in enumerate(exp_ids):
        if i==0:
            exp_label = exposed_label
            nexp_label = unexposed_label    
        else:
            exp_label=nexp_label=None
        if isinstance(color, type(None)):
            color0 = list(plt.rcParams['axes.prop_cycle'])[0]['color']
            color1 = list(plt.rcParams['axes.prop_cycle'])[1]['color']
        ax.scatter(ps[exp], i, marker=markerstyle_exp, color=color0, 
                label=exp_label, s=markersize_exp)
        nexp_ps = ps[exp_nexp_dic[exp]]
        group_arr = np.ones(len(nexp_ps))*i
        ax.scatter(nexp_ps, group_arr, marker=markerstyle_unexp, color=color1, 
                label=nexp_label, s=markersize_unexp)
    if legend:
        ax.legend(fontsize=legend_fs, loc=legend_pos, facecolor=legend_facecolor)
    if set_title:
        ax.set_title(title, fontsize=title_fs)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel(xlabel, fontsize=xlabel_fs)
    ax.set_ylabel(ylabel, fontsize=ylabel_fs)
    ax.tick_params(axis='x', which='major', labelsize=xtickparams_ls)
    ax.tick_params(axis='y', which='major', labelsize=ytickparams_ls)
    if show:
        plt.rcParams["figure.dpi"] = dpi
        plt.show()
    if save:
        fig.savefig(figname, dpi=dpi)
    