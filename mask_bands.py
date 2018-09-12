#!/usr/bin/python3
'''
Abstract:
    This is a program to mask data in some bands with 0. 
Usage:
    mask_bands.py [mask code] [data]
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
    3. Add new options: mask JHK45, and mask 5.
20180912 version alpha 3
    1. Update the mask system, using mask code instead of keywords.
'''
from sys import argv
from dat2npy_lib import mask_and_normalize
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
        print ("Usage: mask_bands.py [mask code] [data]")
        print ("Mask code should be 8 digit decimal number.")
        print ("Example: 00000000 represent no masked; 11111111 represent all masked")
        exit(0)
    mask_code = argv[1]
    data_name = argv[2]
    #-----------------------------------
    # Load data
    data = np.loadtxt(data_name, dtype = np.float64)
    # mask dataset with chosen mask, then normalize to the maximun flux equals 1.
    masked_data = mask_and_normalize(data, mask_code)
    # Save masked data set
    np.savetxt(data_name, masked_data)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
