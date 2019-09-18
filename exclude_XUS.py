#!/usr/bin/python3
'''
Abstract:
    This is a program to exclude the upper limit "U" happened in band 4 ~ 7
    no observation "X" in all 8 bands,
    and saturation "S" in all 8 bands. 
Usage:
    exclude_XUS.py [Q flag table] [data]
    
    Input should looks like:
    Q flag table = 
    [[ A, A, A, A, A, A, A, U],
     [ A, B, A, A, A, A, A, U],
     ...]

Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181128
####################################
update log
20181128 version alpha 1:
    1. The code works
20190117 version alpha 2:
    1. Only exclude the source has upper limit on IRAC1~4
20190906 version alpha 3:
    1. Take saturation into account.
'''
from sys import argv
import time
import numpy as np

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("Wrong numbers of arguments")
        print ("Usage: exclude_ul.py [Q flag table] [data]")
        exit(0)
    ul_table_name = argv[1]
    data_name = argv[2]
    #-----------------------------------
    # Load data
    ul_table = np.loadtxt(ul_table_name, dtype = str)
    data = np.loadtxt(data_name, dtype = str)
    #------------------------------------------
    # Find the line with upper limits
    # Exclude 'X' in all bands.
    print ("Exclude 'X' from data")
    data_woX = data[
                            (ul_table[:,0] != 'X') &\
                            (ul_table[:,1] != 'X') &\
                            (ul_table[:,2] != 'X') &\
                            (ul_table[:,3] != 'X') &\
                            (ul_table[:,4] != 'X') &\
                            (ul_table[:,5] != 'X') &\
                            (ul_table[:,6] != 'X') &\
                            (ul_table[:,7] != 'X')
                            ]
    ul_table_woX = ul_table[
                            (ul_table[:,0] != 'X') &\
                            (ul_table[:,1] != 'X') &\
                            (ul_table[:,2] != 'X') &\
                            (ul_table[:,3] != 'X') &\
                            (ul_table[:,4] != 'X') &\
                            (ul_table[:,5] != 'X') &\
                            (ul_table[:,6] != 'X') &\
                            (ul_table[:,7] != 'X')
                            ]
    # Exclude 'U' in IRAC and 2MASS
    print ("Exclude 'U' from data")
    data_woX_woU = data_woX[  
                            ~((ul_table_woX[:,0] == 'U') & (ul_table_woX[:,1] == 'U') & (ul_table_woX[:,2] == 'U')) &\
                            (ul_table_woX[:,3] != 'U') &\
                            (ul_table_woX[:,4] != 'U') &\
                            (ul_table_woX[:,5] != 'U') &\
                            (ul_table_woX[:,6] != 'U')
                            ]
    ul_table_woX_woU = ul_table_woX[                    
                            ~((ul_table_woX[:,0] == 'U') & (ul_table_woX[:,1] == 'U') & (ul_table_woX[:,2] == 'U')) &\
                            (ul_table_woX[:,3] != 'U') &\
                            (ul_table_woX[:,4] != 'U') &\
                            (ul_table_woX[:,5] != 'U') &\
                            (ul_table_woX[:,6] != 'U')
                            ]
    # Exclude 'S' in all bands
    print ("Exclude 'S' from data")
    data_woX_woU_woS = data_woX_woU[
                            (ul_table_woX_woU[:,0] != 'S') &\
                            (ul_table_woX_woU[:,1] != 'S') &\
                            (ul_table_woX_woU[:,2] != 'S') &\
                            (ul_table_woX_woU[:,3] != 'S') &\
                            (ul_table_woX_woU[:,4] != 'S') &\
                            (ul_table_woX_woU[:,5] != 'S') &\
                            (ul_table_woX_woU[:,6] != 'S') &\
                            (ul_table_woX_woU[:,7] != 'S') ]
    # Save masked data set
    np.savetxt("{0}_exXUS.txt".format(data_name[:-4]), data_woX_woU_woS, fmt = '%s')
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
