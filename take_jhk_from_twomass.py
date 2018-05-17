#!/usr/bin/python3
'''
Abstract:
    This is a program to demo how to code deep learning code.
Usage:
    take_jhk_from_twomass.py [file name]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180517
####################################
update log
20180517 version alpha 1
    1. The code work
'''
import time
import numpy as np
import convert_lib
from dat2npy_noobs_nodet import read_well_known_data
from sys import argv

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------    
    # read the Database UKIDSSDR10PLUS as a catalog
    filename = argv[1]
    catalogs = np.array(read_well_known_data(filename), dtype = np.float64)
    for i in range(5):
        print (catalogs[i])
    # split into J, H, and Ks bands.
    print("### the test on spliter ###")
    print('### J ###')
    j = np.transpose(np.stack((catalogs[:, 0], catalogs[:, 8])))
    for i in range(5):
        print (j[i])
    print('### H ###')
    h = np.transpose(np.stack((catalogs[:, 1], catalogs[:, 9])))
    for i in range(5):
        print (h[i])
    print('### K ###')
    k = np.transpose(np.stack((catalogs[:, 2], catalogs[:, 10])))
    for i in range(5):
        print (k[i])
    # save each band respectively
    np.save("twomass_j.npy", j)
    np.savetxt("twomass_j.txt", j)
    np.save("twomass_h.npy", h)
    np.savetxt("twomass_h.txt", h)
    np.save("twomass_k.npy", k)
    np.savetxt("twomass_k.txt", k)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
