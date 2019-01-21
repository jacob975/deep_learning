#!/usr/bin/python3
'''
Abstract:
    This is a program randomly arranging the train, validate, and test dataset.
Usage:
    dataset_arrange.py [train size] [validate size] [test size]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190109
####################################
update log
'''
import time
from sys import argv
import numpy as np
import os

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 5:
        print ("The number of arguments is wrong.")
        print ("Usage: dataset_arrange.py [# of data] [train size] [validate size] [test size]")
        exit()
    num_data = int(argv[1])
    train_weight = int(argv[2])
    validate_weight = int(argv[3])
    test_weight = int(argv[4])
    #-----------------------------------
    # Make a random seed and apply on data
    randomize = np.arange(num_data)
    np.random.shuffle(randomize)
    total_weight = train_weight + validate_weight + test_weight
    # Derive the size from the weight of dataset and the number of data.
    train_size = int(num_data * train_weight/total_weight)
    validate_size = int(num_data * validate_weight/total_weight)
    test_size = int(num_data * test_weight/total_weight)
    print ("Type 'exit' to close the program.")
    # Apply on dataset iteratively.
    while True:
        file_name = input("Please specify the file you want to do random arrangements:\n")
        if file_name == "exit":
            exit()
        tmp_file = np.loadtxt(file_name, dtype = str)
        tmp_file = tmp_file[randomize]
        file_for_train = tmp_file[:train_size] 
        file_for_validate = tmp_file[train_size:validate_size + train_size]
        file_for_test = tmp_file[validate_size + train_size:]
        # Save the data
        os.system("mkdir -p train")
        os.system("mkdir -p validate")
        os.system("mkdir -p test")
        np.savetxt("train/{0}".format(file_name),    file_for_train, fmt = '%s')
        np.savetxt("validate/{0}".format(file_name), file_for_validate, fmt = '%s')
        np.savetxt("test/{0}".format(file_name),     file_for_test, fmt = '%s')
        print("Done.")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
