#!/usr/bin/python3
'''
Abstract:
    This is a program for removing any columns with null. 
Usage:
    remove_null.py [input table]
Output:
    1. The table without null column.
    2. The index of columns without null.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190527
####################################
update log
20190527 version alpha 1
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
        print ("Usage: remove_null.py [input table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Read the data
    inp_table = np.loadtxt(inp_table_name, dtype = object)
    # Remove any columns with 'null'.
    distance = inp_table[:,1]
    non_null_index = np.where(distance != 'null')
    out_table = inp_table[non_null_index]
    # Save the result and corresponding indexs.
    np.savetxt("{0}_nr.txt".format(inp_table_name[:-4]), out_table, fmt = '%s')
    np.savetxt("{0}_nrindex.txt".format(inp_table_name[:-4]), non_null_index[0], fmt = '%d')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
