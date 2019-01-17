#!/usr/bin/python3
'''
Abstract:
    This is a program to exclude the upper limit "U" happened in band 4 ~ 7 
Usage:
    exclude_ul_4_7.py [Q flag table] [data]
    
    Input should looks like:
    Q flag table = 
    [[ A, A, A, A, A, A, A, U],
     [ A, B, A, A, A, A, A, U],
     ...]

Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181128
####################################
update log
20181128 version alpha 1:
    1. The code works
20190117 version alpha 2:
    1. Only exclude the source has upper limit on IRAC1~4
'''
from sys import argv
import time
import numpy as np

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("Wrong numbers of arguments")
        print ("Usage: exclude_ul_4_7.py [Q flag table] [data]")
        exit(0)
    ul_table_name = argv[1]
    data_name = argv[2]
    #-----------------------------------
    # Load data
    ul_table = np.loadtxt(ul_table_name, dtype = str)
    data = np.loadtxt(data_name, dtype = str)
    #------------------------------------------
    # Find the line with upper limits
    data_no_ul = data[  #(ul_table[:,0] != 'U') &\
                        #(ul_table[:,1] != 'U') &\
                        #(ul_table[:,2] != 'U') &\
                        (ul_table[:,3] != 'U') &\
                        (ul_table[:,4] != 'U') &\
                        (ul_table[:,5] != 'U') &\
                        (ul_table[:,6] != 'U')]
    # Save masked data set
    np.savetxt("{0}_exul_4_7.txt".format(data_name[:-4]), data_no_ul, fmt = '%s')
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
