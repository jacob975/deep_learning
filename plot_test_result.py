#!/usr/bin/python3
'''
Abstract:
    This is a program to show the basic result of AI testing.
Usage:
    plot_test_result.py [main_name of test set]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190306
####################################
update log
20190306 version alpha 1:
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
    # Initialize variables and constants
    data = None
    tracer = None
    cls_pred = None
    cls_true = None
    #----------------------------------------
    # Load argv
    if len(argv) != 2:
        print ("Error!\nUsage: plot_test_result.py [main_name for test set]")
        exit()
    main_name = argv[1]
    #----------------------------------------
    # Load data
    print("Loading ...")
    labels_pred = np.loadtxt("{0}_label_pred.txt".format(main_name))
    cls_pred    = np.argmax(labels_pred, axis = 1)
    cls_true    = np.loadtxt("{0}_cls_true.txt".format(main_name), dtype = int)
    data        = np.loadtxt("{0}_sed.txt".format(main_name))
    Q           = np.loadtxt("{0}_Q.txt".format(main_name), dtype = str)
    coord       = np.loadtxt("{0}_coord.txt".format(main_name))
    template    = np.loadtxt("{0}_template.txt".format(main_name))
    Sp          = np.loadtxt("{0}_Sp.txt".format(main_name), dtype = str)
    Av          = np.loadtxt("{0}_Av.txt".format(main_name), dtype = str)
    print("done")
    #----------------------------------------
    # ploting
    print ("ploting ... ")
    source_type = ['star', 'galaxy', 'YSOc']
    wavelength = [  1.235, 
                    1.662, 
                    2.159, 
                    3.550, 
                    4.493, 
                    5.731, 
                    7.872, 
                    24.00]
    for i, source in enumerate(data):
        fig, ax = plt.subplots(figsize = (8,6))
        #ax.set_aspect(0.4)
        ax.set_title("Actual: {0}, Predicted: {1}\nRA: {2:.4f}, DEC: {3:.4f}".format( 
                        source_type[cls_true[i]], 
                        source_type[cls_pred[i]], 
                        coord[i,0], 
                        coord[i,1]))
        textstr1 = "Quality label: {0}\nprobability: ({1:.3f}, {2:.3f}, {3:.3f})".format(
                        " ".join(Q[i]),
                        labels_pred[i,0],
                        labels_pred[i,1],
                        labels_pred[i,2])
        textstr2 = "{0} with Av={1}$\pm${2}".format(
                        Sp[i],
                        Av[i,0],
                        Av[i,1])
        props2 = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        props1 = dict(boxstyle='round', facecolor='cyan', alpha=0.5)
        y = source[:8]
        yerr = source[8:]
        ax.errorbar(x = wavelength, y = y, yerr = yerr, label = "SED")
        ax.plot(wavelength, template[i], 'k--', label = "best fit template")
        ax.grid(True)
        ax.set_xlabel("wavelength($\mu$m)")
        ax.set_ylabel("flux(m$J_{y}$)")
        ax.set_yscale("log")
        ax.set_xscale('log')
        ax.text(0.87, 0.1, 
                textstr1, 
                transform=ax.transAxes, 
                fontsize = 14, 
                verticalalignment='bottom', 
                horizontalalignment = 'right', 
                bbox=props1) 
        ax.text(0.87, 0.03, 
                textstr2, 
                transform=ax.transAxes, 
                fontsize = 14, 
                verticalalignment='bottom', 
                horizontalalignment = 'right', 
                bbox=props2) 
        ax.set_xticks(wavelength, minor = False)
        ax.set_xticklabels(wavelength)
        ax.legend(loc =1)
        fig.savefig("Source_{0:.4f}_{1:.4f}.png".format(
                        coord[i,0], 
                        coord[i,1]))
        if i%20 == 0:
            plt.close()
    #----------------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
