#!/usr/bin/python3
'''
Abstract:
    This is a program randomly arranging the train, validate, and test dataset.
Usage:
    generate_appendix.py [label table] [ number of partitions]
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

def save(table_arr, name):
    for i in range(len(table_arr)):
        np.savetxt('{0}_part{1}.txt'.format(name, i), table_arr[i], fmt = '%s')
    return 0

def save_to(part_index, table_arr, name):
    for i, table in enumerate(table_arr):
        if i+1 == part_index:
            np.savetxt('part{0}_test/{1}.txt'.format(i+1, name), table, fmt = '%s')
        else:
            np.savetxt('part{0}_train/{1}_part{2}.txt'.format(part_index, name, i+1), table, fmt = '%s')
    os.system("cat part{0}_train/{1}_part*.txt > part{0}_train/{1}.txt".format(part_index, name))
    os.system("rm part{0}_train/{1}_part*.txt".format(part_index, name))
    return 0

def find_index(cls_table, label, num_parts):
    # Find out the index of star, galaxy and ysos.
    index_source = np.where(cls_table == label)[0]
    num_data = len(index_source)
    ticks = np.linspace(0, num_data, num_parts+1, dtype = int)
    print (ticks)
    ticks[-1] += 1
    # Make a random seed and apply on data
    np.random.shuffle(index_source)
    index_array = [None for i in range(num_parts)]
    for i in range(len(index_array)):
        index_array[i] = index_source[ticks[i]:ticks[i+1]]
    return np.array(index_array)

def apply_index_on_files(index_array, tmp_file):
    set_array = [None for x in range(len(index_array))]
    for i in range(len(set_array)):
        set_array[i] = tmp_file[index_array[i]]
    return np.array(set_array)

def apply_concatenate(star_set_array, gala_set_array, ysos_set_array):
    _sets = [None for i in range(len(star_set_array))]
    for i in range(len(star_set_array)):
        _sets[i] = np.concatenate((star_set_array[i], gala_set_array[i], ysos_set_array[i]), axis = 0)
    return np.array(_sets)

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: generate_appendix.py [label table] [number of partitions]")
        exit()
    label_table_name = argv[1]
    num_parts = int(argv[2])
    #-----------------------------------
    # Load table
    label_table = np.loadtxt(label_table_name, dtype = str)
    cls_table = np.argmax(label_table, axis = 1)
    # Find out the index of star, galaxy and ysos.
    star_index_array = find_index(cls_table, 0, num_parts)
    gala_index_array = find_index(cls_table, 1, num_parts)
    ysos_index_array = find_index(cls_table, 2, num_parts)
    print ("Type 'exit' to close the program.")
    # Apply on dataset iteratively.
    while True:
        tmp_file = None
        file_name = input("Please specify the file you want to do random arrangements:\n")
        if file_name == "exit":
            exit()
        tmp_file = np.loadtxt(file_name, dtype = str)
        # Apply index on tmp file.
        star_set_array = apply_index_on_files(star_index_array, tmp_file)
        gala_set_array = apply_index_on_files(gala_index_array, tmp_file)
        ysos_set_array = apply_index_on_files(ysos_index_array, tmp_file)
        _sets = apply_concatenate(star_set_array, gala_set_array, ysos_set_array)
        failure = save(_sets, file_name[:-4])
        # Save the data
        print ("Saving the partitions")
        for i in range(num_parts):
            print ("Part {0}".format(i+1))
            os.system("mkdir -p part{0}_test".format(i+1))
            os.system("mkdir -p part{0}_train".format(i+1))
            failure = save_to(i+1, _sets, file_name[:-4])
        print("Done.")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
