#!/usr/bin/python3
'''
Abstract:
    This is a program for generating a fake Q label with assuming 0.0 = U 
Usage:
    generate_fake_Q.py [sed table]
Output:
    1. The Q label of each band in each source. 
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190804
####################################
update log
20190804 version alpha 1
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
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: generate_fake_Q.py [sed table]")
        exit()
    sed_table_name = argv[1]
    #-----------------------------------
    # Load data
    sed_table = np.loadtxt(sed_table_name)
    fake_Q_table = np.empty((len(sed_table), 8), dtype = str)
    fake_Q_table[:] = 'A'
    index_zero = sed_table[:,:8] <= 0.0
    index_zero_err = sed_table[:,8:] <= 0.0
    fake_Q_table[index_zero] = "U"
    fake_Q_table[index_zero_err] = "U"
    fake_Q_table_2 = []
    for Q in fake_Q_table:
        str_Q = ' '.join(Q) 
        fake_Q_table_2.append(str_Q)
    np.savetxt('fake_Q.txt', fake_Q_table_2, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
