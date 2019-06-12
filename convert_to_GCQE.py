#!/usr/bin/python3
'''
Abstract:
    This is a program for converting coord table using GCQE format
Usage:
    convert_to_GCQE.py [table]
Output:
    1. The tabel in the GCQE format
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180531
####################################
update log
20190531 version alpha 1
    1. The code works.
'''
import tensorflow as tf
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
        print ("Usage: convert_to_GCQE.py [table]")
        print ("Temporary, only 2-column coordinates table can use it.")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data
    inp_table = np.loadtxt(inp_table_name, dtype = float)
    titles =( 
    "\keyword = value          \n"          
    "\ Comment                 \n" 
    "|   ra      |   dec     | \n"
    "|   double  |   double  | \n"
    "|   deg     |   deg     | \n"
    "|   null    |   null    | \n")
    np.savetxt( '{0}_GCQE.txt'.format(inp_table_name[:-4]), 
                inp_table,
                header = titles,
                delimiter = '|',
                fmt = '%11f')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
