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
20180912 version alpha 2
    1. Update the mask system, using mask code instead of keywords.
'''
import time
import re           # this is used to apply multiple spliting
import numpy as np
from sys import argv

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

def mask(inp, mask_code = np.zeros(8)):
    # The number of source in the input file.
    h = len(inp)
    # Mask some bands
    mask_code = [ int(x) for x in list(mask_code)]
    for index, value in enumerate(mask_code):
        if value:
            inp[:,index] = 0.0
            inp[:,index + 8] = 0.0
    # make each no observation having the same value
    inp[inp == -9.99e+02] = 0.0
    inp[inp == 0.0] = 0.0
    return inp

def normalize(inp):
    # Normailze
    h = len(inp)
    outp = np.zeros(inp.shape)
    norm = np.amax(inp, axis=1)
    outp = inp / norm.reshape(h,1)
    return outp

#------------------------------------------------------
# Common filters for no-detected sources and no-observed sources.

def no_observation_filter_smaller_than_or_eq_0(inp, maximun, data_width):
    # set up MaxLoss filter
    _filter= np.array([ np.count_nonzero(row <= 0.0) <= maximun for row in inp])
    # apply filter
    outp = inp[_filter]
    outp.reshape(-1, data_width)
    return outp, _filter

def no_observation_filter_eq_0(inp, maximun, data_width):
    # set up MaxLoss filter
    _filter= np.array([ np.count_nonzero(row == 0.0) <= maximun for row in inp])
    # apply filter
    outp = inp[_filter]
    outp.reshape(-1, data_width)
    return outp, _filter

def no_observation_filter_smaller_than_or_eq_minus1(inp, maximun, data_width):
    # set up MaxLoss filter
    _filter= np.array([ np.count_nonzero(row <= -1.0) <= maximun for row in inp])
    # apply filter
    outp = inp[_filter]
    outp.reshape(-1, data_width)
    return outp, _filter

def no_observation_filter_eq_minus1(inp, maximun, data_width):
    # set up MaxLoss filter
    _filter= np.array([ np.count_nonzero(row == -1.0) <= maximun for row in inp])
    # apply filter
    outp = inp[_filter]
    outp.reshape(-1, data_width)
    return outp, _filter

#------------------------------------------------------
# Special filters
def select_high_flux_error_correlated_source(   data, 
                                                bkg_noise = [0,0,0,1e-2, 1e-2, 1e-1, 1e-1, 8e-1], 
                                                error_flux_ratio = [0,0,0,0.047,0.047,0.047,0.047, 0.095]):
    # Check the format the inputs.
    if len(bkg_noise) != 8 or len(error_flux_ratio) != 8:
        print ("The format of given bkg noise and given error flux ratio is not correct.")
        return 1
    exclusion = np.zeros(len(data))
    # Range all bands.
    for i in range(8):
        # Don't select in bands J, H, K
        if i < 3:
            pass
        else:
            ratio = np.divide(data[:,i+8], data[:,i])
            exclusion = (exclusion == True) | \
                        (data[:,i+8]> bkg_noise[i]) & \
                        (ratio > 5 * error_flux_ratio[i])
    return exclusion 
