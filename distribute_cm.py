#!/usr/bin/python3
'''
Abstract:
    This is a program for distributing elements by labels of A and B models. 
Usage:
    distribute_cm.py [A label table] [# of A label] [B label table] [# of B label] [target table]
Output:
    Tables of sources for specific labels on A and B.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20191202
####################################
update log
20191202 version alpha 1
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
    if len(argv) != 6:
        print ("The number of arguments is wrong.")
        print ("Usage: distribute_cm.py [A label table] [# of A label] [B label table] [# of B label] [target table]") 
        exit()
    A_label_table_name = argv[1]
    num_A = int(argv[2])
    B_label_table_name = argv[3]
    num_B = int(argv[4])
    target_table_name = argv[5]
    #-----------------------------------
    # Load data
    print ('Loading')
    A_label_table = np.loadtxt(A_label_table_name)
    A_cls = np.argmax(A_label_table[:, :num_A], axis = 1)
    B_label_table = np.loadtxt(B_label_table_name)
    B_cls = np.argmax(B_label_table[:, :num_B], axis = 1)
    target_table = np.loadtxt(target_table_name, dtype = str)
    # Pick sources
    for A_label in range(num_A):
        for B_label in range(num_B):
            print ("cm{0}{1}".format(A_label, B_label))
            index = np.where((A_cls == A_label) & (B_cls == B_label))
            selected_target_table = target_table[index]
            # Save data
            np.savetxt(
                '{0}_cm{1}{2}.txt'.format(target_table_name[:-4], A_label, B_label),
                selected_target_table,
                fmt = '%s',
            )
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
