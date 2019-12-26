#!/usr/bin/python3
'''
Abstract:
    This is a program for calculating the averaged SNR for a list of sources. 
Usage:
    calculate_avg_SNR.py [sed table] 
Output:
    1. Print out the SNR with std of it.    
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20191202
####################################
update log
20191202 version alpha 1
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
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: calculate_avg_SNR.py [sed_table]")
        exit()
    sed_table_name = argv[1]
    #-----------------------------------
    # Load data
    sed_table = np.loadtxt(sed_table_name)
    print ("table name: {0}".format(sed_table_name))
    # Calculate the signal noise ratio
    for i in range(8):
        flux = sed_table[:,i]
        error = sed_table[:,i+8]
        SNR_array = np.divide(flux, error)
        SNR_mean = np.mean(SNR_array)
        print ('Average SNR = {0}'.format(SNR_mean))
        n, bins, patches = plt.hist(SNR_array, 50, facecolor='g', alpha=0.75)
        # Show the histogram
        plt.savefig("{0}_band{1}.png".format(sed_table_name[:-4], i))
        plt.close()
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
