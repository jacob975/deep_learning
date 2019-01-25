#!/usr/bin/python3
'''
Abstract:
    This is a program randomly arranging the train, validate, and test dataset.
Usage:
    arrange_dataset.py [train size] [validate size] [test size]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190109
####################################
update log
20190125 version alpha 2:
    1. Delete the validation part, and try to distribute source equally.
'''
import time
from sys import argv
import numpy as np
import os

def find_index(cls_table, label, train_weight, test_weight):
    # Find out the index of star, galaxy and ysos.
    index_source = np.where(cls_table == label)[0]
    num_data = len(index_source)
    # Make a random seed and apply on data
    np.random.shuffle(index_source)
    total_weight = train_weight + test_weight
    # Derive the size from the weight of dataset and the number of data.
    train_size = int(num_data * train_weight/total_weight)
    test_size = int(num_data * test_weight/total_weight)
    train_index = index_source[:train_size] 
    test_index = index_source[train_size:]
    print (len(train_index), len(test_index))
    return train_index, test_index

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 4:
        print ("The number of arguments is wrong.")
        print ("Usage: arrange_dataset.py [label table] [train weight] [test weight]")
        exit()
    label_table_name = argv[1]
    train_weight = int(argv[2])
    test_weight = int(argv[3])
    #-----------------------------------
    # Load table
    label_table = np.loadtxt(label_table_name, dtype = str)
    cls_table = np.argmax(label_table, axis = 1)
    # Find out the index of star, galaxy and ysos.
    train_star_index, test_star_index = find_index(cls_table, 0, train_weight, test_weight)
    train_gala_index, test_gala_index = find_index(cls_table, 1, train_weight, test_weight)
    train_ysos_index, test_ysos_index = find_index(cls_table, 2, train_weight, test_weight)
    print ("Type 'exit' to close the program.")
    # Apply on dataset iteratively.
    while True:
        train_star_set=None
        train_gala_set=None
        train_ysos_set=None
        test_star_set=None
        test_gala_set=None
        test_ysos_set=None
        train_sets=None
        test_sets=None
        tmp_file = None
        file_name = input("Please specify the file you want to do random arrangements:\n")
        if file_name == "exit":
            exit()
        tmp_file = np.loadtxt(file_name, dtype = str)
        # Apply index on tmp file.
        train_star_set = tmp_file[train_star_index]
        train_gala_set = tmp_file[train_gala_index]
        train_ysos_set = tmp_file[train_ysos_index]
        test_star_set = tmp_file[test_star_index]
        test_gala_set = tmp_file[test_gala_index]
        test_ysos_set = tmp_file[test_ysos_index]
        train_sets = np.concatenate((train_star_set, train_gala_set, train_ysos_set), axis = 0)
        test_sets = np.concatenate((test_star_set, test_gala_set, test_ysos_set), axis = 0)
        # Save the data
        os.system("mkdir -p train")
        os.system("mkdir -p test")
        np.savetxt("train/{0}".format(file_name),    train_sets, fmt = '%s')
        np.savetxt("test/{0}".format(file_name),     test_sets, fmt = '%s')
    
    print("Done.")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
