#!/usr/bin/python3
'''
Abstract:
    This is a program to convert hms coordinates to degree coordinates. 
Usage:
    hms2deg.py [input hms table]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181003
####################################
update log
'''
from astropy import units as u
from astropy.coordinates import SkyCoord
import time
from sys import argv
import numpy as np

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("Error! The number of arguments is wrong.")
        print ("Usage: hms2deg.py [input hms table]")
        exit()
    # Load hms table
    coords_name = argv[1]
    hms_coords_name = "{0}_hms{1}".format(coords_name[:-4], coords_name[-4:])
    hms_coords = np.loadtxt(coords_name, dtype = str)
    deg_coords = np.zeros((len(hms_coords), 2), dtype = float)
    # Convert from hms to degree
    for index, hms in enumerate(hms_coords):
        coord = SkyCoord(hms[0], hms[1], frame='icrs')
        deg_coords[index,0] = coord.ra.degree
        deg_coords[index,1] = coord.dec.degree
    # Save the result
    np.savetxt(coords_name, deg_coords)
    np.savetxt(hms_coords_name, hms_coords, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
