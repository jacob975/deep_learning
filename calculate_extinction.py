#!/usr/bin/python3
'''
Abstract:
    This is a program for calculate the extinction of each source with NICER
Usage:
    calculate_extinction.py [coord_table] [mag_table] [err_mag_table]
Editor:
    JW Wang, Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180104
####################################
update log
20180815 version alpha 1
    1. The code works
'''
import numpy as np
from pnicer import ApparentMagnitudes as AM
from astropy.coordinates import *
import matplotlib.pyplot as plt
from sys import argv
import time
import DL_conf

#--------------------------------------------
# main code
if __name__ == "__main__":
    # measure time
    start_time = time.time()
    #--------------------------------------------
    # Load argv
    if len(argv) != 4:
        print ("Wrong number of arguments")
        print ("Usage: calculate_extinction.py [coord_table] [mag_table] [err_mag_table]")
        exit(1)
    coord_table_name = argv[1]
    mag_table_name = argv[2]
    err_mag_table_name = argv[3]
    #--------------------------------------------
    # Load files
    science_coord = np.loadtxt(coord_table_name, dtype = float)
    science_coord = SkyCoord(science_coord, frame='icrs', unit='deg')
    science_mag = np.loadtxt(mag_table_name, dtype = float)
    science_err_mag = np.loadtxt(err_mag_table_name, dtype = float)
    control_coord = np.loadtxt("{0}/ELAIS_N1_NICER_control_image/star_coord.txt".format(DL_conf.path_of_data), dtype = float)
    control_coord = SkyCoord(control_coord, frame='icrs', unit='deg')
    control_mag = np.loadtxt("{0}/ELAIS_N1_NICER_control_image/twomass_mag.txt".format(DL_conf.path_of_data), dtype = float)
    control_err_mag = np.loadtxt("{0}/ELAIS_N1_NICER_control_image/err_twomass_mag.txt".format(DL_conf.path_of_data), dtype = float)
    # read allOBS data only
    index_science_allOBS = np.where((science_mag[:,0] != 0) & (science_mag[:,1] != 0) &(science_mag[:,2] != 0))
    index_control_allOBS = np.where((control_mag[:,0] != 0) & (control_mag[:,1] != 0) &(control_mag[:,2] != 0))
    science_coord = science_coord[index_science_allOBS]
    science_mag = science_mag[index_science_allOBS]
    science_mag = np.rot90(science_mag)
    science_err_mag = science_err_mag[index_science_allOBS]
    science_err_mag = np.rot90(science_err_mag)
    control_coord = control_coord[index_control_allOBS]
    control_coord = control_coord[:len(control_coord)//4]
    control_mag = control_mag[index_control_allOBS]
    control_mag = control_mag[:len(control_mag)//4]
    control_mag = np.rot90(control_mag)
    control_err_mag = control_err_mag[index_control_allOBS]
    control_err_mag = control_err_mag[:len(control_err_mag)//4]
    control_err_mag = np.rot90(control_err_mag)
    #--------------------------------------------
    # Calculate the extinction
    # Initialize
    mag_names = ["Ks"  , "H"   , "J"   ]
    extvec =    [0.1193, 0.1847, 0.2939]
    science = AM(magnitudes = science_mag,
                errors = science_err_mag,
                extvec = extvec,
                coordinates = science_coord,
                names = mag_names)
    control = AM(magnitudes = control_mag,
                errors = control_err_mag,
                extvec = extvec,
                coordinates = control_coord,
                names = mag_names)
    science_color = science.mag2color()
    control_color = control.mag2color()
    ext_nicer = science.nicer(control=control)
    print (ext_nicer.extinction)
    #--------------------------------------------
    # Plot
    #                                pixel size(degree)                   gaussian in pixel
    nicer_emap = ext_nicer.build_map(bandwidth=5./60., metric="gaussian", sampling=3        , use_fwhm=True)
    # Extinction map
    nicer_emap.save_fits(path="./emap_nicer.fits")
    # Histogram
    Av_nicer=ext_nicer.extinction
    Av_hist = np.histogram(Av_nicer, np.arange(-10, 20))
    Av_hist_plot = plt.figure("Av histogram")
    plt.title("Av histogram")
    plt.xlabel("Av")
    plt.ylabel("# of sources")
    plt.bar(np.arange(-9.5, 19.5, 1), Av_hist[0])
    Av_hist_plot.savefig("Av_hist.png")
    #--------------------------------------------
    # save the result
    np.savetxt('Av_nicer.dat',Av_nicer)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
