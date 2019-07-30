#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH2.
Usage:
    20180329_CH2_6_challenger_space_shuttle_disaster.py
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

def logistic(x, beta, alpha = 0):
    return 1.0/ (1.0 + np.exp(beta * x + alpha))

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------
    # load data
    challenger_data = np.genfromtxt("/home/Jacob975/bin/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/Chapter2_MorePyMC/data/challenger_data.csv",
                                    skip_header = 1, 
                                    usecols = [1, 2],
                                    missing_values= "NA",
                                    delimiter = ",")
    challenger_data = challenger_data[~np.isnan(challenger_data[:, 1])]
    if VERBOSE>0:
        # test
        figsize(12.5, 3.5)
        print ("Temp(F), O-ring failure")
        print (challenger_data)
        # plot
        plt.scatter(challenger_data[:, 0], challenger_data[:, 1], s = 75, color="k", alpha=0.5)
        plt.yticks([0, 1])
        plt.ylabel("Damage incident?")
        plt.xlabel("Outside temperature (Fahrenheit)")
        plt.title("Defects of the space shuttle O-ring versus temperature")
        plt.show()
    #-----------------------------------
    # initialize variables and constants
    temperature = challenger_data[:, 0]
    D = challenger_data[:, 1]
    # Notice the "value" here. We will explain it later.
    beta = pm.Normal("beta", 0, 0.001, value = 0)
    alpha = pm.Normal("alpha", 0, 0.001, value = 0)
    @pm.deterministic
    def p(t=temperature, alpha = alpha, beta = beta):
        return 1.0/ (1. + np.exp(beta*t + alpha))
    #-----------------------------------
    # Connect the probabilities in "p" with our observations through a
    # Bernoulli random variable.
    observed = pm.Bernoulli("bernoulli_obs", p, value = D, observed = True)
    model = pm.Model([observed, beta, alpha])
    # mysterious code to be explained in Chapter 3
    map_ = pm.MAP(model)
    map_.fit()
    mcmc = pm.MCMC(model)
    mcmc.sample(120000, 100000, 2)
    #-----------------------------------
    # show answers
    alpha_samples = mcmc.trace("alpha")[:, None]    # best to make them 1D
    beta_samples = mcmc.trace("beta")[:, None]
    if VERBOSE>0:
        # histogram of the samples
        figsize(12.5, 6)
        plt.subplot(211)
        plt.title(r"Posterior distributions of the model parameters $\alpha, \beta$")
        plt.hist(beta_samples, histtype='stepfilled', bins=35, alpha =0.85, label = r"posterior of $\beta$", color="#7A68A6", normed=True)
        plt.legend()
        
        plt.subplot(212)
        plt.hist(alpha_samples, histtype="stepfilled", bins=35, alpha=0.85, label = r"posterior of $\alpha$", color="#A60628", normed=True)
        plt.xlabel("Value of parameter")
        plt.ylabel("Density")
        plt.legend()

        plt.show()
    figsize(12.5, 6)
    plt.plot(alpha_samples, beta_samples, "ro", alpha = 0.3, label = "beta versus alpha")
    plt.legend()
    plt.show()

    #-----------------------------------
    # show the expected probability
    t = np.linspace(temperature.min() -5, temperature.max()+5, 50)[:, None]
    p_t = logistic(t.T, beta_samples, alpha_samples)

    mean_prob_t = p_t.mean(axis = 0)

    if VERBOSE>0:
        figsize(12.5, 4)
        plt.plot(t, mean_prob_t, lw=3, label="average posterior \nprobability of defect")
        plt.plot(t, p_t[0, :], ls="--", label="realization from posterior")
        plt.plot(t, p_t[-2, :], ls="--", label="realization from posterior")
        plt.scatter(temperature, D, color="k", s=50, alpha=0.5)
        plt.title("Posterior expected value of the probability of defect, \
                including two realizations")
        plt.legend(loc="lower left")
        plt.ylim(-0.1, 1.1)
        plt.xlim(t.min(), t.max())
        plt.ylabel("Probability")
        plt.xlabel("Temperature")
        
        plt.show()

    #-----------------------------------
    # show what temperatures are we most uncertain about the defect probability
    from scipy.stats.mstats import mquantiles
    if VERBOSE>0:
        # vectorized bottom and top 2.5% quantiles for "credible interval"
        qs = mquantiles(p_t, [0.025, 0.975], axis=0)
        plt.fill_between(t[:, 0], *qs, alpha = 0.7, color = "#7A68A6")
        plt.plot(t[:, 0], qs[0], label = "95% CI", color="#7A68A6", alpha = 0.7)
        plt.plot(t, mean_prob_t, lw = 1, ls="--", color="k", label="average posterior \nprobability of defect")
        plt.xlim(t.min(), t.max())
        plt.ylim(-0.02, 1.02)
        plt.legend(loc="lower left")
        plt.scatter(temperature, D, color="k", s=50, alpha=0.5)
        plt.xlabel("Temperature, $t$")
        plt.ylabel("Probability estimate")
        plt.title("Posterior probability of estimates, given temperature $t$")
        plt.show()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
