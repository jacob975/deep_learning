#!/usr/bin/python3
'''
Abstract:
    This is a program to plot the relation between two dataset with the same band.
    Currently, we focus on twomass and ukidss
Usage:
    plot_compared_histograms.py [twomass] [ukidss]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180611
####################################
update log
20180611 version alpha 1
    1. the code works
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
        print ("Error!\nUsage: plot_compared_histograms.py [two mass] [ukidss]")
        print ("Example: plot_compared_histograms.py star_sed_j.txt ukidss_j_star.txt")
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
    no_loss_for_ukidss = np.where((ukidss[:,0] != 0) & (ukidss[:,0] < 50) )
    no_loss_for_twomass = np.where((twomass[:,0] != 0) & (twomass[:, 0] < 50))
    figsize(12.5, 5)
    result_plt = plt.figure("Histograms of {0} and {1}".format(name_twomass[:-4], name_ukidss[:-4]))
    plt.title("{0} and {1}".format(name_twomass[:-4], name_ukidss[:-4]))
    plt.ylabel('# of sources')
    plt.xlabel('$log_{10}(mjy)$')
    plt.hist(np.log10(twomass[no_loss_for_twomass[0], 0]), 50, range = (-3, 2), histtype = "bar", color = "r", alpha=0.50, label = "{0}".format(name_twomass[:-4]))
    plt.hist(np.log10(ukidss[no_loss_for_ukidss[0], 0]), 50, range = (-3, 2), histtype = "bar", color = "g", alpha=0.50, label = "{0}".format(name_ukidss[:-4]))
    plt.legend()
    result_plt.savefig("hist_{0}_and_{1}.png".format(name_twomass[:-4], name_ukidss[:-4]))
    # plot the same figure but normalized
    normed_result_plt = plt.figure("Normalized histograms of {0} and {1}".format(name_twomass[:-4], name_ukidss[:-4]))
    plt.title("{0} and {1}".format(name_twomass[:-4], name_ukidss[:-4]))
    plt.ylabel('normalized # of sources')
    plt.xlabel('$log_{10}(mjy)$')
    plt.hist(np.log10(twomass[no_loss_for_twomass[0], 0]), 50, range = (-3, 2), normed = True, histtype = "bar", color = "r", alpha=0.50, label = "{0}".format(name_twomass[:-4]))
    plt.hist(np.log10(ukidss[no_loss_for_ukidss[0], 0]), 50, range = (-3, 2), normed = True, histtype = "bar", color = "g", alpha=0.50, label = "{0}".format(name_ukidss[:-4]))
    plt.legend()
    normed_result_plt.savefig("hist_{0}_and_{1}_n.png".format(name_twomass[:-4], name_ukidss[:-4]))
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
