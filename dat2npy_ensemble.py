#!/usr/bin/python3
'''
Abstract:
    This is a program to convert .dat files to npy files
Usage:
    dat2npy.py [file name 1] [file name 2] [file name 3] ...
    [file name]:
        The file you want to processed.
        The first will be labeded as 0, the second will be labeded as 1, so as on.
Example:

    You have a data file "Toy.dat", "Toy2.dat", and "Toy3.dat"

    Then, do this cmd.
    $ dat2npy Toy.dat Toy2.dat Toy3.dat
    you get two series of files, one is data, another is label
    each series are sort by number of zero in a data.

Editor:
    Jacob975

20180123
####################################
update log
20180123 version alpha 1
    Now it works, the code can convert both source and label into tensorflow readable
20180124 version alpha 2
    1. Now feature, you can choose processing label or data by argv.
    2. Now the data will be normalized.
20180301 version alpha 3
    1. You can choose how many zero will be tolerated.
20180306 version alpha 4
    1. no argv for data mod and label mod anymore, for replacement, the code will generate label with data process.
    2. now you can process a sequence of data with label in order.
20180320 version alpha 5 
    1. add a tracer to dat data set
20180322 version alpha 6
    1. rename tracer
20180323 version alpha 7:
    1. rearrange the tracer
20180414 version alpha 8:
    1. denote no-observation as -9.99+e02
    2. rename func nozero_filter as no_observation_filter
20180415 version alpha 9:
    1. denote no-observation as 0 instead of -9.99+e02, if you need -9.99e+02, please use dat2npy_const.py
20180430 version alpha 10:
    1. This program become a prototype
    2. the default setting of no observation and no detections is 0, 0
20180530 version alpha 11:
    1. add a new func to save coord infomations
20180531 version alpha 12:
    1. all dat2npy programs are collected into the ensemble version
'''
import time
import re           # this is used to apply multiple spliting
import numpy as np
from sys import argv
from dat2npy_lib import read_well_known_data, apply_filter_on

# how many element in a data vector
data_width = 16

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    # initialize
    options = ['0_r', '0_r_noH', '0_r_noMIPS', '0_r_noH_noMIPS', '0_r_noJHK', '0_r_noH78', '1_1', '1_0', '1_r', '0_0']
    #----------------------------------
    # check argv is right
    if len(argv) < 3:
        print ("Error!\nUsage: dat2npy_ensemble.py [mod] [dat files]")
        print("possible mods: ")
        print(", ".join('%s'%x for x in options))
        exit()
    # read argv
    # Base on mod, loading corresponding functions
    mod = argv[1]
    if mod == '0_r':
        from dat2npy_lib import normalize_0_r as normalize
        from dat2npy_lib import no_observation_filter_eq_0 as no_observation_filter
    elif mod == '0_r_noH_noMIPS':
        from dat2npy_lib import normalize_0_r_noH_noMIPS as normalize
        from dat2npy_lib import no_observation_filter_eq_0 as no_observation_filter
    elif mod == '0_r_noH':
        from dat2npy_lib import normalize_0_r_noH as normalize
        from dat2npy_lib import no_observation_filter_eq_0 as no_observation_filter
    elif mod == '0_r_noMIPS':
        from dat2npy_lib import normalize_0_r_noMIPS as normalize
        from dat2npy_lib import no_observation_filter_eq_0 as no_observation_filter
    elif mod == '0_r_noJHK':
        from dat2npy_lib import normalize_0_r_noJHK as normalize
        from dat2npy_lib import no_observation_filter_eq_0 as no_observation_filter
    elif mod == '0_r_noH78':
        from dat2npy_lib import normalize_0_r_noH78 as normalize
        from dat2npy_lib import no_observation_filter_eq_0 as no_observation_filter
    elif mod == '1_1':
        from dat2npy_lib import normalize_1_1 as normalize
        from dat2npy_lib import no_observation_filter_smaller_than_or_eq_minus1 as no_observation_filter
    elif mod == '1_r':
        from dat2npy_lib import normalize_1_r as normalize
        from dat2npy_lib import no_observation_filter_eq_minus1 as no_observation_filter
    elif mod == '1_0':
        from dat2npy_lib import normalize_1_0 as normalize
        from dat2npy_lib import no_observation_filter_eq_minus1 as no_observation_filter
    elif mod == '0_0':
        from dat2npy_lib import normalize_0_0 as normalize
        from dat2npy_lib import no_observation_filter_smaller_than_or_eq_0 as no_observation_filter
    else:
        print("Wrong mod, program stops.")
        print("possible mods: ")
        print(", ".join('%s'%x for x in options))
        exit()
    data_name_list = argv[2:]
    print ("The command is:\n {0}".format(argv))
    print ("data to be processed: {0}".format(data_name_list))
    # how many element in a data vector
    data_width = 16
    #-----------------------------------
    # Load data, label, tracer, and coordinate
    sum_data = [[] for x in range(data_width)]
    sum_label = [[] for x in range(data_width)]
    sum_tracer = [[] for x in range(data_width)]
    sum_coord = [[] for x in range(data_width)]
    for ind, data_name in enumerate(data_name_list, start = 0):
        print ("##############################")
        print ("data name = {0}".format(data_name))
        print ("label = {0}".format(ind))
        # convert data from string to float
        str_data = read_well_known_data(data_name)
        data = np.array(str_data, dtype = float)
        data_n = normalize(data)
        # no observation filter
        # i is the tolarence of loss in a single datum
        for i in range(data_width):
            data_n_z, _filter= no_observation_filter(data_n, i)
            name_tracer = "{0}_tracer.dat".format(data_name[:4])
            name_coord = "{0}_coord.dat".format(data_name[:4])
            failure, tracer_outp = apply_filter_on(name_tracer, _filter)
            failure, coord_outp = apply_filter_on(name_coord, _filter)
            print ("MaxLoss = {0}, number of data = {1}".format(i, len(data_n_z)))
            label_z = np.array([ind for x in range(len(data_n_z)) ])
            label_z_f = [[0 for k in range(3)] for j in range(len(label_z))]
            for u in range(len(label_z_f)):
                label_z_f[u][int(label_z[u])] = 1
            #-----------------------------------------------------
            # stack them
            sum_data[i] = np.append(sum_data[i], data_n_z)
            sum_label[i] = np.append(sum_label[i], label_z_f)
            sum_tracer[i] = np.append(sum_tracer[i], tracer_outp)
            # if the coord file is not found, appending 0 into coord file
            if not failure:
                sum_coord[i] = np.append(sum_coord[i], coord_outp)
            elif failure:
                sum_coord[i] = np.append(sum_coord[i], np.zeros(2* len(_filter)))
            #-----------------------------------------------------
    # save data, label, tracer, and coordinate
    print ("###############################")
    print ("save data, label, tracer, and coordinate")
    for i in range(data_width):
        # reshape the data because np.append smooth the array.
        sum_data[i] = np.reshape(sum_data[i], (-1, data_width))
        sum_label[i] = np.reshape(sum_label[i], (-1, 3))
        sum_coord[i] = np.reshape(sum_coord[i], (-1, 2))
        print ("number of data with MaxLoss {0} = {1}".format(i, len(sum_data[i])))
        np.save("source_sed_MaxLoss{0}.npy".format(i), sum_data[i])
        np.savetxt("source_sed_MaxLoss{0}.txt".format(i), sum_data[i])
        np.save("source_id_MaxLoss{0}.npy".format(i), sum_label[i])
        np.savetxt("source_id_MaxLoss{0}.txt".format(i), sum_label[i])
        np.savetxt("source_tracer_MaxLoss{0}.txt".format(i), sum_tracer[i])
        np.save("source_tracer_MaxLoss{0}.npy".format(i), sum_tracer[i])
        np.savetxt("source_coord_MaxLoss{0}.txt".format(i), sum_coord[i])
        np.save("source_coord_MaxLoss{0}.npy".format(i), sum_coord[i])
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")