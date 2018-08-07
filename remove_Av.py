#!/usr/bin/python3
'''
Abstract:
    This is a program for remove Av and show the intrinsic flux of sources. 
Usage:
    remove_Av.py [extinction table] [source table]
    Example: Remove_Av.py table source_table.tbl
Editor:
    T.H. Heish, Jacob

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180807
####################################
update log
20180807 version alpha 1
    1. The code works
'''
from math import pi
from numpy import arcsin
from sys import argv
import time
import numpy as np

def find_the_closest_extinction_position(source, catalog):
    # Initialize
    # Read central position of source
    RA_degree  = source[0]
    DEC_degree = source[2]
    # Convert degree to radian
    RA_enoch  = RA_degree/360*2*pi
    DEC_enoch = DEC_degree/360*2*pi
    # The radius of an extinction region in unit degree
    tolerance_radius = 0.05
    RA_ca  = np.divide(catalog[:,0], 360) * 2 * pi
    DEC_ca = np.divide(catalog[:,1], 360) * 2 * pi
    diff_X = np.cos(RA_enoch) * np.cos(DEC_enoch) - np.cos(RA_ca) * np.cos(DEC_ca) 
    diff_Y = np.cos(RA_enoch) * np.sin(DEC_enoch) - np.cos(RA_ca) * np.sin(DEC_ca)
    diff_Z = np.sin(DEC_enoch) * np.sin(DEC_ca)
    square_distance_array = np.power(diff_X, 2) + np.power(diff_Y, 2) + np.power(diff_Z, 2)
    min_square_distance = np.min(square_distance_array)
    index_min_square_distance = np.argmin(square_distance_array) 
    return min_square_distance, index_min_square_distance

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #--------------------------------------------
    # Load argv
    if len(argv) != 3:
        print ("Error!\nUsage: Remove_Av.py [extinction table] [source table]") 
        print ("Example: Remove_Av.py extinction_table source_table.tbl")
        exit()
    extinction_table_name = argv[1]
    source_table_name = argv[2]
    #--------------------------------------------
    # Load tables
    # The table of extinction map.
    extinction_table = np.loadtxt(extinction_table_name, dtype = float, comment = "#")
    # The source to be corrected
    source_table = np.loadtxt(source_table_name, dtype = float, comment = "#")
    # Citation needed
    parameter =[['J'  ,33 ,0.2741],
                ['H'  ,54 ,0.1622],
                ['K'  ,75 ,0.1119],
                ['IR1',96 ,0.0671],
                ['IR2',117,0.0543],
                ['IR3',138,0.0444],
                ['IR4',159,0.0463],
                ['MP1',180,0.0259],
                ['MP2',201,0.     ]]
    for source in source_table:
        # Find the closest extinction position for sources.
        minSQ, index_min = find_the_closest_extinction_position(source, extinction_table)
        # Show angular size, the distance in arc second.
        ars_dis=arcsin(minSQ**0.5/2)/(2*pi)*360*60*60
        print (ars_dis)
        if ars_dis > 0.05:
            # do something
        # Read the Av of the selected extinction point.
        Av = extinction_table[index_min, 6]
        print ("Av = {0}".format(Av))
        # Apply extinction correction on source.
        source[17]=Av
        for band in parameter:
            flux = source[band[1]]
            C_av = band[2]
            if flux<0:
                new_far_flux = flux
            if flux>=0:
                new_far_flux = flux*10**(C_av*Av/2.5)
            source[band[1]]=new_far_flux
    # Save the table
    np.savetxt("{0}_intrinsic.tbl".format(source_table_name), source_table)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
