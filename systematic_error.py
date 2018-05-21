#!/usr/bin/python3
'''
Abstract:
    This is a program to plot the relation between two dataset with the same band.
    Currently, we focus on twomass and ukidss
Usage:
    systematic_error.py [twomass] [ukidss]
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
    if len(argv) != 3:
        print ("Error!\nUsage: systematic_error.py [two mass] [ukidss]")
        exit()
    # read argv
    name_twomass = argv[1]
    name_ukidss = argv[2]
    #-----------------------------------
    # load data
    twomass = np.load(name_twomass)
    ukidss = np.load(name_ukidss)
    for i in range(1110, 1120):
        print ("2mass: {0}; ukidss:{1}".format(twomass[i], ukidss[i]))
    #-----------------------------------
    # plot the intensities in 2mass versus difference of intensities in 2mass and ukidss.
    no_loss = np.where((ukidss[:,0] != 0) & (twomass[:,0] != 0) & (ukidss[:,0] < 200) & (twomass[:, 0] < 200))
    #no_loss = np.where((ukidss[:,0] != 0) & (twomass[:,0] != 0))
    err_diff = np.sqrt(np.power(ukidss[no_loss[0], 1], 2) + np.power(twomass[no_loss[0], 1], 2))
    result_plt = plt.figure("systematic error between {0} and {1}".format(argv[1], argv[2]))
    plt.title("{0} versus {1}".format(name_twomass, name_ukidss))
    plt.xlabel('2mass (mJy)')
    plt.ylabel('ukidss -2mass (mjy)')
    plt.errorbar(twomass[no_loss[0], 0], ukidss[no_loss[0], 0] -twomass[no_loss[0], 0] , yerr=[err_diff, 2*err_diff], \
                xerr=[twomass[no_loss[0], 1], 2*twomass[no_loss[0], 1]], fmt = 'ro')
    result_plt.savefig("syserr_{0}_{1}.png".format(name_twomass[:-4], name_ukidss[:-4]))
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
