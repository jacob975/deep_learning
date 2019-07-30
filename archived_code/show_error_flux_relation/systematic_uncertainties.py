#!/usr/bin/python3
'''
Abstract:
    This is a program to prove my guess 
Usage:
    provement.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181024
####################################
update log
20181024 version alpha 1:
    1. Birthday.
'''
import numpy as np
from scipy import optimize
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

mu = 5
sig = 1

def gaussian(x, amp, const):
    return amp * np.exp(-(x - mu)**2 / (2*(sig**2))) + const

def linear(x, a):
    return a*x

def const(x, c):
    return np.ones(len(x)) * c

def power_law(x, a, p, b):
    return a*x**p + b

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Initialize
    num_test = 500
    num_sample = 11
    x_data = np.arange(num_sample)
    source_fig, axs = plt.subplots(1, 2, figsize = (12,6))
    axs = axs.ravel()
    amp_array = np.zeros(num_test)
    error_array = np.zeros(num_test)
    test_set = np.logspace(-2, 3, num_test)
    # Try all the test sets.
    for i in range(num_test):
        y_data = (1 + np.random.normal(0, 0.17,num_sample))*(gaussian(x_data, test_set[i], 0) + np.random.normal(0, 0.35,num_sample))
        paras, covs = optimize.curve_fit( gaussian, x_data, y_data, p0 = (10, 0))
        amp_array[i] = paras[0]
        error_array[i] = np.sqrt(covs[0,0])
        x_fit = np.arange(0, num_sample, 0.01)
        y_fit = gaussian(x_fit, paras[0], paras[1])
        if i == 199:
            axs[0].set_title("S/N $\cong$ 3")
            axs[0].plot(x_data, y_data, 'r-')
            axs[0].plot(x_fit, y_fit)
        elif i == num_test -1:
            axs[1].set_title("S/N $\gg$ 3")
            axs[1].plot(x_data, y_data, 'r-')
            axs[1].plot(x_fit, y_fit)
    source_fig.show()
    # Fit the head trend
    first_amp = amp_array[:50]
    first_error = error_array[:50]
    paras_h, covs = optimize.curve_fit(const, first_amp, first_error)
    x_fit_first = np.array([first_amp[0], first_amp[-1]])
    y_fit_first = const(x_fit_first, paras_h[0])
    # Fit the tale trend
    last_amp = amp_array[-50:]
    last_error = error_array[-50:]
    paras_t, covs = optimize.curve_fit(linear, last_amp, last_error)
    x_fit_last = np.array([last_amp[0], last_amp[-1]])
    y_fit_last = linear(x_fit_last, paras_t[0])
    # Plot all fitting results
    fig2, axs = plt.subplots(1,1)
    plt.scatter(amp_array, error_array)
    plt.scatter(first_amp, first_error, marker = '+', c = 'y', label = "The const part I fit")
    plt.scatter(last_amp, last_error, marker = '+', c = 'r', label = "The powerlaw part I fit")
    plt.plot(x_fit_first, y_fit_first, 'c-', label = r'y = %.4f' % (paras_h[0]))
    plt.plot(x_fit_last, y_fit_last, 'r-', label = r'y = %.4fx' % (paras_t[0]))
    axs.set_title("Systematic error test")
    axs.set_xscale("log")
    axs.set_yscale("log")
    axs.set_xlabel("amplitude")
    axs.set_ylabel("amplitude uncertainties")
    axs.set_xlim(0.01, 5000.)
    axs.set_ylim(0.01, 500.)
    plt.grid(True, which = 'both')
    plt.legend()
    fig2.show()
    input()
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
