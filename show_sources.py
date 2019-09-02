#!/usr/bin/python3
'''
Abstract:
    This is a program for show sources on image. 
Usage:
    show_sources.py [coord table] [fits image file]

    coord table is a txt file with the following form.
        [[RA, DEC], 
         [RA, DEC],
         ...
        ]
    fits image file is an image file with WCS
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181011
####################################
update log
20181011 version alpha 1:
    1. The code works.
'''
import matplotlib.pyplot as plt
import time
from sys import argv
import numpy as np
from astropy.io import fits as pyfits
from astropy import wcs
from astropy.coordinates import *

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load arguments
    if len(argv) != 3:
        print("The number of arguments is wrong.")
        print("Usage: show_sources.py [coord table] [fits image file]")
        exit(1)
    coord_table_name = argv[1]
    image_name = argv[2]
    #-----------------------------------
    # Load data
    
    hdu = pyfits.open(image_name)
    
    world_coord = None
    pixel_coord = None
    if coord_table_name != 'skip':
        world_coord = np.loadtxt(coord_table_name)
    image = hdu[1].data 
    header = hdu[1].header 
    #-----------------------------------
    # Convert WCS coord to pixel coord
    w = wcs.WCS(header)
    if coord_table_name != 'skip':
        pixel_coord = w.wcs_world2pix(world_coord, 1)
    # Plot and show
    fig = plt.figure(figsize = (8, 8))
    plt.subplot(111, projection = w)
    plt.title("Source on {0}".format(image_name))
    plt_image = plt.imshow(image)
    plt.colorbar()
    if coord_table_name != 'skip':
        plt.scatter(pixel_coord[:,0], pixel_coord[:,1], s= 2, c= 'r' )
    plt.savefig('{0}.png'.format(image_name[:-5]))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
