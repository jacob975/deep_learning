#!/usr/bin/python3
'''
Abstract:
    This is a program to exclude the upper limit "U" happened in band 4 ~ 7
    no observation "X" in all 8 bands,
    and saturation "S" in all 8 bands. 
Usage:
    exclude_XUS_678.py [Q flag table] [data]
    
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

20181014
####################################
update log
20191014 version alpha 1:
    1. The code works
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
        print ("Usage: exclude_XUS_678.py [Q flag table] [data]")
        exit(0)
    Q_table_name = argv[1]
    data_name = argv[2]
    #-----------------------------------
    # Load data
    print ("Loading quality flags...")
    Q_table = np.loadtxt(Q_table_name, dtype = str)
    print ("Loading data...")
    data = np.loadtxt(data_name, dtype = str)
    index = np.arange(len(Q_table))
    #------------------------------------------
    # Find the line with upper limits
    # Exclude 'X' in all bands.
    print ("Exclude 'X' from data")
    data_woX = data[
#                            (Q_table[:,0] != 'X') &\
#                            (Q_table[:,1] != 'X') &\
#                            (Q_table[:,2] != 'X') &\
#                            (Q_table[:,3] != 'X') &\
#                            (Q_table[:,4] != 'X') &\
                            (Q_table[:,5] != 'X') &\
                            (Q_table[:,6] != 'X') &\
                            (Q_table[:,7] != 'X')
                            ]
    Q_table_woX = Q_table[
#                            (Q_table[:,0] != 'X') &\
#                            (Q_table[:,1] != 'X') &\
#                            (Q_table[:,2] != 'X') &\
#                            (Q_table[:,3] != 'X') &\
#                            (Q_table[:,4] != 'X') &\
                            (Q_table[:,5] != 'X') &\
                            (Q_table[:,6] != 'X') &\
                            (Q_table[:,7] != 'X')
                            ]
    index_woX = index[
#                            (Q_table[:,0] != 'X') &\
#                            (Q_table[:,1] != 'X') &\
#                            (Q_table[:,2] != 'X') &\
#                            (Q_table[:,3] != 'X') &\
#                            (Q_table[:,4] != 'X') &\
                            (Q_table[:,5] != 'X') &\
                            (Q_table[:,6] != 'X') &\
                            (Q_table[:,7] != 'X')
                            ]
    # Exclude 'U' in IRAC and 2MASS
    print ("Exclude 'U' from data")
    data_woX_woU = data_woX[  
    #                        ~((Q_table_woX[:,0] == 'U') & (Q_table_woX[:,1] == 'U') & (Q_table_woX[:,2] == 'U')) &\
    #                        (Q_table_woX[:,3] != 'U') &\
    #                        (Q_table_woX[:,4] != 'U') &\
                            (Q_table_woX[:,5] != 'U') &\
                            (Q_table_woX[:,6] != 'U')
                            ]
    Q_table_woX_woU = Q_table_woX[                    
    #                        ~((Q_table_woX[:,0] == 'U') & (Q_table_woX[:,1] == 'U') & (Q_table_woX[:,2] == 'U')) &\
    #                        (Q_table_woX[:,3] != 'U') &\
    #                        (Q_table_woX[:,4] != 'U') &\
                            (Q_table_woX[:,5] != 'U') &\
                            (Q_table_woX[:,6] != 'U')
                            ]
    index_woX_woU = index_woX[                    
    #                        ~((Q_table_woX[:,0] == 'U') & (Q_table_woX[:,1] == 'U') & (Q_table_woX[:,2] == 'U')) &\
    #                        (Q_table_woX[:,3] != 'U') &\
    #                        (Q_table_woX[:,4] != 'U') &\
                            (Q_table_woX[:,5] != 'U') &\
                            (Q_table_woX[:,6] != 'U')
                            ]
    # Exclude 'S' in all bands
    print ("Exclude 'S' from data")
    data_woX_woU_woS = data_woX_woU[
    #                        (Q_table_woX_woU[:,0] != 'S') &\
    #                        (Q_table_woX_woU[:,1] != 'S') &\
    #                        (Q_table_woX_woU[:,2] != 'S') &\
    #                        (Q_table_woX_woU[:,3] != 'S') &\
    #                        (Q_table_woX_woU[:,4] != 'S') &\
                            (Q_table_woX_woU[:,5] != 'S') &\
                            (Q_table_woX_woU[:,6] != 'S') &\
                            (Q_table_woX_woU[:,7] != 'S') ]
    index_woX_woU_woS = index_woX_woU[
    #                        (Q_table_woX_woU[:,0] != 'S') &\
    #                        (Q_table_woX_woU[:,1] != 'S') &\
    #                        (Q_table_woX_woU[:,2] != 'S') &\
    #                        (Q_table_woX_woU[:,3] != 'S') &\
    #                        (Q_table_woX_woU[:,4] != 'S') &\
                            (Q_table_woX_woU[:,5] != 'S') &\
                            (Q_table_woX_woU[:,6] != 'S') &\
                            (Q_table_woX_woU[:,7] != 'S') ]
    
    # Save masked data set
    np.savetxt("{0}_exXUS_678.txt".format(data_name[:-4]), data_woX_woU_woS, fmt = '%s')
    np.savetxt("index_exXUS_678.txt", index_woX_woU_woS, fmt = '%d')
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
