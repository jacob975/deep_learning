#!/usr/bin/python3
'''
Abstract:
    This is a program for plotting the color color diagram of given sources. 
Usage:
    cc_diag.py [Sp] [spitzer sed]
    Sp: source type
    spitzer sed: the SED of spitzer observation.
Output:
    1. The plot of color-color diagram 
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190623
####################################
update log
20190623 version alpha 1
    1. The code works.
'''
import time
import numpy as np
from sys import argv
import convert_lib
from convert_JHK_from_twomass_to_ukidss import mjy_to_mag
from matplotlib import pyplot as plt
#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: cc_diag.py [Sp] [spitzer sed]")
        exit()
    source_type_filename = argv[1]
    sed_filename = argv[2]
    #-----------------------------------
    # Load data
    spitzer_system = convert_lib.set_spitzer()
    source_type_array = np.loadtxt(source_type_filename)
    source_type = np.argmax(source_type_array, axis = 1)
    sed_array = np.loadtxt(sed_filename)
    IR3 = np.transpose(np.array([sed_array[:,5], sed_array[:,13]]))
    IR4 = np.transpose(np.array([sed_array[:,6], sed_array[:,14]]))
    MP1 = np.transpose(np.array([sed_array[:,7], sed_array[:,15]]))
    # Convert from flux to mag
    IR3mag = mjy_to_mag(IR3, 'IR3', spitzer_system)
    IR4mag = mjy_to_mag(IR4, 'IR4', spitzer_system)
    MP1mag = mjy_to_mag(MP1, 'MP1', spitzer_system)
    IR3_IR4 = IR3mag[:,0] - IR4mag[:,0]
    IR4_MP1 = IR4mag[:,0] - MP1mag[:,0]
    # Denote the source with source types
    index_star = np.where(source_type == 0)
    index_gala = np.where(source_type == 1)
    index_ysos = np.where(source_type == 2)
    # Plot the result
    plt.scatter(IR3_IR4[index_star],
                IR4_MP1[index_star], 
                color = 'gray',
                s = 2,
                label = 'star')
    plt.scatter(IR3_IR4[index_gala],
                IR4_MP1[index_gala], 
                color = 'b',
                s = 2,
                label = 'galaxy')
    plt.scatter(IR3_IR4[index_ysos],
                IR4_MP1[index_ysos], 
                color = 'g',
                s = 2,
                label = 'YSO')
    plt.xlabel('IR3 - IR4')
    plt.ylabel('IR4 - MP1')
    plt.legend()
    plt.savefig('cc_diag.png')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
