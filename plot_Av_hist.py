#!/usr/bin/python3
'''
Abstract:
    This is a program for ploting Av histogram 
Usage:
    plot_Av_hist.py [Av table]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180814
####################################
update log
20180814 version alpha 1
    1. The code works
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
    if len(argv) != 2:
        print ("Wrong numbers of arguments.")
        print ("Usage: plot_Av_hist.py [Av table]")
        exit(1)
    Av_table_name = argv[1]
    #-----------------------------------
    # Load table
    Av_table = np.loadtxt(Av_table_name)
    #-----------------------------------
    # plot
    Av_hist = np.histogram(Av_table[:,0], np.arange(-10, 30))
    Av_hist_plot = plt.figure("Av histogram")
    plt.title("Av histogram of file '{0}'".format(Av_table_name))
    plt.xlabel("Av")
    plt.ylabel("# of sources")
    plt.bar(np.arange(-9.5, 29.5, 1), Av_hist[0])
    Av_hist_plot.savefig("{0}_hist.png".format(Av_table_name[:-4]))
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
