import seaborn as sns 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
from matplotlib import lines, patches
from Graphs import ColorConstants as cc

def remove_string(df, columns=['Interest Rate', 'Loan-Value Ratio']):
    ''' Remove rows with string values '''
    df = (df.drop(columns, axis=1).join(df[columns].apply(pd.to_numeric, errors='coerce')))
    df = df[df[columns].notnull().all(axis=1)]
    df.dtypes
    for col, dtype in df.dtypes.items():
        if str(dtype) == 'object':
            print(col, dtype)   
    return df

def filter_extremes_values(df):
    ''' Filter extreme values out - should be one bool probably '''
    df = df[df['Loan-Income Ratio'] < df['Loan-Income Ratio'].quantile(.98)]
    df = df[df['Applicant Income'] < df['Applicant Income'].quantile(.999)]
    df = df[df['Applicant Income'] > 0]
    df = df[df['Family Units Per Capita'] < df['Family Units Per Capita'].quantile(.999)]
    return df

def summary_stats(df, quanitles=[.25, .50, .75]):
    ''' Compute summary stats table - add HTML output?'''
    stat_cols = [col for col in df.columns if col != 'state_name']
    summary_stats = {}
    for col in stat_cols:
        q = list(df[col].quantile(quanitles).values)
        s = [df[col].count(), df[col].min(), q[0], q[1], q[2], df[col].max(), df[col].mean(),\
             df[col].std(), df[col].kurt(), df[col].skew()]
        summary_stats[col] = s 
    stats_df = pd.DataFrame(summary_stats).T
    new_columns = ['Count', 'Minimum', '25th', '50th', '75th', 'Maximum', 'Mean', 'SDV', 'Kurtosis', 'Skew']
    stats_df.columns = new_columns
    return stats_df

def correlation_matrix(df, title='HMDA Correlation Matrix', wanted_label='Loan Approved', 
                       source='Source: 2020 HMDA Data Release'):
    ''' Create correlation matrix with a highlighted label'''

    source_text_color = "#a2a2a2"
    source_font_size = 14
    mycmap_colors = []
    data_cols = [col for col in df.columns if 'state_code' not in col]
    corr_df = df[data_cols].corr()
    mask = np.triu(np.ones_like(corr_df, dtype=bool)) # Broken
    plt.figure(figsize=(26, 14), dpi=100)
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    ax = sns.heatmap(corr_df, annot=True, fmt='.2f', cbar=False, cmap=cmap, linewidths=.05, linecolor='black', mask=None)
    sns.set(font_scale=2)
    plt.title(title , fontsize=28, fontweight='bold', y=1.02)
    plt.ylabel("")

    n = len(data_cols)
    wanted_index = data_cols.index(wanted_label)
    x, y, w, h = 0, wanted_index, n, 1
    for _ in range(2):
        ax.add_patch(patches.Rectangle((x, y), w, h, fill=False, edgecolor=cc.RED, lw=4, clip_on=False))
        x, y = y, x 
        w, h = h, w 
    ax.tick_params(length=0)
    ax.text(0, 25, source, color=source_text_color, fontsize=source_font_size)

    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=18, color='black')
    ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=18, color='black')