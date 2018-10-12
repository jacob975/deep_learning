#!/usr/bin/python3
'''
Abstract:
    This is a program to generate confusion matrix with predictions of two AIs. 
Usage:
    print_crossAI.py [keyword] [DIR where AI saved] [DIR where AI saved]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180917
####################################
update log
20180917 version alpha 1
    1. the code works
'''
import numpy as np
import time
import os
from sys import argv
from load_lib import load_cls_true, load_labels_pred, load_arrangement, confusion_matrix_infos, cross_confusion_matrix_infos
import glob
#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Check argv
    if len(argv) != 4:
        print ("Error\nUsage: crossAI.py [keywords] [DIR where AI saved] [DIR where AI saved]")
        print ("Example: print_crossAI.py MaxLoss15 data_A/alice data_OPH/bob")
        exit()
    # Load arguments
    keyword = argv[1]
    ai_alice = argv[2]
    ai_bob = argv[3]
    work_dir = os.getcwd()
    #----------------------------------------
    # Load prediction 1 and true labels
    print ("### Prediction 1 ###")
    print ("AI DIR = {0}".format(ai_alice))
    os.chdir(ai_alice)
    data_list = glob.glob("AI*test_on*{0}".format(keyword))
    ensemble_cls_true = None
    alice_labels_pred_set = []
    for directory in data_list:
        # load tracer
        failure, data, tracer = load_arrangement(keyword, directory)
        # load label_pred
        failure, labels_pred = load_labels_pred(keyword, directory)
        if not failure:
            temp_labels_pred =  [ value for _,value in sorted(zip(tracer.test, labels_pred))]
            alice_labels_pred_set.append(temp_labels_pred)
        # load cls_true
        failure, cls_true = load_cls_true(keyword, directory)
        if not failure:
            if ensemble_cls_true == None:
                ensemble_cls_true = [ value for _,value in sorted(zip(tracer.test, cls_true))]
    
    alice_labels_pred_set = np.array(alice_labels_pred_set)
    alice_ensemble_labels_pred = np.mean(alice_labels_pred_set, axis = 0)
    ensemble_cls_true = np.array(ensemble_cls_true)
    print ("--- Confusion Matrix ---")
    alice_infos = confusion_matrix_infos(ensemble_cls_true, alice_ensemble_labels_pred)
    failure, cm, cm_reliable = alice_infos.confusion_matrix()
    print("confusion matrix:\n{0}".format(cm))
    os.chdir('..')
    #----------------------------------------
    # Load prediction 2
    print ("### Prediction 2 ###")
    print ("AI DIR = {0}".format(ai_bob))
    os.chdir(ai_bob)
    data_list = glob.glob("AI*test_on*{0}".format(keyword))
    bob_labels_pred_set = []
    for directory in data_list:
        # load tracer
        failure, data, tracer = load_arrangement(keyword, directory)
        # load label_pred
        failure, labels_pred = load_labels_pred(keyword, directory)
        if not failure:
            temp_labels_pred =  [ value for _,value in sorted(zip(tracer.test, labels_pred))]
            bob_labels_pred_set.append(temp_labels_pred)
    bob_labels_pred_set = np.array(bob_labels_pred_set)
    bob_ensemble_labels_pred = np.mean(bob_labels_pred_set, axis = 0)
    print ("--- Confusion Matrix ---")
    bob_infos = confusion_matrix_infos(ensemble_cls_true, bob_ensemble_labels_pred)
    failure, cm, cm_reliable = bob_infos.confusion_matrix()
    print("confusion matrix:\n{0}".format(cm))
    #-----------------------------------------
    # Draw the confusion matrix with prediction 1 and 2
    print ("### Start to compare the predicions ###")
    print ("--- Cross Confusion Matrix ---")
    cross_infos = cross_confusion_matrix_infos(bob_ensemble_labels_pred, alice_ensemble_labels_pred)
    failure, cm, cm_reliable = cross_infos.confusion_matrix()
    print("confusion matrix:\n{0}".format(cm))
    # Draw the confusion matrix of elements respectively
    alice_cls_pred_in_elements = [None for i in range(3)]
    bob_cls_pred_in_elements = [None for i in range(3)]
    label_name_list = ['Star', 'Galaxy', 'YSOc']
    for i in range(3):
        print ("--- True: {0} --- ".format(label_name_list[i]))
        alice_cls_pred_in_elements[i] = alice_ensemble_labels_pred[ensemble_cls_true == i] 
        bob_cls_pred_in_elements[i] = bob_ensemble_labels_pred[ensemble_cls_true == i]
        if len(alice_cls_pred_in_elements[i]) == 0:
            print ("No data")
            continue
        temp_cross_infos = cross_confusion_matrix_infos(bob_cls_pred_in_elements[i], alice_cls_pred_in_elements[i])
        failure, cm, cm_reliable = temp_cross_infos.confusion_matrix()
        print("confusion matrix:\n{0}".format(cm))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
