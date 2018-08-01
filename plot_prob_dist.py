#!/usr/bin/python3
'''
Abstract:
    This is a program for ploting probability distribution of labels. 
Usage:
    plot_prob_dist.py [AI dir]
Editor and Practicer:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180730
####################################
update log
20180730 version alpha 1:
    1. The code works
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf
import numpy as np
import time
from sys import argv
import os
import prettytensor as pt
import itertools
from colour import Color

def degenerate(labels):
    jhk_linescales = np.asarray(list(itertools.product(np.arange(0.1, 1.1, 0.2), repeat=3)))
    answer = np.zeros((len(jhk_linescales), 3))
    for i in range(len(jhk_linescales)):
        ini = i * np.power(5, 5)
        fin = (i+1) * np.power(5, 5)
        answer[i] = np.mean(labels[ini:fin], axis = 0)
    return answer

# Assign RGB color to represent stars, galaxies, and YSOs.
def assign_color(color_code):
    red_code = color_code[:,0]
    green_code = color_code[:,1]
    blue_code = color_code[:,2]
    star_color = [ None for i in range(len(color_code)) ] 
    gala_color = [ None for i in range(len(color_code)) ] 
    ysos_color = [ None for i in range(len(color_code)) ] 
    for i, code in enumerate(red_code):
        star_color[i] = Color(rgb = (code, 0, 0)).hex_l
    for i, code in enumerate(green_code):
        gala_color[i] = Color(rgb = (0, code, 0)).hex_l
    for i, code in enumerate(blue_code):
        ysos_color[i] = Color(rgb = (0, 0, code)).hex_l
    return star_color, gala_color, ysos_color
    
def predict_label(images):
    # Number of images.
    num_images = len(images)
    # initialize
    label_pred = np.zeros(num_images*3).reshape((num_images, 3))
    feed_dict = {x: images}
    # process 
    label_pred = session.run(y_pred, feed_dict=feed_dict)
    return label_pred

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()    
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("Error! Usage: plot_prob_distribution.py [AI dir]")
        exit(1)
    AI_saved_dir = argv[1]
    #-----------------------------------
    # Load AI
    # Dimension setup
    # We know that MNIST images are 28 pixels in each dimension.
    img_size = 16
    print ("image size = {0}".format(img_size))
    # Images are stored in one-dimensional arrays of this length.
    img_size_flat = img_size * 1
    # Tuple with height and width of images used to reshape arrays.
    img_shape = (img_size, 1)
    # Number of colour channels for the images: 1 channel for gray-scale.
    num_channels = 1
    # Number of classes, one class for each of 10 digits.
    num_classes = 3
    #-----------------------------------
    # Define Tensorflow Graph
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
    #-----------------------------------
    # Saver
    saver = tf.train.Saver()
    print ("AI:{0}".format(AI_saved_dir))
    if not os.path.exists(AI_saved_dir):
        print ("No AI can be restore, please check folder ./checkpoints")
        exit(1)
    save_path = os.path.join(AI_saved_dir, 'best_validation')
    #-----------------------------------
    # Tensorflow run
    session = tf.Session()
    # restore previous weight
    saver.restore(sess=session, save_path=save_path)
    batch_size = 512
    print ("batch_size = {0}".format(batch_size))
    #-----------------------------------
    # Calculate the probability distribution of labels
    arti_data = np.asarray(list(itertools.product(np.arange(0.1, 1.1, 0.2), repeat=8)))
    arti_data = np.append(arti_data, np.full((len(arti_data), 8), 0.1), axis = 1)
    label_pred = predict_label(arti_data)
    print (arti_data[:10])
    print ("length of arti_data = {0}".format(len(arti_data)))
    print (label_pred[:10])
    print ("length of label_pred = {0}".format(len(label_pred)))
    # degenerate data and pred_labels to band JHK
    print ('--- degenerate data and pred_labels to band JHK ---')
    arti_data_JHK = np.asarray(list(itertools.product(np.arange(0.1, 1.1, 0.2), repeat = 3))) 
    arti_data_JHK = np.append(arti_data_JHK, np.full((len(arti_data_JHK), 5), 0.5), axis = 1)
    arti_data_JHK = np.append(arti_data_JHK, np.full((len(arti_data_JHK), 8), 0.1), axis = 1)
    label_pred_JHK = degenerate(label_pred)
    print (arti_data_JHK[:10])
    print ("length of arti_data_JHK = {0}".format(len(arti_data_JHK)))
    print (label_pred_JHK)
    print ("length of label_pred_JHK = {0}".format(len(label_pred_JHK)))
    star_color, gala_color, ysos_color = assign_color(label_pred_JHK)
    #-----------------------------------
    # Plot 3D distribution
    fig = plt.figure()
    # Star
    ax = fig.add_subplot(221, projection='3d')
    ax.scatter(xs = arti_data_JHK[:,0], ys = arti_data_JHK[:,1], zs = arti_data_JHK[:,2], zdir='z', s=20, c=star_color, depthshade=False)
    # Galaxy
    ax = fig.add_subplot(222, projection='3d')
    ax.scatter(xs = arti_data_JHK[:,0], ys = arti_data_JHK[:,1], zs = arti_data_JHK[:,2], zdir='z', s=20, c=gala_color, depthshade=False)
    # YSOs
    ax = fig.add_subplot(223, projection='3d')
    ax.scatter(xs = arti_data_JHK[:,0], ys = arti_data_JHK[:,1], zs = arti_data_JHK[:,2], zdir='z', s=20, c=ysos_color, depthshade=False)
    fig.show()
    #-----------------------------------
    # Close session
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
