#!/usr/bin/python3
'''
Abstract:
    This is a program to take band JHK from ukidss catalog, 
    and replace the small signals in 2MASS with signals in UKIDSS in bands JHK.
Usage:
    replace_jhk_with_ukidss.py [ukidss catalog file] [target dat file]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180523
####################################
update log
20180523 version alpha 1
    1. The code work
'''
import time
import numpy as np
import convert_lib
from sys import argv
from dat2npy_noobs_nodet import read_well_known_data

# the function for read csv catalogs
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
        # if JHK is not found...
        if distances[i] == 0.0:
            mjy = err_mjy = 0.0
        # if the distance is larger than 1 beam size of irac...
        elif distances[i] > 0.6:
            mjy = err_mjy = 0.0
        else:
            mjy, err_mjy = convert_lib.mag_to_mJy(ukirt_system[band][2], bands_j[i,0], bands_j[i,1])
        j_mjy.append(mjy)
        err_j_mjy.append(err_mjy)
    return np.array(j_mjy), np.array(err_j_mjy)

def wipe_out_non_physical_numbers(target_list):
    # remove inf
    target_list[target_list > 1e308] = 0 
    # remove -inf
    target_list[target_list < -1e308] = 0 

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------    
    # check argv
    if len(argv) != 3:
        print("Error\nreplace_jhk_with_ukidss.py [ukidss catalog file] [target dat file]")
        exit()
    # read the Database UKIDSSDR10PLUS as a catalog
    name_ukidss_catalog = argv[1]
    name_dat_file = argv[2]
    catalogs = readfile(name_ukidss_catalog)
    # split into J, H, and Ks bands.
    bands_j = catalogs[:,10:12]
    bands_h = catalogs[:,12:14]
    bands_k = catalogs[:,14:16]
    # read id, distance, and coordinate
    global ids
    ids = catalogs[:,0]
    global distances
    distances = catalogs[:,3]
    #-----------------------------------
    # convert mag to mJy
    global ukirt_system
    ukirt_system = convert_lib.set_ukirt()
    print("### converting from magnitude to mJy ###")
    j_mjy, err_j_mjy =  mag_to_mjy(bands_j, 'J')
    h_mjy, err_h_mjy =  mag_to_mjy(bands_h, 'H')
    k_mjy, err_k_mjy =  mag_to_mjy(bands_k, 'K')
    # wipe out non-physical values
    wipe_out_non_physical_numbers(j_mjy)
    wipe_out_non_physical_numbers(h_mjy)
    wipe_out_non_physical_numbers(k_mjy)
    wipe_out_non_physical_numbers(err_j_mjy)
    wipe_out_non_physical_numbers(err_h_mjy)
    wipe_out_non_physical_numbers(err_k_mjy)
    #-----------------------------------
    # save the converted file of ukidss jhk bands
    converted_ukidss = np.stack((j_mjy, h_mjy, k_mjy, err_j_mjy, err_h_mjy, err_k_mjy))
    converted_ukidss = np.transpose(converted_ukidss)
    np.save("converted_{0}.npy".format(name_ukidss_catalog[:-4]), converted_ukidss)
    np.savetxt("converted_{0}.txt".format(name_ukidss_catalog[:-4]), converted_ukidss)
    #-----------------------------------
    # replace the small signals in 2MASS with signals in UKIDSS in bands JHK
    str_dat_file = read_well_known_data(name_dat_file)
    dat_file = np.array(str_dat_file, dtype = np.float64)
    replacement_j = np.where((j_mjy != 0) & (dat_file[:, 0] < 50) & (err_j_mjy != 0))
    replacement_h = np.where((h_mjy != 0) & (dat_file[:, 1] < 50) & (err_h_mjy != 0))
    replacement_k = np.where((k_mjy != 0) & (dat_file[:, 2] < 25) & (err_k_mjy != 0))
    dat_file[replacement_j, 0] = j_mjy[replacement_j]
    dat_file[replacement_h, 1] = h_mjy[replacement_h]
    dat_file[replacement_k, 2] = k_mjy[replacement_k]
    dat_file[replacement_j, 8] = err_j_mjy[replacement_j]
    dat_file[replacement_h, 9] = err_h_mjy[replacement_h]
    dat_file[replacement_k, 10] = err_k_mjy[replacement_k]
    np.save("{0}_u.npy".format(name_dat_file[:-4]), dat_file)
    np.savetxt("{0}_u.txt".format(name_dat_file[:-4]), dat_file)
    np.save("replaced_with_j_in_ukidss_{0}.npy".format(name_dat_file[:-4]), replacement_j[0])
    np.savetxt("replaced_with_j_in_ukidss_{0}.txt".format(name_dat_file[:-4]), replacement_j[0])
    np.save("replaced_with_h_in_ukidss_{0}.npy".format(name_dat_file[:-4]), replacement_h[0])
    np.savetxt("replaced_with_h_in_ukidss_{0}.txt".format(name_dat_file[:-4]), replacement_h[0])
    np.save("replaced_with_k_in_ukidss_{0}.npy".format(name_dat_file[:-4]), replacement_k[0])
    np.savetxt("replaced_with_k_in_ukidss_{0}.txt".format(name_dat_file[:-4]), replacement_k[0])
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
