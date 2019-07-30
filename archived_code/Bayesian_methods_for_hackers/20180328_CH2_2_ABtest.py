#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH2.
Usage:
    20180328_CH2_2_ABtest.py
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
figsize(12, 4)

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------
    # initialize constants
    true_p_A = 0.05
    true_p_B = 0.04
    N_A = 1500
    N_B = 750
    # Generate some observations.
    occurrences_A = pm.rbernoulli(true_p_A, N_A)
    occurrences_B = pm.rbernoulli(true_p_B, N_B)
    print ("numbers of Site A = {0}".format(occurrences_A.sum()))
    print ("numbers of Site B = {0}".format(occurrences_B.sum()))
    #-----------------------------------
    # observed frequency
    print ("What is the observed frequency in Group A? %.4f" % occurrences_A.mean())
    print ("What is the observed frequency in Group B? %.4f" % occurrences_B.mean())
    # Set up the PyMC model, Again assume Uniform priors for p_A and p_B.
    p_A = pm.Uniform("p_A", 0, 1)
    p_B = pm.Uniform("p_B", 0, 1)
    #Define the deterministic delta function. This is our unknown of interest.
    @pm.deterministic
    def delta(p_A = p_A, p_B = p_B):
        return p_A - p_B
    #-----------------------------------
    # apply Bayesian method
    # Set of observations; in this case , we have two oservation datasets.
    obs_A = pm.Bernoulli("obs_A", p_A, value = occurrences_A, observed=True)
    obs_B = pm.Bernoulli("obs_B", p_B, value = occurrences_B, observed=True)
    # to be explained in Chapter 3
    mcmc = pm.MCMC([p_A, p_B, delta, obs_A, obs_B])
    mcmc.sample(25000, 5000)
    #-----------------------------------
    # plot the answer of Bayesian method
    p_A_samples = mcmc.trace("p_A")[:]
    p_B_samples = mcmc.trace("p_B")[:]
    delta_samples = mcmc.trace("delta")[:]
    figsize(12.5, 10)
    # histogram of posteriors
    '''
    # A samples
    ax = plt.subplot(311)
    plt.xlim(0, .1)
    plt.hist(p_A_samples, histtype="stepfilled", bins=30, alpha=0.85,
            label="posterior of $p_A$", color = "#A60628", normed = True)
    plt.vlines(true_p_A, 0, 80, linestyle="--", label="true $p_A$ (unknown)")
    plt.legend(loc="upper right")
    plt.title("Posterior distributions of $p_A$, $p_B$, and delta unknowns")
    plt.ylim(0, 80)
    # B samples
    ax = plt.subplot(312)
    plt.xlim(0, .1)
    plt.hist(p_B_samples, histtype="stepfilled", bins=30, alpha=0.85, 
            label="posterior of $p_B$", color = "#467821", normed = True)
    plt.vlines(true_p_B, 0, 80, linestyle="--", label="true $p_B$ (unknown)")
    plt.legend(loc="upper right")
    plt.ylim(0, 80)
    
    # delta samples
    
    ax = plt.subplot(313)
    plt.hist(delta_samples, histtype='stepfilled', bins=30, alpha=0.85,
             label="posterior of delta", color="#7A68A6", normed=True)
    plt.vlines(true_p_A - true_p_B, 0, 60, linestyle="--",
               label="true delta (unknown)")
    plt.vlines(0, 0, 60, color="black", alpha=0.2)
    plt.legend(loc="upper right");
    plt.show()
    '''
    #-----------------------------------
    # plot two posteriors together
    '''
    figsize(12.5, 3)
    plt.xlim(0, .1)
    plt.hist(p_A_samples, histtype = 'stepfilled', bins = 30, alpha =0.80,
            label = "posterior of $p_A$", color="#A60628", normed = True )
    plt.hist(p_B_samples, histtype = 'stepfilled', bins = 30, alpha =0.80,
            label = "posterior of $p_B$", color="#467821", normed = True )
    plt.legend(loc = "upper right")
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.title("Posterior distributions of $p_A$ and $p_B$")
    plt.ylim(0, 80)
    plt.show()
    '''
    #-----------------------------------
    # Count the number of samples less than 0, i.e., the area under the curve
    # before 0, representing the probability that site A is worse than site B.
    print ("Probability site A is WORSE than site B: {0:.3f}".format((delta_samples < 0).mean()))
    print ("Probability site A is BETTER than site B: {0:.3f}".format((delta_samples > 0).mean()))
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
