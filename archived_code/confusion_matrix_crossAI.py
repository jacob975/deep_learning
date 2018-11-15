#!/usr/bin/python3
'''
Abstract:
    This is a program to generate confusion matrix with predictions of two AIs. 
Usage:
    confusion_matrix_crossAI.py [keyword] [DIR where AI saved] [DIR where AI saved]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180521
####################################
update log
20180521 version alpha 1
    1. the code works
'''
import numpy as np
import time
import os
from sys import argv
from load_lib import confusion_matrix
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
figsize(12, 12)
#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # check argv
    if len(argv) != 4:
        print ("Error\nUsage: confusion_matrix_crossAI.py [keywords] [DIR where AI saved] [DIR where AI saved]")
        print ("Example: confusion_matrix_crossAI.py MaxLoss15 data_A/alice data_OPH/bob")
        exit()
    # load arguments
    keyword = argv[1]
    ai_alice = argv[2]
    ai_bob = argv[3]
    work_dir = os.getcwd()
    #-----------------------------------
    # load prediction 1
    print ("### Prediction 1 ###")
    print ("AI DIR = {0}".format(ai_alice))
    os.chdir(ai_alice)
    alice_sources = np.load("test_set_source_sed_{0}.npy".format(keyword))
    alice_cls_pred = np.load("test_cls_pred_source_sed_{0}.npy".format(keyword))
    alice_cls_tracers = np.load("test_tracer_source_sed_{0}.npy".format(keyword))
    alice_cls_true = np.load("test_cls_true_source_sed_{0}.npy".format(keyword))
    # trace it back to the sorted list with tracers
    alice_sources_sorted =  [ value for _,value in sorted(zip(alice_cls_tracers, alice_sources))]
    alice_cls_pred_sorted = [ value for _,value in sorted(zip(alice_cls_tracers, alice_cls_pred))]
    alice_cls_true_sorted = [ value for _,value in sorted(zip(alice_cls_tracers, alice_cls_true))]
    alice_sources_sorted = np.array(alice_sources_sorted)
    alice_cls_pred_sorted = np.array(alice_cls_pred_sorted)
    alice_cls_true_sorted = np.array(alice_cls_true_sorted)
    print ("--- Confusion Matrix ---")
    failure, cm = confusion_matrix(alice_cls_true_sorted, alice_cls_pred_sorted)
    print (cm)
    #-----------------------------------
    # load prediction 2
    print ("### Prediction 2 ###")
    print ("AI DIR = {0}".format(ai_bob))
    os.chdir(work_dir)
    os.chdir(ai_bob)
    bob_sources = np.load("test_set_source_sed_{0}.npy".format(keyword))
    bob_cls_pred = np.load("test_cls_pred_source_sed_{0}.npy".format(keyword))
    bob_cls_tracers = np.load("test_tracer_source_sed_{0}.npy".format(keyword))
    bob_cls_true = np.load("test_cls_true_source_sed_{0}.npy".format(keyword))
    # trace it back to the sorted list with tracers
    bob_sources_sorted =  [ value for _,value in sorted(zip(bob_cls_tracers, bob_sources))]
    bob_cls_pred_sorted = [ value for _,value in sorted(zip(bob_cls_tracers, bob_cls_pred))]
    bob_cls_true_sorted = [ value for _,value in sorted(zip(bob_cls_tracers, bob_cls_true))]
    bob_sources_sorted = np.array(bob_sources_sorted)
    bob_cls_pred_sorted = np.array(bob_cls_pred_sorted)
    bob_cls_true_sorted = np.array(bob_cls_true_sorted)
    print ("--- Confusion Matrix ---")
    failure, cm = confusion_matrix(bob_cls_true_sorted, bob_cls_pred_sorted)
    print (cm)
    #-----------------------------------
    # draw the confusion matrix with prediction 1 and 2
    print ("### Start to compare the predicions ###")
    print ("--- Cross Confusion Matrix ---")
    failure, cm = confusion_matrix(bob_cls_pred_sorted, alice_cls_pred_sorted)
    print (cm)
    # draw the confusion matrix of elements respectively
    alice_cls_pred_in_elements = [[None for j in range(3)] for i in range(3)]
    bob_cls_pred_in_elements = [[None for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            print ("--- true: {0} pred: {1} --- ".format(i, j))
            alice_cls_pred_in_elements[i][j] = alice_cls_pred_sorted[(alice_cls_true_sorted == i) & (alice_cls_pred_sorted == j )] 
            bob_cls_pred_in_elements[i][j] = bob_cls_pred_sorted[(alice_cls_true_sorted == i) & (alice_cls_pred_sorted == j )]
            if len(alice_cls_pred_in_elements[i][j]) == 0:
                print ("No data")
                continue
            failure, cm = confusion_matrix(bob_cls_pred_in_elements[i][j], alice_cls_pred_in_elements[i][j])
            print (cm)
    '''
    #-----------------------------------
    # print for test
    # This SED is printed as reference.
    yso_sed = alice_sources_sorted[(alice_cls_true_sorted == 2) & (alice_cls_pred_sorted == 2 ) & (bob_cls_pred_sorted == 2)]
    galaxy_sed = alice_sources_sorted[(alice_cls_true_sorted == 1) & (alice_cls_pred_sorted == 1 ) & (bob_cls_pred_sorted == 1)]
    target_sed = alice_sources_sorted[(alice_cls_true_sorted == 1) & (alice_cls_pred_sorted == 2 ) & (bob_cls_pred_sorted == 2)]
    fig, axes = plt.subplots(1, 3, sharex='row')
    axes[0].set_title("True: yso, pred A: yso, pred B: yso")
    print ("numbers of 222: {0}".format(len(yso_sed)))
    for sed in yso_sed:
        axes[0].errorbar(range(1,9), sed[:8], yerr = sed[8:], linestyle = "-", alpha = 0.5 )
    axes[1].set_title("True: gala, pred A: gala, pred B: gala")
    print ("numbers of 111: {0}".format(len(galaxy_sed)))
    for sed in galaxy_sed:
        axes[1].errorbar(range(1,9), sed[:8], yerr = sed[8:], linestyle = "-", alpha = 0.5 )
    axes[2].set_title("True: gala, pred A: yso, pred B: yso")
    print ("numbers of 122: {0}".format(len(target_sed)))
    for sed in target_sed:
        axes[2].errorbar(range(1,9), sed[:8], yerr = sed[8:], linestyle = "-", alpha = 0.5 )
    fig.savefig("test.png")
    #-----------------------------------
    fig2, axes2 = plt.subplots(1, 3, sharex='row')
    axes2[0].set_title("True: yso, pred A: yso, pred B: yso")
    print ("numbers of 222: {0}".format(len(yso_sed)))
    for sed in yso_sed:
        if sed[7] == 1.0:
            axes2[0].errorbar(range(1,9), sed[:8], yerr = sed[8:], linestyle = "-", alpha = 0.5 )
    axes2[1].set_title("True: gala, pred A: gala, pred B: gala")
    print ("numbers of 111: {0}".format(len(galaxy_sed)))
    for sed in galaxy_sed:
        if sed[7] == 1.0:
            axes2[1].errorbar(range(1,9), sed[:8], yerr = sed[8:], linestyle = "-", alpha = 0.5 )
    axes2[2].set_title("True: gala, pred A: yso, pred B: yso")
    print ("numbers of 122: {0}".format(len(target_sed)))
    for sed in target_sed:
        if sed[7] == 1.0:
            axes2[2].errorbar(range(1,9), sed[:8], yerr = sed[8:], linestyle = "-", alpha = 0.5 )
    fig.show()
    fig2.show()
    input()
    '''
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
