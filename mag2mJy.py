#!/usr/bin/python3
'''
Abstract:
    This is a program for converting magnitude to flux. 
Usage:
    mag2mJy.py [band system] [source table]

    source table should be like:
    [[S1, S2, S3, ..., N1, N2, N3, ...  ],
     [S1, S2, S3, ...                   ], 
Output:
    1. print the settings.
    2. Save the fluxes table following the form as input table.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190529
####################################
update log
20180529 version alpha 1:
    1. The code works.
'''
import time
from sys import argv
import numpy as np
import convert_lib
from convert_JHK_from_twomass_to_ukidss import mag_to_mjy

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load arguments
    if len(argv) != 3:
        print ("The number of arugments is wrong.")
        print ("Usage: mJy2mag.py [band system] [source table]")
        print ("Available band system: wise, 2mass, ukirt")
        exit()
    band_system_name = argv[1]
    inp_table_name = argv[2]
    # Load band system
    band_system = None
    num_band = 0
    bands = None
    if band_system_name == "wise":
        band_system = convert_lib.set_wise()
        bands = ['W1', 'W2', 'W3', 'W4'] 
        num_band = 4
    elif band_system_name == "2mass":
        band_system = convert_lib.set_twomass() 
        bands = ['J', 'H', 'Ks'] 
        num_band = 3
    elif band_system_name == "ukirt":
        band_system = convert_lib.set_ukirt() 
        bands = ['J', 'H', 'K'] 
        num_band = 3
    else:
        print ("Please specify a valid band system.")
        exit()
    print ("band system:")
    print (band_system)
    # Load data
    inp_table = np.loadtxt(inp_table_name, dtype = object)
    inp_table[inp_table == 'null'] = '0.0'
    inp_table = np.array(inp_table, dtype = float)
    #-----------------------------------
    # Convert mag to mJy
    output_table = np.zeros(inp_table.shape)
    for i in range(num_band):
        combo_mag = np.transpose(np.array([inp_table[:,i], inp_table[:, i+num_band]])) 
        output = mag_to_mjy(combo_mag, bands[i], band_system)
        output_table[:, i] = output[:,0]
        output_table[:, i+num_band] = output[:,1]
    # Save the result
    np.savetxt("{0}_out.txt".format(inp_table_name[:-4]), output_table)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
