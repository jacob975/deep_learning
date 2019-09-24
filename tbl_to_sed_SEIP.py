#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in SEIP region in IPAC Infrared Science Archive (IRSA) 
    to AI model readable format. 
Usage:
    tbl_to_sed_SEIP.py [SEIP table]
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

def get_quality_flag(flux, e_flux, upper, ftype):
    num_row = len(flux)
    Q = np.chararray(num_row)
    Q[:] = 'X'
    Q[upper != 'null'] = 'U'
    #Q[(flux != 'null') & (e_flux != 'null')]  = 'A'
    Q[flux != 'null'] = 'A'
    Q = np.array(Q, dtype = str)
    if len(ftype) == 0:
        pass
    else:
        ftype[ftype == 'null'] = '-1'
        ftype_int = np.array(ftype, dtype = int)
        Q[ftype_int > 0] = 'S'
    return Q

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
        print ("tbl_to_sed_SEIP.py [SEIP table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data(XX_f_ap1) from input table
    print ('Load data from input table')
    inp_table = np.loadtxt(inp_table_name, dtype = str, comments = ['|', '\\'])
    J2flux  = np.array(np.transpose([inp_table[:,114], inp_table[:,115]]))
    H2flux  = np.array(np.transpose([inp_table[:,116], inp_table[:,117]]))
    K2flux  = np.array(np.transpose([inp_table[:,118], inp_table[:,119]]))
    IR1flux = np.array(np.transpose([inp_table[:, 25], inp_table[:, 26]]))
    IR2flux = np.array(np.transpose([inp_table[:, 35], inp_table[:, 36]]))
    IR3flux = np.array(np.transpose([inp_table[:, 45], inp_table[:, 46]]))
    IR4flux = np.array(np.transpose([inp_table[:, 55], inp_table[:, 56]]))
    MP1flux = np.array(np.transpose([inp_table[:, 65], inp_table[:, 66]]))
    # Load band-fill data(XX_f_ap1_bf) from input table
    #J2upper  = np.array(np.transpose([inp_table[:, 27], inp_table[:, 28]]))
    #H2upper  = np.array(np.transpose([inp_table[:, 29], inp_table[:, 30]]))
    #K2upper  = np.array(np.transpose([inp_table[:, 31], inp_table[:, 32]]))
    IR1upper = np.array(np.transpose([inp_table[:, 29], inp_table[:, 30]]))
    IR2upper = np.array(np.transpose([inp_table[:, 39], inp_table[:, 40]]))
    IR3upper = np.array(np.transpose([inp_table[:, 49], inp_table[:, 50]]))
    IR4upper = np.array(np.transpose([inp_table[:, 59], inp_table[:, 60]]))
    MP1upper = np.array(np.transpose([inp_table[:, 69], inp_table[:, 70]]))
    # Load quality flag
    IR1type = np.array(inp_table[:,21])
    IR2type = np.array(inp_table[:,22])
    IR3type = np.array(inp_table[:,23])
    IR4type = np.array(inp_table[:,24])
    
    fake_upper = np.zeros(len(inp_table))
    J2Q  = get_quality_flag( J2flux[:,0],  J2flux[:,1], fake_upper, []) 
    H2Q  = get_quality_flag( H2flux[:,0],  H2flux[:,1], fake_upper, []) 
    K2Q  = get_quality_flag( K2flux[:,0],  K2flux[:,1], fake_upper, []) 
    IR1Q = get_quality_flag(IR1flux[:,0], IR1flux[:,1], IR1upper[:,0], IR1type) 
    IR2Q = get_quality_flag(IR2flux[:,0], IR2flux[:,1], IR2upper[:,0], IR2type) 
    IR3Q = get_quality_flag(IR3flux[:,0], IR3flux[:,1], IR3upper[:,0], IR3type) 
    IR4Q = get_quality_flag(IR4flux[:,0], IR4flux[:,1], IR4upper[:,0], IR4type) 
    MP1Q = get_quality_flag(MP1flux[:,0], MP1flux[:,1], MP1upper[:,0], []) 
    quality_label = np.array(np.transpose([
                                            J2Q,
                                            H2Q,
                                            K2Q,
                                            IR1Q,
                                            IR2Q,
                                            IR3Q,
                                            IR4Q,
                                            MP1Q
                                            ]))
    # Merge band-fill data and real data
    IR1flux[IR1flux == 'null'] = IR1upper[IR1flux == 'null']
    IR2flux[IR2flux == 'null'] = IR2upper[IR2flux == 'null']
    IR3flux[IR3flux == 'null'] = IR3upper[IR3flux == 'null']
    IR4flux[IR4flux == 'null'] = IR4upper[IR4flux == 'null']
    MP1flux[MP1flux == 'null'] = MP1upper[MP1flux == 'null']
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
    J2flux  = convert_lib.fill_up_flux_error(np.array(J2flux , dtype = float)/1000.0) 
    H2flux  = convert_lib.fill_up_flux_error(np.array(H2flux , dtype = float)/1000.0)
    K2flux  = convert_lib.fill_up_flux_error(np.array(K2flux , dtype = float)/1000.0)
    IR1flux = np.array(IR1flux, dtype = float)/1000.0 
    IR2flux = np.array(IR2flux, dtype = float)/1000.0 
    IR3flux = np.array(IR3flux, dtype = float)/1000.0 
    IR4flux = np.array(IR4flux, dtype = float)/1000.0 
    MP1flux = np.array(MP1flux, dtype = float)/1000.0 
    
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
    # coordinate, Av
    coord = np.transpose(np.array([inp_table[:,4], inp_table[:,5]]))
    fake_Av = np.ones((len(inp_table), 2))
    #-----------------------------------
    # Save the data
    print ('Save the data')
    np.savetxt( '{0}_sed.txt'.format(inp_table_name[:-4]), flux_sed)
    np.savetxt( '{0}_coord.txt'.format(inp_table_name[:-4]), coord, fmt = '%s')
    np.savetxt( '{0}_Av.txt'.format(inp_table_name[:-4]), fake_Av, header = '# fake')
    np.savetxt( '{0}_Q.txt'.format(inp_table_name[:-4]), quality_label, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
