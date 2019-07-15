#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of source 
    in ELAIS N2 region in IPAC Infrared Science Archive (IRSA) 
    to AI model readable format. 
Usage:
    tbl_to_sed_ELAIS_N2_2005.py [ELAIS N2 2005 table]
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
        print ("tbl_to_sed_ELAIS_N2_2005.py [ELAIS N2 2005 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    IR1flux = np.array(np.transpose([inp_table[:, 7], inp_table[:, 8]]))
    IR2flux = np.array(np.transpose([inp_table[:,12], inp_table[:,13]]))
    IR3flux = np.array(np.transpose([inp_table[:,17], inp_table[:,18]]))
    IR4flux = np.array(np.transpose([inp_table[:,22], inp_table[:,23]]))
    MP1flux = np.array(np.transpose([inp_table[:,27], inp_table[:,28]]))
    flux_sed = np.array(np.transpose([  
                                        IR1flux[:,0],
                                        IR2flux[:,0],
                                        IR3flux[:,0],
                                        IR4flux[:,0],
                                        MP1flux[:,0],
                                        IR1flux[:,1],
                                        IR2flux[:,1],
                                        IR3flux[:,1],
                                        IR4flux[:,1],
                                        MP1flux[:,1],
                                        ]))
    # coordinate, Av, source type, and Q label.
    coord = np.transpose(np.array([inp_table[:,2], inp_table[:,3]]))
    fake_Av = np.zeros((len(inp_table), 2))
    fake_Q = np.chararray((len(inp_table), 8))
    fake_Q[:] = 'F' # fake
    #-----------------------------------
    # Save the data
    np.savetxt('ELAIS_N1_2005_sed.txt', flux_sed, fmt = '%s')
    np.savetxt('ELAIS_N1_2005_coord.txt', coord, fmt = '%s')
    np.savetxt('ELAIS_N1_2005_Av.txt', fake_Av)
    np.savetxt('ELAIS_N1_2005_Q.txt', fake_Q, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
