#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH2.
Usage:
    20180328_CH2_1_Atest.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170328
####################################
update log
20180328 version alpha 1:
    1. I don't know

'''
import pymc as pm
import numpy as np
import matplotlib.pyplot as plt
import time
from IPython.core.pylabtools import figsize

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------
    # prior probability
    p = pm.Uniform("p", lower = 0, upper = 1)
    # initialize constants
    p_true = 0.5
    N = 1500
    # sample N Bernoulli random variables frpm Ber(0.05)
    # Each random variable has a 0.05 chance of being a 1.
    # This is the data=generation step.
    occurrences = pm.rbernoulli(p_true, N)
    print ("numbers of 1 = {0}".format(occurrences.sum()))
    #-----------------------------------
    # observed frequency
    print ("What is the observed frequency in Group A? %.4f" % occurrences.mean())
    print ("Does the observed frequency equal the true frequency? {0}".format(occurrences.mean() == p_true))
    #-----------------------------------
    # apply Bayesian method
    # Include the observations, which are Bernoulli.
    obs = pm.Bernoulli("obs", p, value = occurrences, observed=True)

    # to be explained in Chapter 3
    mcmc = pm.MCMC([p, obs])
    mcmc.sample(20000, 1000)
    #-----------------------------------
    # plot the answer of Bayesian method
    figsize(12.5, 4)
    plt.title("Posterior distribution of $p_A$, the true effectiveness of site A")
    plt.vlines(p_true, 0, 90, linestyle="--", label="true $p_A$ (unknown)")
    plt.hist(mcmc.trace("p")[:], bins = 35, histtype = "stepfilled", normed = True)
    plt.xlabel("Value of $p_A$")
    plt.ylabel("Density")
    plt.legend()
    plt.show()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
