#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH4.
Usage:
    20180601_CH4_census_return_rate_challenge.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170601
####################################
update log
20180601 version alpha 1:
    1. The code works

'''
import numpy as np
from IPython.core.pylabtools import figsize
import matplotlib.pyplot as plt

figsize(12.5, 6.5)
import pymc as pm

# load data
data = np.genfromtxt("/home/Jacob975/bin/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/Chapter4_TheGreatestTheoremNeverTold/data/census_data.csv", skip_header = 1, delimiter = ",")
# plot the all data point
plt.scatter(data[:,1], data[:,0], alpha = 0.5, c="#7A68A6")
# plot basic infos
plt.title("Census mail-back rate versus population")
plt.ylabel("Mail-back rate")
plt.xlabel("Population of block group")
plt.xlim(-100, 15e3)
plt.ylim(-5, 105)

i_min = np.argmin(data[:,0])
i_max = np.argmax(data[:,0])

# plot the extreme data point
plt.scatter([data[i_min, 1], data[i_max, 1]], 
            [data[i_min, 0], data[i_max, 0]],
            s=60, marker = "o", facecolors = "none", 
            edgecolors="#A60628", linewidth=1.5, 
            label="most extreme points")
plt.legend(scatterpoints = 1)
plt.show()
