#!/usr/bin/python3
'''
Abstract:
    This is a program for generating a fake Q label with assuming 0.0 = U 
Usage:
    generate_fake_Q.py [sed table]
Output:
    1. The Q label of each band in each source. 
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190804
####################################
update log
20190804 version alpha 1
    1. The code works.
'''
import time
import numpy as np
from sys import argv

def get_saturation_flag(sed_array, e_sed_array):
    # Default quality 
    quality_array = np.chararray(len(sed_array))
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
        print ("Usage: generate_fake_Q.py [sed table]")
        exit()
    sed_table_name = argv[1]
    #-----------------------------------
    # Load data
    sed_table = np.loadtxt(sed_table_name)
    '''
    Jsat   = get_saturation_flag(sed_table[:,0], sed_table[:,8])
    Hsat   = get_saturation_flag(sed_table[:,1], sed_table[:,9])
    Ksat   = get_saturation_flag(sed_table[:,2], sed_table[:,10])
    IR1sat = get_saturation_flag(sed_table[:,3], sed_table[:,11])
    IR2sat = get_saturation_flag(sed_table[:,4], sed_table[:,12])
    IR3sat = get_saturation_flag(sed_table[:,5], sed_table[:,13])
    IR4sat = get_saturation_flag(sed_table[:,6], sed_table[:,14])
    MP1sat = get_saturation_flag(sed_table[:,7], sed_table[:,15])
    fake_Q_table_2 = np.array(np.transpose([
                                        Jsat,  
                                        Hsat,  
                                        Ksat,  
                                        IR1sat,
                                        IR2sat,
                                        IR3sat,
                                        IR4sat,
                                        MP1sat,
                                        ]))
    '''
    fake_Q_table = np.empty((len(sed_table), 8), dtype = str)
    fake_Q_table[:] = 'A'
    index_zero = sed_table[:,:8] <= 0.0
    index_zero_err = sed_table[:,8:] <= 0.0
    fake_Q_table[index_zero] = "U"
    fake_Q_table[index_zero_err] = "U"
    fake_Q_table_2 = []
    for Q in fake_Q_table:
        str_Q = ' '.join(Q) 
        fake_Q_table_2.append(str_Q)
    np.savetxt('fake_Q.txt', fake_Q_table_2, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
