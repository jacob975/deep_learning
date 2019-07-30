#!/usr/bin/python3
'''
Abstract:
    This is a program for testing how csv works. 
Usage:
    test_2mass_table.py [XMM-LSS 2MASS table]
Output:
    1. TBA
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190729
####################################
update log
20190729 version alpha 1
    1. The code works.
'''
import time
import numpy as np
from sys import argv
import convert_lib

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: test_2mass_table.py [XMM-LSS 2MASS table]")
        exit()
    2mass_table_name = argv[1]
    #-----------------------------------
    # Print the test text
    2mass_table = np.loadtxt(  2mass_table_name, 
                                        dtype = str,
                                        delimiter = ',',)
    # Take the AperMag3 as the magnitude.
    distance = np.array(2mass_table[:, 1],   dtype = float)
    Jmag = np.array(2mass_table[:, [11,13]], dtype = float)
    Hmag = np.array(2mass_table[:, [15,17]], dtype = float)
    Kmag = np.array(2mass_table[:, [19,21]], dtype = float)
    # Load 2MASS bands system
    2mass_system = convert_lib.set_twomass()
    # Convert from 2MASSmag to UKIDSSmag.
    # Save the data
    np.savetxt('2MASS_JHKflux.txt', output_table)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
