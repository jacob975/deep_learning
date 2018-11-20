#!/usr/bin/python3
'''
Abstract:
    This is a program to demo how to code deep learning code.
Usage:
    statistic_the_quality.py [quality flag file]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181119
####################################
update log
20181119
'''
import numpy as np
import time
from sys import argv
from collections import Counter

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: statistic_the_quality.py [quality flag file]")
        exit()
    name_quality = argv[1]
    #-----------------------------------
    # Load data
    qualities = np.loadtxt(name_quality, dtype = str)
    # Print the result
    for i in range(8):
        cnt = Counter(qualities[:,i])
        print (cnt) 
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
