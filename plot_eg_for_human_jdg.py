#!/usr/bin/python3
'''
Abstract:
    This is a program to show the SED of human judgement examples.
Usage:
    plot_eg_for_human_jdg.py [main_name of test set]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200221
####################################
update log
20200221 version alpha 1:
    1. The code works.
'''
import numpy as np
import time
from sys import argv
import os
from matplotlib import pyplot as plt

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #----------------------------------------
    # Load argv
    if len(argv) != 2:
        print ("Error!\nUsage: plot_test_result.py [main_name for test set]")
        exit()
    main_name = argv[1]
    #----------------------------------------
    # Load data
    print("Loading ...")
    data        = np.loadtxt("{0}_sed.txt".format(main_name))
    coord       = np.loadtxt("{0}_coord.txt".format(main_name))
    print("done")
    #----------------------------------------
    # Ploting
    print ("ploting ... ")
    source_type = ['galaxy', 'star', 'YSO']
    wavelength = [  1.235, 
                    1.662, 
                    2.159, 
                    3.550, 
                    4.493, 
                    5.731, 
                    7.872, 
                    24.00]
    # Initialize the figure space
    fig, ax = plt.subplots(figsize = (8,6))
    ax.set_xlabel("Wavelength ($\mu$m)", fontsize=16)
    ax.set_ylabel("Flux (m$J_{y}$)", fontsize=16)
    ax.set_yscale("log")
    ax.set_xscale('log')
    ax.set_xticks(wavelength, minor = False)
    ax.set_xticklabels(wavelength)
    ax.grid(True)
    # Plot the sources
    for i, source in enumerate(data):
        y = source[:8]
        yerr = source[8:]
        ax.errorbar(
            x = wavelength, 
            y = y, 
            yerr = yerr, 
            label = r"%s at (%.7f, %.7f)" % (source_type[i], coord[i][0], coord[i][1]),
            fmt='--o',
            capsize=8,
        )
    ax.legend()
    fig.savefig( "SEDs.png".format(coord[i,0], coord[i,1]))
    #----------------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
