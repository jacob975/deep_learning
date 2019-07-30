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

def gaussian(x, amp, mu, sig, const):
    return amp * np.exp(-(x - mu)**2 / (2*(sig**2))) + const

def defect_gaussian(x, amp, const):
    return amp * np.exp(-(x - mu)**2 / (2*(sig**2))) + const - np.where(abs(x-mu) < 1, 0.20*amp, 0)

def linear(x, a):
    return a*x

def power_law(x, a, p, b):
    return a*x**p + b

def const(x, a):
    return np.ones(len(x)) * a

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
    for i in range(num_test):
        y_data = gaussian(x_data, test_set[i], mu, sig, 0) + 0.35 * np.random.normal(0,1,num_sample)
        paras, covs = optimize.curve_fit( defect_gaussian, x_data, y_data, p0 = (10 ,0))
        amp_array[i] = paras[0]
        error_array[i] = np.sqrt(covs[0,0])
        x_fit = np.arange(0, num_sample, 0.01)
        y_fit = defect_gaussian(x_fit, paras[0], paras[1])
        if i == 199:
            axs[0].set_title("S/N $\cong$ 3")
            axs[0].plot(x_data, y_data, 'r-')
            axs[0].plot(x_fit, y_fit)
        elif i == num_test -1:
            axs[1].set_title("S/N $\gg$ 3")
            axs[1].plot(x_data, y_data, 'r-')
            axs[1].plot(x_fit, y_fit)
    source_fig.show()
    # fit the head part
    first_amp = amp_array[:15]
    first_error = error_array[:15]
    paras_h, covs = optimize.curve_fit(const, first_amp, first_error)
    x_fit_head = np.array([first_amp[0], first_amp[-1]])
    y_fit_head = const(x_fit_head, paras_h[0])
    # fit the tail part
    last_amp = amp_array[-20:]
    last_error = error_array[-20:]
    paras, covs = optimize.curve_fit(linear, last_amp, last_error)
    x_fit = np.array([last_amp[0], last_amp[-1]])
    y_fit = linear(x_fit, paras[0])
    # plot every fitting.
    fig2, axs = plt.subplots(1,1)
    plt.scatter(amp_array, error_array)
    plt.scatter(last_amp, last_error, marker = '+', c = 'r', label = "The powerlaw part I fit")
    plt.scatter(first_amp, first_error, marker = '+', c = 'y', label = "The const part I fit")
    plt.plot(x_fit_head, y_fit_head, 'g-', label = r'y = %.4f' % (paras_h[0]))
    plt.plot(x_fit, y_fit, 'b-', label = r'y = %.4fx' % (paras[0]))
    axs.set_title("Defective PSF test")
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
