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
    print("zeropoint: {0} mJy".format(system[band][2]))
    mjy, err_mjy = convert_lib.mag_to_mJy(system[band][2], mag, err_mag)
    mjy[np.isnan(mjy)] = 0
    err_mjy[np.isnan(err_mjy)] = 0
    return np.array(mjy), np.array(err_mjy)

# This function for converting mini Janskey to magnitude
def mjy_to_mag(mjy, err_mjy, band, system):
    print("zeropoint: {0} mJy".format(system[band][2]))
    mag, err_mag = convert_lib.mJy_to_mag(system[band][2], mjy, err_mjy)
    mag[np.isnan(mag)] = 0
    err_mag[np.isnan(err_mag)] = 0
    return np.array(mag), np.array(err_mag)

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
    # print something for check
    print("j = {0}+/-{1}, h = {2}+/-{3} k = {4}+/-{5}".format(j_mjy[0], err_j_mjy[0], h_mjy[0], err_h_mjy[0], k_mjy[0], err_k_mjy[0]))
    # convert from flux to 2MASS bands system
    twomass_system = convert_lib.set_twomass()
    j_mag, err_j_mag =  mjy_to_mag(j_mjy, err_j_mjy, 'J', twomass_system)
    h_mag, err_h_mag =  mjy_to_mag(h_mjy, err_h_mjy, 'H', twomass_system)
    k_mag, err_k_mag =  mjy_to_mag(k_mjy, err_k_mjy, 'Ks',twomass_system)
    # print something for check
    print("j = {0}+/-{1}, h = {2}+/-{3} k = {4}+/-{5}".format(j_mag[0], err_j_mag[0], h_mag[0], err_h_mag[0], k_mag[0], err_k_mag[0]))
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
    # print something for check
    print("j = {0}+/-{1}, h = {2}+/-{3} k = {4}+/-{5}".format(j_mjy_u[0], err_j_mjy_u[0], h_mjy_u[0], err_h_mjy_u[0], k_mjy_u[0], err_k_mjy_u[0]))
    np.save("{0}_u.npy".format(name_dat_file[:-4]), dat_file)
    np.savetxt("{0}_u.txt".format(name_dat_file[:-4]), dat_file)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
