#!/usr/bin/python3
'''
Abstract:
    This is a code for train AI to identify YSO from SED data with Convolutional Neural Network( CNN).
Usage:
    sed_train_cnn.py [option file] [source] [id] [coord] [time_stamp]
    sed_train_cnn.py option_file source_sed.txt source_id.txt source_coords.txt sometimes 

Result tree:

[yyyy-mm-dd hh:mm:ss+08:00] ---------  test -------------   tracer              // tracer index
                                    |-  training        |-   labels             // true label
                                    |-  validation      |-   dataset            // data
                                    |-  cls true of test                        // predicted label of test set
                                    |-  cls pred of test                        // true label of test set
                                    |-  checkpoint_AI_64_8_[file_name]          // this is AI

Quoted from:
    Magnus Erik Hvass Pedersen with MIT license.
Modifier:
    Chi-Ting Ho, Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181016
####################################
update log
20181016 version alpha 1:
    1. The code works
20190123 version alpha 2:
    2. Update the CNN arguments
20190219 version alpha 3:
    1. add more option in option file for easier training.
'''
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.metrics import confusion_matrix
import time
from sys import argv
from save_lib import save_arrangement_ext as save_arrangement
from save_lib import save_coords_ext as save_coords
import astro_mnist
import math
import os
from input_lib import option_train

def weight_variable(shape, std = 0.1):
    initial = tf.truncated_normal(shape) * std
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape = shape)
    return tf.Variable(initial)

def optimize_cross_entropy(num_iterations):
    # Ensure we update the global variables rather than local copies.
    global total_iterations
    global best_score
    global last_improvement
    global equal_batch
    global best_validation_accuracy
    # Start-time used for printing time-usage below.
    start_time = time.time()

    for i in range(num_iterations):

        # Increase the total number of iterations performed.
        # It is easier to update it in each iteration because
        # we need this number several times in the following.
        total_iterations += 1

        # Get a batch of training examples.
        # x_batch now holds a batch of images and
        # y_true_batch are the true labels for those images.
        x_batch, y_true_batch = data.train.next_batch(train_batch_size, equal = equal_batch)
        x_batch = x_batch[:, pick_band_array[0]]
        # Put the batch into a dict with the proper names
        # for placeholder variables in the TensorFlow graph.
        feed_dict_train = {x: x_batch,
                           y_true: y_true_batch}
        val_x_batch = data.validation.images[:, pick_band_array[0]]
        feed_dict_val = {x: val_x_batch,
                         y_true: data.validation.labels}
        # Run the optimizer using this batch of training data.
        # TensorFlow assigns the variables in feed_dict_train
        # to the placeholder variables and then runs the optimizer.
        session.run(optimizer, feed_dict=feed_dict_train)

        # Print status every 100 iterations and after last iteration.
        if (total_iterations % 100 == 0) or (i == (num_iterations - 1)):

            # Calculate the accuracy on the training-batch.
            train_correct, _ = predict_cls_train() 
            acc_train, _ = cls_accuracy(train_correct)
            # Calculate the accuracy on the validation-set.
            acc_validation, _ = validation_accuracy()
            loss_validation = session.run(loss, feed_dict=feed_dict_val)
            # Save the acc and loss of each iter
            validation_list.append([total_iterations, acc_validation, loss_validation])
            # If validation accuracy is an improvement over best-known.
            if acc_validation > best_validation_accuracy:
                # Update the best-known validation accuracy.
                best_validation_accuracy = acc_validation
                # Set the iteration for the last improvement to current.
                last_improvement = total_iterations
                # Save the acc and loss of improved iter
                improved_validation_list.append([total_iterations, acc_validation, loss_validation])
                # Save all variables of the TensorFlow graph to file.
                saver.save(sess=session, save_path=save_path)
                # A string to be printed below, shows improvement found.
                improved_str = '*'
            else:
                # An empty string to be printed below.
                # Shows that no improvement was found.
                improved_str = ''

            # Status-message for printing.
            msg = "Iter: {0:>6}, Train-Batch Accuracy: {1:>6.1%}, Validation Acc: {2:>6.1%} {3}"

            # Print it.
            print(msg.format(i + 1, acc_train, acc_validation, improved_str))

        # If no improvement found in the required number of iterations.
        if total_iterations - last_improvement > require_improvement:
            print("No improvement found in a while, stopping optimization.")
            # Break out from the for-loop.
            break
        elif total_iterations > num_iterations:
            print("Reach {0} iteration, stop.".format(num_iterations))
            break

    # Ending time.
    end_time = time.time()
    # Difference between start and end-times.
    time_dif = end_time - start_time
    # Print the time-usage.
    print("Time usage: {0} sec.".format(int(round(time_dif))))


def optimize_GT_score(num_iterations):
    # Ensure we update the global variables rather than local copies.
    global total_iterations
    global best_score
    global last_improvement
    global equal_batch
    # Start-time used for printing time-usage below.
    start_time = time.time()

    for i in range(num_iterations):

        # Increase the total number of iterations performed.
        # It is easier to update it in each iteration because
        # we need this number several times in the following.
        total_iterations += 1
        
        # Get a batch of training examples.
        # x_batch now holds a batch of images and
        # y_true_batch are the true labels for those images.
        x_batch, y_true_batch = data.train.next_batch(train_batch_size, equal = equal_batch)
        x_batch = x_batch[:, pick_band_array[0]]
        # Put the batch into a dict with the proper names
        # for placeholder variables in the TensorFlow graph.
        feed_dict_train = {x: x_batch,
                           y_true: y_true_batch}
        val_x_batch = data.validation.images[:, pick_band_array[0]]
        feed_dict_val = {x: val_x_batch, 
                         y_true: data.validation.labels}
        # Run the optimizer using this batch of training data.
        # TensorFlow assigns the variables in feed_dict_train
        # to the placeholder variables and then runs the optimizer.
        session.run(optimizer, feed_dict=feed_dict_train)

        # Print status every 100 iterations and after last iteration.
        if (total_iterations % 100 == 0) or (i == (num_iterations - 1)):

            # Calculate the accuracy on the training-batch.
            train_correct, _ = predict_cls_train() 
            acc_train, _ = cls_accuracy(train_correct)
            loss_validation = session.run(loss, feed_dict=feed_dict_val)
            # Calculate the accuracy on the validation-set.
            # The function returns 2 values but we only need the first.
            val_correct, val_pred = predict_cls_validation()
            val_true = data.validation.cls
            acc_validation, _ = cls_accuracy(val_correct)
            val_star_recall = np.sum((val_true == 0) & (val_pred == 0)) / np.sum(val_true == 0)
            val_gala_recall = np.sum((val_true == 1) & (val_pred == 1)) / np.sum(val_true == 1)
            val_ysos_recall = np.sum((val_true == 2) & (val_pred == 2)) / np.sum(val_true == 2)
            val_ysos_precision = np.sum((val_true == 2) & (val_pred == 2)) / np.sum(val_pred == 2)
            val_es_recall = np.sum((val_true == 3) & (val_pred == 3)) / np.sum(val_true == 3)
            # Save the acc and loss of each iter
            validation_list.append([total_iterations, acc_validation, loss_validation])
            # Determind a score for validating the AI.
            score = None
            if validation_func == "GT_score":
                score = acc_train + \
                        val_star_recall + \
                        0.01 * val_gala_recall + \
                        0.1 * val_ysos_recall + \
                        0.1 * val_ysos_precision + \
                        val_es_recall
            elif validation_func == "GT_score_newn":
                score = acc_train + \
                        val_star_recall + \
                        0.01 * val_gala_recall + \
                        0.01 * val_ysos_recall + \
                        0.01 * val_ysos_precision + \
                        val_es_recall
            # If validation accuracy is an improvement over best-known.
            if score > best_score:
                # Update the best-known validation accuracy.
                best_score = score
                # Set the iteration for the last improvement to current.
                last_improvement = total_iterations
                # Save the acc and loss of improved iter
                improved_validation_list.append([total_iterations, acc_validation, loss_validation])
                # Save all variables of the TensorFlow graph to file.
                saver.save(sess=session, save_path=save_path)
                # A string to be printed below, shows improvement found.
                improved_str = '*'
            else:
                # An empty string to be printed below.
                # Shows that no improvement was found.
                improved_str = ''

            # Status-message for printing.
            msg = "Iter: {0:>6}, Train-Batch Accuracy: {1:>6.1%}, Validation Acc: {2:>6.1%} Score: {3:.2f} {4}"

            # Print it.
            print(msg.format(i + 1, acc_train, acc_validation, score, improved_str))
        
        # If no improvement found in the required number of iterations.
        if total_iterations - last_improvement > require_improvement:
            print("No improvement found in a while, stopping optimization.")
            break
        elif total_iterations > num_iterations:
            print("Reach {0} iteration, stop.".format(num_iterations))
            break
            
    # Ending time.
    end_time = time.time()

    # Difference between start and end-times.
    time_dif = end_time - start_time

    # Print the time-usage.
    print("Time usage: {0} sec.".format(int(round(time_dif))))



# the def is used to plot data and their labels
def plot_images(images, cls_true, cls_pred=None):
    assert len(images) == len(cls_true) == 9
    # Create figure with 3x3 sub-plots.
    fig, axes = plt.subplots(3, 3)
    fig.subplots_adjust(hspace=0.3, wspace=0.3)

    for i, ax in enumerate(axes.flat):
        # Plot image.
        ax.plot(range(len(images[i])), images[i])

        # Show true and predicted classes.
        if cls_pred is None:
            xlabel = "True: {0}".format(cls_true[i])
        else:
            xlabel = "True: {0}, Pred: {1}".format(cls_true[i], cls_pred[i])

        ax.set_xlabel(xlabel)

        # Remove ticks from the plot.
        ax.set_xticks([])
        ax.set_yticks([])

    # Ensure the plot is shown correctly with multiple plots
    # in a single Notebook cell.
    plt.show()
    return

def plot_confusion_matrix(cls_pred):
    # cls_pred is an array of the predicted class-number for
    # all images in the test-set.

    # Get the true classifications for the test-set.
    cls_true = data.test.cls
    
    # Get the confusion matrix using sklearn.
    cm = confusion_matrix(y_true=cls_true,
                          y_pred=cls_pred)
    
    # Print the confusion matrix as text.
    print(cm)

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
    i = 0

    while i < num_images:
        # The ending index for the next batch is denoted j.
        j = min(i + batch_size, num_images)

        # Create a feed-dict with the images and labels
        # between index i and j.
        feed_dict = {x: images[i:j, pick_band_array[0]],
                     y_true: labels[i:j, :]}

        # Calculate the predicted class using TensorFlow.
        cls_pred[i:j] = session.run(y_pred_cls, feed_dict=feed_dict)

        # Set the start-index for the next batch to the
        # end-index of the current batch.
        i = j

    # Create a boolean array whether each image is correctly classified.
    correct = (cls_true == cls_pred)

    return correct, cls_pred

def predict_cls_validation():
    return predict_cls(images = data.validation.images,
                       labels = data.validation.labels,
                       cls_true = data.validation.cls)

def predict_cls_train():
    return predict_cls(images = data.train.images,
                       labels = data.train.labels,
                       cls_true = data.train.cls)


def cls_accuracy(correct):
    # Calculate the number of correctly classified images.
    # When summing a boolean array, False means 0 and True means 1.
    correct_sum = correct.sum()

    # Classification accuracy is the number of correctly classified
    # images divided by the total number of images in the test-set.
    acc = float(correct_sum) / len(correct)

    return acc, correct_sum

def validation_accuracy():
    # Get the array of booleans whether the classifications are correct
    # for the validation-set.
    # The function returns two values but we only need the first.
    correct, _ = predict_cls_validation()
    
    # Calculate the classification accuracy and return it.
    return cls_accuracy(correct)

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #-----------------------------------
    stu = option_train()
    # Load arguments
    if len(argv) != 6:
        print ("The number of arguments is wrong.")
        print ("Usage: sed_train_cnn.py [options file] [source] [id] [coord] [time_stamp]")
        print ("Example: sed_train_cnn.py option_train.txt source_sed.txt source_id.txt source_coords.txt sometimes ")
        stu.create()
        exit(1)
    option_file_name = argv[1]
    global images_name
    images_name = argv[2]
    labels_name = argv[3]
    coords_name = argv[4]
    time_stamp = argv[5]
    imply_mask, consider_error, batch_format, iterations_upperlimit, validation_func = stu.load(option_file_name)
    print ('#----------------------------------')
    print ('Input parameters:')
    print ('sed_name = {0}'.format(images_name))
    print ('label name = {0}'.format(labels_name))
    print ('coords_name = {0}'.format(labels_name))
    print ('imply mask: {0}'.format(imply_mask))
    print ('consider error: {0}'.format(consider_error))
    print ('batch format: {0}'.format(batch_format))
    print ('iterations upper limit: {0}'.format(iterations_upperlimit))
    print ('validation function: {0}'.format(validation_func))
    iterations_upperlimit = int(iterations_upperlimit)
    if batch_format == 'equal':
        equal_batch = True
    elif batch_format == 'random':
        equal_batch = False
    else:
        print ("Wrong batch_format option")
        exit()
    #------------------------------------
    # Load Data
    # We should play a mask on image
    print ("starting time: {0}".format(time_stamp))
    data, tracer, coords = astro_mnist.read_data_sets(images_name, labels_name, coords_name)
    print("Size of:")
    print("- Training-set:\t\t{}".format(len(data.train.labels)))
    print("- Test-set:\t\t{}".format(len(data.test.labels)))
    print("- Validation-set:\t{}".format(len(data.validation.labels)))
    #-----------------------------------
    # save arrangement and coords
    failure = save_arrangement(time_stamp, data, tracer)
    if not failure:
        print ("tracers and data are saved.")
    failure = save_coords(time_stamp, coords)
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
    num_label = len(data.train.labels[0])
    #-----------------------------------
    # Construct an AI
    x = tf.placeholder(tf.float32, [None, width_of_data * img_maj], name = 'x')
    y_true = tf.placeholder(tf.float32, [None, num_label], name = 'y_true')
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
    # Calculate the loss
    cross_entropy = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits = layer_last, labels = y_true))
    beta = 0.1
    regularizers = tf.nn.l2_loss(W_conv1)
    loss = tf.reduce_mean(cross_entropy + beta * regularizers)
    # The number of iterations
    iters = iterations_upperlimit
    print ("number of iterations = {0}".format(iters))
    #----------------------------------
    # The size of a batch for training and validating
    # Batch size for training
    train_batch_size = 450
    print ("train batch size = {0}".format(train_batch_size))
    # Batch size for validating 
    batch_size = 450
    print ("batch size = {0}".format(batch_size))
    #-----------------------------------
    # Best validation accuracy seen so far.
    best_validation_accuracy = 0.0
    # Get the true classes for those images.
    data.test.cls = np.argmax(data.test.labels, axis=1)
    data.train.cls = np.argmax(data.train.labels, axis=1)
    data.validation.cls = np.argmax(data.validation.labels, axis=1)
    # Learning rate 
    optimizer = tf.train.AdamOptimizer(learning_rate=0.005, epsilon=1e-7).minimize(loss)
    #-----------------------------------
    # Saver
    validation_list = []
    improved_validation_list = []
    saver = tf.train.Saver()
    save_dir = '{0}/checkpoint'.format(time_stamp)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, 'best_validation')
    #-----------------------------------
    # Tensorflow run
    session = tf.Session()
    def init_variables():
        session.run(tf.global_variables_initializer())
    init_variables()
    # restore previous weight
    #saver.restore(sess=session, save_path=save_path)
    # Best validation accuracy seen so far.
    best_score = 0.0
    # Iteration-number for last improvement to validation accuracy.
    last_improvement = 0
    # Stop optimization if no improvement found in this many iterations.
    require_improvement = 50000
    # Counter for total number of iterations performed so far.
    total_iterations = 0
    if any([validation_func == "GT_score", validation_func == "GT_score_newn"]):
        optimize_GT_score(num_iterations=iters)
    elif validation_func == "cross_entropy":
        optimize_cross_entropy(num_iterations=iters)
    np.savetxt('{0}/validation_acc_loss.txt'.format(save_dir), validation_list, fmt = '%s')
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
