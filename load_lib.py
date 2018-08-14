#!/usr/bin/python3
'''
Abstract:
    This is a program to load the tracer and data from files. 
Usage:
    import load_lib.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170411
####################################
update log

20180411 version alpha 1:
    1. The library work...no

20180412 version alpha 2:
    1. It is hard to create pointer in python, so I back to call by value
    2. add a func to print confusion matrix
20180414 version alpha 3:
    1. add funcs for printing precision and recall-rate.
20180523 version alpha 4: 
    1. add funcs for printing accuracy of predictions.
20180601 version alpha 5:
    1. add funcs for selecting high reliability sources from dataset
    2. delete some imported module never used.
'''
import tensorflow as tf
import time
import numpy as np
import os

from six.moves import xrange  # pylint: disable=redefined-builtin

from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.framework import dtypes

from astro_mnist import DataSet, shuffled_tracer

# This is used to load data, label, and shuffle tracer
def load_arrangement(sub_name, 
                    directory, 
                    reshape=False,
                    dtype=dtypes.float32,
                    seed=None,
                    ):
    # directory is where you save AI
    # sub_name is used to denote filename
    # data contains data set and label
    # tracer is just tracer
    # initialize variables
    train_tracer    = np.array([])
    train_data      = np.array([]) 
    train_labels    = np.array([])
    valid_tracer    = np.array([])
    valid_data      = np.array([])
    valid_labels    = np.array([])
    test_tracer     = np.array([])
    test_data       = np.array([])
    test_labels     = np.array([])
    # create folder
    if not os.path.exists(directory):
        print("Directory not found")
        return 1, None
    # if directory is not null, load data, labels and tracers
    try:
        train_tracer    = np.load("{0}/training_tracer_source_sed_{1}.npy".format(directory, sub_name))
        train_data      = np.load("{0}/training_set_source_sed_{1}.npy".format(directory, sub_name))
        train_labels    = np.load("{0}/training_label_source_sed_{1}.npy".format(directory, sub_name))
    except:
        print("In train dataset, data or label or tracer aren't completed")
    try:
        valid_tracer    = np.load("{0}/validation_tracer_source_sed_{1}.npy".format(directory, sub_name))
        valid_data      = np.load("{0}/validation_set_source_sed_{1}.npy".format(directory, sub_name))
        valid_labels    = np.load("{0}/validation_labels_source_sed_{1}.npy".format(directory, sub_name))
    except:
        print("In validation dataset, data or label or tracer aren't completed")
    try:
        test_tracer     = np.load("{0}/test_tracer_source_sed_{1}.npy".format(directory, sub_name))
        test_data       = np.load("{0}/test_set_source_sed_{1}.npy".format(directory, sub_name))
        test_labels     = np.load("{0}/test_labels_source_sed_{1}.npy".format(directory, sub_name))
    except:
        print("In test dataset, data or label or tracer aren't completed")
    options = dict(dtype=dtype, reshape=reshape, seed=seed)
    # generate tracer
    tracer = shuffled_tracer(train_tracer, valid_tracer, test_tracer)
    # generate data and index
    train = DataSet(train_data, train_labels, **options)
    validation = DataSet(valid_data, valid_labels, **options)
    test = DataSet(test_data, test_labels, **options)
    data = base.Datasets(train=train, validation=validation, test=test)
    return 0, data, tracer

def load_dat_tracer():
    return 0, dat_tracer

def load_table_tracer():
    return 0, table_tracer

# This is used to loading the index of pred label
def load_cls_pred(sub_name, directory):
    # directory is used to create a uniq folder
    # sub_name is used to denote filename
    # cls_pred is the index of predicted labels
    try:
        cls_pred = np.load("{0}/test_cls_pred_source_sed_{1}.npy".format(directory, sub_name))
    except:
        print("test_cls_pred not found")
        return 1, None
    return 0, cls_pred

# This is used to loading pred label
def load_labels_pred(sub_name, directory):
    # directory is used to create a uniq folder
    # sub_name is used to denote filename
    # cls_pred is predicted label
    try:
        labels_pred = np.load("{0}/test_labels_pred_source_sed_{1}.npy".format(directory, sub_name))
    except:
        print("test_labels_pred not found")
        return 1, None
    return 0, labels_pred

# THis is used to loading the index of true lable
def load_cls_true(sub_name, directory):
    # directory is used to create a uniq folder
    # sub_name is used to denote filename
    # cls_pred is the index of true labels
    try:
        cls_true = np.load("{0}/test_cls_true_source_sed_{1}.npy".format(directory, sub_name))
    except:
        print ("test_cls_true not found")
        return 1, None
    return 0, cls_true

# This is the func to load coordinates of corresponding sources.
def load_coords(sub_name, directory):
    try:
        train_coords = np.load("{0}/train_coords_source_sed_{1}.npy".format(directory, sub_name))
    except:
        print ("train coords not found")
        train_coords = None
    try:
        validation_coords = np.load("{0}/validation_coords_source_sed_{1}.npy".format(directory, sub_name))
    except:
        print ("validation coords not found")
        validation_coords = None
    try:
        test_coords = np.load("{0}/test_coords_source_sed_{1}.npy".format(directory, sub_name))
    except:
        print ("test coords not found")
        test_coords = None
    coords = shuffled_tracer(train_coords, validation_coords, test_coords)
    return 0, coords

# generate confusion matrix with given cls_true and cls_pred
def confusion_matrix(cls_true, cls_pred):
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_true=cls_true,
                          y_pred=cls_pred,
                          labels = range(3))
    return 0, cm

def print_accuracy(y_true, y_pred):
    print("### accuracy ###")
    correctly_predicted = np.where((y_pred == y_true))
    accuracy = len(correctly_predicted[0])/len(y_true)
    print("accuracy of prediction: {0:.2f}% ({1} /{2} )"\
    .format(accuracy*100, len(correctly_predicted[0]), len(y_true)))
    return

def print_precision(y_true, y_pred):
    print ("### precision ###")
    objects = ['star', 'galaxy', 'yso']
    for label in range(3):
        denominator = np.where(y_pred == label)
        numerator = np.where((y_pred == label) & (y_true == label))
        precision = len(numerator[0])/len(denominator[0])
        print("precision for predict {0} is : {1:.2f}% ({2} /{3} )"\
        .format(objects[label], precision*100, len(numerator[0]), len(denominator[0])))
    return

def print_recall_rate(y_true, y_pred):
    print ("### recall-rate ###")
    objects = ['star', 'galaxy', 'yso']
    for label in range(3):
        denominator = np.where(y_true == label)
        numerator = np.where((y_pred == label) & (y_true == label))
        precision = len(numerator[0])/len(denominator[0])
        print("recall-rate for true {0} is : {1:.2f}% ({2} /{3} )"\
        .format(objects[label], precision*100, len(numerator[0]), len(denominator[0])))
    return

#-------------------------------------------------------------------
# This class is used to print infomations about prediction and truth
class confusion_matrix_infos():
    objects = ['star', 'galaxy', 'yso']
    def __init__(self, cls_true, labels_pred):
        self.cls_true = cls_true
        self.labels_pred = labels_pred
        self.cls_pred = np.argmax(self.labels_pred, axis = 1)
        self.reliable = np.where((np.max(self.labels_pred, axis = 1) > 0.8))
        self.cls_true_reliable = self.cls_true[self.reliable]
        self.cls_pred_reliable = self.cls_pred[self.reliable]
        return

    def confusion_matrix(self):
        from sklearn.metrics import confusion_matrix
        # all of them
        cm = confusion_matrix(y_true=self.cls_true,
                              y_pred=self.cls_pred)
        # only reliable
        cm_reliable = confusion_matrix(y_true=self.cls_true_reliable, y_pred=self.cls_pred_reliable)
        return 0, cm, cm_reliable
    
    def print_accuracy(self):
        # all of them
        print("### accuracy ###")
        correctly_predicted = np.where((self.cls_pred == self.cls_true))
        accuracy = len(correctly_predicted[0])/len(self.cls_true)
        print("accuracy of prediction: {0:.2f}% ({1} /{2} )"\
        .format(accuracy*100, len(correctly_predicted[0]), len(self.cls_true)))
        # only reliable
        print("### reliable accuracy ###")
        correctly_predicted = np.where((self.cls_pred_reliable == self.cls_true_reliable))
        accuracy = len(correctly_predicted[0])/len(self.cls_true_reliable)
        print("accuracy of prediction: {0:.2f}% ({1} /{2} )"\
        .format(accuracy*100, len(correctly_predicted[0]), len(self.cls_true_reliable)))
        return
    
    def print_precision(self):
        # all of them
        print ("### precision ###")
        for label in range(3):
            denominator = np.where(self.cls_pred == label)
            numerator = np.where((self.cls_pred == label) & (self.cls_true == label))
            try:
                precision = len(numerator[0])/len(denominator[0])
            except:
                precision = np.inf
            print("precision for predict {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        # only reliable
        print ("### reliable precision ###")
        for label in range(3):
            denominator = np.where(self.cls_pred_reliable == label)
            numerator = np.where((self.cls_pred_reliable == label) & (self.cls_true_reliable == label))
            try:
                precision = len(numerator[0])/len(denominator[0])
            except:
                precision = np.inf
            print("precision for predict {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        return
    
    def print_recall_rate(self):
        # all of them
        print ("### recall-rate ###")
        for label in range(3):
            denominator = np.where(self.cls_true == label)
            numerator = np.where((self.cls_pred == label) & (self.cls_true == label))
            try:
                precision = len(numerator[0])/len(denominator[0])
            except:
                precision = np.inf
            print("recall-rate for true {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        # only reliable
        print ("### reliable recall-rate ###")
        for label in range(3):
            denominator = np.where(self.cls_true_reliable == label)
            numerator = np.where((self.cls_pred_reliable == label) & (self.cls_true_reliable == label))
            try:
                precision = len(numerator[0])/len(denominator[0])
            except:
                precision = np.inf
            print("recall-rate for true {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        return
