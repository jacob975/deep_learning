#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in Gould belt region in IPAC Infrared Science Archive (IRSA) 
    to AI model readable format. 
Usage:
    tbl_to_sed_Gould_belt_2015.py [Gould belt 2015 table]
Output:
    1. The SED of sources in JHK, IRAC, and MIPS 
    2. The fake coordinate of sources.
    3. The fake Av
    4. The Quality label
    5. Source types
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190814
####################################
update log
20190814 version alpha 1:
    1. The code works.
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
        print ("tbl_to_sed_Gould_belt_2015.py [Gould belt 2015 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    print ('Load data from input table')
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    J2flux  = np.array(np.transpose([inp_table[:, 33], inp_table[:, 34]]), dtype = float)
    H2flux  = np.array(np.transpose([inp_table[:, 54], inp_table[:, 55]]), dtype = float)
    K2flux  = np.array(np.transpose([inp_table[:, 75], inp_table[:, 76]]), dtype = float)
    IR1flux = np.array(np.transpose([inp_table[:, 96], inp_table[:, 97]]), dtype = float)
    IR2flux = np.array(np.transpose([inp_table[:,117], inp_table[:,118]]), dtype = float)
    IR3flux = np.array(np.transpose([inp_table[:,138], inp_table[:,139]]), dtype = float)
    IR4flux = np.array(np.transpose([inp_table[:,159], inp_table[:,160]]), dtype = float)
    MP1flux = np.array(np.transpose([inp_table[:,180], inp_table[:,181]]), dtype = float)
    #-----------------------------------
    # Convert 2MASSflux to UKIDSSflux
    print ('Convert 2MASSflux to UKIDSSflux')
    twomass_system = convert_lib.set_twomass()
    ukirt_system = convert_lib.set_ukirt()
    J2mag   = convert_lib.ensemble_mjy_to_mag(  J2flux, 
                                                'J', 
                                                twomass_system) 
    H2mag   = convert_lib.ensemble_mjy_to_mag(  H2flux, 
                                                'H', 
                                                twomass_system) 
    K2mag   = convert_lib.ensemble_mjy_to_mag(  K2flux, 
                                                'Ks',
                                                twomass_system) 
    JUmag, HUmag, KUmag = convert_lib.ensemble_two2u(   J2mag, 
                                                        H2mag, 
                                                        K2mag)
    JUflux, eJUflux = convert_lib.ensemble_mag_to_mjy_ufloat(JUmag, 'J', ukirt_system)
    HUflux, eHUflux = convert_lib.ensemble_mag_to_mjy_ufloat(HUmag, 'H', ukirt_system)
    KUflux, eKUflux = convert_lib.ensemble_mag_to_mjy_ufloat(KUmag, 'K', ukirt_system)
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
    # coordinate, Av, source type, and Q label.
    coord = np.transpose(np.array([inp_table[:,0], inp_table[:,2]]))
    fake_Av = np.ones((len(inp_table), 2))
    # Quality flag
    J2_Q  = np.array(inp_table[:, 37])
    H2_Q  = np.array(inp_table[:, 58])
    K2_Q  = np.array(inp_table[:, 79])
    IR1_Q = np.array(inp_table[:,100])
    IR2_Q = np.array(inp_table[:,121])
    IR3_Q = np.array(inp_table[:,142])
    IR4_Q = np.array(inp_table[:,163])
    MP1_Q = np.array(inp_table[:,184])
    real_Q = np.array(np.transpose([J2_Q,
                                    H2_Q,
                                    K2_Q,
                                    IR1_Q,
                                    IR2_Q,
                                    IR3_Q,
                                    IR4_Q,
                                    MP1_Q,
                                    ]))
    source_types = np.array(inp_table[:, 16])
    #-----------------------------------
    # Save the data
    print ('Save the data')
    np.savetxt( '{0}_sed.txt'.format(inp_table_name[:-4]), flux_sed)
    np.savetxt( '{0}_coord.txt'.format(inp_table_name[:-4]), coord, fmt = '%s')
    np.savetxt( '{0}_Av.txt'.format(inp_table_name[:-4]), fake_Av, header = '# fake')
    np.savetxt( '{0}_Q.txt'.format(inp_table_name[:-4]), real_Q, fmt = '%s')
    np.savetxt( '{0}_Sp.txt'.format(inp_table_name[:-4]), source_types, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
