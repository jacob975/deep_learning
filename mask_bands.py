#!/usr/bin/python3
'''
Abstract:
    This is a program to mask data in some bands with 0. 
Usage:
    mask_bands.py [mod] [data]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180724
####################################
update log
20180724 version alpha 1
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
        print ("Usage: mask_bands.py [mod] [data]")
        print ("Available mod: noJHK, noH, noH78.")
        exit(0)
    mod = argv[1]
    data_name = argv[2]
    #-----------------------------------
    # Load data
    data = np.loadtxt(data_name, dtype = np.float64)
    # Choose mask with bands set
    if mod == 'noJHK':
        from dat2npy_lib import normalize_0_r_noJHK as normalize
    if mod == 'noH':
        from dat2npy_lib import normalize_0_r_noH as normalize
    if mod == 'noH78':
        from dat2npy_lib import normalize_0_r_noH78 as normalize
    # mask dataset with chosen mask, then normalize to the maximun flux equals 1.
    masked_data = normalize(data)
    # Save masked data set
    np.savetxt(data_name, masked_data)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
