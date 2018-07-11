#!/usr/bin/python3
'''
Abstract:
    This is a program to take band JHK form ukidss catalog
Usage:
    take_jhk_from_ukidss_GPS.py [ukidss catalog file] [label]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180612
####################################
update log
20180612 version alpha 1
    1. The code works
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
    print("zeropoint: {0}".format(ukirt_system[band][2]))
    # convert
    for i in range(len(bands_j)):
        '''
        # if the distance is larger than 1 beam size of irac...
        elif distances[i] > 1.2:
            mjy = err_mjy = 0.0
        '''
        # if JHK is not found...
        if distances[i] == 0.0:
            mjy = err_mjy = 0.0
        elif distances[i] > 0.6:
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
    # check argv
    if len(argv) != 3:
        print("Error\nUsage: take_jhk_from_ukidss_GPS.py [ukidss catalog file] [label]")
        exit()
    # read the Database UKIDSSDR10PLUS as a catalog
    filename = argv[1]
    label = argv[2]
    catalogs = readfile(filename)
    # split into J, H, and Ks bands.
    print("### the test on spliter ###")
    print('### J ###')
    bands_j = catalogs[:,10:12]
    for i in range(5):
        print (bands_j[i])
    print('### H ###')
    bands_h1 = catalogs[:,12:14]
    for i in range(5):
        print (bands_h1[i])
    print('### K1 ###')
    bands_k1 = catalogs[:,14:16]
    for i in range(5):
        print (bands_k1[i])
    # read id, distance, and coordinate
    global ids
    ids = catalogs[:,0]
    global distances
    distances = catalogs[:,3]
    coords_uploaded = catalogs[:, 1:3]
    coords_detected = catalogs[:, 6:8]
    coords = np.hstack((coords_uploaded, coords_detected))
    print (coords)
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
    print('### H1 ###')
    h1_mjy = []
    err_h1_mjy = []
    h1_mjy, err_h1_mjy =  mag_to_mjy(bands_h1, 'H')
    # print and check
    for i in range(11,20):
        print ("{0}: {1}, {2}".format(ids[i], h1_mjy[i], err_h1_mjy[i]))
    print('### K1 ###')
    k1_mjy = []
    err_k1_mjy = []
    k1_mjy, err_k1_mjy =  mag_to_mjy(bands_k1, 'K')
    # print and check
    for i in range(11,20):
        print ("{0}: {1}, {2}".format(ids[i], k1_mjy[i], err_k1_mjy[i]))
    #-----------------------------------
    # save each band and coord respectively
    j = np.stack((j_mjy, err_j_mjy))
    j = np.transpose(j)
    np.save("ukidss_j_{0}.npy".format(label), j)
    np.savetxt("ukidss_j_{0}.txt".format(label), j)
    h1 = np.stack((h1_mjy, err_h1_mjy))
    h1 = np.transpose(h1)
    np.save("ukidss_h1_{0}.npy".format(label), h1)
    np.savetxt("ukidss_h1_{0}.txt".format(label), h1)
    k1 = np.stack((k1_mjy, err_k1_mjy))
    k1 = np.transpose(k1)
    np.save("ukidss_k1_{0}.npy".format(label), k1)
    np.savetxt("ukidss_k1_{0}.txt".format(label), k1)
    np.save("ukidss_coords_{0}.npy".format(label), coords)
    np.savetxt("ukidss_coords_{0}.txt".format(label), coords)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
