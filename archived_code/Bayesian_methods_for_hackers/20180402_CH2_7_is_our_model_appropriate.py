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

def separation_plot( p, y, **kwargs ):
    """
    This function creates a separation plot for logistic and probit classification. 
    See http://mdwardlab.com/sites/default/files/GreenhillWardSacks.pdf
    
    p: The proportions/probabilities, can be a nxM matrix which represents M models.
    y: the 0-1 response variables.
    
    """
    assert p.shape[0] == y.shape[0], "p.shape[0] != y.shape[0]"
    n = p.shape[0]

    try:
        M = p.shape[1]
    except:
        p = p.reshape( n, 1 )
        M = p.shape[1]

    colors_bmh = np.array( ["#eeeeee", "#348ABD"] )


    fig = plt.figure( )

    for i in range(M):
        ax = fig.add_subplot(M, 1, i+1)
        ix = np.argsort( p[:,i] )
        #plot the different bars
        bars = ax.bar( np.arange(n), np.ones(n), width=1.,
                color = colors_bmh[ y[ix].astype(int) ],
                edgecolor = 'none')
        ax.plot( np.arange(n+1), np.append(p[ix,i], p[ix,i][-1]), "k",
                 linewidth = 1.,drawstyle="steps-post" )
        #create expected value bar.
        ax.vlines( [(1-p[ix,i]).sum()], [0], [1] )
        plt.xlim( 0, n)

    plt.tight_layout()

    return


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
    # generate simulation data
    observed = pm.Bernoulli("bernoulli_obs", p, value = D, observed = True)
    simulated_data = pm.Bernoulli("simulation_data", p)
    simulated = pm.Bernoulli("bernoulli_sim", p)
    N = 10000
    mcmc = pm.MCMC([simulated, alpha, beta, observed])
    mcmc.sample(N)
    #-----------------------------------
    # plot the result
    simulations = mcmc.trace("bernoulli_sim")[:].astype(int)
    if VERBOSE>0:
        figsize(12.5, 5)
        print ("Shape of simulations array: ", simulations.shape)
        plt.title("Simulated datasets using posterior parameters")
        for i in range(4):
            ax = plt.subplot(4, 1, i+1)
            plt.scatter(temperature, simulations[1000*i, :], color = 'k', s=50, alpha = 0.6)
        plt.show()
    #-----------------------------------
    # Separation plot
    posterior_probability = simulations.mean(axis = 0)
    if VERBOSE>0:
        print ("Obs. | Array of Simulated Defects\
                    | Posterior Probability of Defect | Realized Defect ")
        for i in range(len(D)):
            print ("%s   | %s    |   %.2f                |   %d" %\
                    (str(i).zfill(2), str(simulations[:10, i])[:-1] + "...]".ljust(12), posterior_probability[i], D[i]))
    #-----------------------------------
    # sort the separation plot
    ix = np.argsort(posterior_probability)
    if VERBOSE>0:
        print ("Posterior Probability of Defect | Realized Defect")
        for i in range(len(D)):
            print ("%.2f                           |   %d " % (posterior_probability[ix[i]], D[ix[i]]))
    #-----------------------------------
    # compare different model with separation plot
    figsize(11, 1.25)
    separation_plot(posterior_probability, D)
    plt.title("Our Bayesian temperature-dependent model")

    # perfect model
    # (the probability of defect is equal to if a defect occurred or not)
    p = D
    separation_plot(p, D)
    plt.title("Perfect model")
    
    # random predictions
    p = np.random.rand(23)
    separation_plot(p, D)
    plt.title("Random model")

    # constant model
    constant_prob = 7./23*np.ones(23)
    separation_plot(constant_prob, D)
    plt.title("Constant-prediction model")
    plt.show()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
