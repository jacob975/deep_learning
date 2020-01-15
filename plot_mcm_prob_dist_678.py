#!/usr/bin/python3
'''
Abstract:
    This is a program for ploting probability distribution of labels. 
Usage:
    plot_prob_distribution.py [AI dir list] [star sed list] [gala sed list] [yso sed list]
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

def plot_prob(arti_mag, sort_order, star_67, gala_67, yso_67):
    # Print YSO lower bond
    fig, ax = plt.subplots(
        figsize = (8,4))

    arti_mag_67 = np.unique(arti_mag[:,:2], axis = 0)
    print (arti_mag.shape)
    print (arti_mag_67.shape)
    arti_mag_8 = np.zeros(len(arti_mag_67))
    for i, s in enumerate(arti_mag_67):
        # Denote the row matching the given IR3, IR4 fluxes.
        match = np.where(
            (arti_mag[:,0] == s[0]) &\
            (arti_mag[:,1] == s[1]))[0]
        # Assign the minimum value
        # Skip if no YSOs are found.
        #print (len(match))
        if len(match) == 0:
            arti_mag_8[i] == -4 
        else:
            arti_mag_8[i] = np.amin(arti_mag[match,2]) 
    
    x = np.transpose(np.reshape(arti_mag_67[:,0], (num_ticks, num_ticks//2)))
    y = np.transpose(np.reshape(arti_mag_67[:,1], (num_ticks, num_ticks//2)))
    z = np.transpose(np.reshape(arti_mag_8, (num_ticks, num_ticks//2)))
    levels = np.linspace(-0.5, 4.5, 11)
    conti_levels = np.linspace(-0.5, 4.5, 1001)
    origin = 'lower'
    cs = ax.contourf(
        x, y, z,
        levels = conti_levels,
        cmap=cm.PuBu_r,
        origin = origin)
    cs2 = ax.contour(
        cs, 
        levels = levels, 
        colors=('k',),
        #linewidths=(3, 1,1,1,1,1,1,1,1,1),
        linewidths=(1,),
        origin = origin)
    cbar = plt.colorbar(cs)
    cbar.set_ticks([0.0, 1.0, 2.0, 3.0, 4.0])
    cbar.set_ticklabels([0.0, 1.0, 2.0, 3.0, 4.0])
    cbar.ax.set_ylabel(
        r'%s ($log_{10}$(mJy))' % sort_order[2],
        fontsize = 16)
    cbar.add_lines(cs2)
    # Plot real sources
    """
    ax.scatter(
        np.log10(star_67[:,0]),
        np.log10(np.divide(star_67[:,0], star_67[:,1])),
        s = 1, c = 'b')
    ax.scatter(
        np.log10(gala_67[:,0]),
        np.log10(np.divide(gala_67[:,0], gala_67[:,1])),
        s = 1, c = 'g')
    """
    ax.scatter(
        np.log10(yso_67[:,0]),
        np.log10(np.divide(yso_67[:,0], yso_67[:,1])),
        s = 1, c = 'r')
    # Plot line ratios
    """
    ratios = np.array([0.2, 0.5, 1, 2])
    log_ratios = np.log(ratios)
    for i, r in enumerate(log_ratios):
        ax.plot(
            [-3, 4], 
            [-3-r, 4-r], 
            label = 'IR3/IR4 flux ratio = {0}'.format(ratios[i]))
    """
    # Set labels
    ax.set_xlim([-1, 4])
    ax.set_ylim([-1.5, 1.5])
    ax.set_xlabel(
        r"%s ($log_{10}$(mJy))" % sort_order[0],
        fontsize=16)
    ax.set_ylabel(
        r"$log_{10}$(%s(mJy)/%s(mJy))" % (sort_order[0], sort_order[1]),
        fontsize=16)
    plt.legend()
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.savefig(
        'mcm_contour_probability_for_all_sources.png',
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
    if len(argv) != 5:
        print ("Error! Usage: plot_prob_distribution.py [AI dir list] [star sed list] [gala sed list] [yso sed list]")
        exit(1)
    AI_saved_dir_list_name = argv[1]
    star_list_name = argv[2]
    gala_list_name = argv[3]
    yso_list_name = argv[4]
    # Load data
    AI_saved_dir_list = np.loadtxt(
        AI_saved_dir_list_name, 
        dtype = str,
        delimiter = '\n')
    star_sed_list = np.loadtxt(star_list_name)
    star_67 = star_sed_list[:,5:7]
    gala_sed_list = np.loadtxt(gala_list_name)
    gala_67 = gala_sed_list[:,5:7]
    yso_sed_list = np.loadtxt(yso_list_name)
    yso_67 = yso_sed_list[:,5:7]
    #-----------------------------------
    # Initialize
    num_ticks = 200
    # Calculate the probability distribution of labels
    # Build the 3D flux cube
    # Flux first
    band_system = convert_lib.set_SCAO()
    IR3_arti_flux = np.logspace(-1, 4, num=num_ticks)
    MP1_arti_flux = np.logspace(-3, 5, num=num_ticks)
    IR3_IR4_ratio = np.logspace(-1.5, 1.5, num=num_ticks//2)
    flux_ratio_flux_cube = np.asarray(list(itertools.product(   
        IR3_arti_flux, 
        IR3_IR4_ratio, 
        MP1_arti_flux)))
    
    corr_IR4_flux = np.divide(flux_ratio_flux_cube[:,0], flux_ratio_flux_cube[:,1])
    
    arti_flux_678 = np.transpose([
        flux_ratio_flux_cube[:,0],
        corr_IR4_flux,
        flux_ratio_flux_cube[:,2]]) 
   
    # Then magnitude
    IR3_arti_mag = np.log10(IR3_arti_flux)
    MP1_arti_mag = np.log10(MP1_arti_flux)
    
    mag_ratio_mag_cube = np.asarray(list(itertools.product(
        IR3_arti_mag,
        np.log10(IR3_IR4_ratio),
        MP1_arti_mag)))
    
    corr_IR4_mag = mag_ratio_mag_cube[:,0] - mag_ratio_mag_cube[:,1]

    arti_mag_678 = np.transpose([
        mag_ratio_mag_cube[:,0],
        corr_IR4_mag,
        mag_ratio_mag_cube[:,2]]) 
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
    # Shows the degenerate data and pred_labels to band IRAC3, IRAC4, and MIPS1
    sort_order_678 = ['IRAC 3', 'IRAC 4', 'MIPS 1']
    # Plot YSO only
    index_YSO = np.where(mean_cls_pred_678 == 2)
    arti_mag_678_YSO = arti_mag_678[index_YSO]
    mag_ratio_mag_cube_YSO = mag_ratio_mag_cube[index_YSO]
    print ('Plot the 2D map')
    #plot_prob(arti_mag_678_YSO, sort_order_678, star_67, gala_67, yso_67)
    plot_prob(mag_ratio_mag_cube_YSO, sort_order_678, star_67, gala_67, yso_67)
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
