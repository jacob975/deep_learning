#!/usr/bin/python3
'''
Abstract:
    This is a program for trace the order back using tracers and id 
Usage:
    trace_back.py [tracer] [id]
Output:
    1. The index of orders
Editor:
    Jacob975
##################################
#   Python3                      #
#   This code is made in python3 #
##################################
20200806
####################################
update log
20200806 version alpha 1
    1. The code works
'''
import time
import numpy as np
from sys import argv

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
        print ("Usage: trace_back.py [tracer] [id]")
        exit()
    tracer_table_name = argv[1]
    id_table_name = argv[2]
    #-----------------------------------
    # Load data
    tracer_table = np.loadtxt(tracer_table_name)
    tracer_table = np.array(tracer_table, dtype = int)
    id_table = np.loadtxt(id_table_name)
    cls_table = np.argmax(id_table, axis = 1)
    index_star = np.where(cls_table == 0)[0]
    index_gala = np.where(cls_table == 1)[0]
    index_ysos = np.where(cls_table == 2)[0]
    print(index_star.shape)
    print(index_gala.shape)
    print(index_ysos.shape)
    # Get the index of the order of each label
    temp_tracer_table = np.copy(tracer_table)
    temp_tracer_table[index_gala] = temp_tracer_table[index_gala] + 1000000
    temp_tracer_table[index_ysos] = temp_tracer_table[index_ysos] + 2000000
    outp_index = np.argsort(temp_tracer_table)
    '''
    star_tracer_table = tracer_table[index_star]
    gala_tracer_table = tracer_table[index_gala]
    ysos_tracer_table = tracer_table[index_ysos]
    star_sort_index = np.argsort(star_tracer_table)
    gala_sort_index = np.argsort(gala_tracer_table) + len(index_star)
    ysos_sort_index = np.argsort(ysos_tracer_table) + len(index_star) + len(index_gala)
    outp_index = np.zeros(len(tracer_table), dtype = int)
    outp_index[index_star] = star_sort_index
    outp_index[index_gala] = gala_sort_index
    outp_index[index_ysos] = ysos_sort_index
    '''
    sorted_id_table = id_table[outp_index]
    sorted_tracer_table = tracer_table[outp_index]
    np.savetxt('outp_index.txt', outp_index, fmt = '%d')
    np.savetxt('sorted_id.txt', sorted_id_table, fmt = '%d')
    np.savetxt('sorted_tracer.txt', sorted_tracer_table, fmt = '%d')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
