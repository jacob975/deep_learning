#!/usr/bin/python3
'''
Abstract:
    This is a program for ploting 
Usage:
    plot_signal_noise_ratio.py [sed data]
    
    The input sed data should arranged like that:
    [ S1, S2, S3, ..., N1, N2, N3, ...], 
    [ S1, S2, S3, ..., N1, N2, N3, ...],
    ...


Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181023
####################################
update log
20181023 version alpha 1
    1. The code works
20181119 version alpha 2
    1. Allow you to upload two datalog for comparison
'''
import time
import numpy as np
import matplotlib.pyplot as plt
from sys import argv

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) < 2 or len(argv) > 3 :
        print ("The numbers of arguments is wrong.")
        print ("Usage: plot_signal_noise_ratio.py [sed data]")
        exit(1)
    sed_name = argv[1]
    # This program allow you compare SNR.
    if len(argv) == 3:
        sed_name_2 = argv[2]
    #-----------------------------------
    # Load table
    sed_table = np.loadtxt(sed_name)
    sed_table_2 = None
    if len(argv) == 3:
        sed_table_2 = np.loadtxt(sed_name_2)
    band_name = ['J', 'H', 'K', 'IRAC1', 'IRAC2', 'IRAC3', 'IRAC4', 'MIPS1']
    #-----------------------------------
    # Plot the ratio
    ratio = [0, 0, 0, 0.047, 0.047, 0.047, 0.047, 0.095]
    fig, axs = plt.subplots(3, 3, figsize = (12, 12), sharex = 'all', sharey = 'all')
    plt.suptitle("SNR_{0}".format(sed_name[:4]), fontsize=28)
    axs = axs.ravel()
    for i in range(len(sed_table[0])//2):
        axs[i].set_title(band_name[i])
        axs[i].set_ylabel('uncertainties(mJy)')
        axs[i].set_xlabel('flux(mJy)')
        axs[i].grid(True)
        axs[i].set_yscale("log", nonposx='clip')
        axs[i].set_xscale('log', nonposy='clip')
        axs[i].set_ylim(ymin = 1e-3, ymax = 1e4)
        axs[i].set_xlim(xmin = 1e-3, xmax = 1e4)
        axs[i].plot([3e-3, 3e3], [1e-3, 1e3], 'k--', alpha = 0.5)
        axs[i].scatter(sed_table[:,i], sed_table[:,i+8], s = 5, c = 'r' )
        if len(argv) ==3:
            axs[i].scatter(sed_table_2[:,i], sed_table_2[:,i+8], s = 5, c = 'b' )
        if ratio[i] != 0:
            axs[i].plot([0.01, 2000], [0.01*ratio[i], 2000*ratio[i]], 'r-', label = r'$\frac{N}{S}$ = %.4f' % ratio[i])
        axs[i].legend()
    plt.savefig('{0}_signal_noise_relation.png'.format(sed_name[:4]))
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
