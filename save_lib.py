#!/usr/bin/python3
'''
Abstract:
    This is a program to save the arrangement of random data process. 
Usage:
    import save_lib.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170104
####################################
update log

20180321 version alpha 1:
    1. save the arrangement of random data process.
20180322 version alpha 2:
    1. rearrange save condition.

20180323 version alpha 3:
    1. add explaination
20180530 version alpha 4:
    1. add a func for saving coords of sources
20180601 version alpha 5:
    1. add a func for saving predicted labels
'''
import tensorflow as tf
import time
import numpy as np
import os

# This is used to save data, label, and tracer
def save_arrangement(keyword, time_stamp, data, tracer):
    # time_stamp is used to create a uniq folder
    # keyword is used to denote filename
    # data contains data set and label
    # tracer is just tracer
    # create folder
    if not os.path.exists(time_stamp):
        os.makedirs(time_stamp)
    # if train set is not null, save data, labels and tracers
    if len(data.train.images):
        np.savetxt("{0}/training_tracer_{1}.txt".format(time_stamp, keyword), tracer.train, fmt = '%d')
        np.savetxt("{0}/training_set_{1}.txt".format(time_stamp, keyword), data.train.images)
        np.savetxt("{0}/training_label_{1}.txt".format(time_stamp, keyword), data.train.labels)
    if len(data.validation.images):
        np.savetxt("{0}/validation_tracer_{1}.txt".format(time_stamp, keyword), tracer.validation, fmt = '%d')      
        np.savetxt("{0}/validation_set_{1}.txt".format(time_stamp, keyword), data.validation.images)
        np.savetxt("{0}/validation_labels_{1}.txt".format(time_stamp, keyword), data.validation.labels)
    if len(data.test.images):
        np.savetxt("{0}/test_tracer_{1}.txt".format(time_stamp, keyword), tracer.test, fmt = '%d')
        np.savetxt("{0}/test_set_{1}.txt".format(time_stamp, keyword), data.test.images)
        np.savetxt("{0}/test_labels_{1}.txt".format(time_stamp, keyword), data.test.labels)
    return 0

def save_arrangement_ext(time_stamp, data, tracer):
    # time_stamp is used to create a uniq folder
    # data contains data set and label
    # tracer is just tracer
    # create folder
    if not os.path.exists(time_stamp):
        os.makedirs(time_stamp)
    # if train set is not null, save data, labels and tracers
    if len(data.train.images):
        np.savetxt("{0}/training_tracer.txt".format(time_stamp), tracer.train, fmt = '%d')
        np.savetxt("{0}/training_set.txt".format(time_stamp), data.train.images)
        np.savetxt("{0}/training_label.txt".format(time_stamp), data.train.labels)
    if len(data.validation.images):
        np.savetxt("{0}/validation_tracer.txt".format(time_stamp), tracer.validation, fmt = '%d')      
        np.savetxt("{0}/validation_set.txt".format(time_stamp), data.validation.images)
        np.savetxt("{0}/validation_labels.txt".format(time_stamp), data.validation.labels)
    if len(data.test.images):
        np.savetxt("{0}/test_tracer.txt".format(time_stamp), tracer.test, fmt = '%d')
        np.savetxt("{0}/test_set.txt".format(time_stamp), data.test.images)
        np.savetxt("{0}/test_labels.txt".format(time_stamp), data.test.labels)
    return 0

# This is used to saving pred cls
def save_cls_pred(keyword, time_stamp, cls_pred):
    # time_stamp is used to create a uniq folder
    # keyword is used to denote filename
    # cls_pred is the index of predicted label
    np.savetxt("{0}/test_cls_pred_{1}.txt".format(time_stamp, keyword), cls_pred)
    return 0

# This is used to saving pred label
def save_label_pred(keyword, time_stamp, label_pred):
    # time_stamp is used to create a uniq folder
    # keyword is used to denote filename
    # label_pred is predicted label
    np.savetxt("{0}/test_labels_pred_{1}.txt".format(time_stamp, keyword), label_pred)
    return 0

# THis is used to saving true cls
def save_cls_true(keyword, time_stamp, cls_true):
    # time_stamp is used to create a uniq folder
    # keyword is used to denote filename
    # cls_pred is the index of true label
    np.savetxt("{0}/test_cls_true_{1}.txt".format(time_stamp, keyword), cls_true, fmt = '%d')
    return 0

# This is used to saving coords
def save_coords(keyword, time_stamp, coords):
    if len(coords.train):
        np.savetxt("{0}/train_coords_{1}.txt".format(time_stamp, keyword), coords.train)
    if len(coords.validation):
        np.savetxt("{0}/validation_coords_{1}.txt".format(time_stamp, keyword), coords.validation)
    if len(coords.test):
        np.savetxt("{0}/test_coords_{1}.txt".format(time_stamp, keyword), coords.test)
    return 0

# This is used to saving coords
def save_coords_ext(time_stamp, coords):
    if len(coords.train):
        np.savetxt("{0}/train_coords.txt".format(time_stamp), coords.train)
    if len(coords.validation):
        np.savetxt("{0}/validation_coords.txt".format(time_stamp), coords.validation)
    if len(coords.test):
        np.savetxt("{0}/test_coords.txt".format(time_stamp), coords.test)
    return 0

def save_any(filename, time_stamp, files):
    np.savetxt("{0}/{1}.txt".format(time_stamp, filename), files)
    return 0
