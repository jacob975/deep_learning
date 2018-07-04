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
# take j band as example
def mag_to_mjy(bands, band, distances, system):
    # initialize variables
    j_mjy = []
    err_j_mjy = []
    print("zeropoint: {0}".format(ukirt_system[band][2]))
    # convert
    for i in range(len(bands)):
        # if JHK is not found...
        if distances[i] == 0.0:
            mjy = err_mjy = 0.0
        # if the distance is larger than 1 beam size of irac...
        elif distances[i] > 0.6:
            mjy = err_mjy = 0.0
        else:
            try:
                mjy, err_mjy = convert_lib.mag_to_mJy(system[band][2], bands[i].n, bands[i].s)
            except:
                mjy, err_mjy = convert_lib.mag_to_mJy(system[band][2], bands[i,0], bands[i,1])
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
    # Load and check argv
    if len(argv) != 4:
        print("Error\nreplace_jhk_with_ukidss.py [ukidss catalog file] [twomass catalog file] [target dat file]")
        exit()
    name_ukidss_catalog = argv[1]
    name_twomass_catalog = argv[2]
    name_dat_file = argv[3]
    #-----------------------------------
    # read the Database UKIDSSDR10PLUS as a catalog
    catalogs = readfile(name_ukidss_catalog)
    # split into J, H, and Ks bands.
    ukidss_bands_j = catalogs[:,14:16]
    ukidss_bands_h = catalogs[:,16:18]
    ukidss_bands_k = catalogs[:,18:20]
    # read distance
    ukidss_distances = catalogs[:,3]
    # convert mag to mJy
    ukirt_system = convert_lib.set_ukirt()
    print("### converting from magnitude to mJy ###")
    ukidss_j_mjy, ukidss_err_j_mjy =  mag_to_mjy(ukidss_bands_j, 'J', ukidss_distances, ukirt_system)
    ukidss_h_mjy, ukidss_err_h_mjy =  mag_to_mjy(ukidss_bands_h, 'H', ukidss_distances, ukirt_system)
    ukidss_k_mjy, ukidss_err_k_mjy =  mag_to_mjy(ukidss_bands_k, 'K', ukidss_distances, ukirt_system)
    # wipe out non-physical values
    wipe_out_non_physical_numbers(ukidss_j_mjy)
    wipe_out_non_physical_numbers(ukidss_h_mjy)
    wipe_out_non_physical_numbers(ukidss_k_mjy)
    wipe_out_non_physical_numbers(ukidss_err_j_mjy)
    wipe_out_non_physical_numbers(ukidss_err_h_mjy)
    wipe_out_non_physical_numbers(ukidss_err_k_mjy)
    # save the converted file of ukidss jhk bands
    ukidss_flux = np.stack((ukidss_j_mjy, ukidss_h_mjy, ukidss_k_mjy, ukidss_err_j_mjy, ukidss_err_h_mjy, ukidss_err_k_mjy))
    ukidss_flux = np.transpose(ukidss_flux)
    np.save("{0}_flux.npy".format(name_ukidss_catalog[:-4]), ukidss_flux)
    np.savetxt("{0}_flux.txt".format(name_ukidss_catalog[:-4]), ukidss_flux)
    #-----------------------------------
    # read the Database 2MASS as a catalog
    twomass_catalogs = np.loadtxt(name_twomass_catalog, skiprows = 79, dtype = np.str)
    # split into J, H, and Ks bands.
    twomass_bands_j = twomass_catalogs[:,11:13]
    twomass_bands_j[twomass_bands_j == 'null'] = '0.0'
    twomass_bands_j = np.array(twomass_bands_j, dtype = np.float64)
    twomass_bands_h = twomass_catalogs[:,15:17]
    twomass_bands_h[twomass_bands_h == 'null'] = '0.0'
    twomass_bands_h = np.array(twomass_bands_h, dtype = np.float64)
    twomass_bands_k = twomass_catalogs[:,19:21]
    twomass_bands_k[twomass_bands_k == 'null'] = '0.0'
    twomass_bands_k = np.array(twomass_bands_k, dtype = np.float64)
    # convert from 2MASS bands system to UKIDSS bands system
    twomass_bands_ju = []
    twomass_bands_hu = []
    twomass_bands_ku = []
    for i in range(len(catalogs)):
        twomass_band_j = ufloat(twomass_bands_j[i,0], twomass_bands_j[i,1])
        twomass_band_h = ufloat(twomass_bands_h[i,0], twomass_bands_h[i,1])
        twomass_band_k = ufloat(twomass_bands_k[i,0], twomass_bands_k[i,1])
        TwotoU = TWOMASS_to_UKIDSS(twomass_band_j, twomass_band_h, twomass_band_k)
        if (twomass_band_j.n != 0.0) and (twomass_band_h.n != 0.0):
            twomass_band_ju = TwotoU.Jw
            twomass_band_hu = TwotoU.Hw
        else:
            twomass_band_ju = ufloat(0.0, 0.0)
            twomass_band_hu = ufloat(0.0, 0.0)
        if (twomass_band_j.n != 0.0) and (twomass_band_k.n != 0.0):
            twomass_band_ku = TwotoU.Kw
        else:
            twomass_band_ku = ufloat(0.0, 0.0)
        # append
        twomass_bands_ju.append(twomass_band_ju)
        twomass_bands_hu.append(twomass_band_hu)
        twomass_bands_ku.append(twomass_band_ku)
    # convert mag to flux
    twomass_j_mjy = []
    twomass_err_j_mjy = []
    twomass_h_mjy = []
    twomass_err_h_mjy = []
    twomass_k_mjy = []
    twomass_err_k_mjy = []
    # grab distance of target and table
    twomass_distances = twomass_catalogs[:,1]
    twomass_distances[twomass_distances == 'null'] = '999.0'
    twomass_distances = np.array(twomass_distances, dtype = np.float64)
    # convert mag to mJy
    ukirt_system = convert_lib.set_ukirt()
    print("--- In mJy ---")
    twomass_j_mjy, twomass_err_j_mjy =  mag_to_mjy(twomass_bands_ju, 'J', twomass_distances, ukirt_system)
    twomass_h_mjy, twomass_err_h_mjy =  mag_to_mjy(twomass_bands_hu, 'H', twomass_distances, ukirt_system)
    twomass_k_mjy, twomass_err_k_mjy =  mag_to_mjy(twomass_bands_ku, 'K', twomass_distances, ukirt_system)
    # save the converted file of ukidss jhk bands
    twomass_flux = np.stack((twomass_j_mjy, twomass_h_mjy, twomass_k_mjy, twomass_err_j_mjy, twomass_err_h_mjy, twomass_err_k_mjy))
    twomass_flux = np.transpose(twomass_flux)
    np.save("{0}_flux.npy".format(name_twomass_catalog[:-4]), twomass_flux)
    np.savetxt("{0}_flux.txt".format(name_twomass_catalog[:-4]), twomass_flux)
    #-----------------------------------
    # replace the small signals in 2MASS with signals in UKIDSS in bands JHK
    str_dat_file = read_well_known_data(name_dat_file)
    dat_file = np.array(str_dat_file, dtype = np.float64)
    dat_file[:,0] = twomass_j_mjy
    dat_file[:,1] = twomass_h_mjy
    dat_file[:,2] = twomass_k_mjy
    dat_file[:,8] = twomass_err_j_mjy
    dat_file[:,9] = twomass_err_h_mjy
    dat_file[:,10] = twomass_err_k_mjy
    replacement_j = np.where((ukidss_j_mjy != 0) & (dat_file[:, 0] < 30) & (ukidss_err_j_mjy != 0))
    replacement_h = np.where((ukidss_h_mjy != 0) & (dat_file[:, 1] < 15) & (ukidss_err_h_mjy != 0))
    replacement_k = np.where((ukidss_k_mjy != 0) & (dat_file[:, 2] < 15) & (ukidss_err_k_mjy != 0))
    dat_file[replacement_j, 0] = ukidss_j_mjy[replacement_j]
    dat_file[replacement_h, 1] = ukidss_h_mjy[replacement_h]
    dat_file[replacement_k, 2] = ukidss_k_mjy[replacement_k]
    dat_file[replacement_j, 8] = ukidss_err_j_mjy[replacement_j]
    dat_file[replacement_h, 9] = ukidss_err_h_mjy[replacement_h]
    dat_file[replacement_k, 10] = ukidss_err_k_mjy[replacement_k]
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
