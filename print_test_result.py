#!/usr/bin/python3
'''
Abstract:
    This is a program to show the basic result of AI testing.
Usage:
    print_test_result.py [keyword]
Example:
    print_test_result.py MaxLoss15
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180430
####################################
update log
20180430 version alpha 1:
    1. The code work 
'''
import numpy as np
import time
import load_lib
import collections
from load_lib import print_precision, print_recall_rate
from sys import argv
from glob import glob

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #----------------------------------------
    # initialize variables and constants
    data = None
    tracer = None
    cls_pred = None
    cls_true = None
    #----------------------------------------
    # load argv
    if len(argv) != 2:
        print ("Error!\nUsage: print_test_result.py [keyword]")
        exit()
    keyword = argv[1]
    #----------------------------------------
    data_list = glob("AI*test_on*")
    for directory in data_list:
        print ("#################################")
        print ("start to loading data saved in {0}".format(directory))
        # load tracer
        failure, data, tracer = load_lib.load_arrangement(keyword, directory)
        if not failure:
            print ("load data and tracer success")
        # load cls_pred
        failure, cls_pred = load_lib.load_cls_pred(keyword, directory)
        if not failure:
            print ("load cls_pred success")
        # load cls_true
        failure, cls_true = load_lib.load_cls_true(keyword, directory)
        if not failure:
            print ("load cls_true success")
        # confusion matrix
        print ("### confusion matrix ###")
        failure, cm = load_lib.confusion_matrix(cls_true, cls_pred)
        if not failure:
            print ("confusion matrix success")
        print (cm)
        #-----------------------------------
        # print the properties
        star_length = len(cls_true[cls_true == 0])
        print ("number of stars: {0}".format(len(cls_true[cls_true == 0])))
        gala_length = len(cls_true[cls_true == 1])
        print ("number of galaxies: {0}".format(len(cls_true[cls_true == 1])))
        yso_length = len(cls_true[cls_true == 2])
        print ("number of YSOs: {0}".format(len(cls_true[cls_true == 2])))
        # recall rate
        print_recall_rate(y_true = cls_true, y_pred = cls_pred)
        # precision
        print_precision(y_true = cls_true, y_pred = cls_pred)
    #----------------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
