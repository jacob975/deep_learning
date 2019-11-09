#!/usr/bin/python3
'''
Abstract:
    This is a program for show regions on all sky map. 
Usage:
    show_sources_mollweide.py [fits files]
    
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20191001
####################################
update log
20191001 version alpha 1:
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

def plot_procedure(given_coords, given_color):
    gala_coords = equatorial2galactic(given_coords)
    hp.projscatter( gala_coords[:,0], gala_coords[:,1], \
                    lonlat = True, \
                    s=1, \
                    c = given_color, \
                  )
    

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load arguments
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: show_sources_mollweide.py [fits file]")
        print ("Hint: This program suits planck archive image only.")
        exit(1)
    image_name = argv[1]
    #-----------------------------------
    # Load images
    m = hp.read_map(image_name)
    # Setup the image scales. 
    fig = plt.figure(figsize = (16,12))
    sub_fig = plt.subplot(111, projection="mollweide")
    # Plot background
    hp.mollview(m, fig = 1, cmap = 'Greys', norm = 'log', cbar = False, \
                title = '', \
                #title = 'Locations of our datasets in the whole sky map', \
                notext = True
                )
    hp.graticule()
    plt.grid(True)
    # Plot the sources
    while True:
        coord_table_name = input("Name of coordinate table:")
        color = input("The color of sources:")
        coords = np.loadtxt(coord_table_name, dtype = float)
        plot_procedure(coords, color)
        status = input("Continue? (y/n):")
        if status == 'y':
            continue
        elif status == 'n':
            break
        else:
            print ("Unrecongnized symbles, continue.")
    fig.savefig('shown_sources.png', dpi = 300)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
