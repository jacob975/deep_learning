#!/usr/bin/python3
'''
Abstract:
    This is a program to demo how to code deep learning code.
Usage:
    mJy2mag.py [source table]

    source table should be like:
    [[S1, S2, S3, ...S8, N1, N2, N3, ... N8],
     [S1, S2, S3, ...                      ], 
     ...
    ]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181026
####################################
update log
20181026 version alpha 1:
    1. The code works.
'''
import time
from sys import argv
import numpy as np

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load arguments
    if len(argv) != 2:
        print ("The number of arugments is wrong.")
        print ("Usage: mJy2mag.py [source table]")
        exit()
    source_table_name
    # Load sources
    source_table = np.loadtxt(source_table_name)
    flux_table = source_table[:8]
    error_table = source_table[8:]
    mag_table = np.zeros(flux_table.shape)
    err_mag_table = np.zeros(flux_table.shape)
    zeropoints = None       # TBA
    # mJy to Magnitude
    for i in range(len(flux_table):
        mag_table[i], err_mag_table[i]  = mJy2mag(zeropoint, flux_table[i], error_table[i]) 
    # Mask the data we don't want 
    mask = np.where((mag_table == 0) & (err_mag_table == 0))    # TBA
    mag_table[mask] = 0
    # Save the result and mask

    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
