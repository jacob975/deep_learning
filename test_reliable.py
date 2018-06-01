#!/usr/bin/python3
'''
Abstract:
    This is a program to demo how to trace a datum 
Usage:
    test_reliable.py [DIR] [keyword]
Example:
    test_reliable.py . MaxLoss15
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180601
####################################
update log
20180601 version alpha 1:
    1. The code works 
'''
import time
import load_lib
from sys import argv

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #----------------------------------------
    # initialize variables
    cls_true = None
    label_pred = None
    #----------------------------------------
    # Loading section
    # load argv
    if len(argv) != 3:
        print ("Error!\nUsage: test_reliable.py [directory] [keyword]")
        exit()
    directory = argv[1]
    keyword = argv[2]
    # load cls_true and label_pred
    failure, cls_true = load_lib.load_cls_true(keyword, directory)
    if not failure:
        print ("load cls_true success")
    failure, label_pred = load_lib.load_labels_pred(keyword, directory)
    if not failure:
        print ("load label_pred success")
    #----------------------------------------
    # test if the loading is successful or not
    infos = load_lib.confusion_matrix_infos(cls_true, label_pred)
    print(infos.cls_true.shape)
    print(infos.cls_true_reliable.shape)
    print(infos.cls_pred.shape)
    print(infos.cls_pred_reliable.shape)
    print(infos.reliable[0].shape)
    failure, cm, cm_reliable = infos.confusion_matrix()
    print("confusion matrix:\n{0}".format(cm))
    print("reliable confusion matrix:\n{0}".format(cm_reliable))
    infos.print_accuracy()
    infos.print_precision()
    infos.print_recall_rate()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
