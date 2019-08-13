#!/usr/bin/python3
'''
Abstract:
    This is a program for obtaining data from 2MASS table in GCQE format. 
Usage:
    get_twomass_GCQE.py [2MASS GCQE table]
Output:
    1. sed table
    2. coord table
    3. distance table
    4. Q table
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190731
####################################
update log
20190731 version alpha 1
    1. The code works.
'''
import time
import numpy as np
from sys import argv
import convert_lib
import replace_jhk_with_ukidss
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
        print ("Usage: get_twomass_GCQE.py [2MASS GCQE table]")
        exit()
    twomass_table_name = argv[1]
    #-----------------------------------
    # Print the test text
    print ("Loading SED data...")
    twomass_table = np.loadtxt( twomass_table_name, 
                                dtype = str)
    print ('Finished!')
    # Take the distance to the uploaded coordinate. 
    print ("Converting from 2MASSmag to UKIDSSflux...")
    dist_table = np.array(twomass_table[:,1])
    dist_table[dist_table == 'null'] = '0.0'
    dist_table = np.array(dist_table, dtype = float)
    # Take the magnitude.
    # And also replace 'null' with -999
    J2mag = np.array(twomass_table[:, 11:13], dtype = str)
    J2mag[J2mag == 'null'] = '-999'
    J2mag = np.array(J2mag, dtype = float)
    H2mag = np.array(twomass_table[:, 15:17], dtype = str)
    H2mag[H2mag == 'null'] = '-999'
    H2mag = np.array(H2mag, dtype = float)
    K2mag = np.array(twomass_table[:, 19:21], dtype = str)
    K2mag[K2mag == 'null'] = '-999'
    K2mag = np.array(K2mag, dtype = float)
    # Load UKIDSS bands system
    ukidss_system = convert_lib.set_ukirt()
    # Convert from 2MASSmag to UKIDSSmag
    JUmag, HUmag, KUmag = convert_lib.ensemble_two2u(   J2mag, 
                                                        H2mag, 
                                                        K2mag)
    # Convert from UKIDSSmag to UKIDSSflux.
    Jflux, eJflux =  replace_jhk_with_ukidss.mag_to_mjy_ufloat( JUmag, 
                                                                'J', 
                                                                dist_table, 
                                                                ukidss_system)
    Hflux, eHflux =  replace_jhk_with_ukidss.mag_to_mjy_ufloat( HUmag, 
                                                                'H', 
                                                                dist_table, 
                                                                ukidss_system)
    Kflux, eKflux =  replace_jhk_with_ukidss.mag_to_mjy_ufloat( KUmag, 
                                                                'K', 
                                                                dist_table, 
                                                                ukidss_system)
    sed_table = np.array(np.transpose([
                                            Jflux,
                                            Hflux,
                                            Kflux,
                                            eJflux,
                                            eHflux,
                                            eKflux
                                            ]))
    print ('Finished!')
    print ('Obtaining coordinate and Quality labels...')
    coord_table = np.array(twomass_table[:,5:7], dtype = str)
    Q_table = np.array(twomass_table[:,23], str)
    print ('Finished!')
    # Save the data
    print ('Saving results')
    np.savetxt( '{0}_sed.txt'.format(twomass_table_name[:-4]), 
                sed_table)
    np.savetxt( '{0}_coord.txt'.format(twomass_table_name[:-4]), 
                coord_table,
                fmt = '%s')
    np.savetxt( '{0}_dist.txt'.format(twomass_table_name[:-4]), 
                dist_table)
    np.savetxt( '{0}_Q.txt'.format(twomass_table_name[:-4]), 
                Q_table, 
                fmt = '%s')
    print ('Finished!')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
