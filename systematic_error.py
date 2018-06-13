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
20180602 version alpha 2
    1. add a func to wipe out non-sense data
'''
import time
import numpy as np
from sys import argv
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize

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
        print ("Example: systematic_error.py sed_star_j.txt ukidss_j_star.txt")
        exit()
    # read argv
    name_twomass = argv[1]
    name_ukidss = argv[2]
    #-----------------------------------
    # load data
    twomass = np.loadtxt(name_twomass, dtype = np.float64)
    ukidss = np.loadtxt(name_ukidss, dtype = np.float64)
    # wipe out non-sense data
    twomass_too_high = np.where(twomass > 1E308)
    twomass[twomass_too_high] = 0.0
    twomass_too_low = np.where(twomass <= -999)
    twomass[twomass_too_low] = 0.0
    ukidss_too_high = np.where(ukidss > 1E308)
    ukidss[ukidss_too_high] = 0.0
    ukidss_too_low = np.where(ukidss <= -999)
    ukidss[ukidss_too_low] = 0.0
    # print 10 data point as examples
    try:
        for i in range(1110, 1120):
            print ("2mass: {0}; ukidss:{1}".format(twomass[i], ukidss[i]))
    except:
        pass
    #-----------------------------------
    # plot the intensities in 2mass versus difference of intensities in 2mass and ukidss.
    no_loss = np.where((ukidss[:,0] != 0) & (twomass[:,0] != 0) & (ukidss[:,0] < 50) & (twomass[:, 0] < 50))
    #no_loss = np.where((ukidss[:,0] != 0) & (twomass[:,0] != 0))
    err_diff = np.sqrt(np.power(ukidss[no_loss[0], 1], 2) + np.power(twomass[no_loss[0], 1], 2))
    figsize(12.5, 5)
    result_plt = plt.figure("systematic error between {0} and {1}".format(argv[1], argv[2]))
    plt.title("{0} versus {1}".format(name_twomass, name_ukidss))
    plt.xlabel('2mass (mJy)')
    plt.ylabel('ukidss -2mass (mjy)')
    axes = plt.gca()
    axes.set_ylim([-20,5])
    plt.errorbar(twomass[no_loss[0], 0], ukidss[no_loss[0], 0] -twomass[no_loss[0], 0] , yerr=[err_diff, err_diff], \
                xerr=[twomass[no_loss[0], 1], twomass[no_loss[0], 1]], alpha = 0.1, fmt = 'ro')
    plt.plot((-5, 55), (0, 0), linestyle='--')
    result_plt.savefig("syserr_{0}_{1}.png".format(name_twomass[:-4], name_ukidss[:-4]))
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
