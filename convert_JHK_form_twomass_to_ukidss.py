#!/usr/bin/python3
'''
Abstract:
    This is a program for converting band system from 2MASS to UKIDSS
Usage:
    convert_JHK_form_twomass_to_ukidss.py [dat file name]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180704
####################################
update log
20180704 version alpha 1
    1. The code work
'''
import time
import numpy as np
import convert_lib
from convert_lib import TWOMASS_to_UKIDSS
from sys import argv
from dat2npy_noobs_nodet import read_well_known_data
from uncertainties import ufloat

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
def mag_to_mjy(mag, err_mag, band, system):
    # initialize variables
    mjy_array = []
    err_mjy_array = []
    print("zeropoint: {0}".format(system[band][2]))
    # convert
    for i in range(len(j_mag)):
        mjy, err_mjy = convert_lib.mag_to_mJy(system[band][2], mag[i], err_mag[i])
        mjy_array.append(mjy)
        err_mjy_array.append(err_mjy)
    return np.array(mjy_array), np.array(err_mjy_array)

# This function for converting mini Janskey to magnitude
def mjy_to_mag(mjy, err_mjy, band, system):
    # initialize variables
    mag_array = []
    err_mag_array = []
    print("zeropoint: {0}".format(system[band][2]))
    # convert
    for i in range(len(mjy)):
        mag, err_mag = convert_lib.mJy_to_mag(system[band][2], mjy[i], err_mjy[i])
        mag_array.append(mag)
        err_mag_array.append(err_mag)
    return np.array(mag_array), np.array(err_mag_array)

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
    # Load and check argv
    if len(argv) != 2:
        print("Error convert_JHK_from_twomass_to_ukidss.py [dat file name]") 
        print("Example: convert_JHK_from_twomass_to_ukidss.py ysos_sed.dat")
        exit()
    name_dat_file = argv[1]
    #-----------------------------------
    # replace the small signals in 2MASS with signals in UKIDSS in bands JHK
    str_dat_file = read_well_known_data(name_dat_file)
    dat_file = np.array(str_dat_file, dtype = np.float64)
    j_mjy = dat_file[:,0]
    h_mjy = dat_file[:,1]
    k_mjy = dat_file[:,2]
    err_j_mjy = dat_file[:,8] 
    err_h_mjy = dat_file[:,9] 
    err_k_mjy = dat_file[:,10]
    # convert from flux to 2MASS bands system
    twomass_system = convert_lib.set_twomass()
    j_mag, err_j_mag =  mjy_to_mag(j_mjy, err_j_mjy, 'J', twomass_system)
    h_mag, err_h_mag =  mjy_to_mag(h_mjy, err_h_mjy, 'H', twomass_system)
    k_mag, err_k_mag =  mjy_to_mag(k_mjy, err_k_mjy, 'Ks',twomass_system)
    # convert from 2MASS bands system to UKIDSS bands system
    ukirt_system = convert_lib.set_ukirt()
    j_mjy_u, err_j_mjy_u =  mag_to_mjy(j_mag, err_j_mag, 'J', ukirt_system)
    h_mjy_u, err_h_mjy_u =  mag_to_mjy(h_mag, err_h_mag, 'H', ukirt_system)
    k_mjy_u, err_k_mjy_u =  mag_to_mjy(k_mag, err_k_mag, 'K', ukirt_system)
    dat_file[:,0] = j_mjy_u
    dat_file[:,1] = h_mjy_u
    dat_file[:,2] = k_mjy_u
    dat_file[:,8] = err_j_mjy_u
    dat_file[:,9] = err_h_mjy_u
    dat_file[:,10] = err_k_mjy_u
    np.save("{0}_u.npy".format(name_dat_file[:-4]), dat_file)
    np.savetxt("{0}_u.txt".format(name_dat_file[:-4]), dat_file)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
