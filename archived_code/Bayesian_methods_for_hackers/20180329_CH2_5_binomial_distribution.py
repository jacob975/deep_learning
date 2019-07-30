#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH2.
Usage:
    20180329_CH2_5_binomial_distribution.py
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
    # generate answer
    figsize(12.5, 4)
    import scipy.stats as stats
    binomial = stats.binom
    parameters = [(10, .4), (10, .9)]
    print (parameters)
    colors = ["#348ABD", "#A60628"]
    # plot answer
    for i in range(2):
        N, p = parameters[i]
        _x = np.arange(N+1)
        print (_x)
        plt.bar(_x - 0.5, binomial.pmf(_x, N, p), color = colors[i], edgecolor=colors[i],
                alpha = 0.6, label = "$N$: %d, $p$: %.1f" % (N, p), linewidth=3)
    plt.legend(loc = "upper left")
    plt.xlim(0, 20.5)
    plt.xlabel("$k$")
    plt.ylabel("$P(X=k)$")
    plt.title("Probability mass distributions of binomial random variables")
    plt.show()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
