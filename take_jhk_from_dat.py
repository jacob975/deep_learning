#!/usr/bin/python3
'''
Abstract:
    This is a program to take J, H, Ks bands from dat files.
Usage:
    take_jhk_from_dat.py [file name]
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
    # check argv
    if len(argv) != 2:
        print("Error\nUsage: take_jhk_from_dat.py [file name]")
        exit()
    # read the dat file as catalog
    name_dat_file = argv[1]
    catalogs = np.array(read_well_known_data(name_dat_file), dtype = np.float64)
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
    np.save("{0}_j.npy".format(name_dat_file[:-4]), j)
    np.savetxt("{0}_j.txt".format(name_dat_file[:-4]), j)
    np.save("{0}_h.npy".format(name_dat_file[:-4]), h)
    np.savetxt("{0}_h.txt".format(name_dat_file[:-4]), h)
    np.save("{0}_k.npy".format(name_dat_file[:-4]), k)
    np.savetxt("{0}_k.txt".format(name_dat_file[:-4]), k)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
