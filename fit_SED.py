#!/usr/bin/python3
'''
Abstract:
    This is a program for :
    1. Choose a source and corresponding Av.
    2. Find the most suitable template for that source.
    3. Save result
Usage:
    fit_SED.py [SED table] [Av table] [Star template]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190308
####################################
update log
20190308 version alpha 1:
    1. The code works.
'''
import matplotlib.pyplot as plt
import time
import numpy as np
from scipy import optimize
from scipy.stats import chisquare
from sys import argv
from extinction_curves_lib import WD_55B_ukidss as WD_55B
from uncertainties import ufloat

def apply_Av(source, Av):
    ans_source = np.zeros(source.shape)
    for band in WD_55B:
        flux = source[band[1]]
        C_av = band[3]
        # If both flux and Av are valid, apply it!
        if flux > 0.0:
            # error propagation are needed
            ans_source[band[1]] = flux*10**(C_av*Av/-2.5)
    return ans_source

# Find the best fit of this template
def minimum_chi(source, template):
    # Initialize
    x_linspace = np.logspace(-1, 1, 200)
    ratios = x_linspace * source[2]
    table = np.outer(ratios, template)
    chi, p = chisquare(source, f_exp = table, axis = 1)
    index = np.argmin(chi)
    ref_chi = chi[index]
    ref_p = p[index]
    ref_ratio = ratios[index]
    return ref_chi, ref_p, ref_ratio

# Find the best template of this observation data.
def find_best_template(source, templates, Av):
    # Initialize 
    index = 0
    ref_chi = -1
    ref_ratio = 0
    match_template = None
    # Take each row, calculate the chi-square value.
    for i in range(len(templates)):
        selected_template = templates[i]
        selected_template = apply_Av(selected_template, Av[0])
        chi, p, ratio = minimum_chi(source[:8], selected_template)
        # If better, take it
        if ref_chi == -1 or ref_chi > chi:
            index = i
            ref_chi = chi
            ref_ratio = ratio
            match_template = ratio * selected_template
    return index, ref_chi, match_template

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 4:
        print ('The number of arguments is wrong.')
        print ('fit_SED.py [SED table] [Av table] [Star template]')
        print ('fit_SED.py sed_table.txt Av_table.txt, star_template.txt')
        exit()
    sed_table_name = argv[1]
    Av_table_name = argv[2]
    star_template_name = argv[3]
    #-----------------------------------
    # Load data
    sed_table = np.loadtxt(sed_table_name)
    Av_table = np.loadtxt(Av_table_name)
    # Load the star template
    star_template = np.loadtxt(star_template_name, dtype = str)
    stage = star_template[:,0]
    Spectral_type = star_template[:,1]
    SED_template = np.array(star_template[:,2:], dtype = float)
    #-----------------------------------
    # Calculation
    spectral_type_table = []
    ans_template = []
    # Fitting template with near-infrared data and given temprature.
    for index, source in enumerate(sed_table):
        # Find the matched SED spectrum
        index, \
        chi, \
        given_template= find_best_template( source, 
                                            SED_template,
                                            Av_table[index]) 
        ans_template.append(given_template) 
        spectral_type_table.append(Spectral_type[index])
    ans_template = np.array(ans_template)
    spectral_type_table = np.array(spectral_type_table)
    # Save the answer
    np.savetxt("best_template.txt", ans_template)
    np.savetxt("spec_type_table.txt", spectral_type_table, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
