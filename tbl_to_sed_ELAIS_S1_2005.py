#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of SWIRE ELAIS S1 survey (2005) to AI model readable format. 
Usage:
    tbl_to_sed_ELAIS_S1_2005.py [ELAIS S1 2005 table]
Output:
    1. The SED of sources in JHK, IRAC, and MIPS 
    2. The coordinate of sources.
    3. The fake source type
    4. The fake Av
    5. The Quality label
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190719
####################################
update log
20190719 version alpha 1:
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
        print ("tbl_to_sed_ELAIS_S1_2005.py [ELAIS_S1 2005 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    inp_table[inp_table == '-99.00'] = 'null'
    inp_table[inp_table == '-99.0'] = 'null'
    #Jmag   = np.array(np.transpose([inp_table[:,4] , inp_table[:, 5]]), dtype = float)
    #Hmag   = np.array(np.transpose([inp_table[:,6] , inp_table[:, 7]]), dtype = float)
    #Kmag   = np.array(np.transpose([inp_table[:,8] , inp_table[:, 9]]), dtype = float)
    IR1flux = np.array(np.transpose([inp_table[:, 2], inp_table[:, 3]])) 
    IR2flux = np.array(np.transpose([inp_table[:, 4], inp_table[:, 5]])) 
    IR3flux = np.array(np.transpose([inp_table[:, 6], inp_table[:, 7]])) 
    IR4flux = np.array(np.transpose([inp_table[:, 8], inp_table[:, 9]])) 
    MP1flux = np.array(np.transpose([inp_table[:,10], inp_table[:,11]])) 
    print ('Loading, done.')
    flux_sed = np.array(np.transpose([  
                                        #Jflux[:,0],
                                        #Hflux[:,0],
                                        #Kflux[:,0],
                                        IR1flux[:,0],
                                        IR2flux[:,0],
                                        IR3flux[:,0],
                                        IR4flux[:,0],
                                        MP1flux[:,0],
                                        #Jflux[:,1],
                                        #Hflux[:,1],
                                        #Kflux[:,1],
                                        IR1flux[:,1],
                                        IR2flux[:,1],
                                        IR3flux[:,1],
                                        IR4flux[:,1],
                                        MP1flux[:,1],
                                        ]))
    flux_sed[flux_sed == 'null'] = '0.0'
    flux_sed = np.array(flux_sed, dtype = float)/1000
    print ('Arrange, done.')
    # coordinate, Av, source type, and Q label.
    coord = np.transpose(np.array([inp_table[:,0], inp_table[:,1]]))
    fake_Av = np.ones((len(inp_table), 2))
    source_type = np.zeros((len(inp_table), 3))
    source_type[:,0] = 1
    fake_Q = np.chararray((len(inp_table), 5))
    fake_Q[:] = 'A'
    fake_Q = np.array(fake_Q, dtype= str)
    #-----------------------------------
    # Save the data
    np.savetxt('ELAIS_S1_sed.txt', flux_sed)
    np.savetxt('ELAIS_S1_coord.txt', coord, fmt = '%s')
    np.savetxt('ELAIS_S1_c2d2007_Sp.txt', source_type, header = '# fake source type')
    np.savetxt('ELAIS_S1_Av.txt', fake_Av, header = '# fake Av')
    np.savetxt('ELAIS_S1_Q.txt', fake_Q, fmt = '%s', header = '# fake quality label')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
