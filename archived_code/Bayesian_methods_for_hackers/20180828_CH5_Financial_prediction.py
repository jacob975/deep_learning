#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH5.
Usage:
    20180828_CH5_financial_prediction.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170828
####################################
update log
20180828 version alpha 1:
    1. The code works

'''
import numpy as np
from IPython.core.pylabtools import figsize
import matplotlib.pyplot as plt
figsize(12.5, 4)
import pymc as pm
from pymc.Matplot import plot as mcplot
import time

def stock_loss(true_return, yhat, alpha  = 100.):
    if true_return*yhat < 0:
        # opposite signs, not good
        return alpha*yhat**2 - np.sign(true_return)*yhat + abs(true_return)
    else:
        return abs(true_return - yhat)

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Initialize
    true_value = 0.05
    pred = np.linspace(-0.04, 0.12, 75)
    # plot the error
    fig_1 = plt.figure()
    plt.plot(pred, [stock_loss(true_value, _p) for _p in pred], \
        label = "loss associated with\n prediction if true value = 0.05", lw = 3)
    plt.vlines(0, 0, 0.25, linestyles = "--")
    plt.xlabel("Prediction")
    plt.ylabel("Loss")
    plt.xlim(-0.04, 0.12)
    plt.ylim(0, 0.25)

    true_value = -0.02
    plt.plot(pred, [stock_loss(true_value, _p) for _p in pred], alpha = 0.6, \
        label = "loss associated with\n prediction if true value = -0.02", lw = 3)
    plt.legend()
    plt.title("Stock returns loss if true value = 0.05, -0.02")
    fig_1.show()
    #-----------------------------------
    # Make a Bayesian linear regression on this dataset.
    # code to create artificial data
    N = 100
    X = 0.025 * np.random.randn(N)
    Y = 0.5 * X + 0.01 * np.random.randn(N)

    ls_coef_ = np.cov(X, Y)[0,1]/np.var(X)
    ls_intercept = Y.mean() - ls_coef_*X.mean()

    # plot the error
    fig_2 = plt.figure()
    plt.scatter(X, Y, c = 'k')
    plt.xlabel("Trading signal")
    plt.ylabel("Returns")
    plt.title("Empirical returns versus trading signal")
    plt.plot(X, ls_coef_ * X + ls_intercept, label = "least-squares line")
    plt.xlim(X.min(), X.max())
    plt.ylim(Y.min(), Y.max())
    plt.legend(loc = "upper left")
    fig_2.show()
    
    std = pm.Uniform("std", 0, 100, trace = False)

    @pm.deterministic
    def prec (U = std):
        return 1.0/U**2
    beta = pm.Normal("beta", 0, 0.001)
    alpha = pm.Normal("alpha", 0, 0.001)
    
    @pm.deterministic
    def mean(X=X, alpha = alpha, beta = beta):
        return alpha + beta * X
    obs = pm.Normal("obs", mean, prec, value = Y, observed = True)
    mcmc = pm.MCMC([obs, beta, alpha, std, prec])
    mcmc.sample(100000, 80000)
    # show the result
    figsize(12.5, 6)
    from scipy.optimize import fmin
    
    def stock_loss (price, pred, coef = 500):
        sol = np.zeros_like(price)
        ix = price*pred < 0
        sol[ix] = coef * pred**2 - np.sign(price[ix]) * pred + abs(price[ix])
        sol[~ix] = abs(price[~ix] - pred)
        return sol

    tau_samples = mcmc.trace("prec")[:]
    alpha_samples = mcmc.trace("alpha")[:]
    beta_samples = mcmc.trace("beta")[:]
    N = tau_samples.shape[0]
    noise = 1.0 / np.sqrt(tau_samples) * np.random.randn(N)
    possible_outcomes = lambda signal: alpha_samples + beta_samples * signal \
    + noise
    opt_predictions = np.zeros(50)
    trading_signals = np.linspace(X.min(), X.max(), 50)
    for i, _signal in enumerate(trading_signals):
        _possible_outcomes = possible_outcomes(_signal)
        tomin = lambda pred: stock_loss(_possible_outcomes, pred).mean()
        opt_predictions[i] = fmin(tomin, 0, disp = False)

    # plot the error
    fig_3 = plt.figure()
    plt.xlabel("Trading signal")
    plt.ylabel("Prediction")
    plt.title("Least-squares prediction versus Bayes action prdiction")
    plt.plot(X, ls_coef_ * X + ls_intercept, label = "least-squares prediction")
    plt.xlim(X.min(), X.max())
    plt.plot(trading_signals, opt_predictions, label = "Bayes action prediction")
    plt.legend(loc = "upper left")
    fig_3.show()
    input()
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
