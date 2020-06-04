#!/usr/bin/python3
'''
Abstract:
    This is a program for show sources on image. 
Usage:
    show_YSO_sources.py [coord table] [cls_pred table] [fits image file]

    1. coord table is a txt file with the following form.
        [[RA, DEC], 
         [RA, DEC],
         ...
        ]
    2. cls_pred table is a text file containing a list of cls index.
    ex.
    [ 0, 0, 1, 0, 2, 0, ...,]
    3. fits image file is an image file with WCS
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
from matplotlib.colors import LogNorm
import time
from sys import argv
import numpy as np
from astropy.io import fits as pyfits
from astropy import wcs
from astropy.coordinates import *
from astropy.coordinates import SkyCoord
from astropy import units as u

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load arguments
    if len(argv) != 4:
        print("The number of arguments is wrong.")
        print("Usage: show_YSO_sources.py [coord table] [cls_pred table] [fits image file]")
        exit(1)
    coord_table_name = argv[1]
    cls_pred_name = argv[2]
    image_name = argv[3]
    #-----------------------------------
    # Load data
    world_coord = np.loadtxt(coord_table_name)
    cls_pred = np.loadtxt(cls_pred_name, dtype = int)
    image = pyfits.getdata(image_name) 
    hdu = pyfits.open(image_name)
    #header = hdu[0].header
    header = hdu[1].header
    print(header)
    #-----------------------------------
    # Find the YSO index
    yso_index = np.where(cls_pred == 2)[0]
    # Convert WCS coord to pixel coord
    w = wcs.WCS(header)
    # Plot and show
    fig = plt.figure(figsize = (8, 8))
    ax = plt.subplot(111, projection = w)
    plt.title("Source on {0}".format(image_name))
    plt_image = plt.imshow(
        image,
        norm = LogNorm(
            vmax = np.max(image),
            vmin = np.min(image)
        )
    )
    plt.colorbar()
    plt.scatter(
        world_coord[yso_index,0], 
        world_coord[yso_index,1], 
        s= 2, 
        c= 'r',
        transform=ax.get_transform('icrs')
    )
    plt.savefig('{0}_yso.png'.format(image_name[:-5]))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
