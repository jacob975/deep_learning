#!/usr/bin/python3
'''
Abstract:
    This is a program for plotting the histogram of certain band on SED. 
Usage:
    plot_sed_hist.py [index band] [sed table]
Output:
    1. The image of given-band histogram
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20191016
####################################
update log
20191016 version alpha 1:
    1. The code works.
'''
import time
import numpy as np
from sys import argv
from matplotlib import pyplot as plt

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_sed_hist.py [index band ] [sed table]")
        print ("The [index band] should range from 0 to 7")
        exit()
    ind_band = int(argv[1])
    sed_table_name = argv[2]
    #-----------------------------------
    # Load data
    print ("Loading data...")
    sed_table = np.loadtxt(sed_table_name)
    # Plot the result
    print ("Plotting the histogram")
    n, bins, patches = plt.hist(np.log10(sed_table[:,ind_band]), 50)
    plt.xlim(-2, 4)
    plt.yscale('log')
    plt.grid()
    plt.show()
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
