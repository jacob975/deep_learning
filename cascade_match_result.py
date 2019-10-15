#!/usr/bin/python3
'''
Abstract:
    This is a program for cascading the result from match_catalog.py
Usage:
    cascade_match_result.py [master] [slave] [margin of index]
Example:
    cascade_match_result.py split_Marton00_match_sources.txt split_Marton01_match_sources.txt 1000000
Output:
    1. The new master will replace the old one.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20191015
####################################
update log
20191015 version alpha 1
    1. The code works.
'''
import time
import numpy as np
from sys import argv

def pick_near_one(pred_1, pred_2):
    if pred_1[6] < pred_2[6]:
        return pred_1
    else:
        return pred_2

def cascade_pred(pred_1, pred_2):
    if (pred_1[3] == -1) and (pred_2[3] == -1):
        return pred_1
    elif (pred_1[3] == -1) and (pred_2[3] != -1):
        return pred_2
    elif (pred_1[3] != -1) and (pred_2[3] == -1):
        return pred_1
    elif (pred_1[3] != -1) and (pred_2[3] != -1):
        print (pred_1, pred_2)
        near_pred = pick_near_one(pred_1, pred_2)
        return near_pred

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
        print ("Usage: cascade_match_result.py [master] [slave] [margin of index]")
        exit()
    master_name = argv[1]
    slave_name  = argv[2]
    margin = int(argv[3])
    #-----------------------------------
    # Load data
    print ("Loading data...")
    master_pred_array = np.loadtxt(master_name)
    slave_pred_array  = np.loadtxt(slave_name)
    index_slave_match = np.where(slave_pred_array[:,3] != -1)[0]
    slave_pred_array[index_slave_match,3] += margin
    #-----------------------------------
    # Match master and slave
    print ("Match predictions") 
    ans_pred_array = np.zeros(master_pred_array.shape)
    num_source = len(master_pred_array)
    for i in range(num_source):
        if i%1000 == 0:
            elapsed_time = time.time() - start_time
            print ("({0}/{1}) time: {2}".format(i, num_source, elapsed_time))
        ans_pred = cascade_pred(master_pred_array[i],
                                slave_pred_array[i])
        ans_pred_array[i] = ans_pred
    #-----------------------------------
    # Make a backup for master array and Save the result
    print ("Saving the result")
    np.savetxt(master_name, ans_pred_array)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
