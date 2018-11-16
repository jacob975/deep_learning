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

class option_dat2npy():
    def __init__(self):
        self.opts = None
    def create(self):
        s = [   '# mask code:',
                '# \t[mask code should] be a 8 digit binary number.',
                '# Example: 00000000 represent no masked; 11111111 represent all masked',
                '',
                '# number of lost:',
                '# \t[number of lost] represent the tolerance for data',
                '# Example: 0 means only data without loss will be saved, [number of lost] should be a integer between 0 and 15',
                '',
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
                '',]
        np.savetxt('option_dat2npy.txt', s, fmt = '%s')
    def load(self, file_name):
        self.opts = np.loadtxt(file_name, dtype = str)
        self.opts = list(self.opts)
        return self.opts
