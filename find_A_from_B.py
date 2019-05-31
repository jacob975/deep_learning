#!/usr/bin/python3
'''
Abstract:
    This is a program for finding the index of A in the table B. 
Usage:
    find_A_from_B.py [table A] [table B]
Output:
    1. Index of matched items
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190529
####################################
update log
20190529 version alpha 1
    1. The code works.
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
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: find_A_from_B.py [table A] [table B]")
        exit()
    table_A_name = argv[1]
    table_B_name = argv[2]
    #-----------------------------------
    # Load data
    table_A = np.loadtxt(table_A_name, dtype = str, delimiter = '|')
    table_B = np.loadtxt(table_B_name, dtype = str, delimiter = '|')
    # Find the index of A in table B
    index_table = np.zeros(len(table_A))
    for i, A in enumerate(table_A):
        index = np.where(table_B == A)
        if len(index[0]) == 0:
            index_table[i] = -1
        else:
            index_table[i] = index[0][0]
    # Save the result
    np.savetxt("index.txt", index_table, fmt = '%d')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
