#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of 
    Formation and Evolution of Planetary Systems (FEPS) survey (2008) 
    to AI model readable format. 
Usage:
    tbl_to_sed_FEPS_2008.py [FEPS 2008 table]
Output:
    1. The SED of sources in JHK, IRAC, and MIPS 
    2. The coordinate of sources.
    3. The fake Av
    4. The Quality label
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
        print ("tbl_to_sed_FEPS_2008.py [FEPS 2008 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    inp_table[inp_table == 'null'] = '0.0'
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
    flux_sed = np.array(flux_sed, dtype = float)
    print ('Arrange, done.')
    # coordinate, Av, source type, and Q label.
    coord = np.transpose(np.array([inp_table[:,0], inp_table[:,1]]))
    fake_Av = np.ones((len(inp_table), 2))
    fake_Q = np.chararray((len(inp_table), 5))
    fake_Q[:] = '--'
    fake_Q = np.array(fake_Q, dtype= str)
    #-----------------------------------
    # Save the data
    np.savetxt('FEPS_2008_sed.txt', flux_sed)
    np.savetxt('FEPS_2008_coord.txt', coord, fmt = '%s')
    np.savetxt('FEPS_2008_Av.txt', fake_Av, header = '# fake Av')
    np.savetxt('FEPS_2008_Q.txt', fake_Q, fmt = '%s', header = '# fake quality label')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
