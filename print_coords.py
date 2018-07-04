#!/usr/bin/python3
'''
Abstract:
    This is a program to print coords of data in certain positions of confusion matrix.
Usage:
    print_coords.py [DIR where AI saved] [keyword] [true_label] [pred_label]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180529
####################################
update log
20180529 version alpha 1
    1. the code is under testing
20180605 version alpha 2
    1. Add a func to print the coordinates of high reliable data only.
'''
import time
import numpy as np
import load_lib
from sys import argv

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 5:
        print ("Error!\nUsage:\tprint_coords.py [DIR where AI saved] [keyword] [true_label] [pred_label]")
        print ("Example:print_coords.py . MaxLoss15 1 1")
        exit()
    directory = argv[1]
    keyword = argv[2]
    true_label = int(argv[3])
    pred_label = int(argv[4])
    # Load files
    failure, labels_pred = load_lib.load_labels_pred(keyword, directory)
    if not failure:
        print ("load labels_pred success")
    failure, cls_true = load_lib.load_cls_true(keyword, directory)
    if not failure:
        print ("load cls_true success")
    # load_coord haven't done in load_lib
    failure, coords = load_lib.load_coords(keyword, directory)
    if not failure:
        print ("load coordinates success")
    infos = load_lib.confusion_matrix_infos(cls_true, labels_pred)
    failure, cm = load_lib.confusion_matrix(cls_true, infos.cls_pred)
    print(cm)
    #------------------------------------
    # read the coords of data in certain position of confusion matrix
    index_of_certain_data = np.where((cls_true == true_label) & (infos.cls_pred == pred_label))
    coords_of_certain_data = coords.test[index_of_certain_data]
    index_of_high_reliable_certain_data = np.where((cls_true == true_label) & (infos.cls_pred == pred_label) & (np.max(infos.labels_pred, axis = 1) > 0.8))
    coords_of_high_reliable_certain_data = coords.test[index_of_high_reliable_certain_data]
    # print coords out to test if the list correct.
    print("number of coords of selected sources: {0}".format(len(coords_of_certain_data)))
    print("5 examples")
    for i in range(5):
        try:
            print("{0} {1}".format(coords_of_certain_data[i][0], coords_of_certain_data[i][1]))
        except:
            break
    print("...\n")
    print("number of coords of selected high reliable sources: {0}".format(len(coords_of_high_reliable_certain_data)))
    print("5 examples")
    for i in range(5):
        try:
            print("{0} {1}".format(coords_of_high_reliable_certain_data[i][0], coords_of_high_reliable_certain_data[i][1]))
        except:
            break
    print("...\n")
    # save the result
    np.savetxt("{0}/coords_test_{1}_{2}.txt".format(directory, true_label, pred_label), coords_of_certain_data)
    np.savetxt("{0}/coords_test_HR_{1}_{2}.txt".format(directory, true_label, pred_label), coords_of_high_reliable_certain_data)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
