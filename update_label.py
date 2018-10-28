#!/usr/bin/python3
'''
Abstract:
    This is a program for updating labels in a text file using a given catalog. 
Usage:
    update_label.py [coord table] [given catalog]
    
    coord table: [[RA, DEC],
                  [RA, DEC],
                  [RA, DEC],
                  ...
                 ]

    given catalog: [[RA, DEC],
                    [RA, DEC],
                    [RA, DEC],
                    ...
                   ]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181028
####################################
update log
20181028 version alpha 1:
    1. The code works.
'''
import numpy as np
import time
from sys import argv
from astropy.coordinates import SkyCoord
from astropy import units as u 

# This is class for finding matched source
# The units of all quantities are degree.
class find_sources():
    def __init__(self, coord_table, tolerance = 0.0):
        self.coord_table = coord_table
        self.tolerance = tolerance
        return
    def find(self, coord):
        source_coord = SkyCoord(coord[0], coord[1], unit = 'deg') 
        ref_coords = SkyCoord(self.coord_table[:,0], self.coord_table[:,1], unit = 'deg')
        # Calculate the distance
        distance_object_array = ref_coords.separation(source_coord)
        distance_array = distance_object_array.deg
        # Pick the nearest one
        min_distance = np.min(distance_array)
        index_min_distance = np.argmin(distance_array) 
        if min_distance < self.tolerance:
            return False, min_distance, index_min_distance
        else:
            return True, 0.0, 0

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 5:
        print ("Error!")
        print ("The number of arguments is wrong.")
        print ("Usage: update_label.py [origin label] [given label] [coord table] [given catalog]")
        exit(1)
    origin_label = argv[1]
    given_label = argv[2]
    coord_table_name = argv[3]
    given_catalog_name = argv[4]
    #-----------------------------------
    # Load data
    coord_table = np.loadtxt(coord_table_name)
    given_catalog = np.loadtxt(given_catalog_name)
    # Given by c2d final delivery, Chap.2.4.1, in degree
    tolerance = 2./3600.
    print ("The number of source in coord table: {0}".format(len(coord_table)))
    print ("The number of source in given catalog: {0}".format(len(given_catalog)))
    stu = find_sources(coord_table, tolerance)
    new_label = np.full(len(coord_table), origin_label, dtype = str) 
    found_counter = 0
    for i in range(len(given_catalog)):
        failure, distance, jndex = stu.find(given_catalog[i])
        if not failure:
            found_counter += 1
            print (coord_table[jndex], given_catalog[i])
            new_label[jndex] = given_label
    print ("Total number of found sources: {0}".format(found_counter))
    # Determine the label name
    label_name = coord_table_name[:4]
    given_name = given_catalog_name.split("_")[0]
    # Save the new label
    np.savetxt('{0}_{1}_label.txt'.format(given_name, label_name), new_label, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
