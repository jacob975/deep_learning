#!/usr/bin/python3
'''
Abstract:
    This is a program for take the first 8 column from a table. 
Usage:
    take_first_8.py [table]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190120
####################################
update log
20190120 version alpha 1:
    1. The code works
'''
import time
import numpy as np
from sys import argv

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
        print ("Usage: take_first_8.py [table]")
        exit()
    table_name = argv[1]
    # take the first 8 column
    table = np.loadtxt(table_name)
    new_table = table[:,:8]
    np.savetxt(table_name, new_table)
    print("Done.")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
