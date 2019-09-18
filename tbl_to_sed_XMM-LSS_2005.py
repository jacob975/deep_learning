#!/usr/bin/python3
'''
Abstract:
    This is a program for convert the SED data of SWIRE XMM-LSS survey (2005) to AI model readable format. 
Usage:
    tbl_to_sed_XMM-LSS_2005.py [XMM-LSS 2005 table]
Output:
    1. The SED of sources in JHK, IRAC, and MIPS 
    2. The coordinate of sources.
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

def get_saturation_flag(flag_array):
    # Default quality 
    quality_array = np.chararray(len(flag_array))
    quality_array[:] = 'A'
    # Saturation quality
    for i, flag in enumerate(flag_array):
        if flag == 'null':
            quality_array[i] = 'X'
            continue 
        SE_flag = int(flag[2:])
        bin_SED_flag =  bin(SE_flag)
        if len(bin_SED_flag) < 3:
            continue
        elif bin_SED_flag[-3] == '1':
            quality_array[i] = 'S'
            continue
    # Convert from char to string
    quality_array = np.array(quality_array, dtype = str)
    return quality_array

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
        print ("tbl_to_sed_XMM-LSS_2005.py [XMM-LSS 2005 table]")
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
    flux_sed[flux_sed == 'null'] = '0.0'
    flux_sed = np.array(flux_sed, dtype = float)/1000
    print ('Arrange, done.')
    # coordinate, Av, source type, and Q label.
    coord = np.transpose(np.array([inp_table[:,2], inp_table[:,3]]))
    fake_Av = np.ones((len(inp_table), 2))
    # Flag and saturation index
    IR1flag = np.array(inp_table[:,10])
    IR2flag = np.array(inp_table[:,15])
    IR3flag = np.array(inp_table[:,20])
    IR4flag = np.array(inp_table[:,25])
    MP1flag = np.array(inp_table[:,32])
    IR1sat = get_saturation_flag(IR1flag) 
    IR2sat = get_saturation_flag(IR2flag) 
    IR3sat = get_saturation_flag(IR3flag) 
    IR4sat = get_saturation_flag(IR4flag) 
    MP1sat = get_saturation_flag(MP1flag) 
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
    np.savetxt('XMM_LSS_sed.txt', flux_sed)
    np.savetxt('XMM_LSS_coord.txt', coord, fmt = '%s')
    np.savetxt('XMM_LSS_Av.txt', fake_Av, header = '# fake Av')
    np.savetxt('XMM_LSS_Q.txt', sat_index, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
