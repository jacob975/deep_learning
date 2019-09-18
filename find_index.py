#!/usr/bin/python3
'''
Abstract:
    This is a program for find the index of each label in label predicted files. 
Usage:
    find_index.py [label_pred.txt]
Output:
    1. cls_pred files 
    2. star index 
    3. gala index 
    4. ysos index 
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190906
####################################
update log
'''
import tensorflow as tf
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
        print ("Usage: find_index.py [label_pred.txt]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    inp_table = np.loadtxt(inp_table_name)
    cls_pred = np.argmax(inp_table, axis = 1)
    star_index = np.where(cls_pred == 0)
    gala_index = np.where(cls_pred == 1)
    ysos_index = np.where(cls_pred == 2)
    np.savetxt('student_cls_pred.txt', cls_pred, fmt = '%d')
    np.savetxt('star_index.txt', star_index, fmt = '%d')
    np.savetxt('gala_index.txt', gala_index, fmt = '%d')
    np.savetxt('ysos_index.txt', ysos_index, fmt = '%d')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
