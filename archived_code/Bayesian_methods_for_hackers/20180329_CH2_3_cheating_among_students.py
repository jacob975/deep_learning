#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH2.
Usage:
    20180329_CH2_3_cheating_among_students.py
Editor:
    Jacob975

concept:
    Privacy algorithm
    assume interviewer didn't know how many fliping you do.
    Head or tails for each flip.

    flip coin   -> heads    -> tell the truth
                -> tails    -> flip the coin again  -> Say Yes for head, say no for tail 

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170329
####################################
update log
20180329 version alpha 1:
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
    # Initialize variables and constants
    N = 100                              
    p = pm.Uniform("freq_cheating", 0, 1)
    true_answer = pm.Bernoulli("truths", p, size = N)
    first_coin_flips = pm.Bernoulli("firtst_flips", 0.5, size = N)
    second_coin_flips = pm.Bernoulli("second_flips", 0.5, size = N)
    
    @pm.deterministic
    def observed_proportion(t_a = true_answer, fc = first_coin_flips, sc = second_coin_flips):
        observed = fc * t_a + (1 - fc)*sc
        return observed.sum() / float(N)
    
    #-----------------------------------
    # import datasets
    X = 35
    observations = pm.Binomial("obs", N, observed_proportion, observed = True, value = X)
    if VERBOSE>0:
        print ("Property of observations:")
        print (observations)
        print (observations.value)
        print (type(observations))
    model = pm.Model([p, true_answer, first_coin_flips, second_coin_flips, observed_proportion, observations])
    # to be explained in Chapter 3
    mcmc = pm.MCMC(model)
    mcmc.sample(40000, 15000)
    #-----------------------------------
    # plot the answer
    figsize(12.5, 3)
    p_trace = mcmc.trace("freq_cheating")[:]
    plt.hist(p_trace, histtype = "stepfilled", normed = True, alpha = 0.85, bins = 30, label = "posterior distribution", color = "#348ABD")
    #plt.vlines([.05, .35], [0, 0], [5, 5], alpha = 0.3)
    plt.xlim(0, 1)
    plt.xlabel("Value of $p$")
    plt.ylabel("Density")
    plt.title("Posterior distribution of parameter $p$")
    plt.legend()
    plt.show()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
