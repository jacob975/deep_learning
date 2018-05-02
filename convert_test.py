#!/usr/bin/python3
'''
Abstract:
    This is a program to test the convert_lib.py 
Usage:
    convert_test.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180502
####################################
update log
20180502 version alpha 1
    1. The code work
'''
import numpy as np
import convert_lib
import time

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------
    # test once a input
    ukirt_system = convert_lib.set_ukirt()
    flux_density_mJy = 0.0186
    err_flux_density_mJy = 0.0005
    print("The flux density in mJy is {0}+-{1}".format(flux_density_mJy, err_flux_density_mJy))
    
    flux_density_Jy, err_flux_density_Jy = convert_lib.mJy_to_Jy(flux_density_mJy, err_flux_density_mJy)
    print("mJy to Jy")
    print("{0:.2e}+-{1:.2e}".format(flux_density_Jy, err_flux_density_Jy))

    result_mag, result_err_mag = convert_lib.mJy_to_mag(ukirt_system['K'][2], flux_density_mJy, err_flux_density_mJy)
    print("mJy to mag")
    print("{0:.2e}+-{1:.2e}".format(result_mag, result_err_mag))
    
    result_mag, result_err_mag = convert_lib.Jy_to_mag(ukirt_system['K'][2], flux_density_Jy, err_flux_density_Jy)
    print("Jy to mag")
    print("{0:.2e}+-{1:.2e}".format(result_err_mag, result_err_mag))
    # mag to flux density
    magnitude = 15.629217
    err_magnitude = 0.004075
    print("The magnitude is {0}+-{1}".format(magnitude, err_magnitude))
    
    result_mJy, result_err_mJy = convert_lib.mag_to_mJy(ukirt_system['K'][2], magnitude, err_magnitude)
    print("mag to mJy")
    print("{0:.2e}+-{1:.2e}".format(result_mJy, result_err_mJy))

    result_Jy, result_err_Jy = convert_lib.mag_to_Jy(ukirt_system['K'][2], magnitude, err_magnitude)
    print("mag to Jy")
    print("{0:.2e}+-{1:.2e}".format(result_Jy, result_err_Jy))
    #-----------------------------------
    # test a array of input
    # flux density to mag
    flux_density_mJy_array = np.array([1.02e+00, 9.39e-01, 2.48e+00, 0.00e+00, 7.71e+01])
    err_flux_density_mJy_array = np.array([1.25e-01, 9.34e-02, 1.40e-01, 0.00e+00, 1.49e+00])
    print (flux_density_mJy_array)
    print (err_flux_density_mJy_array)

    flux_density_Jy_array, err_flux_density_Jy_array = convert_lib.mJy_to_Jy(flux_density_mJy_array, err_flux_density_mJy_array)
    print("mJy to Jy")
    print (flux_density_Jy_array)
    print (err_flux_density_Jy_array)
    
    result_mag_array, result_err_mag_array = convert_lib.mJy_to_mag(ukirt_system['K'][2], flux_density_mJy_array, err_flux_density_mJy_array)
    print("mJy to mag")
    print (result_mag_array)
    print (result_err_mag_array)
    
    result_mag_array, result_err_mag_array = convert_lib.Jy_to_mag(ukirt_system['K'][2], flux_density_Jy_array, err_flux_density_Jy_array)
    print("Jy to mag")
    print (result_mag_array)
    print (result_err_mag_array)
    
    # mag to flux density
    magnitude_array = np.array([15.626494, 0.0, 17.933249, 16.698133, 10.292841])
    err_magnitude_array = np.array([0.004088, 0.0, 0.016952, 0.009206, 0.000318])
    result_mJy_array, result_err_mJy_array = convert_lib.mag_to_mJy(ukirt_system['K'][2], magnitude_array, err_magnitude_array)
    print("mag to mJy")
    print(result_mJy_array)
    print(result_err_mJy_array)

    result_Jy_array, result_err_Jy_array = convert_lib.mag_to_Jy(ukirt_system['K'][2], magnitude_array, err_magnitude_array)
    print("mag to Jy")
    print(result_Jy_array)
    print(result_err_Jy_array)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
