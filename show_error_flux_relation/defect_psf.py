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

def gaussian(x, amp, mu, sig, const):
    return amp * np.exp(-(x - mu)**2 / (2*(sig**2))) + const

def defect_gaussian(x, amp, mu, sig, const):
    return amp * np.exp(-(x - mu)**2 / (2*(sig**2))) + const - np.where(abs(x-mu) < 5, 0.1*amp, 0)

def linear(x, a, b):
    return a*x + b

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
    num_test = 100
    num_sample = 100
    x_data = np.arange(num_sample)
    source_fig, axs = plt.subplots(1, 2, figsize = (12,6))
    axs = axs.ravel()
    amp_array = np.zeros(num_test)
    error_array = np.zeros(num_test)
    test_set = np.logspace(0, 3, num_test)
    for i in range(num_test):
        y_data = gaussian(x_data, test_set[i], 50, 10, 0) + np.random.normal(0,1,num_sample)
        paras, covs = optimize.curve_fit( defect_gaussian, x_data, y_data, p0 = (10, 50 ,10 ,0))
        amp_array[i] = paras[0]
        error_array[i] = np.sqrt(covs[0,0])
        x_fit = np.arange(0, num_sample, 0.01)
        y_fit = defect_gaussian(x_fit, paras[0], paras[1], paras[2], paras[3])
        if i == 0:
            axs[0].scatter(x_data, y_data, c = 'r', marker = '+')
            axs[0].plot(x_fit, y_fit)
        elif i == num_test -1:
            axs[1].scatter(x_data, y_data, c = 'r', marker = '+')
            axs[1].plot(x_fit, y_fit)
    source_fig.show()
    last_amp = amp_array[-15:]
    last_error = error_array[-15:]
    paras, covs = optimize.curve_fit(power_law, last_amp, last_error)
    x_fit = np.array([last_amp[0], last_amp[-1]])
    y_fit = power_law(x_fit, paras[0], paras[1], paras[2])
    fig2, axs = plt.subplots(1,1)
    plt.scatter(amp_array, error_array)
    plt.scatter(last_amp, last_error, marker = '+', c = 'r', label = "The powerlaw part I fit")
    plt.plot(x_fit, y_fit, 'b-', label = r'y = %.4f$x^{%.4f}$ + %.4f' % (paras[0], paras[1], paras[2]))
    axs.set_xscale("log")
    axs.set_yscale("log")
    axs.set_xlabel("flux(mJy)")
    axs.set_ylabel("flux uncertainties(mJy)")
    plt.grid(True, which = 'both')
    plt.legend()
    fig2.show()
    input()
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
