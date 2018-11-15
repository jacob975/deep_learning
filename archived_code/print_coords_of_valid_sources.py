#!/usr/bin/python3
'''
Abstract:
    This is a program to print coordinates of valid sources.
Usage:
    print_coords_of_valid_sources.py [source data file] [coord files]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180611
####################################
update log
20180611 version alpha 1
    1. The code works
'''
import time
import numpy as np
from sys import argv

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("Error!\nUsage:\tprint_coords_of_valid_sources.py [source data files] [coord files]") 
        print ("Example:print_coords_of_valid_sources.py ukidss_j_star.txt star_coord.dat")
        exit()
    name_sources = argv[1]
    name_coords = argv[2]
    # Load files
    sources = np.loadtxt(name_sources)
    coords = np.loadtxt(name_coords)
    # wipe out non sense data
    sources_too_high = np.where(sources > 1E308)
    sources[sources_too_high] = 0.0
    sources_too_low = np.where(sources <= -999)
    sources[sources_too_low] = 0.0
    # valid means no loss and no saturations
    no_loss = np.where((sources[:,0] != 0) & (sources[:, 0] < 50))
    coords = coords[no_loss]
    # Save searching result and shuffled result
    randomize = np.arange(len(coords))
    np.random.shuffle(randomize)
    rand_coords = coords[randomize]
    np.savetxt("coords_of_valid_{0}.txt".format(name_sources[:-4]), coords)
    np.savetxt("rand_coords_of_valid_{0}.txt".format(name_sources[:-4]), rand_coords)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
