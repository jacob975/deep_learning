#!/usr/bin/python3
'''
Abstract:
    This is a program for getting extinction curves of near IR 
    from Synthetic Extinction Curves 
    given by https://www.astro.princeton.edu/~draine/dust/dustmix.html 
Usage:
    get_extinction_curves.py [a text file saved extinction curves table]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180813
####################################
update log
20180813 version alpha 1
'''
import numpy as np
import time
from sys import argv

# Find the closest freq with the given freq
def match_freq(extinction_table, freq):
    for index in range(len(extinction_table)):
        if freq < extinction_table[index][0]:
            return index
    return -1

# Calculate the interpolation of two value in given indices.
def interpolation(extinction_table, freq, index_1, index_2):
    value_1 = extinction_table[index_1][3]
    value_2 = extinction_table[index_2][3]
    weight_1 = abs(freq - extinction_table[index_2][0]) 
    weight_2 = abs(freq - extinction_table[index_1][0] )
    value = (value_1 * weight_1 + value_2 * weight_2) / (weight_1 + weight_2)
    return value

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("Wrong number of arguments")
        print ("Usage: get_extinction_curves.py [extinction curves table]")
        exit(1)
    table_name = argv[1]
    #-----------------------------------
    # Load table
    extinction_table = np.loadtxt(table_name, dtype = float, comments = "#")
    extinction_table = extinction_table[extinction_table[:,0].argsort()]
    # Initialize
    band_freq_list = [[  'V', 0.546, 0.0],
                      [  'J', 1.235, 0.0],
                      [  'H', 1.662, 0.0],
                      [  'K', 2.159, 0.0],
                      ['IR1', 3.6  , 0.0],
                      ['IR2', 4.5  , 0.0],
                      ['IR3', 5.8  , 0.0],
                      ['IR4', 8.0  , 0.0],
                      ['MP1', 24.  , 0.0]]
    # Calculate the result
    for band in band_freq_list:
        index = match_freq(extinction_table, band[1])
        band[2] = interpolation(extinction_table, band[1], index, index - 1)
    band_freq_array = np.array(band_freq_list, dtype = object)
    band_freq_array[:,2] = np.divide( band_freq_array[:,2], band_freq_array[0,2])
    print ("name wave_length A_lambda/A_v")
    for band in band_freq_array:
        print ("{0} {1} {2:.4f}".format(band[0], band[1], band[2]))
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
