#!/usr/bin/python3
'''
Abstract:
    This is a program for rearrange labels. 
Usage:
    arrange_label.py [data] [selector]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181030
####################################
update log
'''
import numpy as np
import time
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
        print ('Error')
        print ('The number of arguments is wrong.')
        print ('Usage: arrange_label.py [data] [selector]')
        exit()
    data_name = argv[1]
    selector_name = argv[2]
    #-----------------------------------
    # Load data
    data = np.loadtxt(data_name)
    selector = np.loadtxt(selector_name, dtype = int)
    sub_names = ['star', 'gala', 'ysos']
    for i in range(3):
        sub_selector = np.where(selector == i)
        sub_data = data[sub_selector]
        np.savetxt('{0}_{1}.txt'.format(data_name[:-4], sub_names[i]), sub_data)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
