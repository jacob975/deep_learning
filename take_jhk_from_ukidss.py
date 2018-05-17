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

# this function is used to convert magnitude to mini Janskey
# take j band as example
def mag_to_mjy(bands_j, band):
    # initialize variables
    j_mjy = []
    err_j_mjy = []
    # convert
    for i in range(len(bands_j)):
        # if JHK is not found...
        if distances[i] == 0.0:
            mjy = err_mjy = 0.0
        # if the distance is larger than 1 beam size of irac...
        elif distances[i] > 1.2:
            mjy = err_mjy = 0.0
        else:
            mjy, err_mjy = convert_lib.mag_to_mJy(ukirt_system[band][2], bands_j[i,0], bands_j[i,1])
        j_mjy.append(mjy)
        err_j_mjy.append(err_mjy)
    return np.array(j_mjy), np.array(err_j_mjy)

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------    
    # read the Database UKIDSSDR10PLUS as a catalog
    filename = argv[1]
    catalogs = readfile(filename)
    # split into J, H, and Ks bands.
    print("### the test on spliter ###")
    print('### J ###')
    bands_j = catalogs[:,10:12]
    for i in range(5):
        print (bands_j[i])
    print('### H ###')
    bands_h = catalogs[:,12:14]
    for i in range(5):
        print (bands_h[i])
    print('### K ###')
    bands_k = catalogs[:,14:16]
    for i in range(5):
        print (bands_k[i])
    # read distance
    global ids
    ids = catalogs[:,0]
    global distances
    distances = catalogs[:,3]
    #-----------------------------------
    # convert mag to mJy
    global ukirt_system
    ukirt_system = convert_lib.set_ukirt()
    print("### converting from magnitude to mJy ###")
    print('### J ###')
    j_mjy = []
    err_j_mjy = []
    j_mjy, err_j_mjy =  mag_to_mjy(bands_j, 'J')
    # print and check
    for i in range(11,20):
        print ("{0}: {1}, {2}".format(ids[i], j_mjy[i], err_j_mjy[i]))
    print('### H ###')
    h_mjy = []
    err_h_mjy = []
    h_mjy, err_h_mjy =  mag_to_mjy(bands_h, 'H')
    # print and check
    for i in range(11,20):
        print ("{0}: {1}, {2}".format(ids[i], h_mjy[i], err_h_mjy[i]))
    print('### K ###')
    k_mjy = []
    err_k_mjy = []
    k_mjy, err_k_mjy =  mag_to_mjy(bands_k, 'K')
    # print and check
    for i in range(11,20):
        print ("{0}: {1}, {2}".format(ids[i], k_mjy[i], err_k_mjy[i]))
    # save each band respectively
    j = np.stack((j_mjy, err_j_mjy))
    j = np.transpose(j)
    print (j)
    np.save("ukidss_j.npy", j)
    np.savetxt("ukidss_j.txt", j)
    h = np.stack((h_mjy, err_h_mjy))
    h = np.transpose(h)
    np.save("ukidss_h.npy", h)
    np.savetxt("ukidss_h.txt", h)
    k = np.stack((k_mjy, err_k_mjy))
    k = np.transpose(k)
    np.save("ukidss_k.npy", k)
    np.savetxt("ukidss_k.txt", k)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
