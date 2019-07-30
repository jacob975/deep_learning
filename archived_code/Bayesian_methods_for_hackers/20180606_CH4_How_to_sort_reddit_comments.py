#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH4.
Usage:
    20180601_CH4_How_to_sort_reddit_comments.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170606
####################################
update log
20180606 version alpha 1:
    1. The code works

'''
import numpy as np
from IPython.core.pylabtools import figsize
import matplotlib.pyplot as plt
import top_showerthoughts_submissions
figsize(12.5, 4)
import pymc as pm
'''
Contents: an array of the test from all comments on the pic
Votes: a 2D NumPy array of upvotes, downvotes for each comment
'''
n_comments = len(contents)
comments = np.random.randint(n_comments, size = 4)
print("Some Comments (out of %d total) \n----------"%n_comments)
for i in comments:
    print('"(0)"'.format(contents[i]))
    print("upvotes/downvotes: {0}".format(votes[i, :]))
    print
