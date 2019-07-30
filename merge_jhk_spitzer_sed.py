#!/usr/bin/python3
'''
Abstract:
    This is a program for merging JHK and SPITZER sed table. 
Usage:
    merge_jhk_spitzer_sed.py [jhk table] [spitzer table] 
Output:
    1. The sed table with JHK, IRAC, and MIPS 1 observations.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180731
####################################
update log
20190731 version alpha 6
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
    if len(argv) != 4:
        print ("The number of arguments is wrong.")
        print ("Usage: merge_jhk_spitzer_sed.py [jhk table] [spitzer table] [distance table]")
        exit()
    JHK_table_name = argv[1]
    spitzer_table_name = argv[2]
    distance_table_name = argv[3]
    #-----------------------------------
    # Load data
    JHK_table = np.loadtxt(JHK_table_name, dtype = str)
    spitzer_table = np.loadtxt(spitzer_table_name, dtype = str)
    spitzer_table[spitzer_table == 'null'] = '0.0'
    distance_table = np.loadtxt(distance_table_name, dtype = float)
    # Merge two SED table
    fake_sources = np.where(distance_table > 0.6)
    JHK_table[fake_sources] = np.array(['0','0','0','0','0','0'])
    JHKflux = JHK_table[:,0:3]
    eJHKflux = JHK_table[:,3:6]
    spitzerflux = spitzer_table[:,0:5]
    espitzerflux = spitzer_table[:,5:10]
    merged_flux = np.hstack((JHKflux, spitzerflux))
    merged_eflux = np.hstack((eJHKflux, espitzerflux))
    merged_table = np.hstack((merged_flux, merged_eflux))
    # Save the result
    np.savetxt('merged_sed_table.txt', merged_table, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
