#!/usr/bin/python3
'''
Abstract:
    This is a code for testing AI with given sed data using CNN.
Usage:
    sed_test_cnn_lite.py [option file] [source] [id] [coord] [where to save] [AI]
Editor and Practicer:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181019
####################################
update log
20181019 version alpha 1
    1. The code works.
20190124 version alpha 2
    1. Add more arguments to describe the format of datasets.
'''
import tensorflow as tf
import numpy as np
import time
from sys import argv
import os

def weight_variable(shape, std = 0.1):
    initial = tf.truncated_normal(shape) * std
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape = shape)
    return tf.Variable(initial)


def main(test_images, test_labels):
    #-----------------------------------
    # Load arguments
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: sed_test_cnn.py [AI]")
        exit(1)
    AI_saved_dir = argv[1]
    #-----------------------------------
    # Data dimension
    img_maj = 8 
    width_of_data = 2
    pick_band_array = np.arange(16)
    image_shape = (2, 8)
    kernal_shape = (2, 2)
    num_kernal_1 = 32
    num_kernal_2 = 64
    num_conn_neural = 100
    num_label = 3
    print ('#--------------------------------------------')
    print ('Parameters:') 
    print ('img_maj:            {0}'.format(img_maj))
    print ('width_of_data:      {0}'.format(width_of_data))
    print ('pick_band_array:\n  {0}'.format(pick_band_array))
    print ('image_shape:\n      {0}'.format(image_shape))
    print ('kernal_shape:\n     {0}'.format(kernal_shape))
    print ('num_kernal_1:       {0}'.format(num_kernal_1))
    print ('num_kernal_2:       {0}'.format(num_kernal_2))
    print ('num_conn_neural:    {0}'.format(num_conn_neural))
    print ('num_label:          {0}'.format(num_label))
    #-----------------------------------
    # Construct an AI
    x = tf.placeholder(tf.float32, [None, width_of_data * img_maj], name = 'x')
    y_true = tf.placeholder(tf.float32, [None, num_label], name = 'y_true')
    y_true_cls = tf.argmax(y_true, axis=1)
    x_image = tf.reshape(x, [-1, image_shape[0], image_shape[1], 1])
    # First layer( First kernal)
    W_conv1 = weight_variable([kernal_shape[0], kernal_shape[1], 1, num_kernal_1])
    b_conv1 = bias_variable([num_kernal_1])
    h_conv1 = tf.nn.selu(tf.nn.conv2d(x_image, W_conv1, [1,1,1,1], 'SAME') + b_conv1)
    # Second layer( Second kernal)
    W_conv2 = weight_variable([kernal_shape[0], kernal_shape[1], num_kernal_1, num_kernal_2])
    b_conv2 = bias_variable([num_kernal_2])
    h_conv2 = tf.nn.selu(tf.nn.conv2d(h_conv1, W_conv2, [1,1,1,1], 'SAME') + b_conv2)
    # Third layer ( Fully connected)
    W_fc1 = weight_variable([image_shape[0] * image_shape[1] * num_kernal_2, num_conn_neural])
    b_fc1 = bias_variable([num_conn_neural])
    h_conv2_flat = tf.reshape(h_conv2, [ -1, image_shape[0] * image_shape[1] * num_kernal_2])
    h_fc1 = tf.nn.selu(tf.matmul(h_conv2_flat, W_fc1) + b_fc1)
    # Output layer
    W_fc2 = weight_variable([num_conn_neural, num_label])
    b_fc2 = bias_variable([num_label])
    layer_last = tf.matmul(h_fc1, W_fc2) + b_fc2
    y_pred = tf.nn.softmax(layer_last)
    y_pred_cls = tf.argmax(y_pred, axis=1)
    correct_prediction = tf.equal(y_pred_cls, y_true_cls)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    #-----------------------------------
    # Saver
    saver = tf.train.Saver()
    print ("AI:{0}".format(AI_saved_dir))
    if not os.path.exists(AI_saved_dir):
        print ("No AI can be restore, please check folder ./checkpoints")
    save_path = os.path.join(AI_saved_dir, 'best_validation')
    #-----------------------------------
    # Tensorflow run
    session = tf.Session()
    # restore previous weight
    saver.restore(sess=session, save_path=save_path)
    
    def predict_label(images, labels):
        # Number of images.
        num_images = len(images)
        # initialize
        label_pred = np.zeros(num_images*3).reshape((num_images, 3))
        feed_dict = {x: images[:,pick_band_array], y_true: labels[:]}
        # process 
        label_pred = session.run(y_pred, feed_dict=feed_dict)
        return label_pred
    
    label_pred = predict_label(test_images, test_labels)
    
    print ('label_pred:{0}'.format(label_pred))

    session.close()


#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    # Data for testing the main functions.
    test_images = np.arange(16).reshape((-1,16))
    test_labels = np.array([1,0,0]).reshape((-1, 3))
    main(test_images, test_labels)
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
