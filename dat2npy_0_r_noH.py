#!/usr/bin/python3
'''
Abstract:
    This is a program to convert .dat files to npy files
    The feature of this version is that set all number smaller than 0 as 0

--------------------------------------------------
                no observation      no detection
--------------------------------------------------
dat2npy         0.00                0.00
dat2npy_const   -9.99e+02           -9.99e+02
dat2npy_pair    -9.99e+02           0.00
--------------------------------------------------

Usage:
    dat2npy_0_r_noH.py [file name 1] [file name 2] [file name 3] ...
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

20180530
####################################
update log
'''
import tensorflow as tf
import time
import re           # this is used to apply multiple spliting
import numpy as np
from sys import argv
from dat2npy_noobs_nodet import read_well_known_data

# how many element in a data vector
data_width = 16

def normalize(inp):
    # take norm
    h = len(inp)
    # remove band H
    inp[:,1] = 0.0
    inp[:,9] = 0.0
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[inp == -9.99e+02] = 0.0
    outp[inp == 0.0] = 0.0
    outp.reshape(-1, data_width)
    return outp

def no_observation_filter(inp, maximun):
    # set up MaxLoss filter
    _filter= np.array([ np.count_nonzero(row == 0.0) <= maximun for row in inp])
    # apply filter
    outp = inp[_filter]
    outp.reshape(-1, data_width)
    return outp, _filter

# This code is used to apply filter on certain files
def apply_filter_on(name_file, _filter):
    try:
        inp = np.loadtxt(name_file)
    except:
        print ("No such file or directory: {0}".format(name_file))
        return 1, None
    outp = inp[_filter]
    return 0, outp

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #----------------------------------
    # check argv is right
    if len(argv) == 1:
        print ("Error!\nUsage: dat2npy_0_r_noH.py [dat files]")
        exit()
    # read argv
    data_name_list = argv[1:]
    print ("The command is:\n {0}".format(argv))
    print ("data to be processed: {0}".format(data_name_list))
    # how many element in a data vector
    data_width = 16
    #-----------------------------------
    # Load data
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
        for i in range(data_width):
            data_n_z, _filter = no_observation_filter(data_n, i)
            name_tracer = "{0}_tracer.dat".format(data_name[:4])
            name_coord = "{0}_coord.dat".format(data_name[:4])
            failure, tracer_outp = apply_filter_on(name_tracer, _filter)
            failure, coord_outp = apply_filter_on(name_coord, _filter)
            print ("MaxLoss = {0}, number of data = {1}".format(i, len(data_n_z)))
            label_z = np.array([ind for x in range(len(data_n_z)) ])
            label_z_f = [[0 for k in range(3)] for j in range(len(label_z))]
            for u in range(len(label_z_f)):
                label_z_f[u][int(label_z[u])] = 1
            #-------------------------------------------------------------
            # stack them
            sum_data[i] = np.append(sum_data[i], data_n_z)
            sum_label[i] = np.append(sum_label[i], label_z_f)
            sum_tracer[i] = np.append(sum_tracer[i], tracer_outp)
            # if the coord file is not found, appending 0 into coord file
            if not failure:
                sum_coord[i] = np.append(sum_coord[i], coord_outp)
            elif failure:
                sum_coord[i] = np.append(sum_coord[i], np.zeros(2* len(_filter)))
            #-------------------------------------------------------------
    # save data
    print ("###############################")
    print ("save data, label, and tracer")
    for i in range(data_width):
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