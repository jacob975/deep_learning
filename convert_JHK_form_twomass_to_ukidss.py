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
from convert_lib import TWOMASS_to_UKIDSS, fill_up_error
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
def mag_to_mjy(mag, band, system):
    print("zeropoint: {0} mJy".format(system[band][2]))
    mjy, err_mjy = convert_lib.mag_to_mJy(system[band][2], mag[:,0], mag[:,1])
    mjy = np.nan_to_num(mjy)
    err_mjy = np.nan_to_num(err_mjy)
    mjy = np.transpose(np.stack((mjy, err_mjy)))
    return np.array(mjy)

# This function for converting mini Janskey to magnitude
def mjy_to_mag(mjy, band, system):
    print("zeropoint: {0} mJy".format(system[band][2]))
    mag, err_mag = convert_lib.mJy_to_mag(system[band][2], mjy[:,0], mjy[:,1])
    mag = np.nan_to_num(mag)
    err_mag = np.nan_to_num(err_mag)
    mag = np.transpose(np.stack((mag, err_mag)))
    return np.array(mag)

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
    j_mjy = np.transpose(np.stack((dat_file[:, 0], dat_file[:, 8])))
    h_mjy = np.transpose(np.stack((dat_file[:, 1], dat_file[:, 9])))
    k_mjy = np.transpose(np.stack((dat_file[:, 2], dat_file[:, 10])))
    # reomve exotic number before processed
    j_mjy[j_mjy == -9.99e+02] = 0.0
    h_mjy[h_mjy == -9.99e+02] = 0.0
    k_mjy[k_mjy == -9.99e+02] = 0.0
    # print something for check
    print("j = {0}+/-{1}, h = {2}+/-{3} k = {4}+/-{5}".format(j_mjy[0, 0], j_mjy[0, 1], h_mjy[0,0], h_mjy[0,1], k_mjy[0, 0], k_mjy[0, 1]))
    # convert from flux to 2MASS bands system
    twomass_system = convert_lib.set_twomass()
    j_mag =  mjy_to_mag(j_mjy, 'J', twomass_system)
    h_mag =  mjy_to_mag(h_mjy, 'H', twomass_system)
    k_mag =  mjy_to_mag(k_mjy, 'Ks',twomass_system) 
    # fill up empty error
    j_mag = fill_up_error(j_mag)
    h_mag = fill_up_error(h_mag)
    k_mag = fill_up_error(k_mag)
    # print something for check
    print("j = {0}+/-{1}, h = {2}+/-{3} k = {4}+/-{5}".format(j_mjy[0, 0], j_mjy[0, 1], h_mjy[0,0], h_mjy[0,1], k_mjy[0, 0], k_mjy[0, 1]))
    # convert from 2MASS bands system to UKIDSS bands system
    ukirt_system = convert_lib.set_ukirt()
    j_mjy_u =  mag_to_mjy(j_mag, 'J', ukirt_system)
    h_mjy_u =  mag_to_mjy(h_mag, 'H', ukirt_system)
    k_mjy_u =  mag_to_mjy(k_mag, 'K', ukirt_system)
    dat_file[:,0] = j_mjy_u[:,0]
    dat_file[:,1] = h_mjy_u[:,0]
    dat_file[:,2] = k_mjy_u[:,0]
    dat_file[:,8] = j_mjy_u[:,1]
    dat_file[:,9] = h_mjy_u[:,1]
    dat_file[:,10] =k_mjy_u[:,1]
    # print something for check
    print("j = {0}+/-{1}, h = {2}+/-{3} k = {4}+/-{5}".format(j_mjy[0, 0], j_mjy[0, 1], h_mjy[0,0], h_mjy[0,1], k_mjy[0, 0], k_mjy[0, 1]))
    np.save("{0}_u.npy".format(name_dat_file[:-4]), dat_file)
    np.savetxt("{0}_u.txt".format(name_dat_file[:-4]), dat_file)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
