#!/usr/bin/python3
'''
Abstract:
    This is a program for show regions on all sky map. 
Usage:
    show_all_emap.py [bkg fits file] [fits image file 1] [fits image file 2]  [fits image file 3]
    
    You have to follow this order:
    CHA_II_120asec_Av.fits 
    OPH_270asec_Av.fits 
    ELAIS_N1_2MASS_j_sub22.fits 
    LUP_I_120asec_Av.fits 
    LUP_III_120asec_Av.fits 
    LUP_IV_120asec_Av.fits 
    PER_180asec_Av.fits 
    SER_120asec_Av.fits
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181012
####################################
update log
20181012 version alpha 1:
    1. The code works.
'''
import matplotlib.pyplot as plt
import time
from sys import argv
import numpy as np
from astropy.io import fits as pyfits
from astropy import wcs
from astropy.coordinates import *
import healpy as hp

def equatorial2galactic(coords):
    c = SkyCoord(coords[:,0], coords[:,1], frame='icrs', unit='deg')
    gala_l = c.galactic.l.deg
    gala_b = c.galactic.b.deg
    gala_coords = np.transpose(np.array([gala_l, gala_b]))
    return gala_coords

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load arguments
    print("Usage: show_all_emap.py [bkg image file] [fits image file 1] [fits image file 2]  [fits image file 3]") 
    if len(argv) < 3:
        print ("The number of arguments is wrong.")
        exit(1)
    bkg_name = argv[1]
    image_name_list = argv[2:]
    #-----------------------------------
    # Load data
    #-----------------------------------
    # Plot and show
    fig = plt.figure(figsize = (8,8))
    sub_fig = plt.subplot(111, projection="mollweide")
    m = hp.read_map(bkg_name)
    hp.mollview(m, fig = 1, cmap = 'Greys', norm = 'log', cbar = False, title = 'Locations of our datasets in the whole sky map', notext = True)
    hp.graticule()
    plt.grid(True)
    region_name_list = ['CHA II',
                        'OPH',
                        'ELAIS N1',
                        'LUP I',
                        'LUP III',
                        'LUP IV',
                        'PER',
                        'SER'
                        ]
    color_list = ['b', 'g', 'r', 'olive', 'm', 'indigo', 'orange', 'cyan']
    text_offset = np.array([[-0.05, -0.15],
                            [-0.05, -0.15],
                            [-0.05, -0.15],
                            [-0.00,  0.10],
                            [-0.40,  0.00],
                            [ 0.04, -0.10],
                            [-0.05, -0.15],
                            [-0.05, -0.15]])
    plt.plot(np.pi, np.pi/2, c= 'w', label = 'Training sets')
    for index, name in enumerate(image_name_list):
        if index == 3:
            plt.plot(np.pi, np.pi/2, c= 'w', label = 'Test sets')
        image = pyfits.getdata(name)
        header = pyfits.getheader(name)
        w = wcs.WCS(header)
        indices_tuple = np.where(~np.isnan(image))
        pixel_coords = np.transpose(np.array([indices_tuple[0], indices_tuple[1]]))
        world_coords = w.wcs_pix2world(pixel_coords, 1)
        gala_coords = equatorial2galactic(world_coords)
        print ("{1}, {0}".format(name, gala_coords[0]))
        hp.projplot(gala_coords[:,0], gala_coords[:,1], lonlat = True, c = color_list[index], label = region_name_list[index])
    plt.legend()
    fig.savefig('Locations_of_our_datasets_in_whole_sky_map.png', dpi = 300)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
