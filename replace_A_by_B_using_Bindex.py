#!/usr/bin/python3
'''
Abstract:
    This is a program for replacing the items in table A with items in table B using specified Bindex. 
Usage:
    replace_A_by_B_using_Bindex.py [table A] [table B] [table Bindex]
Output:
    1. The table A with replaced items.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190530
####################################
update log
20190530 version alpha 1
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
        print ("Usage: replace_A_by_B_using_Bindex.py [table A] [table B] [table Bindex]")
        print ("Assigning 'null' for table A, the program will generate a empty table A for process.")
        exit()
    table_A_name = argv[1]
    table_B_name = argv[2]
    Bindex_name = argv[3]
    #-----------------------------------
    # Load data
    table_B = np.loadtxt(table_B_name, dtype = object, delimiter = '|')
    Bindex = np.loadtxt(Bindex_name, dtype = int)
    if table_A_name == 'null':
        table_A_name = 'null.txt'
        table_A = np.zeros(len(Bindex), dtype = object)
    else:
        table_A = np.loadtxt(table_A_name, dtype = object, delimiter = '|')
    # Replace the items in table A with items in table B
    for i, index in enumerate(Bindex):
        if index == -1:
            continue
        else:
            table_A[i] = table_B[index]
    # Save the result
    np.savetxt("{0}_out.txt".format(table_A_name[:-4]), table_A, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
