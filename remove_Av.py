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
from uncertainties import ufloat

def find_the_closest_extinction_position(source, extinction_table):
    # Initialize
    # Read central position of source
    RA_degree  = float(source[2])
    DEC_degree = float(source[4])
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
    if len(argv) != 3:
        print ("Error!\nUsage: Remove_Av.py [extinction table] [source table]") 
        print ("Example: Remove_Av.py extinction_table source_table.tbl")
        exit()
    extinction_table_name = argv[1]
    source_table_name = argv[2]
    #--------------------------------------------
    # Load data
    # The table of extinction map.
    extinction_table = np.loadtxt(extinction_table_name, dtype = float, comments = "#")
    # The source to be corrected
    source_table = np.loadtxt(source_table_name, dtype = object, skiprows = 7,comments = "#")
    intrinsic_source_table = source_table[:] 
    # Define the extinction curves
    from extinction_curves_lib import WD_31B, WD_55B
    for index, source in enumerate(intrinsic_source_table):
        #------------------------------------------------
        # Find Av
        Av = 0.0
        err_Av = 0.0
        # If the label of source is star and Av exists, just apply it.
        print (source[14])
        if source[14] == 'star' and Av != -9.99e02:
            Av = float(source[15])
            err_Av = float(source[16])
        # Find the closest extinction position for sources.
        else:
            min_distance, index_min = find_the_closest_extinction_position(source, extinction_table)
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
                intrinsic_source_table[index, 16] = Av
                intrinsic_source_table[index, 17] = err_Av
        print ("Av = {0}".format(Av))
        #------------------------------------------------
        # Apply extinction correction on source.
        if Av == 0.0 or Av == -9.99e+02:
            continue
        elif Av > 1.0:
            for band in WD_55B:
                flux = float(source[band[1]])
                err_flux = float(source[band[2]])
                C_av = band[3]
                # If both flux and Av are valid, apply it!
                if flux > 0.0 and err_flux > 0.0:
                    # error propagation are needed
                    uflux = ufloat(flux, err_flux)
                    uAv   = ufloat(Av  , err_Av)
                    intrinsic_flux = uflux*10**(C_av*uAv/2.5)
                    intrinsic_source_table[index, band[1]] = intrinsic_flux.n
                    intrinsic_source_table[index, band[2]] = intrinsic_flux.s
        elif Av < 1.0 and Av > 0.0:
            for band in WD_31B:
                flux = float(source[band[1]])
                err_flux = float(source[band[2]])
                C_av = band[3]
                # If both flux and Av are valid, apply it!
                if flux > 0.0 and err_flux > 0.0:
                    # error propagation are needed
                    uflux = ufloat(flux, err_flux)
                    uAv   = ufloat(Av  , err_Av)
                    intrinsic_source_table[index, band[1]] = intrinsic_flux.n
                    intrinsic_source_table[index, band[2]] = intrinsic_flux.s
    # Save the table
    np.savetxt("{0}_intrinsic.tbl".format(source_table_name), intrinsic_source_table)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
