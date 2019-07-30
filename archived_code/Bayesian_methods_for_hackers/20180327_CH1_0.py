#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH1.
Usage:
    20180327_CH1_0.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170104
####################################
update log
20180327 version alpha 1:
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
    # load and exhabit the data
    count_data = np.loadtxt("/home/Jacob975/bin/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/Chapter1_Introduction/data/txtdata.csv")
    n_count_data = len(count_data)
    plt.bar(np.arange(n_count_data), count_data, color="#348ABD")
    plt.xlabel("Time (days)")
    plt.ylabel("count of text-msgs received")
    plt.title("Did the user's texting habits change over time?")
    plt.xlim(0, n_count_data);
    plt.show()
    #-----------------------------------
    # modeling
    alpha = 1.0 / count_data.mean()     # Recall count_data is the
                                        # variable that holds our txt counts
    print ("alpha = {0}".format(alpha))
    lambda_1 = pm.Exponential("lambda_1", alpha)
    print ("lambda_1 = {0}".format(lambda_1.value))
    print ("lambda_1 = {0}".format(lambda_1.value))
    lambda_2 = pm.Exponential("lambda_2", alpha)
    print ("lambda_2 = {0}".format(lambda_2.value))
    tau = pm.DiscreteUniform("tau", lower=0, upper=n_count_data)
    print ("tau = {0}".format(tau.value))
    # test random
    print ("Random output:", tau.random(), tau.random(), tau.random())
    #---------------------------------------------------------------
    # def function
    @pm.deterministic
    def lambda_(tau=tau, lambda_1=lambda_1, lambda_2=lambda_2):
        out = np.zeros(n_count_data)
        out[:tau] = lambda_1  # lambda before tau is lambda1
        out[tau:] = lambda_2  # lambda after (and including) tau is lambda2
        return out
    #---------------------------------------------------------------
    observation = pm.Poisson("obs", lambda_, value=count_data, observed=True)
    model = pm.Model([observation, lambda_1, lambda_2, tau])
    # Mysterious code to be explained in Chapter 3.
    mcmc = pm.MCMC(model)
    mcmc.sample(40000, 10000, 1)
    lambda_1_samples = mcmc.trace('lambda_1')[:]
    lambda_2_samples = mcmc.trace('lambda_2')[:]
    tau_samples = mcmc.trace('tau')[:]
    # figures show
    figsize(12.5, 10)
    #----------------------------------
    # histogram of the samples: 
    ax = plt.subplot(311)
    ax.set_autoscaley_on(False)
    
    plt.hist(lambda_1_samples, histtype='stepfilled', bins=30, alpha=0.85,
             label="posterior of $\lambda_1$", color="#A60628", normed=True)
    plt.legend(loc="upper left")
    plt.title(r"""Posterior distributions of the variables $\lambda_1,\;\lambda_2,\;\tau$""")
    plt.xlim([15, 30])
    plt.xlabel("$\lambda_1$ value")
    #
    ax = plt.subplot(312)
    ax.set_autoscaley_on(False)
    plt.hist(lambda_2_samples, histtype='stepfilled', bins=30, alpha=0.85,
            label="posterior of $\lambda_2$", color="#7A68A6", normed=True)
    plt.legend(loc="upper left")
    plt.xlim([15, 30])
    plt.xlabel("$\lambda_2$ value")
    #
    plt.subplot(313)
    w = 1.0 / tau_samples.shape[0] * np.ones_like(tau_samples)
    plt.hist(tau_samples, bins=n_count_data, alpha=1,
             label=r"posterior of $\tau$",
             color="#467821", weights=w, rwidth=2.)
    plt.xticks(np.arange(n_count_data))
    plt.legend(loc="upper left")
    plt.ylim([0, .75])
    plt.xlim([35, len(count_data) - 20])
    plt.xlabel(r"$\tau$ (in days)")
    plt.ylabel("probability");
    plt.show()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
