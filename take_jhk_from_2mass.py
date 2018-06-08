#!/usr/bin/python3
'''
Abstract:
    This is a program to take band JHK form 2mass catalog
Usage:
    take_jhk_from_2mass.py [2mass catalog file] [label]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180608
####################################
update log
20180608 version alpha 1
    1. The code works
'''
import time
import numpy as np
import convert_lib
from sys import argv

# this function is used to convert magnitude to mini Janskey
# take j band as example
def mag_to_mjy(bands_j, band):
    # initialize variables
    j_mjy = []
    err_j_mjy = []
    print("zeropoint: {0}".format(twomass_system[band][2]))
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
            mjy, err_mjy = convert_lib.mag_to_mJy(twomass_system[band][2], bands_j[i,0], bands_j[i,1])
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
        print("Error\nUsage: take_jhk_from_2mass.py [2mass catalog file] [label]")
        exit()
    # read the Database UKIDSSDR10PLUS as a catalog
    filename = argv[1]
    label = argv[2]
    catalogs = np.loadtxt(filename, skiprows = 79, dtype = np.str)
    for i in range(5):
        print(catalogs[i])
    
    # split into J, H, and Ks bands.
    print("### the test on spliter ###")
    print('### J ###')
    bands_j = catalogs[:,11:13]
    bands_j[bands_j == 'null'] = '0.0'
    bands_j = np.array(bands_j, dtype = np.float64)
    for i in range(5):
        print (bands_j[i])
    print('### H ###')
    bands_h = catalogs[:,15:17]
    bands_h[bands_h == 'null'] = '0.0'
    bands_h = np.array(bands_h, dtype = np.float64)
    for i in range(5):
        print (bands_h[i])
    print('### K ###')
    bands_k = catalogs[:,19:21]
    bands_k[bands_k == 'null'] = '0.0'
    bands_k = np.array(bands_k, dtype = np.float64)
    for i in range(5):
        print (bands_k[i])
    
    # read id, distance, and coordinate
    global ids
    ids = np.array(catalogs[:,0], dtype = int)
    global distances
    distances = catalogs[:,1]
    distances[distances == 'null'] = '999.0'
    distances = np.array(distances, dtype = np.float64)
    coords_uploaded = np.array(catalogs[:, 3:5], dtype = np.float64)
    coords_detected = catalogs[:,5:7]
    coords_detected[ coords_detected == 'null'] = '0.0'
    coords_detected = np.array(coords_detected, dtype = np.float64)
    coords = np.hstack((coords_uploaded, coords_detected))
    for i in range(5):
        print(coords[i], distances[i])
    #-----------------------------------
    # convert mag to mJy
    global twomass_system
    twomass_system = convert_lib.set_twomass()
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
    k_mjy, err_k_mjy =  mag_to_mjy(bands_k, 'Ks')
    # print and check
    for i in range(11,20):
        print ("{0}: {1}, {2}".format(ids[i], k_mjy[i], err_k_mjy[i]))
    #-----------------------------------
    # save each band and coord respectively
    j = np.stack((j_mjy, err_j_mjy))
    j = np.transpose(j)
    np.save("twomass_j_{0}.npy".format(label), j)
    np.savetxt("twomass_j_{0}.txt".format(label), j)
    h = np.stack((h_mjy, err_h_mjy))
    h = np.transpose(h)
    np.save("twomass_h_{0}.npy".format(label), h)
    np.savetxt("twomass_h_{0}.txt".format(label), h)
    k = np.stack((k_mjy, err_k_mjy))
    k = np.transpose(k)
    np.save("twomass_k_{0}.npy".format(label), k)
    np.savetxt("twomass_k_{0}.txt".format(label), k)
    np.save("twomass_coords_{0}.npy".format(label), coords)
    np.savetxt("twomass_coords_{0}.txt".format(label), coords)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
