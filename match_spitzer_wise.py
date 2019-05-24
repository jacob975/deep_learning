#!/usr/bin/python3
'''
Abstract:
    This is a program for matching the sources in ALLWISE catalogue and c2d+SWIRE catalogue. 
Usage:
    match_spitzer_wise.py [spitzer coord] [wise coord]
Output:
    1. index of matched sources
    2. coordinates of matched sources
    3. index of un-matched sources
    4. coordinates of un-matched sources
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190522
####################################
update log
20190522 version alpha 1
    1. The code works. 
'''
import time
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
from sys import argv

# This is a class for match the coordinates efficiently.
class find_sources():
    def __init__(self, coord_table, tolerance = 0.0):
        self.coord_table = coord_table
        self.tolerance = tolerance
        self.ref_coords = SkyCoord(self.coord_table[:,0], self.coord_table[:,1], unit = 'deg')
        return
    def find(self, coord):
        source_coord = SkyCoord(coord[0], coord[1], unit = 'deg')
        # Calculate the distance
        distance_object_array = self.ref_coords.separation(source_coord)
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
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: match_sp_wise.py [spitzer coord] [wise coord]")
        exit()
    spitzer_coord_table_name = argv[1]
    wise_coord_table_name = argv[2]
    #-----------------------------------
    # Load data
    spitzer_coord = np.loadtxt(spitzer_coord_table_name)
    wise_coord = np.loadtxt(wise_coord_table_name)
    #wise_coord = np.loadtxt(wise_coord_table_name, delimiter = '|')
    match_wise_index_list = []
    unmatch_wise_index_list = []
    # Find the matched detections.
    # The tolerance is 1 arcsec.
    stu = find_sources(spitzer_coord, tolerance = 0.00028)
    num_source_in_wise = len(wise_coord)
    for i, wise in enumerate(wise_coord):
        if i%1000 == 0:
            print ('({0}/{1})'.format(i, num_source_in_wise))
        failure, distance, index = stu.find(wise)
        if not failure:
            match_wise_index_list.append(i)
        elif failure:
            unmatch_wise_index_list.append(i)
    # Save the result
    match_wise_index_array = np.array(match_wise_index_list)
    unmatch_wise_index_array = np.array(unmatch_wise_index_list)
    match_coord = wise_coord[match_wise_index_list]
    unmatch_coord = wise_coord[unmatch_wise_index_list] 
    np.savetxt("{0}_match_index.txt".format(wise_coord_table_name[:-4]), match_wise_index_array, fmt = '%d')
    np.savetxt("{0}_match_coord.txt".format(wise_coord_table_name[:-4]), match_coord)
    np.savetxt("{0}_unmatch_index.txt".format(wise_coord_table_name[:-4]), unmatch_wise_index_array, fmt = '%d')
    np.savetxt("{0}_unmatch_coord.txt".format(wise_coord_table_name[:-4]), unmatch_coord)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
