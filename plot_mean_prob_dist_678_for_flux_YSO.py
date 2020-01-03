#!/usr/bin/python3
'''
Abstract:
    This is a program for ploting probability distribution of labels. 
Usage:
    plot_prob_dist.py [AI dir list]
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
20191016 version alpha 2:
    1. Assign star as blue, YSO as red.
'''
import matplotlib.pyplot as plt
from matplotlib import cm
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
from scipy.interpolate import RegularGridInterpolator

# Assign RGB color to represent MP 1 magnitude. 

def rebin3d(arr, new_shape):
    shape = (new_shape[0], arr.shape[0] // new_shape[0],
             new_shape[1], arr.shape[1] // new_shape[1],
             new_shape[2], arr.shape[2] // new_shape[2],
    )
    return arr.reshape(shape).mean(-1).mean(3).mean(1)

def plot_prob(arti_mag, sort_order):
    # Print the color for each MP1 slice
    fig = plt.figure(
        figsize = (8,8)
        )
    ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(
    #    arti_mag[:, 0], 
    #    arti_mag[:, 1], 
    #    arti_mag[:, 2], 
    #    s = 1,
    #)
    ax.plot_trisurf(
        arti_mag[:, 0], 
        arti_mag[:, 1], 
        arti_mag[:, 2], 
        cmap='jet',
        edgecolor='none'
    )
    ax.set_xlim(np.amin(IR3_arti_mag[:,0]), np.amax(IR3_arti_mag[:,0]))
    ax.set_ylim(np.amin(IR4_arti_mag[:,0]), np.amax(IR4_arti_mag[:,0]))
    ax.set_zlim(np.amin(MP1_arti_mag[:,0]), np.amax(MP1_arti_mag[:,0]))
    ax.set_xlabel(
        "{0} (log(mJy))".format(sort_order[0]),
        fontsize=16)
    ax.set_ylabel(
        "{0} (log(mJy))".format(sort_order[1]),
        fontsize=16)
    ax.set_zlabel(
        "{0} (log(mJy))".format(sort_order[2]),
        fontsize=16)
    #plt.show()
    plt.savefig(
        'probability_distribution_for_YSO.png',
        dpi = 300,
        )
    return

# This is a function for classifying sources using Model IV.
def scao_model_iv(AI_saved_dir, arti_flux_678, arti_label_678):
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
    #-----------------------------------
    # Make a prediction
    def predict_label(images, labels):
        # Number of images.
        num_images = len(images)
        # initialize
        label_pred = np.zeros(num_images*3).reshape((num_images, 3))
        feed_dict = {x: images[:], y_true: labels[:]}
        # process 
        label_pred = session.run(y_pred, feed_dict=feed_dict)
        return label_pred
    label_pred_678 = predict_label(arti_flux_678, arti_label_678)
    #-----------------------------------
    # Close session
    session.close()
    return label_pred_678
         

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure times
    start_time = time.time()    
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("Error! Usage: plot_prob_distribution.py [AI dir list]")
        exit(1)
    AI_saved_dir_list_name = argv[1]
    # Load data
    AI_saved_dir_list = np.loadtxt(
        AI_saved_dir_list_name, 
        dtype = str,
        delimiter = '\n')
    #-----------------------------------
    # Initialize
    #reduced_num_ticks = 50
    num_ticks = 400
    # Calculate the probability distribution of labels
    band_system = convert_lib.set_SCAO()
    fake_error = np.ones(num_ticks)
    IR3_arti_flux = np.transpose(
        [   np.logspace(
                np.log10(0.000107), 
                np.log10(100.0), 
                num=num_ticks),
            fake_error])
    IR4_arti_flux = np.transpose(
        [   np.logspace(
                np.log10(0.000216), 
                np.log10(320.0), 
                num=num_ticks),
            fake_error])
    MP1_arti_flux = np.transpose(
        [   np.logspace(
                np.log10(0.000898), 
                np.log10(1000.0), 
                num=num_ticks),
            fake_error])
    IR3_arti_mag = np.log10(IR3_arti_flux)
    IR4_arti_mag = np.log10(IR4_arti_flux)
    MP1_arti_mag = np.log10(MP1_arti_flux)
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
    # Make predictions using each run
    sum_label_pred_678 = np.zeros(arti_flux_678.shape)
    for AI_saved_dir in AI_saved_dir_list:
        label_pred_678 = scao_model_iv(AI_saved_dir, arti_flux_678, arti_label_678)
        sum_label_pred_678 += label_pred_678
    mean_label_pred_678 = np.divide(sum_label_pred_678, len(AI_saved_dir_list))
    #-----------------------------------
    # Quantize the probability
    mean_label_pred_678[mean_label_pred_678 >= 0.5] = 1.0
    mean_label_pred_678[mean_label_pred_678 < 0.5]  = 0.0
    mean_cls_pred_678 = np.argmax(mean_label_pred_678, axis = 1)
    #-----------------------------------
    # Shows the degenerate data and pred_labels to band IRAC3, IRAC4, and MIPS1
    sort_order_678 = ['IRAC3', 'IRAC4', 'MIPS1']
    # Plot YSO only
    index_YSO = np.where(mean_cls_pred_678 == 2)
    arti_mag_678_YSO = arti_mag_678[index_YSO]
    print ('Plot the 3D map')
    plot_prob(arti_mag_678_YSO, sort_order_678)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
