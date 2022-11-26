import matplotlib.pyplot as plt
plt.style.use('ggplot')
colors = plt.rcParams['axes.prop_cycle']
import numpy as np
from matplotlib.ticker import MaxNLocator

def plot_matching(ps, case_control_dic,
    title='Optimal PS matching results',
    set_title=True,
    title_fs=18,
    xlabel='Propensity Score',
    xlabel_fs=18,
    ylabel='Group Number',
    ylabel_fs=18,
    case_label='case',
    control_label='not case',
    legend=True,
    legend_fs=18,
    legend_pos=0,
    legend_facecolor='white',
    show=True,
    save=False,
    figname='opmatch\\tests\\matched_ps.png',
    color=None,
    markerstyle_case='x',
    markersize_case=60,
    markerstyle_control='o',
    markersize_control=60,
    xtickparams_ls=14,
    ytickparams_ls=14,
    figsize=(7,5),
    dpi=100):
    
    fig, ax = plt.subplots(figsize=figsize)
    case_ids = list(case_control_dic.keys())

    for i, case in enumerate(case_ids):
        if i==0:
            case_label = case_label
            control_label = control_label    
        else:
            case_label=control_label=None
        if isinstance(color, type(None)):
            color0 = list(plt.rcParams['axes.prop_cycle'])[0]['color']
            color1 = list(plt.rcParams['axes.prop_cycle'])[1]['color']
        ax.scatter(ps[case], i, marker=markerstyle_case, color=color0, 
                label=case_label, s=markersize_case)
        control_ps = ps[case_control_dic[case]]
        group_arr = np.ones(len(control_ps))*i
        ax.scatter(control_ps, group_arr, marker=markerstyle_control, color=color1, 
                label=control_label, s=markersize_control)
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
    