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
    1. The code works
20180910 version alpha 2
    1. replace name 'no' with 'mask'.
    2. Add new options: mask JHK4, and mask 4.
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
    options = ['maskJHK', 'maskH', 'maskH78', 'mask78', 'maskJHK4', 'mask4']
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("Wrong numbers of arguments")
        print ("Usage: mask_bands.py [mod] [data]")
        print ("Available mod: {0}".format(", ".join('%s'%x for x in options)))
        exit(0)
    mod = argv[1]
    data_name = argv[2]
    #-----------------------------------
    # Load data
    data = np.loadtxt(data_name, dtype = np.float64)
    # Choose mask with bands set
    if mod == 'maskJHK':
        from dat2npy_lib import normalize_0_r_noJHK as normalize
    if mod == 'maskH':
        from dat2npy_lib import normalize_0_r_noH as normalize
    if mod == 'maskH78':
        from dat2npy_lib import normalize_0_r_noH78 as normalize
    if mod == 'mask78':
        from dat2npy_lib import normalize_0_r_no78 as normalize
    if mod == 'maskJHK4':
        from dat2npy_lib import normalize_0_r_noJHK4 as normalize
    if mod == 'mask4':
        from dat2npy_lib import normalize_0_r_no4 as normalize
    # mask dataset with chosen mask, then normalize to the maximun flux equals 1.
    masked_data = normalize(data)
    # Save masked data set
    np.savetxt(data_name, masked_data)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
