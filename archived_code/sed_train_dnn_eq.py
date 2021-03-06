#!/usr/bin/python3
'''
License (MIT)
Copyright (c) 2016 by Magnus Erik Hvass Pedersen
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Abstract:
    This is a code for train AI to identify YSO from SED data
    with 64 neurals per layer, 8 layers.
Usage:
    sed_train_dnn_eq.py [source] [label] [coords] [time_stamp]

Result tree:

[yyyy-mm-dd hh:mm:ss+08:00] ---------  test -------------   tracer              // tracer index
                                    |-  training        |-   labels             // true label
                                    |-  validation      |-   dataset            // data
                                    |-  cls true of test                        // predicted label of test set
                                    |-  cls pred of test                        // true label of test set
                                    |-  checkpoint_AI_64_8_[file_name]          // this is AI

Quoted from:
    Magnus Erik Hvass Pedersen
Modifier:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170301
####################################
update log
    20180301 version alpha 1
    The code is base on sed_04
    1. Add milestone in the optimize iteration, when acheive the milestone, AI will be saved and test to a new folder.
    2. the neural network is 64 neurals per layer, 8 layers.

    20180306 version alpha 2
    1. add flexible data length.

    20180310 version alpha 3
    1. Training set, validation set, test set will be saved after arrangement.

    20180320 version alpha 4 
    1. arrange saving direction.
'''
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.metrics import confusion_matrix
import time
from sys import argv
from save_lib import save_arrangement, save_cls_pred, save_cls_true, save_coords
import astro_mnist
import math
import os

def new_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))

def new_biases(length):
    return tf.Variable(tf.constant(0.05, shape=[length]))

def new_fc_layer(input,          # The previous layer.
                 num_inputs,     # Num. inputs from prev. layer.
                 num_outputs,    # Num. outputs.
                 use_relu=True): # Use Rectified Linear Unit (ReLU)?

    # Create new weights and biases.
    weights = new_weights(shape=[num_inputs, num_outputs])
    biases = new_biases(length=num_outputs)

    # Calculate the layer as the matrix multiplication of
    # the input and weights, and then add the bias-values.
    layer = tf.matmul(input, weights) + biases

    # Use ReLU?
    if use_relu:
        layer = tf.nn.relu6(layer)

    return layer

def optimize(num_iterations):
    # Ensure we update the global variables rather than local copies.
    global total_iterations
    global best_validation_accuracy
    global last_improvement
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
        x_batch, y_true_batch = data.train.next_batch(train_batch_size, equal = True)

        # Put the batch into a dict with the proper names
        # for placeholder variables in the TensorFlow graph.
        feed_dict_train = {x: x_batch,
                           y_true: y_true_batch}
        feed_dict_val = {x: data.validation.images,
                         y_true: data.validation.labels}

        # Run the optimizer using this batch of training data.
        # TensorFlow assigns the variables in feed_dict_train
        # to the placeholder variables and then runs the optimizer.
        session.run(optimizer, feed_dict=feed_dict_train)

        # Print status every 100 iterations and after last iteration.
        if (total_iterations % 100 == 0) or (i == (num_iterations - 1)):

            # Calculate the accuracy on the training-batch.
            acc_train = session.run(accuracy, feed_dict=feed_dict_train)
            loss_validation = session.run(loss, feed_dict=feed_dict_val)
            # Calculate the accuracy on the validation-set.
            # The function returns 2 values but we only need the first.
            acc_validation, _ = validation_accuracy()
            # Save the acc and loss of each iter
            validation_list.append([total_iterations, acc_validation, loss_validation])
            # If validation accuracy is an improvement over best-known.
            if acc_validation > best_validation_accuracy:
                # Update the best-known validation accuracy.
                best_validation_accuracy = acc_validation
            
                # Set the iteration for the last improvement to current.
                last_improvement = total_iterations
                # Save the acc and loss of improved iter
                improved_validation_list.append([total_iterations*100, acc_validation, loss_validation])
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

def plot_example_errors(cls_pred, correct):
    # This function is called from print_test_accuracy() below.

    # cls_pred is an array of the predicted class-number for
    # all images in the test-set.

    # correct is a boolean array whether the predicted class
    # is equal to the true class for each image in the test-set.

    # Negate the boolean array.
    incorrect = (correct == False)
    
    # Get the images from the test-set that have been
    # incorrectly classified.
    images = data.test.images[incorrect]
    
    # Get the predicted classes for those images.
    cls_pred = cls_pred[incorrect]

    # Get the true classes for those images.
    cls_true = data.test.cls[incorrect]
    
    # Plot the first 9 images.
    plot_images(images=images[0:9],
                cls_true=cls_true[0:9],
                cls_pred=cls_pred[0:9])

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
    '''
    # Plot the confusion matrix as an image.
    plt.matshow(cm)

    # Make various adjustments to the plot.
    plt.colorbar()
    tick_marks = np.arange(num_classes)
    plt.xticks(tick_marks, range(num_classes))
    plt.yticks(tick_marks, range(num_classes))
    plt.xlabel('Predicted')
    plt.ylabel('True')

    # Ensure the plot is shown correctly with multiple plots
    # in a single Notebook cell.
    plt.show()
    '''

def print_test_accuracy(show_example_errors=False,
                        show_confusion_matrix=False):

    # For all the images in the test-set,
    # calculate the predicted classes and whether they are correct.
    correct, cls_pred = predict_cls_test()
    #----------------------------------------
    # save cls_pred and cls_true
    save_cls_pred(images_name[:-4], time_stamp, cls_pred)
    save_cls_true(images_name[:-4], time_stamp, data.test.cls)
    #----------------------------------------
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

    # Plot some examples of mis-classifications, if desired.
    if show_example_errors:
        print("Example errors:")
        plot_example_errors(cls_pred=cls_pred, correct=correct)

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
        feed_dict = {x: images[i:j, :],
                     y_true: labels[i:j, :]}

        # Calculate the predicted class using TensorFlow.
        cls_pred[i:j] = session.run(y_pred_cls, feed_dict=feed_dict)

        # Set the start-index for the next batch to the
        # end-index of the current batch.
        i = j

    # Create a boolean array whether each image is correctly classified.
    correct = (cls_true == cls_pred)

    return correct, cls_pred

def predict_cls_test():
    return predict_cls(images = data.test.images,
                       labels = data.test.labels,
                       cls_true = data.test.cls)

def predict_cls_validation():
    return predict_cls(images = data.validation.images,
                       labels = data.validation.labels,
                       cls_true = data.validation.cls)

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
    time_stamp = argv[4]
    print ("starting time: {0}".format(time_stamp))
    #-----------------------------------
    # Load Data
    global images_name
    images_name = argv[1]
    labels_name = argv[2]
    coords_name = argv[3]
    data, tracer, coords = astro_mnist.read_data_sets(images_name, labels_name, coords_name)
    print("Size of:")
    print("- Training-set:\t\t{}".format(len(data.train.labels)))
    print("- Test-set:\t\t{}".format(len(data.test.labels)))
    print("- Validation-set:\t{}".format(len(data.validation.labels)))
    data.test.cls = np.argmax(data.test.labels, axis=1)
    #-----------------------------------
    # save arrangement and coords
    failure = save_arrangement(images_name[:-4], time_stamp, data, tracer)
    if not failure:
        print ("tracers and data are saved.")
    failure = save_coords(images_name[:-4], time_stamp, coords)
    if not failure:
        print ("coords are saved.")
    #-----------------------------------
    # Data dimension
    # We know that from the length of a data. 
    img_size = len(data.train.images[0])
    print ("image size = {0}".format(img_size))
    # Images are stored in one-dimensional arrays of this length.
    img_size_flat = img_size * 1
    # Tuple with height and width of images used to reshape arrays.
    img_shape = (img_size, 1)
    # Number of colour channels for the images: 1 channel for gray-scale.
    num_channels = 1
    # Number of classes, one class for each of 10 digits.
    num_classes = 3
    # the number of iterations
    iters = 1000000
    print ("number of iterations = {0}".format(iters))
    # the size of a batch
    if len(data.validation.labels) < 512:
        train_batch_size = 128
    else:
        train_batch_size = 512
    print ("train batch size = {0}".format(train_batch_size))
    # Split the data-set in batches of this size to limit RAM usage.
    if len(data.validation.labels) < 512:
        batch_size = 128
    else:
        batch_size = 512
    print ("batch size = {0}".format(batch_size))
    #-----------------------------------
    # Get the true classes for those images.
    data.test.cls = np.argmax(data.test.labels, axis=1)
    data.validation.cls = np.argmax(data.validation.labels, axis=1)
    #-----------------------------------
    # Tensorflow Graph
    x = tf.placeholder(tf.float32, shape=[None, img_size_flat], name='x')
    x_image = tf.reshape(x, [-1, img_size])
    y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')
    y_true_cls = tf.argmax(y_true, axis=1)
    #-----------------------------------
    layer_fc1 = new_fc_layer(input = x_image,
                            num_inputs = img_size,
                            num_outputs = 64,
                            use_relu=True)
    layer_fc2 = new_fc_layer(input = layer_fc1,
                            num_inputs = 64,
                            num_outputs = 64,
                            use_relu=True)
    layer_fc3 = new_fc_layer(input = layer_fc2,
                            num_inputs = 64,
                            num_outputs = 64,
                            use_relu=True)
    layer_fc4 = new_fc_layer(input = layer_fc3,
                            num_inputs = 64,
                            num_outputs = 64,
                            use_relu=True)
    layer_fc5 = new_fc_layer(input = layer_fc4,
                            num_inputs = 64,
                            num_outputs = 64,
                            use_relu=True)
    layer_fc6 = new_fc_layer(input = layer_fc5,
                            num_inputs = 64,
                            num_outputs = 64,
                            use_relu=True)
    layer_fc7 = new_fc_layer(input = layer_fc6,
                            num_inputs = 64,
                            num_outputs = 64,
                            use_relu=True)
    layer_fc8 = new_fc_layer(input = layer_fc7,
                            num_inputs = 64,
                            num_outputs = 64,
                            use_relu=True)
    layer_last = new_fc_layer(input = layer_fc8,
                             num_inputs=64,
                             num_outputs=num_classes,
                             use_relu=False)
    y_pred = tf.nn.softmax(layer_last)
    cross_entropy = \
        tf.nn.softmax_cross_entropy_with_logits(logits=layer_last,
                                                labels=y_true)
    loss = tf.reduce_mean(cross_entropy)
    starter_learning_rate = 1e-4
    print ("starter learning rate = {0}".format(starter_learning_rate))
    base = 0.96
    print ("base = {0}".format(base))
    unit_step = 100000
    print ("unit_step = {0}".format(unit_step))
    global_step = tf.Variable(0, trainable=False)
    learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step , unit_step, base, staircase=True)
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss, global_step = global_step)
    y_pred_cls = tf.argmax(y_pred, axis=1)
    correct_prediction = tf.equal(y_pred_cls, y_true_cls)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    #-----------------------------------
    # Saver
    validation_list = []
    improved_validation_list = []
    saver = tf.train.Saver()
    save_dir = '{0}/checkpoint_AI_64_8_{1}'.format(time_stamp, images_name[:-4])
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
    best_validation_accuracy = 0.0
    # Iteration-number for last improvement to validation accuracy.
    last_improvement = 0
    # Stop optimization if no improvement found in this many iterations.
    require_improvement = 100000
    # Counter for total number of iterations performed so far.
    total_iterations = 0
    optimize(num_iterations=iters)
    print ( "final_learning_rate = {0}".format(session.run(learning_rate)))
    #print_test_accuracy(show_example_errors=False, show_confusion_matrix=True)
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
