#!/usr/bin/python3
'''
Abstract:
    This is a program to take band JHK from 2mass catalog
Usage:
    take_jhk_from_2mass.py [2mass catalog file] [band system] [label]
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
from convert_lib import TWOMASS_to_UKIDSS
from sys import argv
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize


####################################
from uncertainties import unumpy, ufloat
# How to cite this package
# If you use this package for a publication (in a journal, on the web, etc.),
# please cite it by including as much information as possible from the following:
# Uncertainties: a Python package for calculations with uncertainties, Eric O. LEBIGOT,
# http://pythonhosted.org/uncertainties/. Adding the version number is optional.
####################################

# this function is used to convert magnitude to mini Janskey
# take j band as example
def mag_to_mjy(bands, band, system):
    # initialize variables
    j_mjy = []
    err_j_mjy = []
    print("zeropoint: {0} mJy".format(system[band][2]))
    # convert
    for i in range(len(bands)):
        # if the distance is larger than 1 beam size of irac...
        # if JHK is not found...
        if distances[i] == 0.0:
            mjy = err_mjy = 0.0
        elif distances[i] > 0.6:
            mjy = err_mjy = 0.0
        elif bands[i].n == 0 or bands[i].s == 0:
            mjy = err_mjy = 0.0
        else:
            mjy, err_mjy = convert_lib.mag_to_mJy(system[band][2], bands[i].n, bands[i].s)
        j_mjy.append(mjy)
        err_j_mjy.append(err_mjy)
    j_mjy = np.nan_to_num(j_mjy)
    err_j_mjy = np.nan_to_num(err_j_mjy)
    return np.array(j_mjy), np.array(err_j_mjy)

# This def is used to fill up empty error with median one.
def fill_up_error(bands):
    # load data
    flux_with_error = bands[(bands[:,1] != 0.0),0]
    bands_with_error = bands[(bands[:,1] != 0.0)]
    # find the upper bond of flux with error
    flux_with_error = np.sort(flux_with_error)
    flux_upper_bond = flux_with_error[-1]
    # if flux over upper bond of flux with error, abandom that data.
    # if flux is below the upper bond of flux with error, replace error with median
    bands[(bands[:,1] == 0) & (bands[:,0] != 0.0) & (bands[:,0] > flux_upper_bond), 0] = 0.0
    index_of_bands_below_upper_bond_without_error = np.where((bands[:,1] == 0.0) & (bands[:,0] != 0.0))
    for index in index_of_bands_below_upper_bond_without_error[0]:
        candidates = bands_with_error[(bands_with_error[:,0] < bands[index, 0] + 0.115)  & (bands_with_error[:,0] > bands[index, 0] - 0.115), 1]
        bands[index, 1] = np.median(candidates)
    return bands

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    init = 0
    #-----------------------------------    
    # check argv
    if len(argv) != 4:
        print("Error\nUsage: take_jhk_from_2mass.py [2mass catalog file] [band system] [label]")
        print("Available band system: UKIDSS, TWOMASS")
        exit()
    # read the Database 2MASS Query as a catalog
    filename = argv[1]
    band_system = argv[2]
    label = argv[3]
    catalogs = np.loadtxt(filename, skiprows = 79, dtype = np.str)
    # split into J, H, and Ks bands.
    # If flux are detected but error not, assume the error is 10%
    # (5/2)^x = 0.9
    # x is around 0.115
    bands_j = catalogs[:,11:13]
    bands_j[bands_j == 'null'] = '0.0'
    bands_j = np.array(bands_j, dtype = np.float64)
    bands_h = catalogs[:,15:17]
    bands_h[bands_h == 'null'] = '0.0'
    bands_h = np.array(bands_h, dtype = np.float64)
    bands_k = catalogs[:,19:21]
    bands_k[bands_k == 'null'] = '0.0'
    bands_k = np.array(bands_k, dtype = np.float64)
    #-----------------------------------------------
    # plot the error distribution
    import matplotlib.pyplot as plt
    from IPython.core.pylabtools import figsize
    figsize(12, 6)
    fig, axes = plt.subplots(3,2, sharex='col')
    
    axes[0,0].set_title("band J")
    axes[0,0].plot(bands_j[:,0], bands_j[:,1], 'ro', alpha = 0.1)
    axes[0,0].grid(True)
    axes[0,0].set_xlim(10, 20)
    axes[1,0].set_title("band H")
    axes[1,0].plot(bands_h[:,0], bands_h[:,1], 'ro', alpha = 0.1)
    axes[1,0].grid(True)
    axes[1,0].set_xlim(10, 20)
    axes[2,0].set_title("band K")
    axes[2,0].plot(bands_k[:,0], bands_k[:,1], 'ro', alpha = 0.1)
    axes[2,0].grid(True)
    axes[2,0].set_xlim(10, 20)
    # fill up empty error
    bands_j = fill_up_error(bands_j)
    bands_h = fill_up_error(bands_h)
    bands_k = fill_up_error(bands_k)
    # plot the error distribution after filling up
    axes[0,1].set_title("band J")
    axes[0,1].plot(bands_j[:,0], bands_j[:,1], 'ro', alpha = 0.1)
    axes[0,1].grid(True)
    axes[0,1].set_xlim(10, 20)
    axes[1,1].set_title("band H")
    axes[1,1].plot(bands_h[:,0], bands_h[:,1], 'ro', alpha = 0.1)
    axes[1,1].grid(True)
    axes[1,1].set_xlim(10, 20)
    axes[2,1].set_title("band K")
    axes[2,1].plot(bands_k[:,0], bands_k[:,1], 'ro', alpha = 0.1)
    axes[2,1].grid(True)
    axes[2,1].set_xlim(10, 20)
    fig.savefig("err_distribution_after_filling_up.png")
    #--------------------------------------------
    # Show numbers in 2MASS system
    print ("--- In 2MASS system ---")
    for i in range(init, init + 10):
        print ("J: {0}, H: {1}, K: {2}".format(bands_j[i], bands_h[i], bands_k[i]))
    #-------------------------------------------------
    # convert from 2MASS bands system to UKIDSS bands system
    bands_ju = []
    bands_hu = []
    bands_ku = []
    if band_system == "UKIDSS":
        for i in range(len(catalogs)):
            band_j = ufloat(bands_j[i,0], bands_j[i,1])
            band_h = ufloat(bands_h[i,0], bands_h[i,1])
            band_k = ufloat(bands_k[i,0], bands_k[i,1])
            TwotoU = TWOMASS_to_UKIDSS(band_j, band_h, band_k)
            if (band_j.n != 0.0) and (band_h.n != 0.0):
                band_ju = TwotoU.Jw
                band_hu = TwotoU.Hw
            else:
                band_ju = ufloat(0.0, 0.0)
                band_hu = ufloat(0.0, 0.0)
            if (band_j.n != 0.0) and (band_k.n != 0.0):
                band_ku = TwotoU.Kw
            else:
                band_ku = ufloat(0.0, 0.0)
            # append
            bands_ju.append(band_ju)
            bands_hu.append(band_hu)
            bands_ku.append(band_ku)
        # Take a look of numbers in UKIDSS system
        print ("--- In UKIDSS system ---")
        for i in range(init, init + 10):
            print ("J: {0}, H: {1}, K: {2}".format(bands_ju[i], bands_hu[i], bands_ku[i]))
    #-------------------------------------------------
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
    #--------------------------------------------------
    # convert mag to flux
    j_mjy = []
    err_j_mjy = []
    h_mjy = []
    err_h_mjy = []
    k_mjy = []
    err_k_mjy = []
    if band_system == "UKIDSS":
        # convert mag to mJy
        ukirt_system = convert_lib.set_ukirt()
        print("--- In mJy ---")
        j_mjy, err_j_mjy =  mag_to_mjy(bands_ju, 'J', ukirt_system)
        h_mjy, err_h_mjy =  mag_to_mjy(bands_hu, 'H', ukirt_system)
        k_mjy, err_k_mjy =  mag_to_mjy(bands_ku, 'K', ukirt_system)
    elif band_system == "TWOMASS":
        # convert mag to mJy
        twomass_system = convert_lib.set_twomass()
        print("--- In mJy ---")
        j_mjy, err_j_mjy =  mag_to_mjy(bands_j, 'J', twomass_system)
        h_mjy, err_h_mjy =  mag_to_mjy(bands_h, 'H', twomass_system)
        k_mjy, err_k_mjy =  mag_to_mjy(bands_k, 'Ks', twomass_system)
    # print and check
    for i in range(init, init+10):
        print ("{0}: J:[{1:.4f}, {2:.4f}], H:[{3:.4f}, {4:.4f}], K:[{5:.4f}, {6:.4f}]".format(ids[i], j_mjy[i], err_j_mjy[i], h_mjy[i], err_h_mjy[i], k_mjy[i], err_k_mjy[i]))
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
