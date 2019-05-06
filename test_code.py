#!/usr/bin/python3
'''
Abstract:
    This is a program to demo how to code deep learning code.
Usage:
    test_code.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180104
####################################
update log
20180104 version alpha 1
    The code demo good
20180204 version alpha 2
    Move to python3 instead of python2
20180320 version alpha 3
    1. add  a "This is python3" warning
20180821 version alpha 4
    1. Make all sentence with initial upper case letter.
20190121 version alpha 5
    1. Add a new standard on 'argv'
'''
import tensorflow as tf
import time
import numpy as np
from sys import argv

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
        print ("Usage: std_code.py [test]")
        exit()
    test_text = argv[1]
    #-----------------------------------
    # Print the test text
    print (test_text)
    # Compare the difference between normal variable and tensorflow node.
    x = 1
    y = x + 9
    print (y)
    x = tf.constant(1, name = "x")
    y = tf.Variable(x+9, name = "y")    # y save the key of the node.
    model = tf.global_variables_initializer()
    
    sess = tf.Session()
    sess.run(model)
    print (sess.run(y))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
