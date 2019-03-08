#!/usr/bin/python3
'''
Abstract:
    This is a program to show the basic result of AI testing.
Usage:
    find_incorrectly_predicted.py [keyword fo test set]
Example:
    find_incorrectly_predicted.py MaxLoss15
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
from load_lib import confusion_matrix_infos, load_arrangement, load_labels_pred, load_cls_true 
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
    if len(argv) != 2:
        print ("Error!\nUsage: find_incorrectly_predicted.py [keyword for test set]")
        exit()
    keyword = argv[1]
    #----------------------------------------
    # Load data
    print (os.getcwd())
    data_list = glob("AI*test_on*{0}".format(keyword))
    ensemble_cls_true = None
    ensemble_test_data = None
    labels_pred_set = []
    for directory in data_list:
        print ("#################################")
        print ("Load data saved in {0}".format(directory))
        # load tracer
        failure, data, tracer = load_arrangement(keyword, directory)
        if not failure:
            print ("Load data and tracer success")
            if ensemble_test_data == None:
                ensemble_test_data = [value for _,value in sorted(zip(tracer.test, data.test.images))]
        # load label_pred
        failure, labels_pred = load_labels_pred(keyword, directory)
        if not failure:
            print ("Load labels_pred success")
            temp_labels_pred =  [ value for _,value in sorted(zip(tracer.test, labels_pred))]
            labels_pred_set.append(temp_labels_pred)
        # load cls_true
        failure, cls_true = load_cls_true(keyword, directory)
        if not failure:
            print ("Load cls_true success")
            if ensemble_cls_true == None:
                ensemble_cls_true = [ value for _,value in sorted(zip(tracer.test, cls_true))]
    #-----------------------------------
    # print the result of ensemble results
    labels_pred_set = np.array(labels_pred_set)
    ensemble_labels_pred = np.mean(labels_pred_set, axis = 0)
    ensemble_cls_true = np.array(ensemble_cls_true, dtype = int)
    ensemble_test_data = np.array(ensemble_test_data)
    ensemble_Q = np.loadtxt("source_Q_{0}.txt".format(keyword), dtype = str)
    ensemble_coord = np.loadtxt("source_coord_{0}.txt".format(keyword))
    infos = confusion_matrix_infos(ensemble_cls_true, ensemble_labels_pred)
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
    # plot and save the sed
    print("### Incorrectly predicted data ###")
    os.system('mkdir -p incorrect_sed_plots')
    incorrect_pred_source = ensemble_test_data[infos.cls_true != infos.cls_pred]
    incorrect_pred_cls_pred = infos.cls_pred[infos.cls_true != infos.cls_pred]
    incorrect_pred_labels_pred = infos.labels_pred[infos.cls_true != infos.cls_pred]
    incorrect_pred_cls_true = infos.cls_true[infos.cls_true != infos.cls_pred]
    incorrect_pred_Q = ensemble_Q[infos.cls_true != infos.cls_pred]
    incorrect_pred_coord = ensemble_coord[infos.cls_true != infos.cls_pred]
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_sed_{0}.txt".format(keyword), incorrect_pred_source)
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_cls_pred_{0}.txt".format(keyword), incorrect_pred_cls_pred, fmt='%d')
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_labels_pred_{0}.txt".format(keyword), incorrect_pred_labels_pred)
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_cls_true_{0}.txt".format(keyword), incorrect_pred_cls_true, fmt='%d')
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_Q_{0}.txt".format(keyword), incorrect_pred_Q, fmt = "%s")
    np.savetxt("incorrect_sed_plots/incorrect_pred_source_coord_{0}.txt".format(keyword), incorrect_pred_coord)
    print("The number of incorrectly predicted source: {0}".format(len(incorrect_pred_source)))
    #----------------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
