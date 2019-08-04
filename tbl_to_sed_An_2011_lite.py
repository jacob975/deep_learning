#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data in An et al. (2011) to AI model readable format. 
Usage:
    tbl_to_sed_An_2011.py [An 2011 table]
Output:
    1. The SED of sources in JHK, IRAC, and MIPS 
    2. The fake coordinate of sources.
    3. The source type of sources (YSO, of course)
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190630
####################################
update log
20190630 version alpha 1:
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
        print ("tbl_to_sed_An_2011.py [An 2011 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    SCAO_system = convert_lib.set_SCAO()
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    JUmag = np.array(np.transpose([inp_table[:,4], inp_table[:,5]]), dtype = float)
    HUmag = np.array(np.transpose([inp_table[:,6], inp_table[:,7]]), dtype = float)
    KUmag = np.array(np.transpose([inp_table[:,8], inp_table[:,9]]), dtype = float)
    IR1mag = np.array(inp_table[:,10], dtype = float)
    IR2mag = np.array(inp_table[:,11], dtype = float) 
    IR3mag = np.array(inp_table[:,12], dtype = float) 
    IR4mag = np.array(inp_table[:,13], dtype = float) 
    MP1mag = np.array(inp_table[:,14], dtype = float) 
    #-----------------------------------
    JUflux = convert_lib.ensemble_mag_to_mjy(JUmag, 'J', SCAO_system)
    HUflux = convert_lib.ensemble_mag_to_mjy(HUmag, 'H', SCAO_system)
    KUflux = convert_lib.ensemble_mag_to_mjy(KUmag, 'K', SCAO_system)
    IR1flux = convert_lib.mag_to_mJy_noerr(SCAO_system['IR1'][2], IR1mag)
    IR1err = IR1flux*0.047
    IR2flux = convert_lib.mag_to_mJy_noerr(SCAO_system['IR2'][2], IR2mag)
    IR2err = IR2flux*0.047
    IR3flux = convert_lib.mag_to_mJy_noerr(SCAO_system['IR3'][2], IR3mag)
    IR3err = IR3flux*0.047
    IR4flux = convert_lib.mag_to_mJy_noerr(SCAO_system['IR4'][2], IR4mag)
    IR4err = IR4flux*0.047
    MP1flux = []
    for mag in MP1mag:
        if mag == 0:
            MP1flux.append(0.0) 
        else:
            flux = convert_lib.mag_to_mJy_noerr(SCAO_system['MP1'][2], mag)
            MP1flux.append(flux) 
    MP1flux = np.array(MP1flux)
    MP1err = MP1flux*0.095
    flux_sed = np.array(np.transpose([  JUflux[:,0],
                                        HUflux[:,0],
                                        KUflux[:,0],
                                        IR1flux,
                                        IR2flux,
                                        IR3flux,
                                        IR4flux,
                                        MP1flux,
                                        JUflux[:,1],
                                        HUflux[:,1],
                                        KUflux[:,1],
                                        IR1err,
                                        IR2err,
                                        IR3err,
                                        IR4err,
                                        MP1err,
                                        ]))
    # fake coordinate
    fake_coord = np.ones((len(inp_table), 2))
    source_type = np.zeros((len(inp_table), 3))
    source_type[:,2] = 1
    #-----------------------------------
    # Save the data
    np.savetxt('An_2011_sed.txt', flux_sed)
    np.savetxt('An_2011_Sp.txt', source_type)
    np.savetxt('An_2011_coord.txt', fake_coord)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
