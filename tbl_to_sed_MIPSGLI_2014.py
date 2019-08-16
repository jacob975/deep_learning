#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in MIPSGLI region in IPAC Infrared Science Archive (IRSA) 
    to AI model readable format. 
Usage:
    tbl_to_sed_MIPSGLI_2014.py [MIPSGLI 2014 table]
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
        print ("tbl_to_sed_MIPSGLI_2014.py [MIPSGLI 2014 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    print ('Load data from input table')
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    inp_table[inp_table == 'null'] = '0.0'
    J2flux  = np.array(np.transpose([inp_table[:,10], inp_table[:,11]]), dtype = float)
    H2flux  = np.array(np.transpose([inp_table[:,12], inp_table[:,13]]), dtype = float)
    K2flux  = np.array(np.transpose([inp_table[:,14], inp_table[:,15]]), dtype = float)
    IR1flux = np.array(np.transpose([inp_table[:,17], inp_table[:,18]]), dtype = float)
    IR2flux = np.array(np.transpose([inp_table[:,19], inp_table[:,20]]), dtype = float)
    IR3flux = np.array(np.transpose([inp_table[:,21], inp_table[:,22]]), dtype = float)
    IR4flux = np.array(np.transpose([inp_table[:,23], inp_table[:,24]]), dtype = float)
    MP1flux = np.array(np.transpose([inp_table[:, 5], inp_table[:, 6]]), dtype = float)
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
    coord = np.transpose(np.array([inp_table[:,3], inp_table[:,4]]))
    fake_Av = np.ones((len(inp_table), 2))
    fake_Q = np.chararray((len(inp_table), 8))
    fake_Q[:] = 'F' # fake
    fake_Q = np.array(fake_Q, dtype = str)
    #-----------------------------------
    # Save the data
    print ('Save the data')
    np.savetxt( 'MIPSGLI_2014_sed.txt', flux_sed)
    np.savetxt( 'MIPSGLI_2014_coord.txt', coord, fmt = '%s')
    np.savetxt( 'MIPSGLI_2014_Av.txt', fake_Av, header = '# fake')
    np.savetxt( 'MIPSGLI_2014_Q.txt', fake_Q, fmt = '%s', header = '# fake')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
