#!/usr/bin/python3
'''
Abstract:
    This is a program for remove Av and show the intrinsic flux of sources. 
    This correction can only apply on molecular cloud CHA, LUP, OPH, PER, SER
    Citations: Chapman et al. (2009)
Usage:
    remove_Av.py [band system] [extinction table] [source table] [Av table] [coord table]
    Available band systems: ukidss, twomass
    You can skip [Av table]
    Example: remove_Av.py ukidss extinction_table sed_table.txt Av.txt coord.txt
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
from sys import argv
import time
import numpy as np
from uncertainties import ufloat
from astropy.coordinates import SkyCoord
from astropy import units as u
from scipy import optimize
import matplotlib.pyplot as plt

def gaussian(x, amp, mu, sig):
    return amp * np.power(2 * np.pi , -0.5)*np.exp(-np.power(x - mu , 2.) / (2 * np.power(sig, 2.)))/sig

def find_the_closest_extinction_position(coord, extinction_table):
    # Initialize
    # Read central position of source
    source_coord = SkyCoord(coord[0], coord[1], unit = 'deg') 
    extinction_coord = SkyCoord(extinction_table[:,0], extinction_table[:,1], unit = 'deg')
    # Calculate the distance
    distance_object_array = extinction_coord.separation(source_coord)
    distance_array = distance_object_array.deg
    # Pick the nearest one
    min_distance = np.min(distance_array)
    index_min_distance = np.argmin(distance_array) 
    return min_distance, index_min_distance

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #--------------------------------------------
    # Load argv
    if len(argv) != 6:
        print ("Error!\nUsage: Remove_Av.py [band system] [extinction table] [sed table] [Av table] [coord table]") 
        print ("Available band systems: ukidss, twomass")
        print ("You can skip [Av table]")
        print ("Example: remove_Av.py ukidss extinction_table sed_table.txt Av.txt coord.txt")
        exit()
    band_system = argv[1]
    extinction_table_name = argv[2]
    sed_table_name = argv[3]
    Av_table_name = argv[4]
    coord_table_name = argv[5]
    #--------------------------------------------
    # Load data
    # The table of extinction map.
    extinction_table = np.loadtxt(extinction_table_name, dtype = float)
    extinction_table = extinction_table[~np.isnan(extinction_table[:,2])]
    # The source to be corrected
    sed_table = np.loadtxt(sed_table_name, dtype = float)
    # Av of each sources if known.
    Av_table = None
    Av_mean = None
    Av_deviation = None
    if Av_table_name != "skip":
        Av_table = np.loadtxt(Av_table_name, dtype = float)
        # Calculate the deviation of Av.
        Av_table_allOBS = Av_table[Av_table[:,0] != 0.0]
        numbers, bin_edges = np.histogram(Av_table_allOBS[:,0], np.arange(-10, 20))
        index_max = np.argmax(numbers)
        #numbers = numbers[:index_max + 1]
        bin_middles = 0.5*(bin_edges[1:] + bin_edges[:-1])
        paras, cov = optimize.curve_fit(gaussian, bin_middles[:index_max + 1], numbers[:index_max + 1], p0 = [1000, 0, 1])
        if paras[2] < np.sqrt(cov[2][2]):
            print ('The fitting seems failed.')
            exit()
        else:
            Av_mean = paras[1]
            Av_deviation = paras[2]
        # Plot the result
        Av_hist_plot = plt.figure("Av_hist fitting result")
        plt.title("Av_hist fitting result")
        plt.xlabel("Av")
        plt.ylabel("# of sources")
        plt.scatter(bin_middles[index_max + 1:], numbers[index_max + 1:], color = 'b', label = "Datapoints not for fitting")
        plt.scatter(bin_middles[:index_max + 1], numbers[:index_max + 1], color = 'r', label = "Datapoints for fitting")
        x = np.arange(-10, 10, 0.1)
        y = gaussian(x, paras[0], paras[1], paras[2])
        plt.plot(x, y, label = "Fitting result")
        plt.legend()
        Av_hist_plot.savefig("Av_hist.png")
    # coord of each sources
    coord_table = np.loadtxt(coord_table_name, dtype = float)
    # Define the extinction curves
    if band_system == 'ukidss':
        from extinction_curves_lib import WD_55B_ukidss as WD_55B
    if band_system == 'twomass':
        from extinction_curves_lib import WD_55B_twomass as WD_55B
    # The radius of an extinction region in unit degree
    tolerance_radius = 6/60
    # The list for final Av of each source
    final_Av = []
    index_no_Av = [] 
    if Av_table_name != "skip":
        for index, source in enumerate(sed_table):
            #------------------------------------------------
            # Find Av
            Av = 0.0
            err_Av = 0.0
            # If the label of source is star and Av exists, just apply it.
            if Av_table[index, 0] > Av_mean - 3 * Av_deviation:
                Av = Av_table[index, 0]
                err_Av = Av_table[index, 1]
            # Find the closest extinction position for sources.
            else:
                min_distance, index_min = find_the_closest_extinction_position(coord_table[index], extinction_table)
                if min_distance > tolerance_radius:
                    Av = 0.0
                    err_Av = 0.0
                elif extinction_table[index_min, 2] > Av_mean - 3 * Av_deviation:
                    # Read the Av of the selected extinction point.
                    Av = extinction_table[index_min, 2]
                    err_Av = extinction_table[index_min, 3]
            #------------------------------------------------
            # Apply extinction correction on source.
            if Av == 0.0:
                final_Av.append([0.0, 0.0])
                index_no_Av.append(index)
                # If extinction is not detected and not covered by extinction map
                # remove this sources
                for band in WD_55B:
                    sed_table[index,band[1]] = 0.0
                    sed_table[index,band[2]] = 0.0
            else :
                final_Av.append([Av, err_Av])
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
    elif Av_table_name == "skip":
        for index, source in enumerate(sed_table):
            #------------------------------------------------
            # Find Av
            Av = 0.0
            err_Av = 0.0
            # Find the closest extinction position for sources.
            min_distance, index_min = find_the_closest_extinction_position(coord_table[index], extinction_table)
            if min_distance > tolerance_radius:
                Av = 0.0
                err_Av = 0.0
            else:
                # Read the Av of the selected extinction point.
                Av = extinction_table[index_min, 2]
                err_Av = extinction_table[index_min, 3]
            #------------------------------------------------
            # Apply extinction correction on source.
            if Av == 0.0:
                final_Av.append([0.0, 0.0])
                index_no_Av.append(index)
                # If extinction is not detected and not covered by extinction map
                # remove this sources
                for band in WD_55B:
                    sed_table[index,band[1]] = 0.0
                    sed_table[index,band[2]] = 0.0
            else :
                final_Av.append([Av, err_Av])
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
    np.savetxt("{0}_appended_Av.txt".format(sed_table_name[:-4]), final_Av)
    np.savetxt("{0}_index_of_no_Av.txt".format(sed_table_name[:-4]), index_no_Av, fmt = '%d')
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
