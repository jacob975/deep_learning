#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH2.
Usage:
    20180329_CH2_4_cheating_among_students2.py
Editor:
    Jacob975

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
    # Initialize constants
    N = 100                                         # 100 of students
    p = pm.Uniform("freq_cheating", 0, 1)           # The freq I want
    #-----------------------------------
    # Modeling
    true_answer = pm.Bernoulli("truths", p, size = N)
    first_coin_flips = pm.Bernoulli("firtst_flips", 0.5, size = N)
    second_coin_flips = pm.Bernoulli("second_flips", 0.5, size = N)
    @pm.deterministic
    def p_skewed(p=p):
        return 0.5*p +0.25
    yes_responses = pm.Binomial("number_cheaters", 100, p_skewed, value = 35, observed = True)
    print ("{0} : {1}".format(yes_responses, yes_responses.value))
    model = pm.Model([yes_responses, p_skewed, p])
    # to be explain in Chapter 3
    mcmc = pm.MCMC(model)
    mcmc.sample(25000, 2500)
    #-----------------------------------
    # plot the answer
    figsize(12.5, 3)
    p_trace = mcmc.trace("freq_cheating")[:]
    plt.hist(p_trace, histtype = "stepfilled", normed = True, alpha = 0.85, bins = 30, label = "posterior distribution", color = "#348ABD")
    plt.vlines([.05, .35], [0,0], [5, 5], alpha = 0.2)
    plt.xlim(0, 1)
    plt.xlabel("Value of $p$")
    plt.ylabel("Density")
    plt.title("Posterior distribution of parameter $p$, from alternate model")
    plt.legend()
    plt.show()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
