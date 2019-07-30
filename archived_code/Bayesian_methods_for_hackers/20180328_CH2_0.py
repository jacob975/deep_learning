#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH2.
Usage:
    20180328_CH2_0.py
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

def plot_artificail_sms_dataset():
    #----------------------------------
    # initialize both deterministic and stochastic variables
    tau = pm.rdiscrete_uniform(0, 80)
    print ("tau = {0}".format(tau))
    alpha = 1./20.
    lambda_1, lambda_2 = pm.rexponential(alpha, 2)
    print ("lambda_1 = {0}\nlambda_2 = {1}".format(lambda_1, lambda_2))
    lambda_ = np.r_[lambda_1*np.ones(tau), lambda_2*np.ones(80-tau)]
    print ("lambda = \n{0}".format(lambda_))
    data = pm.rpoisson(lambda_)
    print ("data = \n{0}".format(data))
    #-----------------------------------
    # plot the artificial
    plt.bar(np.arange(80), data, color = "#348ABD")
    plt.bar(tau-1, data[tau-1], color = "r", label = "user behavior changed")
    plt.xlabel("Time(days)")
    plt.ylabel("Text messages received")
    plt.xlim(0, 80)
    

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------
    # let create several artifitial data
    figsize(12.5, 5)
    plt.title("more example of artificail datasets from simulating our model")
    for i in range(4):
        plt.subplot(4, 1, i+1)
        plot_artificail_sms_dataset()
    plt.show()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
