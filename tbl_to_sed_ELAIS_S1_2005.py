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

def get_saturation_flag(flag_array, sed_array, e_sed_array):
    # Default quality 
    quality_array = np.chararray(len(flag_array))
    quality_array[:] = 'A'
    quality_array[(sed_array <= 0.0 ) | (e_sed_array <= 0.0)] = 'U'
    
    '''
    # Saturation quality
    for i, flag in enumerate(flag_array):
        if flag == 'null':
            continue
        SE_flag = int(flag[2:])
        bin_SED_flag =  bin(SE_flag)
        if len(bin_SED_flag) < 3:
            continue
        elif bin_SED_flag[-3] == '1':
            quality_array[i] = 'S'
            continue
    '''
    # Convert from char to string
    quality_array = np.array(quality_array, dtype = str)
    return quality_array

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
    IR1flux = np.array(np.transpose([inp_table[:, 9], inp_table[:,10]])) 
    IR2flux = np.array(np.transpose([inp_table[:,16], inp_table[:,17]])) 
    IR3flux = np.array(np.transpose([inp_table[:,23], inp_table[:,24]])) 
    IR4flux = np.array(np.transpose([inp_table[:,30], inp_table[:,31]])) 
    MP1flux = np.array(np.transpose([inp_table[:,37], inp_table[:,38]])) 
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
    # coordinate, Av, and Q label.
    coord = np.transpose(np.array([inp_table[:,2], inp_table[:,3]]))
    fake_Av = np.ones((len(inp_table), 2))
    IR1flag = np.array(inp_table[:,12])
    IR2flag = np.array(inp_table[:,19])
    IR3flag = np.array(inp_table[:,26])
    IR4flag = np.array(inp_table[:,33])
    MP1flag = np.array(inp_table[:,40])
    IR1sat = get_saturation_flag(IR1flag, flux_sed[:,0], flux_sed[:,5]) 
    IR2sat = get_saturation_flag(IR2flag, flux_sed[:,1], flux_sed[:,6]) 
    IR3sat = get_saturation_flag(IR3flag, flux_sed[:,2], flux_sed[:,7]) 
    IR4sat = get_saturation_flag(IR4flag, flux_sed[:,3], flux_sed[:,8]) 
    MP1sat = get_saturation_flag(MP1flag, flux_sed[:,4], flux_sed[:,9]) 
    flags = np.array(np.transpose([
                                    IR1flag,
                                    IR2flag,
                                    IR3flag,
                                    IR4flag,
                                    MP1flag,
                                    ]))
    sat_index = np.array(np.transpose([
                                        IR1sat,
                                        IR2sat,
                                        IR3sat,
                                        IR4sat,
                                        MP1sat
                                    ]))
    #-----------------------------------
    # Save the data
    np.savetxt('ELAIS_S1_Spitzer_sed.txt', flux_sed)
    np.savetxt('ELAIS_S1_coord.txt', coord, fmt = '%s')
    np.savetxt('ELAIS_S1_Av.txt', fake_Av, header = '# fake Av')
    np.savetxt('ELAIS_S1_Spitzer_Q.txt', sat_index, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
