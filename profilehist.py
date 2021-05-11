import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def PlotProfileHistogram(x_data, y_data, nbins='auto', x_label: str = None, y_label: str = None, plot_title: str = None, output_filepath: str = None):
    """Plot a profile histogram 

    Args:
        x_data (list): List of X variables
        y_data (list): List of Y variables
        nbins (str, optional): Number of X-bins for histogram. Defaults to 'auto'.
        x_label (str, optional): Label for X-axis. Defaults to None.
        y_label (str, optional): Label for Y-axis. Defaults to None.
        plot_title (str, optional): Label for plot. Defaults to None.
        output_filepath (str or list, optional): Where to write the file to. A list of multiple paths can be passed. If None pass, plt.show() is called. Defaults to None.
    """
    #   get bin edges using numpy
    bin_edges = np.histogram_bin_edges(x_data, bins=nbins)
    #   note that numpy bin_edges includes first and last, but for digitise we dont need the last
    bin_edges_without_last = bin_edges[0:-1]

    number_of_bins = bin_edges_without_last.size

    # values range from 1 to number of bins
    bin_indices_for_xdata = np.digitize(x_data, bin_edges_without_last)

    # print(f"MIN: {np.min(bin_indices_for_xdata)}")
    # print(f"MAX: {np.max(bin_indices_for_xdata)}")

    binned_y_values = [[] for _bin in bin_edges_without_last]

    for bin_index, y_val in zip(bin_indices_for_xdata, y_data):
        #   add y value to appropriate bin
        binned_y_values[bin_index - 1].append(y_val)

    # print([bin_y for bin_y in binned_y_values])

    # print("debug breakpoint")

    binned_y_values_mean = [np.mean(y_bin) for y_bin in binned_y_values]
    binned_y_values_rms = [np.std(y_bin) for y_bin in binned_y_values]
    binned_y_values_error = [np.std(y_bin) / np.sqrt(len(y_bin))
                             for y_bin in binned_y_values]

    binned_y_values_mean = []
    binned_y_values_rms = []
    binned_y_values_error = []

    skipped_indexes = []

    for idx, y_bin in enumerate(binned_y_values):
        n_entries = len(y_bin)
        if n_entries == 0 or n_entries == 1:
            skipped_indexes.append(idx)
            continue

        mean = np.mean(y_bin)
        rms = np.std(y_bin)
        error = rms / n_entries

        binned_y_values_mean.append(mean)
        binned_y_values_rms.append(rms)
        binned_y_values_error.append(error)

    #   need to compute centre of bins
    x_value_of_bins = [(bin_edges[idx + 1] + bin_edges[idx]) /
                       2.0 for idx in range(number_of_bins) if idx not in skipped_indexes]
    number_of_bins = len(x_value_of_bins)
    # okay because bins are evenly sized by np.histogram_bin_edges
    half_width_of_bins = (x_value_of_bins[0] - x_value_of_bins[1]) / 2.0

    #   do some analysis on the results
    slope, intercept, rvalue, pvalue, stderr = linregress(
        x_value_of_bins, binned_y_values_mean)

    x_theory = x_value_of_bins
    y_theory = np.add(np.multiply(x_theory, slope), intercept)

    #   plot
    cap_size = 4
    fig, axes = plt.subplots()  # (ncols=6, nrows=1, figsize=(21, 5))
    axes.plot(x_theory, y_theory, color="blue", marker='', linestyle='-')
    axes.errorbar(x_value_of_bins, binned_y_values_mean,
                  xerr=half_width_of_bins, ecolor='k', fmt='k+', capsize=cap_size)
    axes.errorbar(x_value_of_bins, binned_y_values_mean, yerr=binned_y_values_rms,
                  ecolor='r', fmt=' ', capsize=cap_size, label='rms')
    axes.errorbar(x_value_of_bins, binned_y_values_mean, yerr=binned_y_values_error,
                  ecolor='g', fmt=' ', capsize=0.5 * cap_size, label='error')
    # axes.plot(x_theory, y_theory)
#    axes.set_title(plot_title)
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)

    legend_loc = 'lower right'
    #   if correlation is negative, put in upper right
    if rvalue < 0:
        legend_loc = 'upper right'

    axes.legend([f"$R$: {rvalue:0.2f}",
                 "bin width", "rms", "error"], loc=legend_loc, fontsize='small')
    if output_filepath is None:
        plt.show()
    else:
        if type(output_filepath) == str:
            fig.savefig(output_filepath, bbox_inches='tight')
            print(f"Profile Histogram plot saved at: {output_filepath}")
        else:
            for filepath in output_filepath:
                fig.savefig(filepath, bbox_inches='tight')
                print(f"Profile Histogram plot saved at: {filepath}")
