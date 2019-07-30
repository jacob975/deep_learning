#!/usr/bin/python3
'''
Abstract:
    This is a program for plotting the comparison of SED. 
Usage:
    compare_sed.py [2mass sed table] [ukidss sed table]
Output:
    1. The plot of J2flux vs. (JU-J2)flux   
    2. The plot of H2flux vs. (HU-H2)flux   
    3. The plot of K2flux vs. (KU-K2)flux   
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180104
####################################
update log
20190731 version alpha 1
    1. The code works.
'''
import time
import numpy as np
from sys import argv
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
        print ("Usage: compare_sed.py [2mass sed table] [ukidss sed table]")
        exit()
    twomass_sed_table_name = argv[1]
    ukidss_sed_table_name = argv[2]
    #-----------------------------------
    # Load data
    twomass_sed_table = np.loadtxt(twomass_sed_table_name)
    ukidss_sed_table = np.loadtxt(ukidss_sed_table_name)
    J_non_zero = np.where((twomass_sed_table[:,0] != 0) & (ukidss_sed_table[:,0] != 0) )
    H_non_zero = np.where((twomass_sed_table[:,1] != 0) & (ukidss_sed_table[:,1] != 0) )
    K_non_zero = np.where((twomass_sed_table[:,2] != 0) & (ukidss_sed_table[:,2] != 0) )
    # Plot the SED comparison 
    plt.figure()
    plt.scatter(twomass_sed_table[J_non_zero,0], 
                ukidss_sed_table[J_non_zero,0] - twomass_sed_table[J_non_zero,0])
    plt.xlim(0, 100)
    plt.ylim(10, -100)
    plt.show()
    
    
    plt.figure()
    plt.scatter(twomass_sed_table[H_non_zero,1], 
                ukidss_sed_table[H_non_zero,1] - twomass_sed_table[H_non_zero,1])
    plt.xlim(0, 100)
    plt.ylim(10, -100)
    plt.show()
    
    
    plt.figure()
    plt.scatter(twomass_sed_table[K_non_zero,2], 
                ukidss_sed_table[K_non_zero,2] - twomass_sed_table[K_non_zero,2])
    plt.xlim(0, 100)
    plt.ylim(10, -100)
    plt.show()
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
