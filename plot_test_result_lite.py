#!/usr/bin/python3
'''
Abstract:
    This is a program to show the basic result of AI testing.
Usage:
    plot_test_result.py [keyword fo test set]
Example:
    plot_test_result.py MaxLoss15
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
from load_lib import confusion_matrix_infos_lite as confusion_matrix_infos
from sys import argv
from glob import glob
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
    if len(argv) != 3:
        print ("Error!\nUsage: plot_test_result.py [keyword for test set] [cls pred name]")
        exit()
    keyword = argv[1]
    cls_pred_name = argv[2]
    #----------------------------------------
    # Load data
    print (os.getcwd())
    #-----------------------------------
    # print the result of ensemble results
    ensemble_cls_pred = np.loadtxt(cls_pred_name, dtype = int)
    ensemble_cls_true = np.argmax(np.loadtxt("source_id_{0}.txt".format(keyword)), axis = 1)
    ensemble_data = np.loadtxt("source_sed_{0}.txt".format(keyword))
    ensemble_Q = np.loadtxt("source_Q_{0}.txt".format(keyword), dtype = str)
    ensemble_coord = np.loadtxt("source_coord_{0}.txt".format(keyword))
    infos = confusion_matrix_infos(ensemble_cls_true, ensemble_cls_pred)
    print ("\n#################################")
    print ("### Prediction of ensemble AI ###")
    print ("#################################")
    print ("### Sources in dataset ### ")
    star_length = len(infos.cls_true[infos.cls_true == 0])
    print ("number of stars: {0}".format(star_length))
    galaxy_length = len(infos.cls_true[infos.cls_true == 1])
    print ("number of galaxies: {0}".format(galaxy_length))
    yso_length = len(infos.cls_true[infos.cls_true == 2])
    print ("number of ysos: {0}".format(yso_length))
    # print the properties of predictions
    failure, cm = infos.confusion_matrix()
    print("confusion matrix:\n{0}".format(cm))
    infos.print_accuracy()
    infos.print_precision()
    infos.print_recall_rate()
    #----------------------------------------
    # plot and save the sed
    print("### Incorrectly predicted data ###")
    os.system('mkdir -p incorrect_sed_plots')
    incorrect_pred_source = ensemble_data[infos.cls_true != infos.cls_pred]
    incorrect_pred_cls_pred = infos.cls_pred[infos.cls_true != infos.cls_pred]
    incorrect_pred_cls_true = infos.cls_true[infos.cls_true != infos.cls_pred]
    incorrect_pred_Q = ensemble_Q[infos.cls_true != infos.cls_pred]
    incorrect_pred_coord = ensemble_coord[infos.cls_true != infos.cls_pred]
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_sed_{0}.txt".format(keyword), incorrect_pred_source)
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_cls_pred_{0}.txt".format(keyword), incorrect_pred_cls_pred, fmt='%d')
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_cls_true_{0}.txt".format(keyword), incorrect_pred_cls_true, fmt='%d')
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_Q_{0}.txt".format(keyword), incorrect_pred_Q, fmt = "%s")
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_coord_{0}.txt".format(keyword), incorrect_pred_coord)
    print("The number of incorrectly predicted source: {0}".format(len(incorrect_pred_source)))
    source_type = ['star', 'galaxy', 'YSOc']
    wavelength = [1.235, 1.662, 2.159, 3.550, 4.493, 5.731, 7.872, 24.00]
    for i, source in enumerate(incorrect_pred_source):
        fig, ax = plt.subplots(figsize = (8,6))
        #ax.set_aspect(0.4)
        ax.set_title("Actual: {0}, Predicted: {1}\nRA: {2:.4f}, DEC: {3:.4f}"\
                .format(source_type[incorrect_pred_cls_true[i]], 
                        source_type[incorrect_pred_cls_pred[i]],
                        incorrect_pred_coord[i,0],
                        incorrect_pred_coord[i,1]))
        textstr = "{0}".format(" ".join(incorrect_pred_Q[i]))
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        y = source[:8]
        yerr = source[8:]
        ax.errorbar(x = wavelength, y = y, yerr = yerr)
        ax.grid(True)
        ax.set_xlabel("wavelength($\mu$m)")
        ax.set_ylabel("flux(m$J_{y}$)")
        ax.set_yscale("log")
        ax.set_xscale('log')
        ax.text(0.50, 0.10, textstr, transform=ax.transAxes, fontsize = 14, verticalalignment='center', horizontalalignment = 'center', bbox=props) 
        ax.set_xticks(wavelength, minor = False)
        ax.set_xticklabels(wavelength)
        fig.savefig("incorrect_sed_plots/Source_{0:.4f}_{1:.4f}.png".format(incorrect_pred_coord[i,0], incorrect_pred_coord[i,1]))
    #----------------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
