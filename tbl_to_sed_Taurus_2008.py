#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in Taurus region in IPAC Infrared Science Archive (IRSA) 
    to AI model readable format. 
Usage:
    tbl_to_sed_Taurus_2008.py [Taurus 2008 table]
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
        print ("tbl_to_sed_Taurus_2008.py [Taurus 2008 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    # -9 means no data available.
    # 0 means trying to measure but fail.
    # More details described in https://irsa.ipac.caltech.edu/data/SPITZER/Taurus/gator_docs/taurus_Oct2008_2.1_colDescriptions.html#i3_05px_flx
    # I choose detection with 5px, which seems containing the most detections.
    print ('Load data from input table')
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    inp_table[inp_table == '-9.000000'] = '0.0'
    inp_table[inp_table == '-999000.0'] = '0.0'
    J2flux  = np.array(np.transpose([inp_table[:, 3], inp_table[:, 4]]), dtype = float)/1000 
    H2flux  = np.array(np.transpose([inp_table[:, 5], inp_table[:, 6]]), dtype = float)/1000 
    K2flux  = np.array(np.transpose([inp_table[:, 7], inp_table[:, 8]]), dtype = float)/1000 
    IR1flux = np.array(np.transpose([inp_table[:,11], inp_table[:,12]]), dtype = float)/1000 
    IR2flux = np.array(np.transpose([inp_table[:,17], inp_table[:,18]]), dtype = float)/1000 
    IR3flux = np.array(np.transpose([inp_table[:,23], inp_table[:,24]]), dtype = float)/1000 
    IR4flux = np.array(np.transpose([inp_table[:,29], inp_table[:,30]]), dtype = float)/1000 
    MP1flux = np.array(np.transpose([inp_table[:,33], inp_table[:,34]]), dtype = float)/1000 
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
    coord = np.transpose(np.array([inp_table[:,1], inp_table[:,2]]))
    fake_Av = np.ones((len(inp_table), 2))
    source_type = np.zeros((len(inp_table), 3))
    source_type[:,0] = 1
    fake_Q = np.chararray((len(inp_table), 8))
    fake_Q[:] = 'F' # fake
    fake_Q = np.array(fake_Q, dtype = str)
    #-----------------------------------
    # Save the data
    print ('Save the data')
    np.savetxt( 'Taurus_2008_sed.txt', 
                flux_sed)
    np.savetxt( 'Taurus_2008_coord.txt', 
                coord, 
                fmt = '%s')
    np.savetxt( 'Taurus_2008_Av.txt', 
                fake_Av, 
                header = '# fake')
    np.savetxt( 'Taurus_2008_Q.txt', 
                fake_Q, 
                fmt = '%s', 
                header = '# fake')
    np.savetxt( 'Taurus_2008_c2d2007_Sp.txt',
                source_type,
                header = '# fake')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
