#!/usr/bin/python3
'''
Abstract:
    This is a program to show the data with different true and prediction 
Usage:
    plot_loss_freq.py [main_name] [no-observation value ] [true label] [pred label]
Example:
    plot_loss_freq.py MaxLoss15 '0.0' 1 2
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
20180509 version alpha 2:
    1. Make the length is constant 16
'''
import numpy as np
import time
import load_lib
import collections
from sys import argv
from glob import glob
import matplotlib.pyplot as plt


def get_loss_freq(data, tracer, collected_tracer_in_confusion_matrix, no_obs):
    # initialize the variables
    loss_pos_collector = np.array([])
    # find out all loss
    for key in collected_tracer_in_confusion_matrix:
        selected_data = data[np.where(tracer == key)]
        loss_pos = np.where(selected_data[0] == no_obs)
        loss_pos_collector = np.append(loss_pos_collector, loss_pos)
    loss_pos_collector += 1
    loss_freq = collections.Counter(loss_pos_collector)
    # normalized by the number of data
    loss_freq = {k: v / len(collected_tracer_in_confusion_matrix) for k, v in loss_freq.items()}
    return loss_freq

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
    collected_sed_in_confusion_matrix = np.array([])
    normed_by_band = None
    true_ = pred_ = ["star", "gala", "yso"]
    #----------------------------------------
    # load argv
    if len(argv) != 5:
        print ("Error!\nUsage: plot_sed.py [main_name] [ no-observation value ] [true label] [pred label]")
        print ("Example: plot_loss_freq.py MaxLoss15 '0.0' 1 2")
        exit()
    main_name = argv[1]
    no_obs = float(argv[2])
    true_label = int(argv[3])
    pred_label = int(argv[4])
    #----------------------------------------
    data_list = glob("AI*test_on*")
    for directory in data_list:
        print ("#################################")
        print ("start to loading data saved in {0}".format(directory))
        # load tracer
        failure, data, tracer = load_lib.load_arrangement(main_name, directory)
        if not failure:
            print ("load data and tracer success")
        # load cls_pred
        failure, cls_pred = load_lib.load_cls_pred(main_name, directory)
        if not failure:
            print ("load cls_pred success")
        # load cls_true
        failure, cls_true = load_lib.load_cls_true(main_name, directory)
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
        np.savetxt("{0}/{1}_tracer_true_{2}_pred_{3}.txt".format(directory, main_name, true_[true_label], pred_[pred_label]), 
                tracer_in_confusion_matrix)
    # save collected_tracer_in_confusion_matrix
    np.savetxt("all_tracer_true_{0}_pred_{1}.txt".format(true_[true_label], pred_[pred_label]), collected_tracer_in_confusion_matrix)
    # calculate the loss freq
    loss_freq = get_loss_freq(data.test.images, tracer.test, collected_tracer_in_confusion_matrix, no_obs)
    print("\n### loss freq ###")
    for k, v in loss_freq.items():
        print ("{0}: {1}".format(k, v))
    # plot the loss freq
    result_plt = plt.figure("loss freq of true: {0}, pred: {1}, {2} data".format(true_[true_label], pred_[pred_label], len(collected_tracer_in_confusion_matrix)))
    plt.title("loss freq of true: {0}, pred: {1}, {2} data".format(true_[true_label], pred_[pred_label], len(collected_tracer_in_confusion_matrix)))
    plt.xlabel("signal/error")
    plt.ylabel("probability")
    plt.bar(list(loss_freq.keys()), list(loss_freq.values()), align='center')
    plt.xlim(0, 17)
    result_plt.savefig("loss_freq_of_true_{0}_pred_{1}_{2}_data.png".format(true_[true_label], pred_[pred_label], len(collected_tracer_in_confusion_matrix)))
    #----------------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("\nExiting Main Program, spending ", elapsed_time, "seconds.")
