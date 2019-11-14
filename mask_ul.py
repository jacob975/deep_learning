#!/usr/bin/python3
'''
Abstract:
    This is a program to mask data which are upper limit.
Usage:
    mask_ul.py [Q flag table] [data]
    
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

# Take the error of the 1% last bright star.
def proper_error(error_list):
    # Sort the list
    error_array = np.sort(error_list)
    index = int(len(error_array) * 0.01)
    error = np.median(error_array[:index])
    return error

# Take the flux of the last bright star.
def proper_flux(flux_list):
    flux_array = np.sort(flux_list)
    flux = flux_array[0] * 0.01
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
        print ("Usage: mask_ul.py [Q flag table] [data]")
        exit(0)
    ul_table_name = argv[1]
    data_name = argv[2]
    bands = ['J', 'H', 'K', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
    #-----------------------------------
    # Load data
    ul_table = np.loadtxt(ul_table_name, dtype = str)
    data = np.loadtxt(data_name, dtype = np.float64)
    prev_data = data
    # With or without error
    no_error = False
    with_error = False
    if len(data[0,:]) == 8:
        no_error = True
    elif len(data[0,:]) == 16:
        with_error = True
    #------------------------------------------
    # Mask dataset with chosen mask
    for i in range(len(ul_table[0])):
        '''
        if i == 1:
            continue
        '''
        # Initialize
        pflux = 0.0
        perror = 0.0
        # Get the mask
        mask = ul_table[:,i] == 'U'
        index_valid_flux = (ul_table[:,i] != 'U') & (ul_table[:,i] != 'R') & (data[:,i] != 0.0)
        # Find a proper value for upperlimit detections.
        pflux = proper_flux(data[index_valid_flux, i])
        # Mask all upper limit detection
        data[mask,i] = pflux 
        # Fill up all no-observation data
        data[data[:,i] == 0.0, i] = pflux
        # Repeat again with error 
        if with_error:
            index_valid_error = (ul_table[:,i] != 'U') & (data[:,i+8] != 0.0)
            perror = proper_error(data[index_valid_error, i+8])
            # Fill up all no-observation data
            data[data[:,i+8] == 0.0, i+8] = perror
        print (bands[i], pflux, perror)
    # Save masked data set
    np.savetxt(data_name, data)
    np.savetxt("{0}_backup.txt".format(data_name[:-4]), prev_data)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
