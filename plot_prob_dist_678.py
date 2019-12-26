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
import itertools
from colour import Color
from sed_test_cnn import bias_variable, weight_variable
from convert_lib import ensemble_mjy_to_mag
import convert_lib

# Assign RGB color to represent stars, galaxies, and YSOs.
def assign_color(color_code):
    sgys_color = [Color(rgb = tuple(color_code[i])).hex_l for i in range(len(color_code))] 
    sgys_color = np.asarray(sgys_color)
    return sgys_color 

def predict_label(images, labels):
    # Number of images.
    num_images = len(images)
    # initialize
    label_pred = np.zeros(num_images*3).reshape((num_images, 3))
    feed_dict = {x: images[:], y_true: labels[:]}
    # process 
    label_pred = session.run(y_pred, feed_dict=feed_dict)
    return label_pred
    
def plot_prob(arti_mag, sgys_color, sort_order):
    # Print the color for each IR3 slice
    print ("IR3")
    for i, IR3 in enumerate(IR3_arti_mag):
        fig = plt.figure(figsize = (8,8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter( xs = arti_mag[np.where(arti_mag[:,0] == IR3[0]), 0], 
                    ys = arti_mag[np.where(arti_mag[:,0] == IR3[0]), 1], 
                    zs = arti_mag[np.where(arti_mag[:,0] == IR3[0]), 2], 
                    zdir='z', 
                    s=5, 
                    c = sgys_color[np.where(arti_mag[:,0] == IR3[0])],
                    depthshade=False)
        ax.set_title("Star/Galaxy/YSO probability")
        ax.set_xlim(np.amin(IR3_arti_mag[:,0]), np.amax(IR3_arti_mag[:,0]))
        ax.set_ylim(np.amin(IR4_arti_mag[:,0]), np.amax(IR4_arti_mag[:,0]))
        ax.set_zlim(np.amin(MP1_arti_mag[:,0]), np.amax(MP1_arti_mag[:,0]))
        ax.set_xlabel(sort_order[0])
        ax.set_ylabel(sort_order[1])
        ax.set_zlabel(sort_order[2])
        plt.savefig('probability_distribution_along_{0}_{1:03d}.png'
                    .format(sort_order[0], 
                    i))
        if i%20 == 0:
            plt.close()
        print ('number {0}, done.'.format(i))
    print ("IR4")
    # Print the color for each IR4 slice
    for i, IR4 in enumerate(IR4_arti_mag):
        fig = plt.figure(figsize = (8,8))
        ax = fig.add_subplot(111, projection='3d')
        #print (np.where(arti_mag[:,1] == IR4[0]))
        ax.scatter( xs = arti_mag[np.where(arti_mag[:,1] == IR4[0]), 0], 
                    ys = arti_mag[np.where(arti_mag[:,1] == IR4[0]), 1], 
                    zs = arti_mag[np.where(arti_mag[:,1] == IR4[0]), 2], 
                    zdir='z', 
                    s=5, 
                    c = sgys_color[np.where(arti_mag[:,1] == IR4[0])],
                    depthshade=False)
        ax.set_title("Star/Galaxy/YSO probability")
        ax.set_xlim(np.amin(IR3_arti_mag[:,0]), np.amax(IR3_arti_mag[:,0]))
        ax.set_ylim(np.amin(IR4_arti_mag[:,0]), np.amax(IR4_arti_mag[:,0]))
        ax.set_zlim(np.amin(MP1_arti_mag[:,0]), np.amax(MP1_arti_mag[:,0]))
        ax.set_xlabel(sort_order[0])
        ax.set_ylabel(sort_order[1])
        ax.set_zlabel(sort_order[2])
        plt.savefig('probability_distribution_along_{0}_{1:03d}.png'
                    .format(sort_order[1], 
                            i))
        if i%20 == 0:
            plt.close()
        print ('number {0}, done.'.format(i))
    print ('MP1')
    # Print the color for each MP1 slice
    for i, MP1 in enumerate(MP1_arti_mag):
        fig = plt.figure(figsize = (8,8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter( xs = arti_mag[np.where(arti_mag[:,2] == MP1[0]), 0], 
                    ys = arti_mag[np.where(arti_mag[:,2] == MP1[0]), 1], 
                    zs = arti_mag[np.where(arti_mag[:,2] == MP1[0]), 2], 
                    zdir='z', 
                    s=5, 
                    c = sgys_color[np.where(arti_mag[:,2] == MP1[0])],
                    depthshade=False)
        ax.set_title("Star/Galaxy/YSO probability")
        ax.set_xlim(np.amin(IR3_arti_mag[:,0]), np.amax(IR3_arti_mag[:,0]))
        ax.set_ylim(np.amin(IR4_arti_mag[:,0]), np.amax(IR4_arti_mag[:,0]))
        ax.set_zlim(np.amin(MP1_arti_mag[:,0]), np.amax(MP1_arti_mag[:,0]))
        ax.set_xlabel(sort_order[0])
        ax.set_ylabel(sort_order[1])
        ax.set_zlabel(sort_order[2])
        plt.savefig('probability_distribution_along_{0}_{1:03d}.png'
                    .format(sort_order[2], 
                            i))
        if i%20 == 0:
            plt.close()
        print ('number {0}, done.'.format(i))
    return

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure times
    start_time = time.time()    
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("Error! Usage: plot_prob_distribution.py [AI dir]")
        exit(1)
    AI_saved_dir = argv[1]
    #-----------------------------------
    # Calculate the probability distribution of labels
    band_system = convert_lib.set_SCAO()
    fake_error = np.ones(100)
    IR3_arti_flux = np.transpose([  np.logspace(np.log10(0.000107), np.log10(5500.0), num=100),
                                    fake_error
                                    ])
    IR4_arti_flux = np.transpose([  np.logspace(np.log10(0.000216), np.log10(3830.0), num=100),
                                    fake_error
                                    ])
    MP1_arti_flux = np.transpose([  np.logspace(np.log10(0.000898), np.log10(4370.0), num=100),
                                    fake_error
                                    ])
    print (IR3_arti_flux.shape)
    print (IR4_arti_flux.shape)
    print (MP1_arti_flux.shape)
    IR3_arti_mag = ensemble_mjy_to_mag(IR3_arti_flux, 'IR3', band_system )
    IR4_arti_mag = ensemble_mjy_to_mag(IR4_arti_flux, 'IR4', band_system )
    MP1_arti_mag = ensemble_mjy_to_mag(MP1_arti_flux, 'MP1', band_system )
    arti_mag_678 = np.asarray(list(itertools.product(   IR3_arti_mag[:,0], 
                                                        IR4_arti_mag[:,0], 
                                                        MP1_arti_mag[:,0]
                                                        )))
    arti_flux_678 = np.asarray(list(itertools.product(  IR3_arti_flux[:,0], 
                                                        IR4_arti_flux[:,0], 
                                                        MP1_arti_flux[:,0]
                                                        )))
    arti_label_678 = np.zeros(arti_flux_678.shape)
    #-----------------------------------
    # Load AI
    print ('Loading AI...')
    width_of_data = 1
    img_maj = 3
    image_shape = (width_of_data, img_maj)
    kernal_shape = (width_of_data, 2)
    num_kernal_1 = 32
    num_kernal_2 = 64
    num_conn_neural = 100
    num_label = 3 
    #-----------------------------------
    # Construct an AI
    tf.reset_default_graph()
    x = tf.placeholder(tf.float32, [None, width_of_data * img_maj], name = 'x')
    y_true = tf.placeholder(tf.float32, [None, 3], name = 'y_true')
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
    # Saver
    saver = tf.train.Saver()
    print ("AI:{0}".format(AI_saved_dir))
    if not os.path.exists(AI_saved_dir):
        print ("No AI can be restore, please check folder ./checkpoints")
        exit(1)
    save_path = os.path.join(AI_saved_dir, 'best_validation')
    session = tf.Session()
    # Restore previous weight
    saver.restore(sess=session, save_path=save_path)
    batch_size = 512
    #-----------------------------------
    # Make a prediction
    label_pred_678 = predict_label(arti_flux_678, arti_label_678)
    #-----------------------------------
    # Shows the degenerate data and pred_labels to band IRAC3, IRAC4, and MIPS1
    sort_order_678 = ['IRAC3', 'IRAC4', 'MIPS1']
    print ('Assign the color')
    sgys_color_678 = assign_color(label_pred_678)
    print ('Plot the 3D map')
    plot_prob(arti_mag_678, sgys_color_678, sort_order_678)
    #-----------------------------------
    # Close session
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
