#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in c2d region in IPAC Infrared Science Archive (IRSA) 
    to AI model readable format. 
Usage:
    tbl_to_sed_c2d.py [c2d table]
Output:
    1. The SED of sources in JHK, IRAC, and MIPS 
    2. The coordinate of sources.
    4. The quality label
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200423
####################################
update log
20200423 version alpha 1:
    1. The code works.
'''

def get_quality_flag(inp_Q):
    # Initialize
    out_Q = inp_Q[:]
    # Replace c2d label 'N' by our label 'X'
    out_Q[out_Q == 'N'] = 'X'
    return out_Q

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
        print ("tbl_to_sed_c2d.py [c2d table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data(XX_f_ap1) from input table
    print ('Load data from input table')
    inp_table = np.loadtxt(inp_table_name, dtype = str, comments = ['|', '\\'])
    J2flux  = np.array(np.transpose([inp_table[:, 7], inp_table[:, 8]]))
    H2flux  = np.array(np.transpose([inp_table[:,10], inp_table[:,11]]))
    K2flux  = np.array(np.transpose([inp_table[:,13], inp_table[:,14]]))
    IR1flux = np.array(np.transpose([inp_table[:,16], inp_table[:,17]]))
    IR2flux = np.array(np.transpose([inp_table[:,19], inp_table[:,20]]))
    IR3flux = np.array(np.transpose([inp_table[:,22], inp_table[:,23]]))
    IR4flux = np.array(np.transpose([inp_table[:,25], inp_table[:,26]]))
    MP1flux = np.array(np.transpose([inp_table[:,28], inp_table[:,29]]))
    # Load quality flag
    J2Q  = inp_table[:, 9]
    H2Q  = inp_table[:,12] 
    K2Q  = inp_table[:,15] 
    IR1Q = inp_table[:,18] 
    IR2Q = inp_table[:,21] 
    IR3Q = inp_table[:,24] 
    IR4Q = inp_table[:,27] 
    MP1Q = inp_table[:,30] 
    quality_label = np.array(np.transpose([
        get_quality_flag(J2Q),
        get_quality_flag(H2Q),
        get_quality_flag(K2Q),
        get_quality_flag(IR1Q),
        get_quality_flag(IR2Q),
        get_quality_flag(IR3Q),
        get_quality_flag(IR4Q),
        get_quality_flag(MP1Q)
    ]))
    # Replace 'null' with '0.0'
    J2flux[  J2flux  == 'null'] = '0.0' 
    H2flux[  H2flux  == 'null'] = '0.0' 
    K2flux[  K2flux  == 'null'] = '0.0' 
    IR1flux[ IR1flux == 'null'] = '0.0' 
    IR2flux[ IR2flux == 'null'] = '0.0' 
    IR3flux[ IR3flux == 'null'] = '0.0' 
    IR4flux[ IR4flux == 'null'] = '0.0' 
    MP1flux[ MP1flux == 'null'] = '0.0' 
    # Convert datatype from string to float
    # flux unit: mJy
    J2flux  = convert_lib.fill_up_flux_error(np.array(J2flux , dtype = float)) 
    H2flux  = convert_lib.fill_up_flux_error(np.array(H2flux , dtype = float))
    K2flux  = convert_lib.fill_up_flux_error(np.array(K2flux , dtype = float))
    IR1flux = np.array(IR1flux, dtype = float) 
    IR2flux = np.array(IR2flux, dtype = float) 
    IR3flux = np.array(IR3flux, dtype = float) 
    IR4flux = np.array(IR4flux, dtype = float) 
    MP1flux = np.array(MP1flux, dtype = float) 
    
    #-----------------------------------
    # Convert 2MASSflux to UKIDSSflux
    print ('Convert 2MASSflux to UKIDSSflux')
    twomass_system = convert_lib.set_twomass()
    ukirt_system = convert_lib.set_ukirt()
    J2mag   = convert_lib.ensemble_mjy_to_mag(  
        J2flux, 
        'J', 
        twomass_system) 
    H2mag   = convert_lib.ensemble_mjy_to_mag(  
        H2flux, 
        'H', 
        twomass_system) 
    K2mag   = convert_lib.ensemble_mjy_to_mag(  
        K2flux, 
        'Ks',
        twomass_system) 
    JUmag, HUmag, KUmag = convert_lib.ensemble_two2u(   
        J2mag, 
        H2mag, 
        K2mag)
    JUflux, eJUflux = convert_lib.ensemble_mag_to_mjy_ufloat(
        JUmag, 
        'J', 
        ukirt_system)
    HUflux, eHUflux = convert_lib.ensemble_mag_to_mjy_ufloat(
        HUmag, 
        'H', 
        ukirt_system)
    KUflux, eKUflux = convert_lib.ensemble_mag_to_mjy_ufloat(
        KUmag, 
        'K', 
        ukirt_system)
    # Form the sed table
    print ('Form the tables')
    flux_sed = np.array(np.transpose([  
        JUflux,
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
    # coordinate, Av
    coord = np.transpose(np.array([inp_table[:,3], inp_table[:,4]]))
    #-----------------------------------
    # Save the data
    print ('Save the data')
    np.savetxt( '{0}_sed.txt'.format(inp_table_name[:-4]), flux_sed)
    np.savetxt( '{0}_coord.txt'.format(inp_table_name[:-4]), coord, fmt = '%s')
    np.savetxt( '{0}_Q.txt'.format(inp_table_name[:-4]), quality_label, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
