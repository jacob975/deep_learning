#!/usr/bin/python3
'''
Abstract:
    This is a program to take band JHK from ukidss catalog, 
    and replace the small signals in 2MASS with signals in UKIDSS in bands JHK.
    Caution!!!!!! For DR10 Only !!!!!!!
Usage:
    replace_jhk_with_ukidss.py [ukidss catalog file] [twomass catalog file] [target dat file]
Output:
    
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
20180711 version alpha 2
    1. Add a func for replace with 2MASS data
    2. Ensemble version for DXS, GPS, GCS
    3. fill up error with median value
20180716 version alpha 3
    1. Add a func for skip
'''
import time
import numpy as np
import convert_lib
from convert_lib import TWOMASS_to_UKIDSS, fill_up_error
from sys import argv
from dat2npy_lib import read_well_known_data
from uncertainties import ufloat
import warnings

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
def mag_to_mjy_numpy(bands, band, distances, system):
    # initialize variables
    mjy_array = []
    err_mjy_array = []
    # convert
    for i in range(len(bands)):
        # if JHK is not found...
        if distances[i] == 0.0:
            mjy = err_mjy = 0.0
        # if the distance is larger than 1 beam size of irac...
        elif distances[i] > 0.6:
            mjy = err_mjy = 0.0
        elif bands[i,0] == 0 or bands[i,1] == 0: 
            mjy = err_mjy = 0.0
        else:
            mjy, err_mjy = convert_lib.mag_to_mJy(system[band][2], bands[i,0], bands[i,1])
        mjy_array.append(mjy)
        err_mjy_array.append(err_mjy)
    mjy_array = np.nan_to_num(mjy_array)
    err_mjy_array = np.nan_to_num(err_mjy_array)
    return np.array(mjy_array), np.array(err_mjy_array)

# this function is used to convert magnitude to mini Janskey
# take j band as example
def mag_to_mjy_ufloat(bands, band, distances, system):
    # initialize variables
    mjy_array = []
    err_mjy_array = []
    # Convert from mag to mjy
    for i in range(len(bands)):
        # if JHK is not found...
        if distances[i] == 0.0:
            mjy = err_mjy = 0.0
        # if the distance is larger than 1 beam size of irac...
        elif distances[i] > 0.6:
            mjy = err_mjy = 0.0
        # If the source is not observed.
        elif bands[i].n == 0 or bands[i].s == 0:
            mjy = err_mjy = 0.0
        elif bands[i].n < -100 or bands[i].s < -100:
            mjy = err_mjy = 0.0
        
        else:
            mjy, err_mjy = convert_lib.mag_to_mJy(system[band][2], bands[i].n, bands[i].s)
        mjy_array.append(mjy)
        err_mjy_array.append(err_mjy)
    mjy_array = np.nan_to_num(mjy_array)
    err_mjy_array = np.nan_to_num(err_mjy_array)
    return np.array(mjy_array), np.array(err_mjy_array)

def wipe_out_non_physical_numbers(target_list):
    # Remove inf
    target_list[target_list > 1e308] = 0 
    # Remove -inf
    target_list[target_list < -1e308] = 0 

def SEDname2Qname(name_dat_file, keyword):
    position = name_dat_file.find(keyword)
    if position >= 0:
        name_Q_file = '{0}{1}_Q.dat'.format(name_dat_file[:position], keyword)
        return 0, name_Q_file
    return 1, ''

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    # Ignore all warnings
    warnings.filterwarnings("ignore")
    #-----------------------------------    
    # Load and check argv
    if len(argv) != 5:
        print("Error\nreplace_jhk_with_ukidss.py [Type of UKIDSS catalog] [ukidss catalog file] [twomass catalog file] [target dat file]")
        print("Available type of UKIDSS catalog: DXS, GCS, GPS")
        print("If you want to skip ukidss or twomass catalog, you can use keyword 'skip'.")
        exit()
    type_ukidss_catalog = argv[1]
    name_ukidss_catalog = argv[2]
    name_twomass_catalog = argv[3]
    name_dat_file = argv[4]
    #-----------------------------------
    # Find the name of Q dat 
    keywords = ['star', 'gala', 'ysos']
    name_Q = ''
    for key in keywords:
        failure, tmp_name_Q = SEDname2Qname(name_dat_file, key)
        if not failure:
            name_Q = tmp_name_Q
    print ("Replace for {0}".format(name_dat_file))
    #-----------------------------------
    # Read the Database UKIDSSDR10PLUS as a catalog
    ukidss_j_mjy = None
    ukidss_h_mjy = None
    ukidss_k_mjy = None
    ukidss_err_j_mjy = None
    ukidss_err_h_mjy = None
    ukidss_err_k_mjy = None
    if name_ukidss_catalog != "skip":
        catalogs = readfile(name_ukidss_catalog)
        # split into J, H, and Ks bands.
        ukidss_bands_j = []  
        ukidss_bands_h = [] 
        ukidss_bands_k = [] 
        if type_ukidss_catalog == "DXS":
            ukidss_bands_j = catalogs[:,10:12]
            ukidss_bands_h = catalogs[:,12:14]
            ukidss_bands_k = catalogs[:,14:16]
        elif type_ukidss_catalog == "GCS":
            ukidss_bands_j = catalogs[:,14:16]
            ukidss_bands_h = catalogs[:,16:18]
            ukidss_bands_k = catalogs[:,18:20]
        elif type_ukidss_catalog == "GPS":
            ukidss_bands_j = catalogs[:,10:12]
            ukidss_bands_h = catalogs[:,12:14]
            ukidss_bands_k = catalogs[:,14:16]
        else:
            print("Wrong type of UKIDSS catalog")
            print("Usage: replace_jhk_with_ukidss.py [Type of UKIDSS catalog] [ukidss catalog file] [twomass catalog file] [target dat file]")
            print("Available type of UKIDSS catalog: DXS, GCS, GPS")
            exit(1)
        # read distance
        ukidss_distances = catalogs[:,3]
        # convert mag to mJy
        ukirt_system = convert_lib.set_ukirt()
        print("--- Let UKIDSS data converted from magnitude to mJy add used in SED ---")
        ukidss_j_mjy, ukidss_err_j_mjy =  mag_to_mjy_numpy(ukidss_bands_j, 'J', ukidss_distances, ukirt_system)
        ukidss_h_mjy, ukidss_err_h_mjy =  mag_to_mjy_numpy(ukidss_bands_h, 'H', ukidss_distances, ukirt_system)
        ukidss_k_mjy, ukidss_err_k_mjy =  mag_to_mjy_numpy(ukidss_bands_k, 'K', ukidss_distances, ukirt_system)
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
        np.savetxt("{0}_flux.txt".format(name_ukidss_catalog[:-4]), ukidss_flux)
    #-----------------------------------
    # read the Database 2MASS as a catalog
    twomass_j_mjy = None 
    twomass_h_mjy = None 
    twomass_k_mjy = None 
    twomass_err_j_mjy = None 
    twomass_err_h_mjy = None
    twomass_err_k_mjy = None
    if name_twomass_catalog != 'skip':
        twomass_catalogs = np.loadtxt(name_twomass_catalog, skiprows = 79, dtype = np.str)
        # Obtain Mag data and split table into J, H, and Ks bands.
        twomass_bands_j = twomass_catalogs[:,11:13]
        twomass_bands_j[twomass_bands_j == 'null'] = '0.0'
        twomass_bands_j = np.array(twomass_bands_j, dtype = np.float64)
        twomass_bands_h = twomass_catalogs[:,15:17]
        twomass_bands_h[twomass_bands_h == 'null'] = '0.0'
        twomass_bands_h = np.array(twomass_bands_h, dtype = np.float64)
        twomass_bands_k = twomass_catalogs[:,19:21]
        twomass_bands_k[twomass_bands_k == 'null'] = '0.0'
        twomass_bands_k = np.array(twomass_bands_k, dtype = np.float64)
        # Fill up non-given error
        twomass_bands_ju = []
        twomass_bands_hu = []
        twomass_bands_ku = []
        twomass_bands_j = fill_up_error(twomass_bands_j)
        twomass_bands_h = fill_up_error(twomass_bands_h)
        twomass_bands_k = fill_up_error(twomass_bands_k)
        # Save band JHK in twomass for checking
        twomass_bands = np.array([twomass_bands_j[:,0], twomass_bands_h[:,0], twomass_bands_k[:,0]])
        twomass_bands = np.transpose(twomass_bands)
        err_twomass_bands = np.array([twomass_bands_j[:,1], twomass_bands_h[:,1], twomass_bands_k[:,1]])
        err_twomass_bands = np.transpose(err_twomass_bands)
        np.savetxt("{0}_twomass_mag.txt".format(name_dat_file[:-4]), twomass_bands)
        np.savetxt("{0}_err_twomass_mag.txt".format(name_dat_file[:-4]), err_twomass_bands)
        # Convert band system from 2MASS to UKIDSS
        for i in range(len(twomass_catalogs)):
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
        # Read the distance between the source found in IRAC1 register and 2MASS register.
        twomass_distances = twomass_catalogs[:,1]
        twomass_distances[twomass_distances == 'null'] = '999.0'
        twomass_distances = np.array(twomass_distances, dtype = np.float64)
        # Convert mag to mJy
        ukirt_system = convert_lib.set_ukirt()
        print ("--- Let 2MASS data converted to UKIDSS band system, and fill up the blank of UKIDSS data --- ")
        twomass_j_mjy, twomass_err_j_mjy =  mag_to_mjy_ufloat(twomass_bands_ju, 'J', twomass_distances, ukirt_system)
        twomass_h_mjy, twomass_err_h_mjy =  mag_to_mjy_ufloat(twomass_bands_hu, 'H', twomass_distances, ukirt_system)
        twomass_k_mjy, twomass_err_k_mjy =  mag_to_mjy_ufloat(twomass_bands_ku, 'K', twomass_distances, ukirt_system)
        # Save the converted file of ukidss jhk bands
        twomass_flux = np.stack((twomass_j_mjy, twomass_h_mjy, twomass_k_mjy, twomass_err_j_mjy, twomass_err_h_mjy, twomass_err_k_mjy))
        twomass_flux = np.transpose(twomass_flux)
        np.savetxt("{0}_flux.txt".format(name_twomass_catalog[:-4]), twomass_flux)
    #-----------------------------------
    # Replace the small signals in 2MASS with signals in UKIDSS in bands JHK
    str_dat_file = read_well_known_data(name_dat_file)
    dat_file = np.array(str_dat_file, dtype = np.float64)
    if name_twomass_catalog != 'skip':
        dat_file[:,0] = twomass_j_mjy
        dat_file[:,1] = twomass_h_mjy
        dat_file[:,2] = twomass_k_mjy
        dat_file[:,8] = twomass_err_j_mjy
        dat_file[:,9] = twomass_err_h_mjy
        dat_file[:,10] = twomass_err_k_mjy
    if name_ukidss_catalog != "skip":
        replacement_k = np.where((ukidss_k_mjy != 0) & (dat_file[:, 2] < 15) & (ukidss_err_k_mjy != 0))
        dat_file[replacement_k, 0] = ukidss_j_mjy[replacement_k]
        dat_file[replacement_k, 1] = ukidss_h_mjy[replacement_k]
        dat_file[replacement_k, 2] = ukidss_k_mjy[replacement_k]
        dat_file[replacement_k, 8] = ukidss_err_j_mjy[replacement_k]
        dat_file[replacement_k, 9] = ukidss_err_h_mjy[replacement_k]
        dat_file[replacement_k, 10] = ukidss_err_k_mjy[replacement_k]
        np.savetxt("replaced_with_ukidss_based_on_k_{0}.txt".format(name_dat_file[:-4]), replacement_k[0])
        # Update the Q flag
        Q_flags = np.loadtxt(name_Q, dtype = str)
        Q_flags[replacement_k,:3] = 'R'
        np.savetxt(name_Q, Q_flags, fmt = '%s')
    np.savetxt("{0}_u.txt".format(name_dat_file[:-4]), dat_file)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
