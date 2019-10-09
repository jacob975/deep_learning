#!/usr/bin/python3
'''
Abstract:
    This is a program for show regions on all sky map. 
Usage:
    show_sources_mollweide.py [coord table] [fits files]
    
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

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load arguments
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: show_sources_mollweide.py [coord table] [fits file]")
        print ("Hint: This program suits planck archive image only.")
        exit(1)
    coord_table_name = argv[1]
    image_name = argv[2]
    #-----------------------------------
    # Plot and show
    fig = plt.figure(figsize = (8,6))
    sub_fig = plt.subplot(111, projection="mollweide")
    # Plot background
    m = hp.read_map(image_name)
    hp.mollview(m, fig = 1, cmap = 'Greys', norm = 'log', cbar = False, \
                title = '', \
                #title = 'Locations of our datasets in the whole sky map', \
                notext = True
                )
    hp.graticule()
    plt.grid(True)
    # Plot the sources
    world_coords = np.loadtxt(coord_table_name, dtype = float)
    gala_coords = equatorial2galactic(world_coords)
    hp.projscatter( gala_coords[:,0], gala_coords[:,1], \
                    lonlat = True, \
                    s=1, \
                    #c = color_list[index], \
                    #label = region_name_list[index]
                  )
    fig.savefig('{0}.png'.format(image_name[:-5]), dpi = 300)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
