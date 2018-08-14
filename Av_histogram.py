#!/usr/bin/python3
'''
Abstract:
    This is a program for ploting Av histogram 
Usage:
    Av_histogram.py
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
        print ("Usage: Av_histogram.py [Av table]")
    Av_table_name = argv[1]
    #-----------------------------------
    # Load table
    Av_table = np.loadtxt(Av_table_name)
    #-----------------------------------
    # plot
    Av_hist = np.histogram(Av_table[:,0], np.arange(-10, 50))
    Av_hist_plot = plt.figure("Av histogram")
    plt.title("Av histogram")
    plt.xlabel("Av")
    plt.ylabel("# of sources")
    plt.bar(np.arange(-9.5, 49.5, 1), Av_hist[0])
    Av_hist_plot.show()
    input()
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
