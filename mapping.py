#!/usr/bin/python3
'''
Abstract:
    This is a program for mapping the sources in Model II and Marton et al. via the Model IV results. 
Usage:
    mapping.py [Model II] [Model IV] [Marton]
Output:
    1. A list of index mapping Model II to Marton
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20191029
####################################
update log
20191029 version alpha 1
    1. The code works.
'''
import tensorflow as tf
import time
import numpy as np
from sys import argv

def find_index(array, keyword):
    ans = np.where(array == keyword)[0]
    if len(ans) == 0:
        return -1
    else:
        return ans[0]

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
        print ("Usage: mapping.py [Model II] [Model IV] [Marton]")
        exit()
    name_Model_II = argv[1]
    name_Model_IV = argv[2]
    name_Marton = argv[3]
    #-----------------------------------
    # Load the data
    print ('Loading...')
    Model_II = np.loadtxt(name_Model_II, dtype = int)
    Model_IV = np.loadtxt(name_Model_IV, dtype = int)
    Marton = np.loadtxt(name_Marton, dtype = int)
    # Mapping
    print ('Mapping...')
    Model_II_match_Model_IV = np.zeros(len(Model_II), dtype = int)
    num_Model_II = len(Model_II)
    for i, c in enumerate(Model_II):
        if i%1000 == 0:
            print ("({0}/{1})".format(i, num_Model_II))
        Model_II_match_Model_IV[i] = find_index(Model_IV, c)
    Model_II_match_Marton = Marton[Model_II_match_Model_IV]
    Model_II_match_Marton[Model_II_match_Model_IV == -1] = -1
    np.savetxt('test.txt', Model_II_match_Marton)    
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
