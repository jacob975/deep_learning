#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in GGD 12-15 2014 region in IPAC Infrared Science Archive (IRSA) 
    to AI model readable format. 
Usage:
    tbl_to_sed_GGD_12-15_2014.py [GGD_12-15 2014 table]
Output:
    1. The SED of sources in JHK, IRAC, and MIPS 
    2. The fake coordinate of sources.
    3. The source type of sources (YSO, of course)
    4. The fake Av
    5. The Quality label
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
# This is a function to convert limit flag to quality flag
def limarray_to_Qarray(limarray):
    limarray = np.array(limarray)
    limarray[limarray == 'null'] = 'X' # No data 
    limarray[limarray == '='] = 'A' # Goooooooood
    limarray[limarray == '>'] = 'U' # Upper limit
    limarray[limarray == '<'] = 'S' # Saturated
    return limarray

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
        print ("tbl_to_sed_GGD_12-15_2014.py [GGD_12-15 2014 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    print ('Load data from input table')
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    # Load Quality flags
    J2Q =  limarray_to_Qarray(inp_table[:,  3])
    H2Q =  limarray_to_Qarray(inp_table[:,  6])
    K2Q =  limarray_to_Qarray(inp_table[:,  9])
    IR1Q = limarray_to_Qarray(inp_table[:, 12])
    IR2Q = limarray_to_Qarray(inp_table[:, 15])
    IR3Q = limarray_to_Qarray(inp_table[:, 18])
    IR4Q = limarray_to_Qarray(inp_table[:, 21])
    MP1Q = limarray_to_Qarray(inp_table[:, 24])
    Q_array = np.array(np.transpose([
                                        J2Q, 
                                        H2Q,
                                        K2Q,
                                        IR1Q, 
                                        IR2Q, 
                                        IR3Q,
                                        IR4Q,
                                        MP1Q,
                                        ]))
    # Load SED data
    inp_table[inp_table == 'null'] = '0.0'
    J2mag  = np.array(np.transpose([inp_table[:, 4], inp_table[:, 5]]), dtype = float) 
    H2mag  = np.array(np.transpose([inp_table[:, 7], inp_table[:, 8]]), dtype = float) 
    K2mag  = np.array(np.transpose([inp_table[:,10], inp_table[:,11]]), dtype = float) 
    IR1mag = np.array(np.transpose([inp_table[:,13], inp_table[:,14]]), dtype = float) 
    IR2mag = np.array(np.transpose([inp_table[:,16], inp_table[:,17]]), dtype = float) 
    IR3mag = np.array(np.transpose([inp_table[:,19], inp_table[:,20]]), dtype = float) 
    IR4mag = np.array(np.transpose([inp_table[:,22], inp_table[:,23]]), dtype = float) 
    MP1mag = np.array(np.transpose([inp_table[:,25], inp_table[:,26]]), dtype = float) 
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
    # coordinate, Av, source type
    coord = np.transpose(np.array([inp_table[:,1], inp_table[:,2]]))
    fake_Av = np.ones((len(inp_table), 2))
    source_type = np.array(inp_table[:, 37])
    source_type[source_type == '0'] = 'null'
    source_type[source_type == '1'] = 'YSO'
    #-----------------------------------
    # Save the data
    print ('Save the data')
    np.savetxt( 'GGD_12-15_2014_sed.txt', 
                flux_sed)
    np.savetxt( 'GGD_12-15_2014_coord.txt', 
                coord, 
                fmt = '%s')
    np.savetxt( 'GGD_12-15_2014_Av.txt', 
                fake_Av, 
                header = '# fake')
    np.savetxt( 'GGD_12-15_2014_Q.txt', 
                Q_array, 
                fmt = '%s')
    np.savetxt( 'GGD_12-15_2014_Sp.txt',
                source_type,
                fmt = '%s'
                )
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
