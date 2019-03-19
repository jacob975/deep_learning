#!/usr/bin/python3
'''
Abstract:
    This is a program for finding the Av base on the position on the emap
Usage:
    remove_Av.py [emap table] [coord table]
    Example: remove_Av.py emap_table coord.txt
Editor:
    Jacob

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

201908308
####################################
update log
20190308 version alpha 1
    1. The code works
'''
from sys import argv
import time
import numpy as np
from uncertainties import ufloat
from astropy.coordinates import SkyCoord
from astropy import units as u
from scipy import optimize
import matplotlib.pyplot as plt

def find_the_closest_extinction_position(coord, emap_table):
    # Initialize
    # Read central position of source
    source_coord = SkyCoord(coord[0], coord[1], unit = 'deg') 
    extinction_coord = SkyCoord(emap_table[:,0], emap_table[:,1], unit = 'deg')
    # Calculate the distance
    distance_object_array = extinction_coord.separation(source_coord)
    distance_array = distance_object_array.deg
    # Pick the nearest one
    min_distance = np.min(distance_array)
    index_min_distance = np.argmin(distance_array) 
    return min_distance, index_min_distance

def find_Av(emap_table, coord_table, tolerance_radius = 6/60):
    Av_table = np.zeros((len(coord_table), 2))
    print ("Start!")
    N = len(coord_table)
    milestone = 0.0
    for index, coord in enumerate(coord_table):
        #------------------------------------------------
        # Find Av
        Av = -999.0
        err_Av = -999.0
        # Find the closest extinction position for sources.
        min_distance, \
        index_min = find_the_closest_extinction_position(
                        coord, 
                        emap_table)
        if min_distance > tolerance_radius:
            pass
        else:
            # Read the Av of the selected extinction point.
            Av_table[index, 0] = emap_table[index_min, 2]
            Av_table[index, 1] = emap_table[index_min, 3]
        if index/N > milestone:
            print ("{0:.2f}%".format(100*milestone))
            milestone += 0.1
    return Av_table

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #--------------------------------------------
    # Load argv
    if len(argv) != 3:
        print ("Error!")
        print ("Usage: find_Av.py [emap table] [coord table]") 
        print ("Available band systems: ukidss, twomass")
        print ("You can skip [Av table]")
        print ("Example: find_Av.py emap_table coord.txt")
        exit()
    emap_table_name = argv[1]
    coord_table_name = argv[2]
    #--------------------------------------------
    # Load data
    # The table of extinction map.
    emap_table = np.loadtxt(emap_table_name, dtype = float)
    emap_table = emap_table[~np.isnan(emap_table[:,2])]
    # Coord table
    coord_table = np.loadtxt(coord_table_name, dtype = float)
    #-----------------------------------
    # The radius of an extinction region in unit degree
    tolerance_radius = 6/60
    # Calculate
    Av_table = find_Av(emap_table, coord_table, tolerance_radius)
    # Save the table
    np.savetxt("Av_table.txt", Av_table, fmt = "%.2f")
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
