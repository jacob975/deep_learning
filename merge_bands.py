#!/usr/bin/python3
'''
Abstract:
    This is a program for mergin two SEDs table. 
Usage:
    band_merge.py [error included] [table A] [table B] 
    error_included: Does error included in the input table?
    Caution: !!!!!! distance is not taken into account !!!!!!!!!
Output:
    1. The merged SEDs table
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190531
####################################
update log
20190531 version alpha 1
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
    if len(argv) != 4:
        print ("The number of arguments is wrong.")
        print ("Usage: band_merge.py [error included] [table A] [table B]")
        print ("error_included can be 'yes' or 'no'.")
        exit()
    error_included = argv[1]
    table_A_name = argv[2]
    table_B_name = argv[3]
    #-----------------------------------
    # Load data
    if error_included == 'yes':
        table_A = np.loadtxt(table_A_name, dtype = object)
        table_B = np.loadtxt(table_B_name, dtype = object)
        num_items_A = table_A.shape[1]
        num_items_B = table_B.shape[1]
        table_merged = np.zeros((len(table_A), num_items_A + num_items_B))
        table_merged[:, :num_items_A//2] = table_A[:, :num_items_A//2]
        table_merged[:, num_items_A//2:num_items_A//2 + num_items_B//2] = table_B[:, :num_items_B//2]
        table_merged[:, num_items_A//2 + num_items_B//2: num_items_A + num_items_B//2] = table_A[:, num_items_A//2:]
        table_merged[:, num_items_A + num_items_B//2:] = table_B[:, num_items_B//2:]
    elif error_included == 'no':
        table_A = np.loadtxt(table_A_name, dtype = object, delimiter = '|')
        table_B = np.loadtxt(table_B_name, dtype = object, delimiter = '|')
        table_merged = np.empty(len(table_A), dtype = str)
        table_merged = table_A + table_B
    else:
        print ("Wrong arguments")
        exit()
    np.savetxt("merged_table.txt", table_merged, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
