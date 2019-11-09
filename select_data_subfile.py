#!/usr/bin/python3
'''
Abstract:
    This is a program to select data with filter, and then save to a destination file. 
Usage:
    select_data.py [margin of index] [filter] [data] [destination]
Output:
    1. The processed table
    2. The backup which is the original table.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181002
####################################
update log
20181002 version alpha 1:
    1. The code works.
'''
import numpy as np
import time
from sys import argv
import os

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 5:
        print ("Error! The number of arguments is wrong.")
        print ("Usage: select_data.py [margin of index] [filter] [data] [destination]")
        exit()
    margin = int(argv[1])
    filter_name = argv[2]
    data_name = argv[3]
    dest_name = argv[4]
    #-----------------------------------
    # Load data
    print ('Loading data...')
    data = np.loadtxt(data_name, dtype = str)
    _filter = np.loadtxt(filter_name, dtype = int)
    num_filter = len(_filter)
    try: 
        dest = np.loadtxt(  dest_name, dtype = object)
    except:
        dest = np.ones( (num_filter, len(data[0])), dtype = object)
    print (dest.dtype) 
    # Apply the filter
    index = np.arange(num_filter)
    _filter = _filter - margin
    _filter_compact = _filter[(_filter < len(data)) & (_filter >= 0)]
    index_compact   = index[(_filter < len(data)) & (_filter >= 0)]
    print ('Calculating...')
    dest[index_compact] = data[_filter_compact]
    print ('Saving...')
    np.savetxt(dest_name, dest, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
