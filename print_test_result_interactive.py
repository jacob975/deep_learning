#!/usr/bin/python3
'''
Abstract:
    This is a program to show the basic result of AI testing.
Usage:
    print_test_result_lite.py [cls true table] [cls pred table]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190307 
####################################
update log
20190307 version alpha 1:
    1. The code works
'''
import numpy as np
import time
from load_lib import confusion_matrix_infos_lite as confusion_matrix_infos
from sys import argv
import os

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #----------------------------------------
    # Initialize variables and constants
    cls_pred = None
    cls_true = None
    #----------------------------------------
    # Load argv
    if len(argv) != 3:
        print ("Error!\nUsage: print_test_result.py [cls true table] [cls pred table]")
        exit()
    cls_true_name = argv[1]
    cls_pred_name = argv[2]
    cls_true = np.loadtxt(cls_true_name)
    cls_true = np.argmax(cls_true, axis=1)
    cls_pred = np.loadtxt(cls_pred_name, dtype = int)
    #-----------------------------------
    # print the properties of sources
    infos = confusion_matrix_infos(cls_true, cls_pred)
    print("### sources in dataset ### ")
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
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
