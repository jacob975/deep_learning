#!/usr/bin/python3
'''
Abstract:
    This is a program to show the basic result of AI testing.
Usage:
    print_cm_reliable.py [label true] [label pred]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20191023 
####################################
update log
20191023 version alpha 1:
    1. The code works
'''
import numpy as np
import time
from load_lib import confusion_matrix_infos_reliable as confusion_matrix_infos
from sys import argv
import os
from input_lib import option_cm_reliable

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #----------------------------------------
    # Load argv
    stu = option_cm_reliable()
    if len(argv) != 4:
        print ("The number of arguements seems wrong.")
        print ("Usage: print_cm_reliable.py [option file] [label true table] [label pred table]")
        stu.create()
        exit()
    option_name = argv[1]
    num_true,\
    num_pred,\
    ll = stu.load(option_name)
    num_true = int(num_true)
    num_pred = int(num_pred)
    ll = float(ll)
    true_name = argv[2]
    pred_name = argv[3]
    print ("#------------ Start -------------")
    print ("true label: {0} with {1} labels".format(true_name, num_true))
    print ("pred label: {0} with {1} labels".format(pred_name, num_pred))
    print ("lower limit for the highest probability: {0}".format(ll))
    #-----------------------------------
    # Load data
    true = np.loadtxt(true_name)
    pred = np.loadtxt(pred_name)
    #-----------------------------------
    # Take probability only, no error included. 
    label_true = true[:,:num_true]
    label_pred = pred[:,:num_pred]
    # print the properties of sources
    infos = confusion_matrix_infos(label_true, label_pred, ll)
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
