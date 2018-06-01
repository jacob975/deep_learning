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
20180601 version alpha 2:
    1. add func to print reliable data out 
'''
import numpy as np
import time
from load_lib import confusion_matrix_infos, load_arrangement, load_labels_pred, load_cls_true 
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
        failure, data, tracer = load_arrangement(keyword, directory)
        if not failure:
            print ("load data and tracer success")
        # load label_pred
        failure, labels_pred = load_labels_pred(keyword, directory)
        if not failure:
            print ("load labels_pred success")
        # load cls_true
        failure, cls_true = load_cls_true(keyword, directory)
        if not failure:
            print ("load cls_true success")
        #-----------------------------------
        # print the properties of sources
        infos = confusion_matrix_infos(cls_true, labels_pred)
        print("### sources in dataset ### ")
        star_length = len(infos.cls_true[infos.cls_true == 0])
        print ("number of stars: {0}".format(star_length))
        galaxy_length = len(infos.cls_true[infos.cls_true == 1])
        print ("number of galaxies: {0}".format(galaxy_length))
        yso_length = len(infos.cls_true[infos.cls_true == 2])
        print ("number of ysos: {0}".format(yso_length))
        print("### reliable sources in dataset ### ")
        star_length = len(infos.cls_true_reliable[infos.cls_true_reliable == 0])
        print ("number of stars: {0}".format(star_length))
        galaxy_length = len(infos.cls_true_reliable[infos.cls_true_reliable == 1])
        print ("number of galaxies: {0}".format(galaxy_length))
        yso_length = len(infos.cls_true_reliable[infos.cls_true_reliable == 2])
        print ("number of ysos: {0}".format(yso_length))
        # print the properties of predictions
        failure, cm, cm_reliable = infos.confusion_matrix()
        print("confusion matrix:\n{0}".format(cm))
        print("reliable confusion matrix:\n{0}".format(cm_reliable))
        infos.print_accuracy()
        infos.print_precision()
        infos.print_recall_rate()
    #----------------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
