#!/usr/bin/python3
'''
Abstract:
    This is a program checks if band J, H, and K exist or not. 
Usage:
    check_JHK_existance.py [loss symbol] [file name]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180104
####################################
update log
20180703 version alpha 1
    1. The code works
'''
import time
import numpy as np
from sys import argv

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # Load argrument
    if len(argv) != 3:
        print ("Error! Wrong arguments")
        print ("Usage: check_JHK_existance.py [loss symbol] [file name]")
        print ("Example: check_JHK_existance.py 0.0 source_sed_MaxLoss15.txt")
        exit()
    name_data = argv[2]
    loss_symbol = float(argv[1])
    data = np.loadtxt(name_data, dtype = np.float64)
    #print (data[:10, :])
    #-----------------------------------
    # Checking
    # The precentage of data that J, H, and K loss
    num_data = len(data)
    existance_J = np.zeros(num_data)
    existance_H = np.zeros(num_data)
    existance_K = np.zeros(num_data)
    
    existance_J[ (data[:,0] != loss_symbol) ] = 1
    existance_H[ (data[:,1] != loss_symbol) ] = 1
    existance_K[ (data[:,2] != loss_symbol) ] = 1
    
    loss_JHK = np.where((existance_J == 0) & (existance_H == 0) & (existance_K == 0))
    exist_JHK = np.where((existance_J == 1) & (existance_H == 1) & (existance_K == 1))
    print ("------")
    print ("Precentage of data that J, H, and K loss( error excluded ): {0:.2f}%({1}/{2})".format(100*len(loss_JHK[0])/num_data, len(loss_JHK[0]), num_data))
    print ("Precentage of data that J, H, and K exists(error excluded): {0:.2f}%({1}/{2})".format(100*len(exist_JHK[0])/num_data, len(exist_JHK[0]), num_data))
    # The precentage of data that J, H, and K loss
    existance_J_err_incld = np.zeros(num_data)
    existance_H_err_incld = np.zeros(num_data)
    existance_K_err_incld = np.zeros(num_data)
    
    existance_J_err_incld[ (data[:,0] != loss_symbol) & (data[:,8] != loss_symbol) ] = 1
    existance_H_err_incld[ (data[:,1] != loss_symbol) & (data[:,9] != loss_symbol) ] = 1
    existance_K_err_incld[ (data[:,2] != loss_symbol) & (data[:,10] != loss_symbol) ] = 1
    
    loss_JHK_err_incld = np.where((existance_J_err_incld == 0) & (existance_H_err_incld == 0) & (existance_K_err_incld == 0))
    exist_JHK_err_incld = np.where((existance_J_err_incld == 1) & (existance_H_err_incld == 1) & (existance_K_err_incld == 1))
    print ("------")
    print ("Precentage of data that J, H, and K loss( error included ): {0:.2f}%({1}/{2})".format(100*len(loss_JHK_err_incld[0])/num_data, len(loss_JHK_err_incld[0]), num_data))
    print ("Precentage of data that J, H, and K exists(error included): {0:.2f}%({1}/{2})".format(100*len(exist_JHK_err_incld[0])/num_data, len(exist_JHK_err_incld[0]), num_data))
    #-----------------------------------
    # Checking
    # The precentage of data that J and K loss
    loss_JK = np.where((existance_J == 0) & (existance_K == 0))
    exist_JK = np.where((existance_J == 1) & (existance_K == 1))
    print ("------")
    print ("Precentage of data that J and K loss( error excluded ): {0:.2f}%({1}/{2})".format(100*len(loss_JK[0])/num_data, len(loss_JK[0]), num_data))
    print ("Precentage of data that J and K exists(error excluded): {0:.2f}%({1}/{2})".format(100*len(exist_JK[0])/num_data, len(exist_JK[0]), num_data))
    # The precentage of data that J, H, and K loss
    loss_JK_err_incld = np.where((existance_J_err_incld == 0) & (existance_K_err_incld == 0))
    exist_JK_err_incld = np.where((existance_J_err_incld == 1) & (existance_K_err_incld == 1))
    print ("------")
    print ("Precentage of data that J and K loss( error included ): {0:.2f}%({1}/{2})".format(100*len(loss_JK_err_incld[0])/num_data, len(loss_JK_err_incld[0]), num_data))
    print ("Precentage of data that J and K exists(error included): {0:.2f}%({1}/{2})".format(100*len(exist_JK_err_incld[0])/num_data, len(exist_JK_err_incld[0]), num_data))
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
