#!/usr/bin/python3
'''
Abstract:
    This is a library to provide functions for converting .dat files to npy files
Editor:
    Jacob975

2018531
####################################
update log
20180531 version alpha 1
    1. This is the library of dat2npy program in ensemble version 
'''
import time
import re           # this is used to apply multiple spliting
import numpy as np
from sys import argv

# how many element in a data vector
data_width = 16

# the def is used to read a list of data with the same class.
def read_well_known_data(data_name):
    if data_name[-3:] == "npy":
        return np.load(data_name)
    elif data_name[-3:] == "txt":
        return np.loadtxt(data_name)
    f = open(data_name, 'r')
    data = []
    for ind, line in enumerate(f.readlines(), start = 0):
        # skip if no data or it's a hint.
        if not len(line) or line.startswith('#'):
            continue
        row = re.split('[,\n\[\]]+', line)
        # clean the empty element
        row_c = [x for x in row if x != ""]
        if len(row_c) != data_width:
            print (line[:-1])
            print ("the row {0} is wrong.\n".format(ind))
            continue
        data.append(row_c)
    f.close()
    return data

#---------------------------------------------------
def normalize_0_0(inp):
    # take norm
    h = len(inp)
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[inp == -9.99e+02 ] = 0.0
    outp[inp == -0.0 ] = 0.0
    outp.reshape(-1, data_width)
    return outp

def normalize_1_1(inp):
    # take norm
    h = len(inp)
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[outp <= 0.0] = -1.0
    outp.reshape(-1, data_width)
    return outp

def normalize_1_r(inp):
    # take norm
    h = len(inp)
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[inp == -9.99e+02] = -1.0
    outp[inp == 0.0] = -1.0
    outp.reshape(-1, data_width)
    return outp

def normalize_1_0(inp):
    # take norm
    h = len(inp)
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[outp <= 0.0] = 0.0
    for row in outp:
        for i in range(len(row)//2):
            if (row[i] <= 0.0) and (row[i+8] <= 0.0):
                row[i] = row[i+8] = -1.0
    outp.reshape(-1, data_width)
    return outp

def normalize_0_r(inp):
    # take norm
    h = len(inp)
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[inp == -9.99e+02] = 0.0
    outp[inp == 0.0] = 0.0
    outp.reshape(-1, data_width)
    return outp

def normalize_0_r_noH(inp):
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
    
def normalize_0_r_noMIPS(inp):
    # take norm
    h = len(inp)
    # remove band MIPS 24 um
    inp[:,7] = 0.0
    inp[:,15] = 0.0
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[inp == -9.99e+02] = 0.0
    outp[inp == 0.0] = 0.0
    outp.reshape(-1, data_width)
    return outp

def normalize_0_r_noH_noMIPS(inp):
    # take norm
    h = len(inp)
    # remove band H
    inp[:,1] = 0.0
    inp[:,9] = 0.0
    # remove band MIPS 24 um
    inp[:,7] = 0.0
    inp[:,15] = 0.0
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[inp == -9.99e+02] = 0.0
    outp[inp == 0.0] = 0.0
    outp.reshape(-1, data_width)
    return outp

def normalize_0_r_noJHK(inp):
    # take norm
    h = len(inp)
    # remove band JHK
    inp[:,0:3] = 0.0
    inp[:,8:11] = 0.0
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[inp == -9.99e+02] = 0.0
    outp[inp == 0.0] = 0.0
    outp.reshape(-1, data_width)
    return outp

def normalize_0_r_noH78(inp):
    # take norm
    h = len(inp)
    # remove band H, IRAC 4, MIPS 1 
    inp[:,1] = 0.0
    inp[:,9] = 0.0
    inp[:,6] = 0.0
    inp[:,14]= 0.0
    inp[:,7] = 0.0
    inp[:,15]= 0.0
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[inp == -9.99e+02] = 0.0
    outp[inp == 0.0] = 0.0
    outp.reshape(-1, data_width)
    return outp

def normalize_0_r_no78(inp):
    # take norm
    h = len(inp)
    # remove band, IRAC 4, MIPS 1 
    inp[:,6] = 0.0
    inp[:,14]= 0.0
    inp[:,7] = 0.0
    inp[:,15]= 0.0
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    # make each no observation having the same value
    outp[inp == -9.99e+02] = 0.0
    outp[inp == 0.0] = 0.0
    outp.reshape(-1, data_width)
    return outp

#------------------------------------------------------
def no_observation_filter_smaller_than_or_eq_0(inp, maximun):
    # set up MaxLoss filter
    _filter= np.array([ np.count_nonzero(row <= 0.0) <= maximun for row in inp])
    # apply filter
    outp = inp[_filter]
    outp.reshape(-1, data_width)
    return outp, _filter

def no_observation_filter_eq_0(inp, maximun):
    # set up MaxLoss filter
    _filter= np.array([ np.count_nonzero(row == 0.0) <= maximun for row in inp])
    # apply filter
    outp = inp[_filter]
    outp.reshape(-1, data_width)
    return outp, _filter

def no_observation_filter_smaller_than_or_eq_minus1(inp, maximun):
    # set up MaxLoss filter
    _filter= np.array([ np.count_nonzero(row <= -1.0) <= maximun for row in inp])
    # apply filter
    outp = inp[_filter]
    outp.reshape(-1, data_width)
    return outp, _filter

def no_observation_filter_eq_minus1(inp, maximun):
    # set up MaxLoss filter
    _filter= np.array([ np.count_nonzero(row == -1.0) <= maximun for row in inp])
    # apply filter
    outp = inp[_filter]
    outp.reshape(-1, data_width)
    return outp, _filter
#------------------------------------------------------

# This code is used to apply filter on certain files
def apply_filter_on(name_file, _filter):
    try:
        inp = np.loadtxt(name_file)
    except:
        print ("No such file or directory: {0}".format(name_file))
        return 1, None
    outp = inp[_filter]
    return 0, outp
