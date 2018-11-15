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
from IPython.core.pylabtools import figsize
import tensorflow as tf
import numpy as np
import time
from sys import argv
import os
import itertools
import prettytensor as pt

def predict_label(images):
    # Number of images.
    num_images = len(images)
    # initialize
    label_pred = np.zeros(num_images*3).reshape((num_images, 3))
    feed_dict = {x: images}
    # process 
    label_pred = session.run(y_pred, feed_dict=feed_dict)
    return label_pred

def plot_mean_possible_sed(star_sed, err_star_sed, gala_sed, err_gala_sed, ysoc_sed, err_ysoc_sed, figure_name):
    fig = plt.figure(figsize=(12, 8))
    # Star
    ax = fig.add_subplot(221)
    ax.errorbar(range(1, 9), star_sed[:8], yerr = err_star_sed[:8])
    ax.set_title("Mean possible SED of stars")
    ax.set_xlabel('bands')
    ax.set_ylabel('normalized flux')
    # Galaxy
    ax = fig.add_subplot(222)
    ax.errorbar(range(1, 9), gala_sed[:8], yerr = err_gala_sed[:8])
    ax.set_title("Mean possible SED of galaxies")
    ax.set_xlabel('bands')
    ax.set_ylabel('normalized flux')
    # YSOs
    ax = fig.add_subplot(223)
    ax.errorbar(range(1, 9), ysoc_sed[:8], yerr = err_ysoc_sed[:8])
    ax.set_title("Mean possible SED of YSOc")
    ax.set_xlabel('bands')
    ax.set_ylabel('normalized flux')
    # Save figure
    plt.savefig(figure_name)
    return

def plot_most_possible_sed(arti_data, index_sorted_by_star, index_sorted_by_gala, index_sorted_by_ysoc):
    fig = plt.figure(figsize=(12, 12))
    # Star
    ax = fig.add_subplot(221)
    for i in range(1, 101):
        ax.plot(range(1, 9), arti_data[index_sorted_by_star[-i],:8], alpha = 0.05)
    ax.set_title("Most possible SED of stars")
    ax.set_xlabel('bands')
    ax.set_ylabel('normalized flux')
    # Galaxy
    ax = fig.add_subplot(222)
    for i in range(1, 101):
        ax.plot(range(1, 9), arti_data[index_sorted_by_gala[-i],:8], alpha = 0.05)
    ax.set_title("Most possible SED of galaxies")
    ax.set_xlabel('bands')
    ax.set_ylabel('normalized flux')
    # YSOs
    ax = fig.add_subplot(223)
    for i in range(1, 101):
        ax.plot(range(1, 9), arti_data[index_sorted_by_ysoc[-i],:8], alpha = 0.05)
    ax.set_title("Most possible SED of YSOc")
    ax.set_xlabel('bands')
    ax.set_ylabel('normalized flux')
    # Save figure
    plt.savefig('Most_possible_SEDs.png')
    return

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure times
    start_time = time.time()    
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("Error! Usage: plot_prob_distribution.py [AI dir] [mask]")
        print ("Available mask: allOBS, maskJHK, mask78")
        exit(1)
    AI_saved_dir = argv[1]
    mask = argv[2]
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
    #-----------------------------------
    # Calculate the probability distribution of labels
    arti_data = np.asarray(list(itertools.product(np.arange(0.1, 1.1, 0.2), repeat=8)))
    arti_data = np.append(arti_data, np.full((len(arti_data), 8), 0.1), axis = 1)
    # Load data mask
    test_arti_data = arti_data[:]
    if mask == "allOBS":
        pass
    elif mask == "maskJHK":
        test_arti_data[:,0] = 0.
        test_arti_data[:,8] = 0.
        test_arti_data[:,1] = 0.
        test_arti_data[:,9] = 0.
        test_arti_data[:,2] = 0.
        test_arti_data[:,10] = 0.
    elif mask == "mask78":
        test_arti_data[:,6] = 0.
        test_arti_data[:,14] = 0.
        test_arti_data[:,7] = 0.
        test_arti_data[:,15] = 0.
    else:
        print ("Wrong mask")
        exit(1)
    label_pred = predict_label(test_arti_data)
    #-----------------------------------
    # Plot the mean of possible SEDs over 99%
    index_over_99_precent_star = np.where(label_pred[:,0] > 0.99)
    index_over_99_precent_gala = np.where(label_pred[:,1] > 0.99)
    index_over_99_precent_ysoc = np.where(label_pred[:,2] > 0.99)
    print (len(index_over_99_precent_star[0]))
    mean_99_star_sed = np.mean(arti_data[index_over_99_precent_star], axis = 0)
    mean_99_gala_sed = np.mean(arti_data[index_over_99_precent_gala], axis = 0)
    mean_99_ysoc_sed = np.mean(arti_data[index_over_99_precent_ysoc], axis = 0)
    err_mean_99_star_sed = np.std(arti_data[index_over_99_precent_star], axis = 0)
    err_mean_99_gala_sed = np.std(arti_data[index_over_99_precent_gala], axis = 0)
    err_mean_99_ysoc_sed = np.std(arti_data[index_over_99_precent_ysoc], axis = 0)
    plot_mean_possible_sed( mean_99_star_sed, err_mean_99_star_sed, 
                            mean_99_gala_sed, err_mean_99_gala_sed, 
                            mean_99_ysoc_sed, err_mean_99_ysoc_sed, 
                            "Mean_of_99_possible_SEDs.png")
    #-----------------------------------
    # Plot the mean of possible SEDs over 99.9%
    index_over_999_precent_star = np.where(label_pred[:,0] > 0.999)
    index_over_999_precent_gala = np.where(label_pred[:,1] > 0.999)
    index_over_999_precent_ysoc = np.where(label_pred[:,2] > 0.999)
    print (len(index_over_999_precent_star[0]))
    mean_999_star_sed = np.mean(arti_data[index_over_999_precent_star], axis = 0)
    mean_999_gala_sed = np.mean(arti_data[index_over_999_precent_gala], axis = 0)
    mean_999_ysoc_sed = np.mean(arti_data[index_over_999_precent_ysoc], axis = 0)
    err_mean_999_star_sed = np.std(arti_data[index_over_999_precent_star], axis = 0)
    err_mean_999_gala_sed = np.std(arti_data[index_over_999_precent_gala], axis = 0)
    err_mean_999_ysoc_sed = np.std(arti_data[index_over_999_precent_ysoc], axis = 0)
    plot_mean_possible_sed( mean_999_star_sed, err_mean_999_star_sed, 
                            mean_999_gala_sed, err_mean_999_gala_sed, 
                            mean_999_ysoc_sed, err_mean_999_ysoc_sed, 
                            "Mean_of_999_possible_SEDs.png")
    #-----------------------------------
    # Plot the most possible SEDs of stars, galaxeis and YSOc
    index_sorted_by_star = label_pred[:,0].argsort()
    index_sorted_by_gala = label_pred[:,1].argsort()
    index_sorted_by_ysoc = label_pred[:,2].argsort()
    '''
    print ("Most possible stars")
    for i in range(1, 101):
        printed_data = [str(x) for x in arti_data[index_sorted_by_star[-i],:8] ]
        print ("{0}. ({1}): {2:.2f}%".format(i, ', '.join(printed_data), label_pred[index_sorted_by_star[-i], 0]*100))
    print ("Most possible galaxies")
    for i in range(1, 101):
        printed_data = [str(x) for x in arti_data[index_sorted_by_gala[-i],:8] ]
        print ("{0}. ({1}): {2:.2f}%".format(i, ', '.join(printed_data), label_pred[index_sorted_by_gala[-i], 1]*100))
    print ("Most possible YSOc")
    for i in range(1, 101):
        printed_data = [str(x) for x in arti_data[index_sorted_by_ysoc[-i],:8] ]
        print ("{0}. ({1}): {2:.2f}%".format(i, ', '.join(printed_data), label_pred[index_sorted_by_ysoc[-i], 2]*100))
    '''
    plot_most_possible_sed(arti_data, index_sorted_by_star, index_sorted_by_gala, index_sorted_by_ysoc)
    #-----------------------------------
    # Close session
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
