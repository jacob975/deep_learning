#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in Cygnus_X 2011 region in IPAC Infrared Science Archive (IRSA) 
    to AI model readable format. 
Usage:
    tbl_to_sed_Cygnus_X_2011.py [Cygnus_X 2011 table]
Output:
    1. The SED of sources in JHK, IRAC, and MIPS 
    2. The fake coordinate of sources.
    3. The fake Av
    4. The fake quality label
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190705
####################################
update log
20190705 version alpha 1:
    1. The code works.
20190801 version alpha 2:
    1. convert uJy to mJy
    2. convert 2MASSflux to UKIDSSflux
'''

import time
import numpy as np
from sys import argv
import sys
import convert_lib
np.set_printoptions(threshold=sys.maxsize)
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
        print ("tbl_to_sed_Cygnus_X_2011.py [Cygnus_X 2011 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    print ('Load data from input table')
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    # Load SED data
    inp_table[inp_table == 'null'] = '0.0'
    J2mag  = np.array(np.transpose([inp_table[:,18], inp_table[:,25]]), dtype = float) 
    H2mag  = np.array(np.transpose([inp_table[:,19], inp_table[:,26]]), dtype = float) 
    K2mag  = np.array(np.transpose([inp_table[:,20], inp_table[:,27]]), dtype = float) 
    IR1mag = np.array(np.transpose([inp_table[:,21], inp_table[:,28]]), dtype = float) 
    IR2mag = np.array(np.transpose([inp_table[:,22], inp_table[:,29]]), dtype = float) 
    IR3mag = np.array(np.transpose([inp_table[:,23], inp_table[:,30]]), dtype = float) 
    IR4mag = np.array(np.transpose([inp_table[:,24], inp_table[:,31]]), dtype = float) 
    MP1mag = np.array(np.transpose([inp_table[:,34], inp_table[:,35]]), dtype = float) 
    #-----------------------------------
    # Convert 2MASSflux to UKIDSSflux
    print ('Convert 2MASSmag to UKIDSSflux')
    ukirt_system = convert_lib.set_ukirt()
    spitzer_system = convert_lib.set_spitzer()
    JUmag, HUmag, KUmag = convert_lib.ensemble_two2u(   J2mag, 
                                                        H2mag, 
                                                        K2mag)
    JUflux, eJUflux = convert_lib.ensemble_mag_to_mjy_ufloat(JUmag, 'J', ukirt_system)
    HUflux, eHUflux = convert_lib.ensemble_mag_to_mjy_ufloat(HUmag, 'H', ukirt_system)
    KUflux, eKUflux = convert_lib.ensemble_mag_to_mjy_ufloat(KUmag, 'K', ukirt_system)
    # Convert Spitzermag to Spitzerflux
    IR1flux = convert_lib.ensemble_mag_to_mjy(IR1mag, 'IR1', spitzer_system)
    IR2flux = convert_lib.ensemble_mag_to_mjy(IR2mag, 'IR2', spitzer_system)
    IR3flux = convert_lib.ensemble_mag_to_mjy(IR3mag, 'IR3', spitzer_system)
    IR4flux = convert_lib.ensemble_mag_to_mjy(IR4mag, 'IR4', spitzer_system)
    MP1flux = convert_lib.ensemble_mag_to_mjy(MP1mag, 'MP1', spitzer_system)
    # Form the sed table
    print ('Form the tables')
    flux_sed = np.array(np.transpose([  JUflux,
                                        HUflux,
                                        KUflux,
                                        IR1flux[:,0],
                                        IR2flux[:,0],
                                        IR3flux[:,0],
                                        IR4flux[:,0],
                                        MP1flux[:,0],
                                        eJUflux,
                                        eHUflux,
                                        eKUflux,
                                        IR1flux[:,1],
                                        IR2flux[:,1],
                                        IR3flux[:,1],
                                        IR4flux[:,1],
                                        MP1flux[:,1],
                                        ]))
    # coordinate, Av, source type, Q label
    coord = np.transpose(np.array([inp_table[:,0], inp_table[:,1]]))
    fake_Av = np.ones((len(inp_table), 2))
    fake_Q = np.chararray((len(inp_table), 8))
    fake_Q[:] = '--'
    fake_Q = np.array(fake_Q, dtype = str)
    #-----------------------------------
    # Save the data
    print ('Save the data')
    np.savetxt( '{0}_sed.txt'.format(inp_table_name[:-4]), flux_sed)
    np.savetxt( '{0}_coord.txt'.format(inp_table_name[:-4]), coord, fmt = '%s')
    np.savetxt( '{0}_Av.txt'.format(inp_table_name[:-4]), fake_Av, header = '# fake')
    np.savetxt( '{0}_Q.txt'.format(inp_table_name[:-4]), fake_Q, fmt = '%s', header = '# fake')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
