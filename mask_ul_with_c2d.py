#!/usr/bin/python3
'''
Abstract:
    This is a program to mask data which are upper limit.
Usage:
    mask_ul_with_c2d.py [Q flag table] [data]
    
    Input should looks like:
    Q flag table = 
    [[ A, A, A, A, A, A, A, U],
     [ A, B, A, A, A, A, A, U],
     ...]

Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181128
####################################
update log
20181128 version alpha 1:
    1. The code works
'''
from sys import argv
import time
import numpy as np

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("Wrong numbers of arguments")
        print ("Usage: mask_ul_with_c2d.py [Q flag table] [data]")
        exit(0)
    ul_table_name = argv[1]
    data_name = argv[2]
    bands = ['J', 'H', 'K', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
    #-----------------------------------
    # Load data
    ul_table = np.loadtxt(ul_table_name, dtype = str)
    data = np.loadtxt(data_name, dtype = np.float64)
    min_flux_array = [1.36e-3, 1.87e-3, 1.76e-3, 2.85e-4, 2.50e-4, 1.30e-5, 2.16e-4, 8.98e-4]
    #------------------------------------------
    # Mask dataset with chosen mask
    for i in range(len(ul_table[0])):
        # Initialize
        pflux = 0.0
        perror = 0.0
        # Get the mask of 
        #       1. all the U label detections, 
        #       2. all the 0 detections
        mask = ul_table[:,i] == 'U'
        index_valid_flux = (ul_table[:,i] != 'U') & (ul_table[:,i] != 'R') & (data[:,i] != 0.0)
        # Find a proper value for upperlimit detections.
        pflux = min_flux_array[i]
        # Mask all upper limit detection
        data[mask,i] = pflux
        # Fill up all no-observation data
        data[data[:,i] == 0.0, i] = pflux
        print (bands[i], pflux)
    # Save masked data set
    np.savetxt(data_name, data)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
