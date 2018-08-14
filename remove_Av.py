#!/usr/bin/python3
'''
Abstract:
    This is a program for remove Av and show the intrinsic flux of sources. 
    This correction can only apply on molecular cloud CHA, LUP, OPH, PER, SER
    Citations: Chapman et al. (2009)
Usage:
    remove_Av.py [extinction table] [source table] [Av table] [coord table]
    Example: remove_Av.py extinction_table sed_table.txt Av.txt coord.txt
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
from uncertainties import ufloat

def find_the_closest_extinction_position(coord, extinction_table):
    # Initialize
    # Read central position of source
    RA_degree  = coord[0]
    DEC_degree = coord[1]
    # Convert degree to radian
    RA_enoch  = RA_degree/360*2*pi
    DEC_enoch = DEC_degree/360*2*pi
    # The radius of an extinction region in unit degree
    tolerance_radius = 0.05
    RA_ca  = np.divide(extinction_table[:,0], 360) * 2 * pi
    DEC_ca = np.divide(extinction_table[:,1], 360) * 2 * pi
    diff_X = np.cos(RA_enoch) * np.cos(DEC_enoch) - np.cos(RA_ca) * np.cos(DEC_ca) 
    diff_Y = np.cos(RA_enoch) * np.sin(DEC_enoch) - np.cos(RA_ca) * np.sin(DEC_ca)
    diff_Z = np.sin(DEC_enoch) * np.sin(DEC_ca)
    distance_array = np.sqrt(np.power(diff_X, 2) + np.power(diff_Y, 2) + np.power(diff_Z, 2))
    min_square_distance = np.min(distance_array)
    index_min_square_distance = np.argmin(distance_array) 
    return min_square_distance, index_min_square_distance

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #--------------------------------------------
    # Load argv
    if len(argv) != 5:
        print ("Error!\nUsage: Remove_Av.py [extinction table] [sed table] [Av table] [coord table]") 
        print ("Example: remove_Av.py extinction_table sed_table.txt Av.txt coord.txt")
        exit()
    extinction_table_name = argv[1]
    sed_table_name = argv[2]
    Av_table_name = argv[3]
    coord_table_name = argv[4]
    #--------------------------------------------
    # Load data
    # The table of extinction map.
    extinction_table = np.loadtxt(extinction_table_name, dtype = float)
    # The source to be corrected
    sed_table = np.loadtxt(sed_table_name, dtype = float)
    # Av of each sources if known.
    Av_table = np.loadtxt(Av_table_name, dtype = float)
    # coord of each sources
    coord_table = np.loadtxt(coord_table_name, dtype = float)
    # Define the extinction curves
    from extinction_curves_lib import WD_55B
    for index, source in enumerate(sed_table):
        #------------------------------------------------
        # Find Av
        Av = 0.0
        err_Av = 0.0
        # If the label of source is star and Av exists, just apply it.
        if Av_table[index, 0] > 0.0:
            Av = Av_table[index, 0]
            err_Av = Av_table[index, 1]
        # Find the closest extinction position for sources.
        else:
            Av_table[index, 0] = 0.0 
            Av_table[index, 1] = 0.0
            min_distance, index_min = find_the_closest_extinction_position(coord_table[index], extinction_table)
            # Show angular size, the distance in arc second.
            # This equation might be wrong
            ars_dis=arcsin(min_distance/2)/(2*pi)*360*60*60
            if ars_dis > 0.05:
                Av = 0.0
                err_Av = 0.0
            else:
                # Read the Av of the selected extinction point.
                Av = extinction_table[index_min, 6]
                err_Av = extinction_table[index_min, 7]
                Av_table[index, 0] = Av
                Av_table[index, 1] = err_Av
        #------------------------------------------------
        # Apply extinction correction on source.
        if Av == 0.0:
            continue
        else :
            for band in WD_55B:
                flux = source[band[1]]
                err_flux = source[band[2]]
                C_av = band[3]
                # If both flux and Av are valid, apply it!
                if flux > 0.0 and err_flux > 0.0:
                    # error propagation are needed
                    uflux = ufloat(flux, err_flux)
                    uAv   = ufloat(Av  , err_Av)
                    intrinsic_flux = uflux*10**(C_av*uAv/2.5)
                    sed_table[index, band[1]] = intrinsic_flux.n
                    sed_table[index, band[2]] = intrinsic_flux.s
    # Save the table
    np.savetxt("{0}_intrinsic.txt".format(sed_table_name[:-4]), sed_table)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
