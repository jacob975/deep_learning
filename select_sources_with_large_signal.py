#!/usr/bin/python3
'''
Abstract:
    This is a program to plot the relation between two dataset with the same band.
    Currently, we focus on twomass and ukidss
Usage:
    select_sources_with_large_signal.py [two mass] [ukidss] [coords]
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
        print ("Error!\nUsage: select_sources_with_large_signal.py [two mass] [ukidss] [coords]")
        exit()
    # read argv
    name_twomass = argv[1]
    name_ukidss = argv[2]
    name_coords = argv[3]
    #-----------------------------------
    # load data
    twomass = np.load(name_twomass)
    ukidss = np.load(name_ukidss)
    coords = np.load(name_coords)
    coords_w_fulldata = np.hstack((coords, twomass, ukidss))
    #-----------------------------------
    # plot the intensities in 2mass versus difference of intensities in 2mass and ukidss.
    large_signal = np.where((ukidss[:,0] != 0) & (twomass[:,0] < 1000) & (twomass[:, 0] > 200))
    err_diff = np.sqrt(np.power(ukidss[large_signal[0], 1], 2) + np.power(twomass[large_signal[0], 1], 2)) 
    result_plt = plt.figure("systematic error between {0} and {1}".format(argv[1], argv[2]))
    plt.title("{0} versus {1}".format(name_twomass, name_ukidss))
    plt.xlabel('2mass (mJy)')
    plt.ylabel('ukidss -2mass (mjy)')
    plt.errorbar(twomass[large_signal[0], 0], ukidss[large_signal[0], 0] -twomass[large_signal[0], 0] , yerr=[err_diff, 2*err_diff], \
                xerr=[twomass[large_signal[0], 1], 2*twomass[large_signal[0], 1]], fmt = 'ro')
    result_plt.savefig("sources_with_large_signals_{0}_{1}.png".format(name_twomass[:-4], name_ukidss[:-4]))
    np.save("{0}_sources_with_large_signal.npy".format(name_twomass[:-4]), coords_w_fulldata[large_signal])
    np.savetxt("{0}_sources_with_large_signals.txt".format(name_twomass[:-4]), coords_w_fulldata[large_signal])
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
