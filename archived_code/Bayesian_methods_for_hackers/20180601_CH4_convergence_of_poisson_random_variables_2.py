#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH4.
Usage:
    20180601_CH4_convergence_of_poisson_random_variables_2.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170601
####################################
update log
20180601 version alpha 1:
    1. The code works

'''
import numpy as np
from IPython.core.pylabtools import figsize
import matplotlib.pyplot as plt

figsize(12.5, 4)
import pymc as pm

# initialize
poi = pm.rpoisson
N_Y = 250 # Use this many to approximate D(N).
# Use this many samples in the approximation to the variance.
N_array = np.arange(1000, 50000, 2500)
D_N_results = np.zeros(len(N_array))
lambda_ = 4.5
expected_value = lambda_ # for X ~ Poi(lambda), E[X] = lambda

def D_N(n):
    '''
    This function approimates D_n, the average variance of using n samples.
    '''
    Z = poi(lambda_, size = (n, N_Y))
    print(Z.shape)
    average_Z = Z.mean(axis = 0)
    return np.sqrt(((average_Z - expected_value)**2 ).mean())

for i, n in enumerate(N_array):
    D_N_results[i] = D_N(n)
plt.xlabel("$N$")
plt.ylabel("Expected squared-distance from true value")
plt.plot(N_array, D_N_results, lw = 3, label = "expected distance between\n\
expected value and \naverage of $N$ random variables")
plt.plot(N_array, np.sqrt(expected_value)/np.sqrt(N_array), lw = 2,  ls="--", label = r"$\frac{\sqrt{\lambda}}{\sqrt{N}}$")
plt.legend()
plt.title("How quickly is the sample average converging?")
plt.show()
