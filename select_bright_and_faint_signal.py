#!/usr/bin/python3
'''
Abstract:
    This is a program to plot the relation between two dataset with the same band.
    Currently, we focus on twomass and ukidss
Usage:
    select_bright_and_faint_signal.py [two mass] [ukidss] [coords]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180517
####################################
update log
20180517 version alpha 1
    1. the code looks good.
'''
import time
import numpy as np
from sys import argv
import matplotlib.pyplot as plt

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------
    # check argv is right
    if len(argv) != 4:
        print ("Error!\nUsage: select_bright_and_faint_signal.py [two mass] [ukidss] [coords]")
        exit()
    # read argv
    name_twomass = argv[1]
    name_ukidss = argv[2]
    name_coords = argv[3]
    #-----------------------------------
    # load data
    twomass = np.loadtxt(name_twomass)
    ukidss = np.loadtxt(name_ukidss)
    coords = np.loadtxt(name_coords)
    coords_w_fulldata = np.hstack((coords, twomass, ukidss))
    #-----------------------------------
    # pick coordinate of bright signals and faint signals
    # then plot the flux in 2mass versus difference of intensities in 2mass and ukidss.
    # save infos of bright signals
    # include flux and coords
    bright_signals = np.where((ukidss[:,0] != 0) & (twomass[:,0] < 1000) & (twomass[:, 0] > 200))
    err_diff = np.sqrt(np.power(ukidss[bright_signals[0], 1], 2) + np.power(twomass[bright_signals[0], 1], 2)) 
    result_plt = plt.figure("systematic error of bright signals between {0} and {1}".format(argv[1], argv[2]))
    plt.title("{0} versus {1}".format(name_twomass, name_ukidss))
    plt.xlabel('2mass (mJy)')
    plt.ylabel('ukidss -2mass (mjy)')
    plt.errorbar(twomass[bright_signals[0], 0], ukidss[bright_signals[0], 0] -twomass[bright_signals[0], 0] , yerr=[err_diff, 2*err_diff], \
                xerr=[twomass[bright_signals[0], 1], 2*twomass[bright_signals[0], 1]], fmt = 'ro')
    result_plt.savefig("sources_with_bright_signals_{0}_{1}.png".format(name_twomass[:-4], name_ukidss[:-4]))
    np.savetxt("{0}_sources_with_bright_signals.txt".format(name_twomass[:-4]), coords_w_fulldata[bright_signals])
    # save infos of faint signals
    # include flux and coords
    faint_signals = np.where((ukidss[:,0] != 0) & (twomass[:,0] != 0) & (twomass[:,0] < 30))
    err_diff = np.sqrt(np.power(ukidss[faint_signals[0], 1], 2) + np.power(twomass[faint_signals[0], 1], 2)) 
    result_plt = plt.figure("systematic error of faint signals between {0} and {1}".format(argv[1], argv[2]))
    plt.title("{0} versus {1}".format(name_twomass, name_ukidss))
    plt.xlabel('2mass (mJy)')
    plt.ylabel('ukidss -2mass (mjy)')
    plt.errorbar(twomass[faint_signals[0], 0], ukidss[faint_signals[0], 0] -twomass[faint_signals[0], 0] , yerr=[err_diff, 2*err_diff], \
                xerr=[twomass[faint_signals[0], 1], 2*twomass[faint_signals[0], 1]], fmt = 'ro')
    result_plt.savefig("sources_with_faint_signals_{0}_{1}.png".format(name_twomass[:-4], name_ukidss[:-4]))
    np.savetxt("{0}_sources_with_faint_signals.txt".format(name_twomass[:-4]), coords_w_fulldata[faint_signals])
    
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
