#!/usr/bin/python3
'''
Abstract:
    This is a code for test AI with given sed data in interactive mode.
Usage:
    sed_test_AI.py [AI]
Editor and Practicer:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181015
####################################
update log
20181015 version alpha 1:
    1. I copy the program from sed_test_AI_64.py, and modify a little bit.
        Now it works.
'''
import tensorflow as tf
import numpy as np
import time
from sys import argv
import os
# We need PrettyTensor.
import prettytensor as pt

# Return the prediction manually.
def test_data():
    _input_sed = None
    _input_label = None
    while True:
        _input_sed_string = input("SED with 16 digits:\n>>> ")
        _input_sed = np.array([[float(x) for x in _input_sed_string.split()]])
        _input_label_string = input("Label with 3 digits:\n>>> ")
        _input_label = np.array([[float(x) for x in _input_label_string.split()]])
        if len(_input_sed[0]) != 16:
            print ("The digits of SED is wrong, 16 needed, {0} provide.".format(len(_input_sed[0])))
            continue
        elif len(_input_label[0]) != 3:
            print ("The digits of label is wrong, 3 needed, {0} provide.".format(len(_input_label[0])))
            continue
        else:
            break
    feed_dict = {   x:_input_sed, 
                    y_true:_input_label }
    cls_pred = session.run(y_pred, feed_dict = feed_dict)
    grad = session.run(gradients, feed_dict = feed_dict)
    print ('The prediction is {0}'.format(cls_pred))
    print ('The gradient is {0}'.format(grad))
    return 

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------
    # Load arguments
    if len(argv) != 2:
        print ('Error')
        print("The number of arguments is wrong")
        exit()
    AI_saved_dir = argv[1]
    #-----------------------------------
    # Define the data dimension
    # Images are stored in one-dimensional arrays of this length.
    img_size_flat = 16
    img_size = 16
    # Tuple with height and width of images used to reshape arrays.
    img_shape = (img_size, 1)
    # Number of colour channels for the images: 1 channel for gray-scale.
    num_channels = 1
    # Number of classes, one class for each of 10 digits.
    num_classes = 3
    #-----------------------------------
    # Tensorflow Graph
    x = tf.placeholder(tf.float32, shape=[None, img_size_flat], name='x')
    x_image = tf.reshape(x, [-1, img_size, 1, num_channels])
    y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')
    y_true_cls = tf.argmax(y_true, axis=1)
    #-----------------------------------
    # PrettyTensor Implementation
    x_pretty = pt.wrap(x_image)
    with pt.defaults_scope(activation_fn=tf.nn.relu6):
        y_pred, loss = x_pretty.\
            flatten().\
            fully_connected(size = 64, name='layer_fc1').\
            fully_connected(size = 64, name='layer_fc2').\
            fully_connected(size = 64, name='layer_fc3').\
            fully_connected(size = 64, name='layer_fc4').\
            fully_connected(size = 64, name='layer_fc5').\
            fully_connected(size = 64, name='layer_fc6').\
            fully_connected(size = 64, name='layer_fc7').\
            fully_connected(size = 64, name='layer_fc8').\
            softmax_classifier(num_classes=num_classes, labels=y_true)
    y_pred_cls = tf.argmax(y_pred, axis=1)
    correct_prediction = tf.equal(y_pred_cls, y_true_cls)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    for v in tf.trainable_variables():
        print (v.name)
    gradients = tf.train.AdamOptimizer().compute_gradients(loss)
    #-----------------------------------
    # Saver
    saver = tf.train.Saver()
    print ("AI:{0}".format(AI_saved_dir))
    if not os.path.exists(AI_saved_dir):
        print ("No AI can be restore, please check folder ./checkpoints")
        exit(1)
    save_path = os.path.join(AI_saved_dir, 'checkpoint_AI_64_8_source_sed_MaxLoss0/best_validation')
    print (save_path)
    #-----------------------------------
    # Tensorflow run
    session = tf.Session()
    # restore previous weight
    saver.restore(sess=session, save_path=save_path)
    batch_size = 512
    print ("batch_size = {0}".format(batch_size))
    # Test the restored AI interactively.
    while True:
        test_data()
        escape = input("Continue? (y/n)")
        if escape == 'n':
            break
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
