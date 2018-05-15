#!/usr/bin/python3
'''
Abstract:
    This is a program to demo how to code deep learning code.
Usage:
    std_code.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180514
####################################
update log
20180514 version alpha 1
    1. The code work
'''
import time
import numpy as np
import convert_lib
from sys import argv

def readfile(filename):
    try:
        f = open(filename, 'r')
    except:
        return []
    data = []
    for line in f.readlines():
        # skip if no data or it's a hint.
        if line == "\n" or line.startswith('#'):
            continue
        datum = np.array(line[:-1].split(','), dtype = np.float64)
        data.append(datum)
    f.close
    return np.array(data)

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------    
    # read a csv file into a catalog
    filename = argv[1]
    catalogs = readfile(filename)
    for i in range(5):
        print (catalogs[i])
    # split into J, H, and Ks bands.
    print("### the test on spliter ###")
    J_bands = catalogs[:,10:12]
    print('### J ###')
    for i in range(5):
        print (J_bands[i])
    H_bands = catalogs[:,12:14]
    print('### H ###')
    for i in range(5):
        print (H_bands[i])
    K_bands = catalogs[:,14:16]
    print('### K ###')
    for i in range(5):
        print (K_bands[i])
    #-----------------------------------
    # convert mag to mJy
    ukirt_system = convert_lib.set_ukirt()
    J_bands_mJy, error_J_bands_mJy = convert_lib.mag_to_mJy(ukirt_system['J'][2], J_bands[:,0:1], J_bands[:,1:2])
    for i in range(10):
        print ("{0}, {1}".format(J_bands_mJy[i], error_J_bands_mJy[i]))
    
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
