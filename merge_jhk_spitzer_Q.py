#!/usr/bin/python3
'''
Abstract:
    This is a program for merging JHK and SPITZER sed table. 
Usage:
    merge_jhk_spitzer_Q.py [jhk table] [spitzer table] [distance table] 
Output:
    1. The Q table with JHK, IRAC, and MIPS 1 observations.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190905
####################################
update log
20190905 version alpha 1
    1. The code works. 
'''
import time
import numpy as np
from sys import argv

def str2array(twomass_table):
    new_twomass_array = np.empty((len(twomass_table), 3), dtype = str)
    for i, Qstr in enumerate(twomass_table):
        Q = np.array(list(Qstr))
        new_twomass_array[i] = Q
    return new_twomass_array
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
        print ("Usage: merge_jhk_spitzer_Q.py [jhk table] [spitzer table] [distance table]")
        exit()
    JHK_table_name = argv[1]
    spitzer_table_name = argv[2]
    distance_table_name = argv[3]
    #-----------------------------------
    # Load data
    distance_table = np.loadtxt(distance_table_name, dtype = float)
    fake_sources = np.where(distance_table > 0.6)
    JHK_table = np.loadtxt(JHK_table_name, dtype = str)
    JHK_table[JHK_table == 'null'] = 'UUU'
    JHK_table[fake_sources] = 'UUU'
    JHKQ = str2array(JHK_table)
    spitzer_table = np.loadtxt(spitzer_table_name, dtype = str)
    spitzerQ = spitzer_table[:,0:5]
    # Merge two SED table
    merged_table = np.hstack((JHKQ, spitzerQ))
    # Save the result
    np.savetxt('merged_Q_table.txt', merged_table, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
