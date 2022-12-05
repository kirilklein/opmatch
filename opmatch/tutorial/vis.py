import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

def age_bmi_scatter_2d(df):
    plt.figure(figsize=(4,3)) 
    plt.plot(df.age[df.case==0], df.bmi[df.case==0], 'bo', label='control')
    plt.plot(df.age[df.case==1], df.bmi[df.case==1], 'ro', label='case')
    plt.xlabel('age')
    plt.ylabel('bmi')
    plt.legend(loc=(0,1.02), ncol=2)

def visualize_matched_scatter(df, cc_dics, titles):
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    fig, axes = plt.subplots(1,len(cc_dics), figsize=(8,4))
    for cc_dic, title, ax in zip(cc_dics,titles,  axes):
        matched = []
        for color, (case, controls) in zip(colors, cc_dic.items()):
            matched.extend(controls)
            matched.append(case)
           
            ax.scatter(df.loc[case, 'age'], df.loc[case, 'bmi'], color = color, marker = 'x')
            ax.scatter(df.loc[controls, 'age'], df.loc[controls, 'bmi'], color = color, marker='o')
        unmatched = [i for i in df.index if i not in matched]
        ax.scatter(df.loc[unmatched, 'age'], df.loc[unmatched, 'bmi'], color = 'k', marker='.', alpha=.2)
        ax.set_title(title)
        
    # set shared label for x and y axis
    fig.text(0.5, 0.04, 'age', ha='center', va='center')
    fig.text(0.04, 0.5, 'bmi', ha='center', va='center', rotation='vertical')

def plot_ps_matched(df, case_control_dic,
    title='Optimal PS matching',
    set_title=True,
    title_fs=18,
    xlabel='Propensity Score',
    xlabel_fs=18,
    ylabel='Case Number',
    ylabel_fs=18,
    case_label='case',
    control_label='matched controls',
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
    markerstyle_control='.',
    markersize_control=40,
    xtickparams_ls=14,
    ytickparams_ls=14,
    figsize=(4,3),
    dpi=100):
    
    fig, ax = plt.subplots(figsize=figsize)
    case_ids = list(case_control_dic.keys())
    ps = df.ps
    ps_control = df[df.case==0].ps
    for i, case in enumerate(case_ids):
        if i==0:
            case_label = case_label
            control_label = control_label    
        else:
            case_label=control_label=None
        if isinstance(color, type(None)):
            color0 = list(plt.rcParams['axes.prop_cycle'])[0]['color']
            color1 = list(plt.rcParams['axes.prop_cycle'])[1]['color']
        ax.scatter(ps[case], i+1, marker=markerstyle_case, color=color0, 
                label=case_label, s=markersize_case)
        control_ps = ps[case_control_dic[case]]
        group_arr = np.ones(len(control_ps))*(i+1)
        ax.scatter(control_ps, group_arr, marker=markerstyle_control, color=color1, 
                label=control_label, s=markersize_control)
    ax.scatter(ps_control, np.zeros(len(ps_control)), label = 'all controls', color='gray', marker='.', s=markersize_control)
    
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
    
def standardized_difference_plot(df, cc_dic, var_cols=['age', 'bmi']):
    # plot standardized difference between cases and controls
    fig, ax = plt.subplots(figsize=(4,3))
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    cases = df[df.case==1]
    controls = df[df.case==0]
    matched = []
    for case, controls_ls in cc_dic.items():
        matched.extend(controls_ls)
    matched_controls = df.loc[matched]
    # before matching
    for i, var in enumerate(var_cols):
        if i==0:
            label='before matching'
            matched_lbl = 'matched'
        else:
            label=None
            matched_lbl = None
        sd = np.abs((cases[var].mean() - controls[var].mean())/np.sqrt((cases[var].std()**2 + controls[var].std()**2)/2))
        matched_sd = np.abs((cases[var].mean() - matched_controls[var].mean())/np.sqrt((cases[var].std()**2 + matched_controls[var].std()**2)/2))
        ax.scatter(sd, i, color=colors[0], label=label, marker='o', s=40, facecolors='none')
        ax.scatter(matched_sd, i, color=colors[0], label=matched_lbl, marker='.', s=80)
    # set y ticks to var names
    ax.set_yticks(range(len(var_cols)))
    ax.set_yticklabels(var_cols)
    ax.set_xlabel('Absolute standardized difference')
    ax.legend()
    # get all matched controls
    
    
    # after matching
    # now compute standardized difference for each case-control pair
    