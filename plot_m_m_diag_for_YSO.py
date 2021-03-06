#!/usr/bin/python3
'''
Abstract:
    This is a program for ploting probability distribution of labels. 
Usage:
    plot_prob_distribution.py [AI dir list] [yso sed list]
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
import tensorflow as tf
import numpy as np
import time
from sys import argv
import os
import itertools
from sed_test_cnn import bias_variable, weight_variable
import convert_lib

def lower_bound(arti_mag_78, arti_flux_78, ratio, AI_saved_dir_list):
    IR3_arti_flux = np.reshape(arti_flux_78[:,0] * ratio, (-1, 1))
    IR3_arti_mag = np.log10(IR3_arti_flux)
    arti_mag_678 = np.hstack((IR3_arti_mag, arti_mag_78))
    arti_flux_678 = np.hstack((IR3_arti_flux, arti_flux_78))
    arti_label_678 = np.zeros(arti_flux_678.shape)
    #-----------------------------------
    # Make predictions using each run
    sum_label_pred_678 = np.zeros(arti_flux_678.shape)
    for AI_saved_dir in AI_saved_dir_list:
        label_pred_678 = scao_model_iv(AI_saved_dir, arti_flux_678, arti_label_678)
        sum_label_pred_678 += label_pred_678
    mean_label_pred_678 = np.divide(sum_label_pred_678, len(AI_saved_dir_list))
    mean_cls_pred_678 = np.argmax(mean_label_pred_678, axis = 1)
    #-----------------------------------
    # Take the YSO region only
    index_YSO = np.where(mean_cls_pred_678 == 2)
    arti_mag_678_YSO = arti_mag_678[index_YSO]
    # Find the IR3-IR4 YSO 50% surface
    yso_lb_MP1 = np.zeros(len(IR4_arti_mag))
    for i, s in enumerate(IR4_arti_mag[:,0]):
        # Denote the row matching the given IR3, IR4 fluxes.
        match = np.where((arti_mag_678_YSO[:,1] == s))[0]
        # Assign the minimum value to not found case.
        # Skip if no YSOs are found.
        if len(match) == 0:
            yso_lb_MP1[i] == 0
        else:
            yso_lb_MP1[i] = np.amin(arti_mag_678_YSO[match,2])
    # Pick sources on the diagnal line on IR3-IR4 surface
    yso_lb_IR3_flux = IR4_arti_flux[:,0] * ratio 
    yso_lb_IR3 = np.log10(yso_lb_IR3_flux) 
    return yso_lb_IR3, yso_lb_MP1 

def plot_line(ax, IR3_mag, MP1_mag, ratio):
    ax.plot(IR3_mag, MP1_mag, '-', label = 'IR3/IR4 flux ratio = {0}'.format(ratio))
    return

def plot_source(ax, star_678, gala_678, yso_678):
    # Plot real yso on this line chart.
    star_6 = np.log10(star_678[:,0])
    star_8 = np.log10(star_678[:,2])
    ax.scatter(star_6, star_8, c='b', s=2, label = 'real star')
    gala_6 = np.log10(gala_678[:,0])
    gala_8 = np.log10(gala_678[:,2])
    ax.scatter(gala_6, gala_8, c='g', s=2, label = 'real gala')
    yso_6 = np.log10(yso_678[:,0])
    yso_8 = np.log10(yso_678[:,2])
    ax.scatter(yso_6, yso_8, c='r', s=2, label = 'real yso')
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
    if len(argv) != 5:
        print ("Error! Usage: plot_prob_distribution.py [AI dir list] [star sed list] [gala sed list] [yso sed list]")
        exit(1)
    AI_saved_dir_list_name = argv[1]
    star_list_name = argv[2]
    gala_list_name = argv[3]
    yso_list_name = argv[4]
    # Load data
    print ('Loading data')
    AI_saved_dir_list = np.loadtxt(
        AI_saved_dir_list_name, 
        dtype = str,
        delimiter = '\n')
    star_sed_list = np.loadtxt(star_list_name)
    star_678 = star_sed_list[:,5:]
    gala_sed_list = np.loadtxt(gala_list_name)
    gala_678 = gala_sed_list[:,5:]
    yso_sed_list = np.loadtxt(yso_list_name)
    yso_678 = yso_sed_list[:,5:]
    #-----------------------------------
    # Initialize
    num_ticks = 400
    # Calculate the probability distribution of labels
    band_system = convert_lib.set_SCAO()
    fake_error = np.ones(num_ticks)
    IR4_arti_flux = np.transpose(
        [   np.logspace(
                np.log10(0.001), 
                np.log10(10000.0), 
                num=num_ticks),
            fake_error])
    MP1_arti_flux = IR4_arti_flux[:]
    # Define IR3/IR4 = ratio
    #ratios = [0.2, 0.5, 1.0, 2]
    ratios = [1.0]
    IR4_arti_mag = np.log10(IR4_arti_flux)
    MP1_arti_mag = np.log10(MP1_arti_flux)
    arti_mag_78 = np.asarray(list(itertools.product(   
        IR4_arti_mag[:,0], 
        MP1_arti_mag[:,0])))
    arti_flux_78 = np.asarray(list(itertools.product(  
        IR4_arti_flux[:,0], 
        MP1_arti_flux[:,0])))
    #---------------------------------------
    # Plot the IR3 vs. MP1 on a line chart
    fig, ax = plt.subplots(
        figsize = (8,6))
    #-----------------------------------------
    # Find the YSO lower bond
    for r in ratios:
        yso_lb_IR3, yso_lb_MP1 = lower_bound(arti_mag_78, arti_flux_78, r, AI_saved_dir_list)
        plot_line(ax, yso_lb_IR3, yso_lb_MP1, r)
    plot_source(ax, star_678, gala_678, yso_678)
    # Set labels
    sort_order = ['IRAC 3', 'IRAC 4', 'MIPS 1']
    ax.set_ylim([-1, 4])
    ax.set_xlabel(
        "{0} (log(mJy))".format(sort_order[0]),
        fontsize=16)
    ax.set_ylabel(
        "{0} (log(mJy))".format(sort_order[2]),
        fontsize=16) 
    plt.legend()
    plt.savefig('IR34_vs_MP1_for_all_sources.png', dpi = 300)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
