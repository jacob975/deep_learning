#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH4.
Usage:
    20180601_CH4_convergence_of_poisson_random_variables.py
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
'''
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.dpi'] = 300
'''
figsize(12.5, 5)
import pymc as pm

# initialize
sample_size = 100000
expected_value = lambda_ = 4.5
poi = pm.rpoisson
N_samples = range(1, sample_size, 100)
# plot three poisson random variables sequence
for k in range(3):
    samples = poi(lambda_, size = sample_size)
    partial_average = [samples[:i].mean() for i in N_samples]
    plt.plot(N_samples, partial_average, lw=1.5, label="average \
    of $n$ samples; seq. %d"%k)
# plot some basic infos
plt.plot(N_samples, expected_value*np.ones_like(partial_average), ls="--", label = "true expected value", c = "k")
plt.ylim(4.35, 4.65)
plt.title("Convergence of the average of \n random variables to their expected value")
plt.ylabel("Average of $n$ samples")
plt.xlabel("Number of samples, $n$")
plt.legend()
plt.show()
