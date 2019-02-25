#!/usr/bin/python3
'''
Abstract:
    This is a program for reading and loading input files. 
Usage:
    print_input_lib.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181113
####################################
update log
20181113 version alpha 1
    1. The code works.
'''
import numpy as np
import time

class option_test():
    def __init__(self):
        self.opts = None
    def create(self):
        s = [   '# mask code:',
                '# \t[mask code should] be a 8 digit binary number.',
                '# Example: 00000000 represent no masked; 11111111 represent all masked',
                '00000000',
                '# consider error:',
                '# \t[consider error] means considering error or not during the convertion.',
                '# Available options: yes, no',
                'yes']
        np.savetxt('option_test.txt', s, fmt = '%s')
    def load(self, file_name):
        self.opts = np.loadtxt(file_name, dtype = str)
        self.opts = list(self.opts)
        return self.opts

class option_train():
    def __init__(self):
        self.opts = None
    def create(self):
        s = [   '# mask code:',
                '# \t[mask code] should be a 8 digit binary number.',
                '# Example: 00000000 represent no masked; 11111111 represent all masked',
                '00000000',
                '# consider error:',
                '# \t[consider error] means considering error or not during the convertion.',
                '# Available options: yes, no',
                'yes',
                '# batch format:',
                '# \t[batch format] means how to get the next batch of sources.',
                '# Available options: equal, random',
                'random',
                '# iterations upperlimits:',
                '# \t[iterations upperlimits] means the training process will end if the model is train by this times.',
                '# It should be an integer',
                '500000',
                '# validation function:',
                '# \t[validation function] means the function we used to judge the model.',
                '# Available options: GT_score, cross_entropy',
                'cross_entropy']
        np.savetxt('option_train.txt', s, fmt = '%s')
    def load(self, file_name):
        self.opts = np.loadtxt(file_name, dtype = str)
        self.opts = list(self.opts)
        return self.opts

class option_dat2npy():
    def __init__(self):
        self.opts = None
    def create(self):
        s = [   '# mask code:',
                '# \t[mask code should] be a 8 digit binary number.',
                '# Example: 00000000 represent no masked; 11111111 represent all masked',
                '00000000',
                '# number of lost:',
                '# \t[number of lost] represent the tolerance for data',
                '# Example: 0 means only data without loss will be saved, [number of lost] should be a integer between 0 and 15',
                '0',
                '# do normalization:',
                '# \t[do normalization] means normalize the SEDs or not during the convertion.',
                '# Available options: yes, no',
                '',
                '# consider error:',
                '# \t[consider error] means considering error or not during the convertion.',
                '# Available options: yes, no',
                '',
                '# High error-flux correlation:',
                '# \t[error_flux_correlation] mean the program only select the source with high error-flux correlation.',
                '# Available options: yes, no',
                'no',
                '# Upper limit of number of sources:',
                '# \t[upper limit of the number of sources] mean the maximum number of the sources',
                '# It can only be a integer.',
                '0',
                '# Trace the Av:',
                '# If you do extinction correction before dat2npy_ensemble.py, you may like to keep the Av information.',
                '# Available option: yes, no',
                'no']
        np.savetxt('option_dat2npy.txt', s, fmt = '%s')
    def load(self, file_name):
        self.opts = np.loadtxt(file_name, dtype = str)
        self.opts = list(self.opts)
        return self.opts
