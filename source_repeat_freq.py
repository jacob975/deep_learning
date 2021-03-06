#!/usr/bin/python3
'''
Abstract:
    This is a program to show the data with different true and prediction 
Usage:
    source_repeat_freq.py [keyword] [true label] [pred label]
Example:
    source_repeat_freq.py MaxLoss15 1 2
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180412
####################################
update log
20180412 version alpha 1:
    1. The code work 
20180509 version alpha 2:
    1. two kinds of histogram will be plot
        (1) serial number versus repeating times.
        (2) repeating times versus number of data.
'''
import numpy as np
import time
import load_lib
import collections
from sys import argv
from glob import glob
from IPython.core.pylabtools import figsize
import matplotlib.pyplot as plt


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
    collected_tracer_in_confusion_matrix = np.array([])
    true_ = pred_ = ["star", "gala", "yso"]
    #----------------------------------------
    # load argv
    if len(argv) != 4:
        print ("Error!\nUsage: source_repeat_freq.py [keyword] [true label] [pred label]")
        exit()
    keyword = argv[1]
    true_label = int(argv[2])
    pred_label = int(argv[3])
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
        star_length = len(cls_true[cls_true == 0])
        print ("number of stars: {0}".format(len(cls_true[cls_true == 0])))
        gala_length = len(cls_true[cls_true == 1])
        print ("number of galaxies: {0}".format(len(cls_true[cls_true == 1])))
        yso_length = len(cls_true[cls_true == 2])
        print ("number of YSOs: {0}".format(len(cls_true[cls_true == 2])))
        tracer_in_confusion_matrix = tracer.test[(cls_true == true_label) &(cls_pred == pred_label)]
        collected_tracer_in_confusion_matrix = np.append(collected_tracer_in_confusion_matrix, tracer_in_confusion_matrix)
        print ("number of gala to yso: {0}".format(len(tracer_in_confusion_matrix)))
        # save tracer_in_confusion_matrix
        np.savetxt("{0}/{1}_true_{2}_pred_{3}.txt".format(directory, keyword, true_[true_label], pred_[pred_label]), 
                tracer_in_confusion_matrix)
    # save collected_tracer_in_confusion_matrix
    np.savetxt("all_true_{0}_pred_{1}.txt".format(true_[true_label], pred_[pred_label]), collected_tracer_in_confusion_matrix)
    # plot serial number versus repeating times
    detected_occurance = collections.Counter(collected_tracer_in_confusion_matrix)
    figsize(12, 9)
    plt.subplot(211)
    plt.title("histogram of true: {0}, pred: {1}".format(true_[true_label], pred_[pred_label]))
    plt.bar(list(detected_occurance.keys()), list(detected_occurance.values()))
    plt.xlabel("serial numbers of objects")
    plt.ylabel("numbers of repeating times")
    # plot repeating times versus number of data.
    repeating_times = collections.Counter(list(detected_occurance.values()))
    plt.subplot(212)
    plt.title("historgram of repeating times")
    plt.bar(list(repeating_times.keys()), list(repeating_times.values()))
    plt.xlabel("repeating times")
    plt.ylabel("numbers of data")
    plt.savefig("histogram_true_{0}_pred_{1}.png".format(true_[true_label], pred_[pred_label]))
    #----------------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
