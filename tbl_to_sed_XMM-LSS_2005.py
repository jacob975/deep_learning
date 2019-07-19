#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of SWIRE XMM-LSS survey (2005) to AI model readable format. 
Usage:
    tbl_to_sed_XMM-LSS_2005.py [XMM-LSS 2015 table]
Output:
    1. The SED of sources in JHK, IRAC, and MIPS 
    2. The fake coordinate of sources.
    3. The source type of sources (YSO, of course)
    4. The fake Av
    5. The Quality label
    6. Stellarity index
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
        print ("tbl_to_sed_XMM-LSS_2005.py [XMM-LSS 2015 table]")
        exit()
    inp_table_name = argv[1]
    #-----------------------------------
    # Load data from input table
    inp_table = np.loadtxt(inp_table_name, dtype = str)
    #Jmag   = np.array(np.transpose([inp_table[:,4] , inp_table[:, 5]]), dtype = float)
    #Hmag   = np.array(np.transpose([inp_table[:,6] , inp_table[:, 7]]), dtype = float)
    #Kmag   = np.array(np.transpose([inp_table[:,8] , inp_table[:, 9]]), dtype = float)
    IR1flux = np.array(np.transpose([inp_table[:, 7], inp_table[:, 8]]))
    IR2flux = np.array(np.transpose([inp_table[:,12], inp_table[:,13]]))
    IR3flux = np.array(np.transpose([inp_table[:,17], inp_table[:,18]]))
    IR4flux = np.array(np.transpose([inp_table[:,22], inp_table[:,23]]))
    MP1flux = np.array(np.transpose([inp_table[:,29], inp_table[:,30]]))
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
    print ('Arrange, done.')
    # coordinate, Av, source type, and Q label.
    coord = np.transpose(np.array([inp_table[:,2], inp_table[:,3]]))
    fake_Av = np.ones((len(inp_table), 2))
    source_type = np.zeros((len(inp_table), 3))
    source_type[:,2] = 1
    human_source_type = np.chararray(len(inp_table))
    human_source_type[:] = 'Fake'
    fake_Q = np.chararray((len(inp_table), 5))
    # Stellarity index
    stellarity_index = np.transpose(np.array([  inp_table[:, 9],
                                                inp_table[:,14],
                                                inp_table[:,19],
                                                inp_table[:,24],
                                                inp_table[:,31],
                                            ]))
    #-----------------------------------
    # Save the data
    np.savetxt('XMM-LSS_sed.txt', flux_sed, fmt = '%s')
    np.savetxt('XMM-LSS_coord.txt', coord, fmt = '%s')
    np.savetxt('XMM-LSS_Av.txt', fake_Av)
    np.savetxt('XMM-LSS_label_pred.txt', source_type)
    np.savetxt('XMM-LSS_Sp.txt', human_source_type, fmt = '%s')
    np.savetxt('XMM-LSS_Q.txt', fake_Q, fmt = '%s')
    np.savetxt('XMM-LSS_stell.txt', stellarity_index, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
