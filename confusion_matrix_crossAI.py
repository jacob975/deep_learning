#!/usr/bin/python3
'''
Abstract:
    This is a program to plot confusion matrix with predictions of two different AIs. 
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

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # check argv
    if len(argv) != 4:
        print ("Error\nUsage: confusion_matrix_crossAI.py [DIR where AI saved] [DIR where AI saved]")
        print ("Example: confusion_matrix_crossAI.py MaxLoss15 data_A/alice data_OPH/bob")
        exit()
    # load arguments
    keyword = argv[1]
    ai_alice = argv[2]
    ai_bob = argv[3]
    work_dir = os.getcwd()
    #-----------------------------------
    # load prediction 1
    print ("### prediction 1 ###")
    print ("AI DIR = {0}".format(ai_alice))
    os.chdir(ai_alice)
    alice_sources = np.load("test_set_source_sed_{0}.npy".format(keyword))
    alice_cls_pred = np.load("test_cls_pred_source_sed_{0}.npy".format(keyword))
    alice_cls_tracers = np.load("test_tracer_source_sed_{0}.npy".format(keyword))
    # trace it back to the sorted list with tracers
    alice_cls_pred_sorted = [ value for _,value in sorted(zip(alice_cls_tracers, alice_cls_pred))]
    #-----------------------------------
    # load prediction 2
    print ("### prediction 2 ###")
    print ("AI DIR = {0}".format(ai_bob))
    os.chdir(work_dir)
    os.chdir(ai_bob)
    bob_sources = np.load("test_set_source_sed_{0}.npy".format(keyword))
    bob_cls_pred = np.load("test_cls_pred_source_sed_{0}.npy".format(keyword))
    bob_cls_tracers = np.load("test_tracer_source_sed_{0}.npy".format(keyword))
    # trace it back to the sorted list with tracers
    bob_cls_pred_sorted = [ value for _,value in sorted(zip(bob_cls_tracers, bob_cls_pred))]
    #-----------------------------------
    # draw the confusion matrix with prediction 1 and 2
    failure, cm = confusion_matrix(alice_cls_pred_sorted, bob_cls_pred_sorted)
    print (cm)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
