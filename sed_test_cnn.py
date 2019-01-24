#!/usr/bin/python3
'''
Abstract:
    This is a code for testing AI with given sed data using CNN.
Usage:
    sed_test_cnn_eq.py [option file] [source] [id] [coord] [where to save] [AI]
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
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.metrics import confusion_matrix
import time
from sys import argv
from save_lib import save_cls_pred, save_cls_true, save_arrangement, save_coords, save_label_pred
from load_lib import print_precision, print_recall_rate
import astro_mnist
import os
from input_lib import option_train_cnn

def weight_variable(shape, std = 0.1):
    initial = tf.truncated_normal(shape) * std
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape = shape)
    return tf.Variable(initial)

def plot_confusion_matrix(cls_pred):
    # This is called from print_test_accuracy() below.

    # cls_pred is an array of the predicted class-number for
    # all images in the test-set.

    # Get the true classifications for the test-set.
    cls_true = data.test.cls
    
    # Get the confusion matrix using sklearn.
    cm = confusion_matrix(y_true=cls_true,
                          y_pred=cls_pred)
    
    # Print the confusion matrix as text.
    print(cm)
    print_precision(y_true = cls_true, y_pred = cls_pred)
    print_recall_rate(y_true = cls_true, y_pred = cls_pred)

def print_test_accuracy(show_confusion_matrix=False):

    # For all the images in the test-set,
    # calculate the predicted classes and whether they are correct.
    correct, cls_pred = predict_cls_test()
    # save cls_pred and cls_true
    save_cls_pred(images_name[:-4], directory, cls_pred)
    save_cls_true(images_name[:-4], directory, data.test.cls)
    
    # Classification accuracy and the number of correct classifications.
    acc, num_correct = cls_accuracy(correct)
    
    # Number of images being classified.
    num_images = len(correct)

    # Print the accuracy.
    msg = "Accuracy on Test-Set: {0:.1%} ({1} / {2})"
    print(msg.format(acc, num_correct, num_images))
    
    # Plot the confusion matrix, if desired.
    if show_confusion_matrix:
        print("Confusion Matrix:")
        plot_confusion_matrix(cls_pred=cls_pred)

def predict_cls(images, labels, cls_true):
    # Number of images.
    num_images = len(images)

    # Allocate an array for the predicted classes which
    # will be calculated in batches and filled into this array.
    cls_pred = np.zeros(shape=num_images, dtype=np.int)

    # Now calculate the predicted classes for the batches.
    # We will just iterate through all the batches.
    # There might be a more clever and Pythonic way of doing this.
    # The starting index for the next batch is denoted i.
    feed_dict = {x: images[:, pick_band_array[0]], y_true: labels[:]}
    # Calculate the predicted class using TensorFlow.
    cls_pred = session.run(y_pred_cls, feed_dict=feed_dict)
    # Set the start-index for the next batch to the
    # end-index of the current batch.

    # Create a boolean array whether each image is correctly classified.
    correct = (cls_true == cls_pred)

    return correct, cls_pred

def predict_label(images, labels):
    # Number of images.
    num_images = len(images)
    # initialize
    label_pred = np.zeros(num_images*3).reshape((num_images, 3))
    feed_dict = {x: images[:,pick_band_array[0]], y_true: labels[:]}
    # process 
    label_pred = session.run(y_pred, feed_dict=feed_dict)
    return label_pred

def predict_cls_test():
    return predict_cls(images = data.test.images,
                       labels = data.test.labels,
                       cls_true = data.test.cls)

def cls_accuracy(correct):
    # Calculate the number of correctly classified images.
    # When summing a boolean array, False means 0 and True means 1.
    correct_sum = correct.sum()

    # Classification accuracy is the number of correctly classified
    # images divided by the total number of images in the test-set.
    acc = float(correct_sum) / len(correct)

    return acc, correct_sum

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------
    # Load arguments
    stu = option_train_cnn()
    if len(argv) != 7:
        print ("The number of arguments is wrong.")
        print ("Usage: sed_test_cnn.py [option_file] [source] [id] [coord] [where to save] [AI]")
        stu.create()
        exit(1)
    option_file_name = argv[1]
    imply_mask, consider_error = stu.load(option_file_name)
    images_name = argv[2]
    labels_name = argv[3]
    coords_name = argv[4]
    directory = argv[5]
    AI_saved_dir = argv[6]
    #-------------------------------------
    # Load Data
    data, tracer, coords = astro_mnist.read_data_sets(images_name, labels_name, coords_name, train_weight = 0, validation_weight = 0, test_weight = 1)
    print("Size of:")
    print("- Training-set:\t\t{}".format(len(data.train.labels)))
    print("- Test-set:\t\t{}".format(len(data.test.labels)))
    print("- Validation-set:\t{}".format(len(data.validation.labels)))
    data.test.cls = np.argmax(data.test.labels, axis=1)
    # save arrangement and coords
    failure = save_arrangement(images_name[:-4], directory, data, tracer)
    if not failure:
        print ("tracer and data is saved.")
    failure = save_coords(images_name[:-4], directory, coords)
    if not failure:
        print ("coords are saved.")
    #-----------------------------------
    # Data dimension
    img_maj = imply_mask.count('0')
    width_of_data = None
    pick_band_array = None
    if consider_error == 'yes':
        width_of_data = 2
        repeat_imply_mask = imply_mask + imply_mask
        pick_band_array = np.where(np.array(list(repeat_imply_mask), dtype = int) == 0)
    elif consider_error == 'no':
        width_of_data = 1
        pick_band_array = np.where(np.array(list(imply_mask), dtype = int) == 0)
    else:
        print('Wrong error consideration.')
        exit()
    image_shape = (width_of_data, img_maj)
    kernal_shape = (width_of_data, 2)
    num_kernal_1 = 32
    num_kernal_2 = 64
    num_conn_neural = 100
    num_label = len(data.test.labels[0])
    #-----------------------------------
    # Construct an AI
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
    y_pred = tf.matmul(h_fc1, W_fc2) + b_fc2
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
    batch_size = 512
    print ("batch_size = {0}".format(batch_size))
    # test the restored AI, show confusion matrix and example_errors
    # and save the cls of prediction
    print_test_accuracy(show_confusion_matrix=True)
    # save labels of prediction
    label_pred = predict_label(data.test.images, data.test.labels)
    save_label_pred(images_name[:-4], directory, label_pred)
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
