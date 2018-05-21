#!/usr/bin/python3
'''
License (MIT)
Copyright (c) 2016 by Magnus Erik Hvass Pedersen
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Abstract:
    This is a program to practice applying tensorflow on 01 Simple Linear Model on https://github.com/Hvass-Labs/TensorFlow-Tutorials.git
Usage:
    tutorial_07_Inception_Model.py
Editor:
    Magnus Erik Hvass Pedersen
Practicer:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180521
####################################
update log
20180521 version alpha 1
    1. the code works
'''
from IPython.display import Image, display
import time
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import os
# Functions and classes for loading and using the Inception model.
import inception

# Helper-function for classifying and plotting images
def classify(image_path):
    # Display the image.
    display(Image(image_path))

    # Use the Inception model to classify the image.
    pred = model.classify(image_path=image_path)

    # Print the scores and names for the top-10 predictions.
    model.print_scores(pred=pred, k=10, only_first_name=True)

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #----------------------------------------
    # version checking
    print(tf.__version__)
    # Load inception model
    inception.data_dir = 'inception/'
    inception.maybe_download()
    model = inception.Inception()
    # Load and make a prediction on a Panda image
    image_path = os.path.join(inception.data_dir, 'cropped_panda.jpg')
    classify(image_path)
    classify('funny_images/airplane.jpg')
    classify('funny_images/kitten.jpg')
    classify('funny_images/mic.gif')
    classify('funny_images/Trump.jpg')
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
