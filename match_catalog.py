#!/usr/bin/python3
'''
Abstract:
    This is a program for matching the sources in reference catalogue and given catalogue. 
Usage:
    match_catalog.py [ref coord] [given coord]
    In every single matching, the program pick a source from given_coords.
    Then find the best-fit in ref_coods.

Output:
    1. index of matched sources in two catalogues
    2. coordinates of matched sources
    3. coordinates of un-matched sources
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
20191014 version alpha 2
    2. Make it more general. Not only WISE and c2d+Spitzer can use but all catalog matching.
'''
import time
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
from sys import argv

# This is a class for match the coordinates efficiently.
class find_sources():
    def __init__(self, ref_coords, tolerance = 0.0):
        self.tolerance = tolerance
        self.ref_quick = np.array(ref_coords, dtype = int)
        self.ref_coords = SkyCoord(ref_coords[:,0], ref_coords[:,1], unit = 'deg')
        return
    def find(self, given_coord):
        self.given_coord = SkyCoord(given_coord[0], given_coord[1], unit = 'deg')
        self.given_quick = np.array(given_coord, dtype = int)
        # Quick select by integer
        quick_ra_dist = np.absolute(self.given_quick[0] - self.ref_quick[:,0])
        quick_select = np.where(quick_ra_dist <= 1)[0]
        if len(quick_select) == 0:
            return True, 0.0, np.zeros(2), 0
        quick_select_ref_coords = self.ref_coords[quick_select]
        # Calculate the distance
        distance_object_array = quick_select_ref_coords.separation(self.given_coord)
        distance_array = distance_object_array.deg
        # Pick the nearest one
        quick_ref_match_index = np.argmin(distance_array)
        min_distance = distance_array[quick_ref_match_index]
        ref_match_index = quick_select[quick_ref_match_index]
        if min_distance < self.tolerance:
            return False, min_distance, self.ref_coords[ref_match_index], ref_match_index
        else:
            return True, 0.0, np.zeros(2), 0

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
        print ("Usage: match_catalog.py [ref coord] [given coord]")
        print ("In every single matching, The program pick a source from given_coords.")
        print ("Then find the best-fit in ref_coods.")
        exit()
    ref_coord_table_name = argv[1]
    given_coord_table_name = argv[2]
    #-----------------------------------
    # Load data
    print ("Loading data...")
    ref_coord = np.loadtxt(ref_coord_table_name)
    given_coord = np.loadtxt(given_coord_table_name)
    # Find the matched detections.
    # The tolerance is 1 arcsec.
    print ("Initialized the process")
    stu = find_sources(ref_coord, tolerance = 0.00028)
    num_given_source = len(given_coord)
    result_table = np.zeros((num_given_source, 7))
    print ("Match start")
    for given_index, given in enumerate(given_coord):
        if given_index%1000 == 0:
            elapsed_time = time.time() - start_time
            print ('({0}/{1}) time: {2}'.format(given_index, num_given_source, elapsed_time))
        failure, distance, ref, ref_index = stu.find(given)
        if not failure:
            result_table[given_index] = np.array([  given_index, given[0], given[1], 
                                                    ref_index, ref.ra.deg, ref.dec.deg, distance])
        elif failure:
            result_table[given_index] = np.array([  given_index, given[0], given[1], 
                                                    -1, 0, 0, 0])
    # Save the result
    np.savetxt( "{0}_match_sources.txt".format(ref_coord_table_name), 
                result_table, 
                header = 'given_index RA DEC ref_index RA DEC distance')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
