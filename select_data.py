#!/usr/bin/python3
'''
Abstract:
    This is a program to select data with filter. 
Usage:
    select_data.py [options] [filter] [data]
    
    options could be: selector, filter
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

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 4:
        print ("Error! The number of arguments is wrong.")
        print ("Usage: select_data.py [options] [filter] [data]")
        print ("Available options: selector, filter")
        exit()
    option = argv[1]
    filter_name = argv[2]
    data_name = argv[3]
    #-----------------------------------
    # Load data
    data = np.loadtxt(data_name, dtype = object)
    _filter = np.loadtxt(filter_name, dtype = int)
    # Apply the filter
    result_data = data[:]
    if option == "filter":
        result_data[_filter] = 0.0
    elif option == "selector":
        result_data = result_data[_filter]
    else:
        print ('Wrong arguments')
        print ('Please check the usage.')
        exit()
    np.savetxt('{0}_backup{1}'.format(data_name[:-4], data_name[-4:]), data, fmt = '%s')
    np.savetxt(data_name, result_data, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
