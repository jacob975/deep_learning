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
import prettytensor as pt
from colour import Color

def degenerate(data, labels, sort_order):
    # sort by sort_order 
    extend_data = np.append(data, labels, axis = 1)
    # set data type of each column
    extend_dtype = [('J', float), 
                    ('H', float), 
                    ('K', float), 
                    ('IRAC1', float), 
                    ('IRAC2', float), 
                    ('IRAC3', float), 
                    ('IRAC4', float), 
                    ('MIPS1', float), 
                    ('err_J', float), 
                    ('err_H', float), 
                    ('err_K', float), 
                    ('err_IRAC1', float), 
                    ('err_IRAC2', float), 
                    ('err_IRAC3', float), 
                    ('err_IRAC4', float), 
                    ('err_MIPS1', float), 
                    ('Star_prob', float), 
                    ('Gala_prob', float), 
                    ('YSOs_prob', float)]
    extend_data = extend_data.view(dtype = extend_dtype)
    extend_data = extend_data.reshape(extend_data.shape[:-1])
    extend_data = np.sort(extend_data, order = sort_order) 
    # Calculate the probability of each data point
    linescales = np.asarray(list(itertools.product(np.arange(0.1, 1.1, 0.2), repeat=3)))
    answer = np.zeros((len(linescales), 3))
    for i in range(len(linescales)):
        ini = i * np.power(5, 5)
        fin = (i+1) * np.power(5, 5)
        # Pick high reliable data (one of prob over 90%) only.
        sectional_data = extend_data[:][ini:fin]
        high_star_prob = np.where(sectional_data['Star_prob'] > 0.9)
        high_gala_prob = np.where(sectional_data['Gala_prob'] > 0.9)
        high_ysos_prob = np.where(sectional_data['YSOs_prob'] > 0.9)
        index_high_prob_data = list(set(high_star_prob[0]) | set(high_gala_prob[0]) | set(high_ysos_prob[0]))
        index_high_prob_data = np.asarray([index_high_prob_data])
        high_prob_data = sectional_data[ index_high_prob_data ]
        if len(high_prob_data) == 0:
            answer[i] = np.array([-999, -999, -999])
        else:
            star_pred = np.mean(high_prob_data['Star_prob'])
            gala_pred = np.mean(high_prob_data['Gala_prob'])
            ysos_pred = np.mean(high_prob_data['YSOs_prob'])
            answer[i] = np.array([star_pred, gala_pred, ysos_pred]) 
    return linescales, answer

# Assign RGB color to represent stars, galaxies, and YSOs.
def assign_color(color_code):
    star_code = color_code[:,0]
    gala_code = color_code[:,1]
    ysos_code = color_code[:,2]
    high_reliable = np.where(star_code != -999)
    star_color = [ None for i in range(len(color_code)) ] 
    gala_color = [ None for i in range(len(color_code)) ] 
    ysos_color = [ None for i in range(len(color_code)) ] 
    for i in range(len(star_code)):
        if star_code[i] == -999:
            star_color[i] = gala_color[i] = ysos_color[i] = 'skip'
        else:
            star_color[i] = Color(rgb = (star_code[i], 0, 0)).hex_l
            gala_color[i] = Color(rgb = (gala_code[i], 0, 0)).hex_l
            ysos_color[i] = Color(rgb = (ysos_code[i], 0, 0)).hex_l
    return high_reliable, np.array(star_color), np.array(gala_color), np.array(ysos_color)
    
def predict_label(images):
    # Number of images.
    num_images = len(images)
    # initialize
    label_pred = np.zeros(num_images*3).reshape((num_images, 3))
    feed_dict = {x: images}
    # process 
    label_pred = session.run(y_pred, feed_dict=feed_dict)
    return label_pred

def plot_prob(index_high_prob_data, arti_data, star_color, gala_color, ysos_color, sort_order):
    fig = plt.figure()
    # Star
    ax = fig.add_subplot(221, projection='3d')
    ax.scatter( xs = arti_data[index_high_prob_data, 0], 
                ys = arti_data[index_high_prob_data, 1], 
                zs = arti_data[index_high_prob_data, 2], 
                zdir='z', 
                s=100, 
                c = star_color[index_high_prob_data],
                depthshade=False)
    ax.set_title("Star probability")
    ax.set_xlabel(sort_order[0])
    ax.set_ylabel(sort_order[1])
    ax.set_zlabel(sort_order[2])
    # Galaxy
    ax = fig.add_subplot(222, projection='3d')
    ax.scatter( xs = arti_data[index_high_prob_data, 0], 
                ys = arti_data[index_high_prob_data, 1], 
                zs = arti_data[index_high_prob_data, 2], 
                zdir='z', 
                s=100, 
                c = gala_color[index_high_prob_data], 
                depthshade=False)
    ax.set_title("Galaxy probability")
    ax.set_xlabel(sort_order[0])
    ax.set_ylabel(sort_order[1])
    ax.set_zlabel(sort_order[2])
    # YSOs
    ax = fig.add_subplot(223, projection='3d')
    ax.scatter( xs = arti_data[index_high_prob_data, 0], 
                ys = arti_data[index_high_prob_data, 1], 
                zs = arti_data[index_high_prob_data, 2], 
                zdir='z', 
                s=100, 
                c = ysos_color[index_high_prob_data], 
                depthshade=False)
    ax.set_title("YSO probability")
    ax.set_xlabel(sort_order[0])
    ax.set_ylabel(sort_order[1])
    ax.set_zlabel(sort_order[2])
    plt.savefig('probability_distribution_{0}_{1}_{2}.png'.format(sort_order[0], sort_order[1], sort_order[2]))
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
    print ("length of arti_data = {0}".format(len(arti_data)))
    print ("length of label_pred = {0}".format(len(label_pred)))
    # degenerate data and pred_labels to band JHK
    sort_order_jhk = ['J', 'H', 'K']
    print ('--- degenerate data and pred_labels to band {0}, {1}, and {2} ---'.format(*sort_order_jhk))
    arti_data_JHK, label_pred_JHK = degenerate(arti_data, label_pred, sort_order_jhk)
    high_reliable_jhk, star_color_jhk, gala_color_jhk, ysos_color_jhk = assign_color(label_pred_JHK)
    # degenerate data and pred_labels to band IRAC1, IRAC3, and MIPS1
    sort_order_468 = ['IRAC1', 'IRAC3', 'MIPS1']
    print ('--- degenerate data and pred_labels to band {0}, {1}, and {2} ---'.format(*sort_order_468))
    arti_data_468, label_pred_468 = degenerate(arti_data, label_pred, sort_order_468)
    high_reliable_468, star_color_468, gala_color_468, ysos_color_468 = assign_color(label_pred_468)
    # degenerate data and pred_labels to band H, IRAC2, and MIPS1
    sort_order_258 = ['H', 'IRAC2', 'MIPS1']
    print ('--- degenerate data and pred_labels to band {0}, {1}, and {2} ---'.format(*sort_order_258))
    arti_data_258, label_pred_258 = degenerate(arti_data, label_pred, sort_order_258)
    high_reliable_258, star_color_258, gala_color_258, ysos_color_258 = assign_color(label_pred_258)
    # degenerate data and pred_labels to band IRAC3, IRAC4, and MIPS1
    sort_order_678 = ['IRAC3', 'IRAC4', 'MIPS1']
    print ('--- degenerate data and pred_labels to band {0}, {1}, and {2} ---'.format(*sort_order_678))
    arti_data_678, label_pred_678 = degenerate(arti_data, label_pred, sort_order_678)
    high_reliable_678, star_color_678, gala_color_678, ysos_color_678 = assign_color(label_pred_678)
    #-----------------------------------
    # Plot 3D distribution
    plot_prob(high_reliable_jhk, arti_data_JHK, star_color_jhk, gala_color_jhk, ysos_color_jhk, sort_order_jhk)
    plot_prob(high_reliable_468, arti_data_468, star_color_468, gala_color_468, ysos_color_468, sort_order_468)
    plot_prob(high_reliable_258, arti_data_258, star_color_258, gala_color_258, ysos_color_258, sort_order_258)
    plot_prob(high_reliable_678, arti_data_678, star_color_678, gala_color_678, ysos_color_678, sort_order_678)
    #-----------------------------------
    # Close session
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
