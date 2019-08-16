#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in GLIMPSE I region in IPAC Infrared Science Archive (IRSA) 
    to AI model readable format. 
Usage:
    tbl_to_sed_GLIMPSE_I_2007.py [GLIMPSE I 2007 table]
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
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("tbl_to_sed_GLIMPSE_I_2007.py [GLIMPSE I 2007 table] [MIPSEGAL 2014 table]")
        exit()
    inp_table_name = argv[1]
    mips_table_name = argv[2]
    #-----------------------------------
    # Load data from input table
    print ('Load data from input table')
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    inp_table[inp_table == '-9.999E+02'] = '0.000E+00'
    mips_table = np.loadtxt(mips_table_name, dtype = str)
    J2flux  = np.array(np.transpose([inp_table[:, 27], inp_table[:, 28]]), dtype = float)
    H2flux  = np.array(np.transpose([inp_table[:, 29], inp_table[:, 30]]), dtype = float)
    K2flux  = np.array(np.transpose([inp_table[:, 31], inp_table[:, 32]]), dtype = float)
    IR1flux = np.array(np.transpose([inp_table[:, 33], inp_table[:, 34]]), dtype = float)
    IR2flux = np.array(np.transpose([inp_table[:, 35], inp_table[:, 36]]), dtype = float)
    IR3flux = np.array(np.transpose([inp_table[:, 37], inp_table[:, 38]]), dtype = float)
    IR4flux = np.array(np.transpose([inp_table[:, 39], inp_table[:, 40]]), dtype = float)
    # Find MIPS 1 detectoin from MIPSGAL
    GLIname_array = np.array(inp_table[:, 1])
    MIPSGAL_GLIname_array = np.array(mips_table[:, 16])
    MP1flux = np.zeros(IR4flux.shape)
    tot_num = len(GLIname_array)
    for i, GLI_name in enumerate(GLIname_array):
        if i%1000 == 0:
            print ("({0}/{1})".format(i, tot_num))
        matched_index = np.where(MIPSGAL_GLIname_array == GLI_name)
        if len(matched_index[0]) == 1: 
            MP1flux[i, 0] = float(mips_table[matched_index[0][0], 5])
            MP1flux[i, 1] = float(mips_table[matched_index[0][0], 6])
    MP1flux = np.array(MP1flux, dtype = float)
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
    coord = np.transpose(np.array([inp_table[:,8], inp_table[:,9]]))
    fake_Av = np.ones((len(inp_table), 2))
    # Quality flag
    fake_Q = np.chararray((tot_num, 8))
    fake_Q[:] = 'F'
    fake_Q = np.array(fake_Q)
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
