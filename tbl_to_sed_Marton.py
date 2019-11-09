#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in Marton 2019 et al. 
    to AI model readable format. 
Usage:
    tbl_to_sed_Marton.py [Marton table]
Output:
    1. Prediction of L machine (full bands)
    2. Prediction of S machine (except W3, W4 bands)
    3. The coordinate of sources.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20191022
####################################
update log
20191022 version alpha 1:
    1. The code works.
'''

import time
import numpy as np
from sys import argv
import sys
import convert_lib
np.set_printoptions(threshold=sys.maxsize)
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
        print ("tbl_to_sed_Marton.py [Marton table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    # coordinate
    coord = np.transpose(np.array([inp_table[:,1], inp_table[:,2]]))
    # Star, galaxy, YSO, and evolve star
    # 4 pred. then 4 errors
    L_pred = np.transpose(np.array([
                                    inp_table[:, 7], 
                                    inp_table[:, 5],
                                    inp_table[:, 9],
                                    inp_table[:, 3],
                                    inp_table[:, 8], 
                                    inp_table[:, 6],
                                    inp_table[:,10],
                                    inp_table[:, 4]
                                    ]))
    S_pred = np.transpose(np.array([
                                    inp_table[:,35], 
                                    inp_table[:,33],
                                    inp_table[:,37],
                                    inp_table[:,31],
                                    inp_table[:,36], 
                                    inp_table[:,34],
                                    inp_table[:,38],
                                    inp_table[:,32]
                                    ]))
    #-----------------------------------
    # Save the data
    print ('Save the data')
    np.savetxt( '{0}_Lpred.txt'.format(inp_table_name[:-4]), L_pred, fmt = '%s',
                header = '# star  galaxy  ysos    evolved e_s     e_g     e_y     e_e')
    np.savetxt( '{0}_Spred.txt'.format(inp_table_name[:-4]), S_pred, fmt = '%s',
                header = '# star  galaxy  ysos    evolved e_s     e_g     e_y     e_e')
    np.savetxt( '{0}_coord.txt'.format(inp_table_name[:-4]), coord, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
