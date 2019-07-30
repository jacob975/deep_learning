#!/usr/bin/python3
'''
Abstract:
    This is a program for obtaining data from UKIDSS DR11. 
    Caution!!! DR11 only
Usage:
    get_ukidss_DXS_DR11.py [UKIDSS DXS table]
Output:
    1. sed table
    2. coord table
    3. distance table
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190729
####################################
update log
20190729 version alpha 1
    1. The code works.
'''
import time
import numpy as np
from sys import argv
import convert_lib

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: get_ukidss_DXS_DR11.py [UKIDSS DXS table]")
        exit()
    ukidss_table_name = argv[1]
    #-----------------------------------
    # Print the test text
    ukidss_table = np.loadtxt(  ukidss_table_name, 
                                dtype = str,
                                delimiter = ',',)
    # Take the AperMag3 as the magnitude.
    distance = np.array(ukidss_table[:, 3], dtype = float)
    Jmag = np.array(ukidss_table[:, 48:50] , dtype = float)
    Hmag = np.array(ukidss_table[:, 73:75] , dtype = float)
    Kmag = np.array(ukidss_table[:, 98:100], dtype = float)
    # Load UKIDSS bands system
    ukidss_system = convert_lib.set_ukirt()
    # Convert mag to flux.
    Jflux = convert_lib.ensemble_mag_to_mjy(Jmag, 'J', ukidss_system)
    Hflux = convert_lib.ensemble_mag_to_mjy(Hmag, 'H', ukidss_system)
    Kflux = convert_lib.ensemble_mag_to_mjy(Kmag, 'K', ukidss_system)
    sed_table = np.array(np.transpose([
                                            Jflux[:,0],
                                            Hflux[:,0],
                                            Kflux[:,0],
                                            Jflux[:,1],
                                            Hflux[:,1],
                                            Kflux[:,1]
                                            ]))
    coord_table = np.array(ukidss_table[:,8:10], dtype = str)
    dist_table = np.array(ukidss_table[:,3], dtype = str)
    saturation_table = np.array(ukidss_table[:,35], dtype = str)
    # Save the data
    np.savetxt( '{0}_sed.txt'.format(ukidss_table_name[:-4]), 
                sed_table)
    np.savetxt( '{0}_coord.txt'.format(ukidss_table_name[:-4]), 
                coord_table,
                fmt = '%s')
    np.savetxt( '{0}_dist.txt'.format(ukidss_table_name[:-4]), 
                dist_table,
                fmt = '%s')
    np.savetxt( '{0}_saturation.txt'.format(ukidss_table_name[:-4]),
                saturation_table,
                fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
