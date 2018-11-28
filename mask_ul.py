#!/usr/bin/python3
'''
Abstract:
    This is a program to mask data which are upper limit detection.
Usage:
    mask_ul.py [upper limit table] [data]
    
    Input should looks like:
    upper limit table = 
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

# Take the error at 20% latter part.
def proper_error(error_list):
    # Sort the list
    error_array = np.sort(error_list)
    # Take the index of the 20% position.
    index = int(len(error_array) * 0.01)
    error = error_array[index]
    return error

# Take the flux at 20% latter part.
def proper_flux(flux_list):
    flux_array = np.sort(flux_list)
    # Take the index of the 20% position.
    index = int(len(flux_array) * 0.01)
    flux = flux_array[index] * 0.1
    return flux

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
        print ("Usage: mask_ul.py [upper limit table] [data]")
        exit(0)
    ul_table_name = argv[1]
    data_name = argv[2]
    #-----------------------------------
    # Load data
    ul_table = np.loadtxt(ul_table_name, dtype = str)
    data = np.loadtxt(data_name, dtype = np.float64)
    #------------------------------------------
    # Mask dataset with chosen mask
    for i in range(len(ul_table[0])):
        if i < 3:
            continue
        # Get the mask
        mask = ul_table[:,i] == 'U'
        index_valid_flux = (ul_table[:,i] != 'U') & (data[:,i] != 0.0)
        index_valid_error = (ul_table[:,i] != 'U') & (data[:,i+8] != 0.0)
        # Find a proper value for upperlimit detections.
        pflux = proper_flux(data[index_valid_flux, i])
        perror = proper_error(data[index_valid_error, i+8])
        print (pflux, perror)
        # Mask all upper limit detection
        data[mask,i] = pflux 
        data[mask,i+8] = perror 
        # Fill up all no-observation data
        data[data[:,i] == 0.0, i] = pflux
        data[data[:,i+8] == 0.0, i+8] = perror
    # Save masked data set
    np.savetxt('{0}_ul_mask.txt'.format(data_name[:-4]), data)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
