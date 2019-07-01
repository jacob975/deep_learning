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
    2. Add a func to print confusion matrix
20180414 version alpha 3:
    1. Add funcs for printing precision and recall-rate.
20180523 version alpha 4: 
    1. Add funcs for printing accuracy of predictions.
20180601 version alpha 5:
    1. Add funcs for selecting high reliability sources from dataset
    2. Delete some imported module never used.
20181005 version alpha 6:
    1. Abandan .npy file format, using .txt file format only.
'''
import tensorflow as tf
import time
import numpy as np
import os
from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.framework import dtypes
from astro_mnist import DataSet, shuffled_tracer

# This is used to load data, label, and shuffle tracer
def load_arrangement(main_name, 
                    directory, 
                    reshape=False,
                    dtype=dtypes.float32,
                    seed=None,
                    VERBOSE = 0
                    ):
    # directory is where you save AI
    # main_name is the main part to of the filename
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
        train_tracer    = np.loadtxt("{0}/training_tracer_{1}_sed.txt".format(directory, main_name))
        train_data      = np.loadtxt("{0}/training_set_{1}_sed.txt".format(directory, main_name))
        train_labels    = np.loadtxt("{0}/training_label_{1}_sed.txt".format(directory, main_name))
    except:
        if VERBOSE != 0:print("In train dataset, data or label or tracer aren't completed")
    try:
        valid_tracer    = np.loadtxt("{0}/validation_tracer_{1}_sed.txt".format(directory, main_name))
        valid_data      = np.loadtxt("{0}/validation_set_{1}_sed.txt".format(directory, main_name))
        valid_labels    = np.loadtxt("{0}/validation_labels_{1}_sed.txt".format(directory, main_name))
    except:
        if VERBOSE != 0:print("In validation dataset, data or label or tracer aren't completed")
    try:
        test_tracer     = np.loadtxt("{0}/test_tracer_{1}_sed.txt".format(directory, main_name))
        test_data       = np.loadtxt("{0}/test_set_{1}_sed.txt".format(directory, main_name))
        test_labels     = np.loadtxt("{0}/test_labels_{1}_sed.txt".format(directory, main_name))
    except:
        if VERBOSE != 0:print("In test dataset, data or label or tracer aren't completed")
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
def load_cls_pred(main_name, directory):
    # directory is used to create a uniq folder
    # main_name is used to denote filename
    # cls_pred is the index of predicted labels
    try:
        cls_pred = np.loadtxt("{0}/test_cls_pred_{1}_sed.txt".format(directory, main_name))
    except:
        print("test_cls_pred not found")
        return 1, None
    return 0, cls_pred

# This is used to loading pred label
def load_labels_pred(main_name, directory):
    # directory is used to create a uniq folder
    # main_name is used to denote filename
    # cls_pred is predicted label
    try:
        labels_pred = np.loadtxt("{0}/test_labels_pred_{1}_sed.txt".format(directory, main_name))
    except:
        print("test_labels_pred not found")
        return 1, None
    return 0, labels_pred

# This is used to loading the index of true lable
def load_cls_true(main_name, directory):
    # directory is used to create a uniq folder
    # main_name is used to denote filename
    # cls_pred is the index of true labels
    try:
        cls_true = np.loadtxt("{0}/test_cls_true_{1}_sed.txt".format(directory, main_name))
    except:
        print ("test_cls_true not found")
        return 1, None
    return 0, cls_true

# This is the func to load coordinates of corresponding sources.
def load_coords(main_name, directory):
    try:
        train_coords = np.loadtxt("{0}/train_coords_{1}_sed.txt".format(directory, main_name))
    except:
        print ("train coords not found")
        train_coords = None
    try:
        validation_coords = np.loadtxt("{0}/validation_coords_{1}_sed.txt".format(directory, main_name))
    except:
        print ("validation coords not found")
        validation_coords = None
    try:
        test_coords = np.loadtxt("{0}/test_coords_{1}_sed.txt".format(directory, main_name))
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
        precision = 0
        if len(denominator[0]) == 0:
            if len(numerator[0]) == 0:
                precision = 0
            else:
                precision = np.inf
        else:
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
class confusion_matrix_infos_lite():
    objects = ['star', 'galaxy', 'yso']
    def __init__(self, cls_true, cls_pred):
        self.cls_true = cls_true
        self.cls_pred = cls_pred 
        return

    def confusion_matrix(self):
        from sklearn.metrics import confusion_matrix
        # all of them
        cm = confusion_matrix(y_true=self.cls_true,
                              y_pred=self.cls_pred)
        return 0, cm
    
    def print_accuracy(self):
        # all of them
        print("### accuracy ###")
        correctly_predicted = np.where((self.cls_pred == self.cls_true))
        accuracy = len(correctly_predicted[0])/len(self.cls_true)
        print("accuracy of prediction: {0:.2f}% ({1} /{2} )"\
        .format(accuracy*100, len(correctly_predicted[0]), len(self.cls_true)))
        return
    
    def print_precision(self):
        # all of them
        print ("### precision ###")
        for label in range(3):
            denominator = np.where(self.cls_pred == label)
            numerator = np.where((self.cls_pred == label) & (self.cls_true == label))
            precision = 0
            if len(denominator[0]) == 0:
                if len(numerator[0]) == 0:
                    precision = 0
                else:
                    precision = np.inf
            else:
                precision = len(numerator[0])/len(denominator[0])
            print("precision for predict {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        return
    
    def print_recall_rate(self):
        # all of them
        print ("### recall-rate ###")
        for label in range(3):
            denominator = np.where(self.cls_true == label)
            numerator = np.where((self.cls_pred == label) & (self.cls_true == label))
            precision = 0
            if len(denominator[0]) == 0:
                if len(numerator[0]) == 0:
                    precision = 0
                else:
                    precision = np.inf
            else:
                precision = len(numerator[0])/len(denominator[0])
            print("recall-rate for true {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        return

class confusion_matrix_infos():
    objects = ['star', 'galaxy', 'yso']
    def __init__(self, cls_true, labels_pred):
        self.cls_true = cls_true
        self.labels_pred = labels_pred
        self.cls_pred = np.array(np.argmax(self.labels_pred, axis = 1), dtype = int)
        try:
            self.reliable = np.where((np.max(self.labels_pred, axis = 1) > 0.8))
            self.cls_true_reliable = self.cls_true[self.reliable]
            self.cls_pred_reliable = self.cls_pred[self.reliable]
            self.reliable = True
        except:
            self.reliable = None
            self.cls_true_reliable = None
            self.cls_pred_reliable = None
            self.reliable = False
        return

    def confusion_matrix(self):
        from sklearn.metrics import confusion_matrix
        # all of them
        cm = confusion_matrix(y_true=self.cls_true,
                              y_pred=self.cls_pred)
        # only reliable
        if self.reliable:
            cm_reliable = confusion_matrix( y_true=self.cls_true_reliable, 
                                            y_pred=self.cls_pred_reliable)
        else:
            cm_reliable = None
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
            precision = 0
            if len(denominator[0]) == 0:
                if len(numerator[0]) == 0:
                    precision = 0
                else:
                    precision = np.inf
            else:
                precision = len(numerator[0])/len(denominator[0])
            print("precision for predict {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        # only reliable
        print ("### reliable precision ###")
        for label in range(3):
            denominator = np.where(self.cls_pred_reliable == label)
            numerator = np.where((self.cls_pred_reliable == label) & (self.cls_true_reliable == label))
            precision = 0
            if len(denominator[0]) == 0:
                if len(numerator[0]) == 0:
                    precision = 0
                else:
                    precision = np.inf
            else:
                precision = len(numerator[0])/len(denominator[0])
            print("precision for predict {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        return
    
    def print_recall_rate(self):
        # all of them
        print ("### recall-rate ###")
        for label in range(3):
            denominator = np.where(self.cls_true == label)
            numerator = np.where((self.cls_pred == label) & (self.cls_true == label))
            precision = 0
            if len(denominator[0]) == 0:
                if len(numerator[0]) == 0:
                    precision = 0
                else:
                    precision = np.inf
            else:
                precision = len(numerator[0])/len(denominator[0])
            print("recall-rate for true {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        # only reliable
        print ("### reliable recall-rate ###")
        for label in range(3):
            denominator = np.where(self.cls_true_reliable == label)
            numerator = np.where((self.cls_pred_reliable == label) & (self.cls_true_reliable == label))
            if len(denominator[0]) == 0:
                if len(numerator[0]) == 0:
                    precision = 0
                else:
                    precision = np.inf
            else:
                precision = len(numerator[0])/len(denominator[0])
            print("recall-rate for true {0} is : {1:.2f}% ({2} /{3} )"\
            .format(self.objects[label], precision*100, len(numerator[0]), len(denominator[0])))
        return

class cross_confusion_matrix_infos(confusion_matrix_infos):
    def __init__(self, cls_pred, labels_pred):
        self.cls_pred = cls_pred
        self.cls_true = np.argmax(self.cls_pred, axis = 1)
        self.labels_pred = labels_pred
        self.cls_pred = np.argmax(self.labels_pred, axis = 1)
        self.reliable = np.where((np.max(self.labels_pred, axis = 1) > 0.8))
        self.cls_true_reliable = self.cls_true[self.reliable]
        self.cls_pred_reliable = self.cls_pred[self.reliable]
        return 

