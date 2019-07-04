#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data in Rivera-Galvez et al. (2015) to AI model readable format. 
Usage:
    tbl_to_sed_Rivera-Galvez 2015.py [Rivera-Galvez 2015 table]
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

20190630
####################################
update log
20190630 version alpha 1:
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
        print ("tbl_to_sed_Rivera-Galvez_2015.py [Rivera-Galvez 2015 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    SCAO_system = convert_lib.set_SCAO()
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    Jmag   = np.array(np.transpose([inp_table[:,4] , inp_table[:, 5]]), dtype = float)
    Hmag   = np.array(np.transpose([inp_table[:,6] , inp_table[:, 7]]), dtype = float)
    Kmag   = np.array(np.transpose([inp_table[:,8] , inp_table[:, 9]]), dtype = float)
    IR1mag = np.array(np.transpose([inp_table[:,10], inp_table[:,11]]), dtype = float)
    IR2mag = np.array(np.transpose([inp_table[:,12], inp_table[:,13]]), dtype = float)
    IR3mag = np.array(np.transpose([inp_table[:,14], inp_table[:,15]]), dtype = float)
    IR4mag = np.array(np.transpose([inp_table[:,16], inp_table[:,17]]), dtype = float)
    MP1mag = np.array(np.transpose([inp_table[:,18], inp_table[:,19]]), dtype = float)
    #-----------------------------------
    # Convert mag to flux and artifical data
    Jflux = convert_lib.ensemble_mag_to_mjy(Jmag, 'J', SCAO_system)
    Hflux = convert_lib.ensemble_mag_to_mjy(Hmag, 'H', SCAO_system)
    Kflux = convert_lib.ensemble_mag_to_mjy(Kmag, 'K', SCAO_system)
    IR1flux = convert_lib.ensemble_mag_to_mjy(IR1mag, 'IR1', SCAO_system)
    IR2flux = convert_lib.ensemble_mag_to_mjy(IR2mag, 'IR2', SCAO_system)
    IR3flux = convert_lib.ensemble_mag_to_mjy(IR3mag, 'IR3', SCAO_system)
    IR4flux = convert_lib.ensemble_mag_to_mjy(IR4mag, 'IR4', SCAO_system)
    MP1flux = convert_lib.ensemble_mag_to_mjy(MP1mag, 'MP1', SCAO_system)
    flux_sed = np.array(np.transpose([  Jflux[:,0],
                                        Hflux[:,0],
                                        Kflux[:,0],
                                        IR1flux[:,0],
                                        IR2flux[:,0],
                                        IR3flux[:,0],
                                        IR4flux[:,0],
                                        MP1flux[:,0],
                                        Jflux[:,1],
                                        Hflux[:,1],
                                        Kflux[:,1],
                                        IR1flux[:,1],
                                        IR2flux[:,1],
                                        IR3flux[:,1],
                                        IR4flux[:,1],
                                        MP1flux[:,1],
                                        ]))
    # coordinate, Av, source type, and Q label.
    coord = np.transpose(np.array([inp_table[:,0], inp_table[:,1]]))
    fake_Av = np.ones((len(inp_table), 2))
    source_type = np.zeros((len(inp_table), 3))
    source_type[:,2] = 1
    human_source_type = np.chararray(len(inp_table))
    human_source_type[:] = 'YSO'
    fake_Q = np.chararray((len(inp_table), 8))
    fake_Q[:] = 'F' # fake
    #-----------------------------------
    # Save the data
    np.savetxt('R-G_2015_sed.txt', flux_sed)
    np.savetxt('R-G_2015_coord.txt', coord, fmt = '%s')
    np.savetxt('R-G_2015_Av.txt', fake_Av)
    np.savetxt('R-G_2015_label_pred.txt', source_type)
    np.savetxt('R-G_2015_Sp.txt', human_source_type, fmt = '%s')
    np.savetxt('R-G_2015_Q.txt', fake_Q, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
