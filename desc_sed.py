#!/usr/bin/python3
'''
Abstract:
    This is a program describing the flux properties of the given sed data. 
Usage:
    desc_sed.py [Q flag table] [data]
    
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

20190715
####################################
update log
20180715 version alpha 1:
    1. The code works
'''
from sys import argv
import time
import numpy as np

# Take the median of the last 1% error. 
def proper_error(error_list):
    # Sort the list
    error_array = np.sort(error_list)
    # Take the indexes of the last 1% error.
    index = int(len(error_array) * 0.01)
    error = np.median(error_array[:index])
    return error

# Take the flux of the minimum valid flux.
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
        print ("Usage: desc_sed.py [Q flag table] [data]" )
        exit(0)
    ul_table_name = argv[1]
    data_name = argv[2]
    bands = ['J', 'H', 'K', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
    #-----------------------------------
    # Load data
    ul_table = np.loadtxt(ul_table_name, dtype = str)
    data = np.loadtxt(data_name, dtype = np.float64)
    # With or without error
    no_error = False
    with_error = False
    if len(data[0,:]) == 8:
        no_error = True
    elif len(data[0,:]) == 16:
        with_error = True
    print ('band\tmax_flux\tmin_flux\terr_min_flux')
    #------------------------------------------
    # Mask dataset with chosen mask
    for i in range(len(ul_table[0])):
        # Initialize
        pflux = 0.0
        perror = 0.0
        # Get the mask
        mask = ul_table[:,i] == 'U'
        index_valid_flux = (ul_table[:,i] != 'U') & (ul_table[:,i] != 'R') & (data[:,i] != 0.0)
        # Find a proper value for upperlimit detections.
        pflux = proper_flux(data[index_valid_flux, i])
        # Repeat again with error 
        if with_error:
            index_valid_error = (ul_table[:,i] != 'U') & (data[:,i+8] != 0.0)
            perror = proper_error(data[index_valid_error, i+8])
        # Find the max flux of that band
        max_flux = np.amax(data[index_valid_flux, i])
        print (bands[i], max_flux, pflux, perror)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
