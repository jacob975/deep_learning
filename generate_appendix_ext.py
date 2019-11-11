#!/usr/bin/python3
'''
Abstract:
    This is a program randomly arranging the train, validate, and test dataset.
    Now we can have more than 3 labels.
Usage:
    generate_appendix_2.py [label table] [ number of partitions]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20191109
####################################
update log
20191109 version alpha 1:
    1. The code works 
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
    return index_array

def apply_index_on_files(index_array, tmp_file):
    set_array = [None for x in range(len(index_array))]
    for i in range(len(set_array)):
        set_array[i] = tmp_file[index_array[i]]
    return set_array

def apply_concatenate(star_set_array, gala_set_array, ysos_set_array):
    _sets = [None for i in range(len(star_set_array))]
    for i in range(len(star_set_array)):
        _sets[i] = np.concatenate((star_set_array[i], gala_set_array[i], ysos_set_array[i]), axis = 0)
    return np.array(_sets)

def flatten_last_dim(_list):
    ans = []
    for l in _list:
        ans.append(l)
    return ans

class shuffle_waiter():
    def __init__(self, num_label, num_parts):
        self.num_label = num_label
        self.num_parts = num_parts
        return
    def assign_index(self, cls_table):
        #-------------------------
        # Initialization
        label_part_index_list = []
        #-------------------------
        # find the index of the given label
        # Iterate through all possible labels
        #
        # label_part_index_list = 
        # [ array of index for label 1,
        #   array of index for label 2,
        #   array of index for label 3, ...
        # ]
        # And each array contains lots of indexes in shape (num_parts, num_index).
        #
        for l in range(self.num_label):
            index_for_labels = find_index(cls_table, l, self.num_parts)
            label_part_index_list.append(index_for_labels)
        self.label_part_index_array = np.array(label_part_index_list)
        return
    def apply_index_on_files(self, inp_file):
        #-------------------------
        # Initialization
        label_part_data_list = []
        #-------------------------
        # Select the data based on given index
        # Iterate through all possible labels.
        for l in range(self.num_label):
            data_for_labels = apply_index_on_files( self.label_part_index_array[l],
                                                    inp_file)
            label_part_data_list.append(data_for_labels)
        self.label_part_data_list = label_part_data_list
        return
    def cascade(self):
        #-------------------------
        # Initialization
        part_data_list = []
        #-------------------------
        # Cascade the data in the same partition but different labels.
        # Iterate throught all partitions.
        for p in range(self.num_parts):    
            tmp_cascaded_part = np.array([sub[p] for sub in self.label_part_data_list])
            tmp_cascaded_part = np.concatenate(tmp_cascaded_part, axis = 0)
            part_data_list.append(tmp_cascaded_part)
        self.part_data_list = part_data_list 
        return
    def save(self, name):
        print ("Saving the partitions")
        for p in range(self.num_parts):
            np.savetxt('{0}_part{1}.txt'.format(name, p), self.part_data_list[p], fmt = '%s')
    
        print ("Saving the training and testing sets.")
        for p in range(num_parts):
            print ("Part {0}".format(p+1))
            os.system("mkdir -p part{0}_test".format(p+1))
            os.system("mkdir -p part{0}_train".format(p+1))
            failure = save_to(p+1, self.part_data_list, name)
        return

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
        print ("Usage: generate_appendix_2.py [label table] [number of partitions]")
        exit()
    label_table_name = argv[1]
    num_parts = int(argv[2])
    #-----------------------------------
    # Load table
    label_table = np.loadtxt(label_table_name, dtype = str)
    num_label = len(label_table[0])
    cls_table = np.argmax(label_table, axis = 1)
    waiter = shuffle_waiter(num_label, num_parts)
    # Find out the index of source types (labels) 
    # And then assign to several partitions.
    waiter.assign_index(cls_table)
    print ("Type 'exit' to close the program.")
    # Apply on dataset iteratively.
    while True:
        inp_file = None
        file_name = input("Please specify the file you want to do random arrangements:\n")
        if file_name == "exit":
            exit()
        inp_file = np.loadtxt(file_name, dtype = str)
        # Apply index on input file.
        waiter.apply_index_on_files(inp_file)
        # Stack the data in the same partition.
        waiter.cascade()
        # Save the data
        waiter.save(file_name[:-4])
        print ("Done.")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
