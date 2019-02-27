#!/usr/bin/python3
'''
Abstract:
    This is a program for generating the appendix that list all incorrectly predicted sources. 
Usage:
    generate_partition.py [# of partition]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190121
####################################
update log
'''
import os
import time
import numpy as np
from sys import argv

# This def is used to seperate the table into given # of partitions
def gen_part(table, ticks):
    partitions = [None for i in range(len(ticks)-1)]
    for i in range(len(partitions)):
        partitions[i] = table[ticks[i]:ticks[i+1]] 
    return partitions

def save_part(table_arr, name, keyword):
    for i, table in enumerate(table_arr):
        np.savetxt('source_{0}_{1}_part{2}.txt'.format(name, keyword, i+1), table, fmt = '%s')
    return 0

def save_to(part_index, table_arr, name, keyword):
    for i, table in enumerate(table_arr):
        if i+1 == part_index:
            np.savetxt('part{2}_test/source_{0}_{1}.txt'.format(name, keyword, i+1), table, fmt = '%s')
        else:
            np.savetxt('part{0}_train/source_{1}_{2}_part{3}.txt'.format(part_index, name, keyword, i+1), table, fmt = '%s')
    os.system("cat part{0}_train/source_{1}_{2}_part*.txt > part{0}_train/source_{1}_{2}.txt".format(part_index, name, keyword))
    os.system("rm part{0}_train/source_{1}_{2}_part*.txt".format(part_index, name, keyword))
    return 0

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
        print ("Usage: generate_appendix.py [# of partition] [Keyword]")
        print ("Keyword means the words after 'sed' before '.txt'")
        exit()
    num_partition = int(argv[1])
    keyword = argv[2]
    #-----------------------------------
    # Load data
    # All tables should contain the same # of sources.
    print ("Loading...")
    source_sed = np.loadtxt("source_sed_{0}.txt".format(keyword), dtype = str)
    source_label = np.loadtxt("source_id_{0}.txt".format(keyword), dtype = str)
    source_tracer = np.loadtxt("source_tracer_{0}.txt".format(keyword), dtype = str)
    source_coord = np.loadtxt("source_coord_{0}.txt".format(keyword), dtype = str)
    source_Q = np.loadtxt("source_Q_{0}.txt".format(keyword), dtype = str)
    source_HL2013 = np.loadtxt("source_HL2013_{0}.txt".format(keyword), dtype = str)
    num_source = len(source_sed)
    #-----------------------------------
    # Shuffle the data
    print ('Shuffle the data')
    randomize = np.arange(num_source)
    np.random.shuffle(randomize)
    source_sed = source_sed[randomize]
    source_label = source_label[randomize]
    source_tracer = source_tracer[randomize]
    source_coord = source_coord[randomize]
    source_Q = source_Q[randomize]
    source_HL2013 = source_HL2013[randomize]
    # Seperate the dataset into given # of partitions.
    print ('Generate ticks and partitions')
    ticks = np.linspace(0, num_source, num_partition+1, dtype = int)
    ticks[-1] += 1
    print ('ticks:{0}'.format(ticks))
    sed_partitions = gen_part(source_sed, ticks)
    label_partitions = gen_part(source_label, ticks)
    tracer_partitions = gen_part(source_tracer, ticks)
    coord_partitions = gen_part(source_coord, ticks)
    Q_partitions = gen_part(source_Q, ticks)
    HL2013_partitions = gen_part(source_HL2013, ticks)
    # Save the partitions
    print ("Saving the partitions")
    failure = save_part(sed_partitions, 'sed', keyword)
    failure = save_part(label_partitions, 'id', keyword)
    failure = save_part(tracer_partitions, 'tracer', keyword)
    failure = save_part(coord_partitions, 'coord', keyword)
    failure = save_part(Q_partitions, 'Q', keyword)
    failure = save_part(HL2013_partitions, 'HL2013', keyword)
    for i in range(num_partition):
        print ("Round {0}".format(i+1))
        os.system("mkdir -p part{0}_test".format(i+1))
        os.system("mkdir -p part{0}_train".format(i+1))
        failure = save_to(i+1, sed_partitions, 'sed', keyword)
        failure = save_to(i+1, label_partitions, 'id', keyword)
        failure = save_to(i+1, tracer_partitions, 'tracer', keyword)
        failure = save_to(i+1, coord_partitions, 'coord', keyword)
        failure = save_to(i+1, Q_partitions, 'Q', keyword)
        failure = save_to(i+1, HL2013_partitions, 'HL2013', keyword)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
