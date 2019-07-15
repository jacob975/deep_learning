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
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    Jflux   = np.array(np.transpose([inp_table[:,3] , inp_table[:, 4]]))
    Hflux   = np.array(np.transpose([inp_table[:,5] , inp_table[:, 6]]))
    Kflux   = np.array(np.transpose([inp_table[:,7] , inp_table[:, 8]]))
    IR1flux = np.array(np.transpose([inp_table[:,13], inp_table[:,14]]))
    IR2flux = np.array(np.transpose([inp_table[:,19], inp_table[:,20]]))
    IR3flux = np.array(np.transpose([inp_table[:,25], inp_table[:,26]]))
    IR4flux = np.array(np.transpose([inp_table[:,31], inp_table[:,32]]))
    MP1flux = np.array(np.transpose([inp_table[:,37], inp_table[:,38]]))
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
    coord = np.transpose(np.array([inp_table[:,1], inp_table[:,2]]))
    fake_Av = np.ones((len(inp_table), 2))
    fake_Q = np.chararray((len(inp_table), 8))
    fake_Q[:] = 'F' # fake
    #-----------------------------------
    # Save the data
    np.savetxt('Taurus_2008_sed.txt', flux_sed, fmt = '%s')
    np.savetxt('Taurus_2008_coord.txt', coord, fmt = '%s')
    np.savetxt('Taurus_2008_Av.txt', fake_Av)
    np.savetxt('Taurus_2008_Q.txt', fake_Q, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
