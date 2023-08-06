import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import itertools

def population_plot(data_summary, breaks_centers, channel_names, channel_names_to_plot=None, plot_SEM = True, figsize=(10, 10)):
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    if channel_names_to_plot is None:
        channel_names_to_plot = channel_names
    for i, name in enumerate(channel_names):
        if name in channel_names_to_plot:
            p = ax.plot(breaks_centers, data_summary[0, i], lw=2, label=name)
            norm = np.sqrt(data_summary[2, i]) if plot_SEM else 1
            ax.fill_between(breaks_centers, data_summary[0, i]+data_summary[1, i]/norm , data_summary[0, i]-data_summary[1, i]/norm, facecolor=p[0].get_color(), alpha=0.5)
    ax.plot([0, 1], [0, 1], transform=ax.transAxes, label="random")
    l=ax.legend(loc="upper left")

def per_nuc_plot(data, breaks_centers, channel_names, channel_names_to_plot=None, figsize=(30, 30), ncols=3):
    nrows = ceil(data.shape[0]/ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    if channel_names_to_plot is None:
        channel_names_to_plot = channel_names
    for i,j in itertools.product(range(nrows), range(ncols)):
        nuc_idx = i*ncols + j
        if nuc_idx >= data.shape[0]:
            axes[i,j].set_axis_off()
        else:
            axes[i,j].set_xlim(0, 1)
            axes[i,j].set_ylim(0, 1)
            for c, name in enumerate(channel_names):
                if name in channel_names_to_plot:
                    axes[i,j].plot(breaks_centers, data[nuc_idx, c], lw=2, label=name)
            axes[i,j].plot([0, 1], [0, 1], transform=axes[i,j].transAxes)
            if nuc_idx==0:
                axes[i,j].legend(loc="upper left")
