#!/usr/bin/python3
'''
Abstract:
    This is a program to select data with filter. 
Usage:
    select_data.py [data] [filter]
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
    if len(argv) != 3:
        print ("Error! The number of arguments is wrong.")
        print ("Usage: select_data.py [data] [filter]")
        exit()
    data_name = argv[1]
    filter_name = argv[2]
    #-----------------------------------
    # Load data
    data = np.loadtxt(data_name)
    _filter = np.loadtxt(filter_name, dtype = int)
    result_data = data[:]
    result_data[_filter] = 0.0
    np.savetxt('{0}_backup{1}'.format(data_name[:-4], data_name[-4:]), data)
    np.savetxt(data_name, result_data)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")