#!/usr/bin/python3
'''
Abstract:
    This is a program for counting the number of labels. 
Usage:
    count_labels.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181108
####################################
update log
'''
import numpy as np
from sys import argv
import time
import collections

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 4:
        print ('The number of arguments is wrong.')
        print ("Usage: count_labels.py [star labels] [galaxy labels] [ysos labels]")
        exit()
    star_name = argv[1]
    gala_name = argv[2]
    ysos_name = argv[3]
    #-----------------------------------
    # Load data
    star_labels = np.loadtxt(star_name, dtype = int)
    gala_labels = np.loadtxt(gala_name, dtype = int)
    ysos_labels = np.loadtxt(ysos_name, dtype = int)
    # Print the result
    print(star_name)
    print(collections.Counter(star_labels))
    print(gala_name)
    print(collections.Counter(gala_labels))
    print(ysos_name)
    print(collections.Counter(ysos_labels))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
