#!/usr/bin/python3
'''
Abstract:
    This is a code for test AI with given sed data in interactive mode.
Usage:
    sed_test_AI.py [AI]
Auther:
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
import matplotlib.pyplot as plt
# We need PrettyTensor.
import prettytensor as pt

def sigmoid(inp):
    return np.divide(1, 1+np.exp(-inp))

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
    grad = session.run(Adam_gradients, feed_dict = feed_dict)
    # Show the prediction in the terminal and gradients in plt.imshow
    print ('The prediction is {0}'.format(cls_pred))
    gradients_fig = plt.figure()
    for k, v in enumerate(grad):
        print ("{0}:\n{1}\n".format(tf.trainable_variables()[k], v[0].shape))
        im = plt.subplot(3, 6, k+1)
        plt.title(tf.trainable_variables()[k].name)
        try:
            plt.imshow(sigmoid(v[0]), vmin = 0, vmax = 1)
        except:
            v_res = np.array([v[0]])
            plt.imshow(sigmoid(v_res), vmin = 0, vmax = 1)
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.075, 0.8])
    plt.colorbar(cax=cax)
    gradients_fig.show()
    return grad 

# Show the ratio of current gradients and the last gradients.
def compare_grad(the_grad, last_grad):
    the_grad = np.array(the_grad)
    last_grad = np.array(last_grad)
    ratio = np.divide(the_grad, last_grad)
    ratio_fig = plt.figure()
    for k, v in enumerate(ratio):
        print ("{0}:\n{1}\n".format(tf.trainable_variables()[k], v[0].shape))
        im = plt.subplot(3, 6, k+1)
        plt.title(tf.trainable_variables()[k].name)
        try:
            plt.imshow(sigmoid(v[0]), vmin = 0, vmax = 1)
        except:
            v_res = np.array([v[0]])
            plt.imshow(sigmoid(v_res), vmin = 0, vmax = 1)
    plt.subplots_adjust(bottom=0.1, right=0.85, top=0.9)
    cax = plt.axes([0.90, 0.1, 0.025, 0.8])
    plt.colorbar(cax=cax)
    ratio_fig.show()
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
        print ("The number of arguments is wrong")
        print ("Usage: sed_test_AI.py [AI]")
        print ("AI could be 'skip', then no AI will be loaded.")
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
    Adam_gradients = tf.train.AdamOptimizer().compute_gradients(loss)
    GD_gradients = tf.train.GradientDescentOptimizer(learning_rate = 0.001).compute_gradients(loss)
    #-----------------------------------
    # Tensorflow run
    session = tf.Session()
    # Restore trained weight
    if AI_saved_dir == 'skip':
        print ('No AI will be loaded.')
        session.run(tf.global_variables_initializer())
    else:
        saver = tf.train.Saver()
        print ("AI:{0}".format(AI_saved_dir))
        if not os.path.exists(AI_saved_dir):
            print ("No AI can be restore, please check folder ./checkpoints")
            exit(1)
        save_path = os.path.join(AI_saved_dir, 'checkpoint_AI_64_8_source_sed_MaxLoss0/best_validation')
        saver.restore(sess=session, save_path=save_path)
    # Test the restored AI interactively.
    last_grad = None
    while True:
        the_grad = test_data()
        # Compare the gradients with the last.
        do_compare = input("Compare with the last gradients? (y/n): ")
        if do_compare == 'y':
            compare_grad(the_grad, last_grad)
        # Stop or continue?
        escape = input("Continue? (y/n): ")
        if escape == 'n':
            break
        else:
            last_grad = the_grad
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
