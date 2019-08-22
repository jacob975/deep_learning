#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of 
    Abell_1763 in 2010
    to AI model readable format. 
Usage:
    tbl_to_sed_Abell_1763_2010.py [Abell_1763 2010 table]
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
        print ("tbl_to_sed_Abell_1763_2010.py [Abell_1763 2010 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    inp_table[inp_table == 'null'] = '0.0'
    #Jmag   = np.array(np.transpose([inp_table[:,4] , inp_table[:, 5]]), dtype = float)
    #Hmag   = np.array(np.transpose([inp_table[:,6] , inp_table[:, 7]]), dtype = float)
    #Kmag   = np.array(np.transpose([inp_table[:,8] , inp_table[:, 9]]), dtype = float)
    IR1flux = np.array(np.transpose([inp_table[:,24], inp_table[:,25]])) 
    IR2flux = np.array(np.transpose([inp_table[:,32], inp_table[:,33]])) 
    IR3flux = np.array(np.transpose([inp_table[:,40], inp_table[:,41]])) 
    IR4flux = np.array(np.transpose([inp_table[:,48], inp_table[:,49]])) 
    MP1flux = np.array(np.transpose([inp_table[:, 3], inp_table[:, 4]])) 
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
    flux_sed = np.array(flux_sed, dtype = float)/1000
    print ('Arrange, done.')
    # coordinate, Av, source type, and Q label.
    coord = np.transpose(np.array([inp_table[:,1], inp_table[:,2]]))
    fake_Av = np.ones((len(inp_table), 2))
    fake_Q = np.chararray((len(inp_table), 5))
    fake_Q[:] = '--'
    fake_Q = np.array(fake_Q, dtype= str)
    #-----------------------------------
    # Save the data
    np.savetxt('Abell_1763_2010_sed.txt', flux_sed)
    np.savetxt('Abell_1763_2010_coord.txt', coord, fmt = '%s')
    np.savetxt('Abell_1763_2010_Av.txt', fake_Av, header = '# fake Av')
    np.savetxt('Abell_1763_2010_Q.txt', fake_Q, fmt = '%s', header = '# fake quality label')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
