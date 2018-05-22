#!/usr/bin/python3
'''
License (MIT)
Copyright (c) 2016 by Magnus Erik Hvass Pedersen
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Abstract:
    This is a program to practice applying tensorflow on 01 Simple Linear Model on https://github.com/Hvass-Labs/TensorFlow-Tutorials.git
Usage:
    tutorial_08_Transfer_Learning.py
Editor:
    Magnus Erik Hvass Pedersen
Practicer:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180522
####################################
update log
20180522 version alpha 1
    1. the code works
'''
from IPython.display import Image, display
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import time
from datetime import timedelta
import os
# Functions and classes for loading and using the Inception model.
import inception
# We use Pretty Tensor to define the new classifier.
import prettytensor as pt

# Helper-function for plotting images
def plot_images(images, cls_true, cls_pred=None, smooth=True):

    assert len(images) == len(cls_true)

    # Create figure with sub-plots.
    fig, axes = plt.subplots(3, 3)

    # Adjust vertical spacing.
    if cls_pred is None:
        hspace = 0.3
    else:
        hspace = 0.6
    fig.subplots_adjust(hspace=hspace, wspace=0.3)

    # Interpolation type.
    if smooth:
        interpolation = 'spline16'
    else:
        interpolation = 'nearest'

    for i, ax in enumerate(axes.flat):
        # There may be less than 9 images, ensure it doesn't crash.
        if i < len(images):
            # Plot image.
            ax.imshow(images[i],
                      interpolation=interpolation)

            # Name of the true class.
            cls_true_name = class_names[cls_true[i]]

            # Show true and predicted classes.
            if cls_pred is None:
                xlabel = "True: {0}".format(cls_true_name)
            else:
                # Name of the predicted class.
                cls_pred_name = class_names[cls_pred[i]]

                xlabel = "True: {0}\nPred: {1}".format(cls_true_name, cls_pred_name)

            # Show the classes as the label on the x-axis.
            ax.set_xlabel(xlabel)
        
        # Remove ticks from the plot.
        ax.set_xticks([])
        ax.set_yticks([])
    
    # Ensure the plot is shown correctly with multiple plots
    # in a single Notebook cell.
    plt.show()

# Helper-function for plotting transfer-values
def plot_transfer_values(i):
    print("Input image:")
    
    # Plot the i'th image from the test-set.
    plt.imshow(images_test[i], interpolation='nearest')
    plt.show()

    print("Transfer-values for the image using Inception model:")
    
    # Transform the transfer-values into an image.
    img = transfer_values_test[i]
    img = img.reshape((32, 64))

    # Plot the image for the transfer-values.
    plt.imshow(img, interpolation='nearest', cmap='Reds')
    plt.show()

def plot_scatter(values, cls):
    # Create a color-map with a different color for each class.
    import matplotlib.cm as cm
    cmap = cm.rainbow(np.linspace(0.0, 1.0, num_classes))

    # Get the color for each sample.
    colors = cmap[cls]

    # Extract the x- and y-values.
    x = values[:, 0]
    y = values[:, 1]

    # Plot it.
    plt.scatter(x, y, color=colors)
    plt.show()

# Helper-function to get a random training-batch
def random_batch():
    # Number of images (transfer-values) in the training-set.
    num_images = len(transfer_values_train)

    # Create a random index.
    idx = np.random.choice(num_images,
                           size=train_batch_size,
                           replace=False)

    # Use the random index to select random x and y-values.
    # We use the transfer-values instead of images as x-values.
    x_batch = transfer_values_train[idx]
    y_batch = labels_train[idx]

    return x_batch, y_batch

# Helper-function to perform optimization
def optimize(num_iterations):
    # Start-time used for printing time-usage below.
    start_time = time.time()

    for i in range(num_iterations):
        # Get a batch of training examples.
        # x_batch now holds a batch of images (transfer-values) and
        # y_true_batch are the true labels for those images.
        x_batch, y_true_batch = random_batch()

        # Put the batch into a dict with the proper names
        # for placeholder variables in the TensorFlow graph.
        feed_dict_train = {x: x_batch,
                           y_true: y_true_batch}

        # Run the optimizer using this batch of training data.
        # TensorFlow assigns the variables in feed_dict_train
        # to the placeholder variables and then runs the optimizer.
        # We also want to retrieve the global_step counter.
        i_global, _ = session.run([global_step, optimizer],
                                  feed_dict=feed_dict_train)

        # Print status to screen every 100 iterations (and last).
        if (i_global % 100 == 0) or (i == num_iterations - 1):
            # Calculate the accuracy on the training-batch.
            batch_acc = session.run(accuracy,
                                    feed_dict=feed_dict_train)

            # Print status.
            msg = "Global Step: {0:>6}, Training Batch Accuracy: {1:>6.1%}"
            print(msg.format(i_global, batch_acc))

    # Ending time.
    end_time = time.time()

    # Difference between start and end-times.
    time_dif = end_time - start_time

    # Print the time-usage.
    print("Time usage: " + str(timedelta(seconds=int(round(time_dif)))))

#------------------------------------------
# Helper-Functions for Showing Results

# Helper-function to plot example errors
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
    images = images_test[incorrect]
    
    # Get the predicted classes for those images.
    cls_pred = cls_pred[incorrect]

    # Get the true classes for those images.
    cls_true = cls_test[incorrect]

    n = min(9, len(images))
    
    # Plot the first n images.
    plot_images(images=images[0:n],
                cls_true=cls_true[0:n],
                cls_pred=cls_pred[0:n])

# Helper-function to plot confusion matrix
# Import a function from sklearn to calculate the confusion-matrix.
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cls_pred):
    # This is called from print_test_accuracy() below.

    # cls_pred is an array of the predicted class-number for
    # all images in the test-set.

    # Get the confusion matrix using sklearn.
    cm = confusion_matrix(y_true=cls_test,  # True class for test-set.
                          y_pred=cls_pred)  # Predicted class.

    # Print the confusion matrix as text.
    for i in range(num_classes):
        # Append the class-name to each line.
        class_name = "({}) {}".format(i, class_names[i])
        print(cm[i, :], class_name)

    # Print the class-numbers for easy reference.
    class_numbers = [" ({0})".format(i) for i in range(num_classes)]
    print("".join(class_numbers))

# Helper-functions for calculating classifications
# Split the data-set in batches of this size to limit RAM usage.
batch_size = 256

def predict_cls(transfer_values, labels, cls_true):
    # Number of images.
    num_images = len(transfer_values)

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
        feed_dict = {x: transfer_values[i:j],
                     y_true: labels[i:j]}

        # Calculate the predicted class using TensorFlow.
        cls_pred[i:j] = session.run(y_pred_cls, feed_dict=feed_dict)

        # Set the start-index for the next batch to the
        # end-index of the current batch.
        i = j

    # Create a boolean array whether each image is correctly classified.
    correct = (cls_true == cls_pred)

    return correct, cls_pred

def predict_cls_test():
    return predict_cls(transfer_values = transfer_values_test,
                       labels = labels_test,
                       cls_true = cls_test)

# Helper-functions for calculating the classification accuracy
def classification_accuracy(correct):
    # When averaging a boolean array, False means 0 and True means 1.
    # So we are calculating: number of True / len(correct) which is
    # the same as the classification accuracy.

    # Return the classification accuracy
    # and the number of correct classifications.
    return correct.mean(), correct.sum()

# Helper-function for showing the classification accuracy
def print_test_accuracy(show_example_errors=False,
                        show_confusion_matrix=False):

    # For all the images in the test-set,
    # calculate the predicted classes and whether they are correct.
    correct, cls_pred = predict_cls_test()

    # Classification accuracy and the number of correct classifications.
    acc, num_correct = classification_accuracy(correct)

    # Number of images being classified.
    num_images = len(correct)

    # Print the accuracy.
    msg = "Accuracy on Test-Set: {0:.1%} ({1} / {2})"
    print(msg.format(acc, num_correct, num_images))

    # Plot some examples of mis-classifications, if desired.
    if show_example_errors:
        print("Example errors:")
        plot_example_errors(cls_pred=cls_pred, correct=correct)

    # Plot the confusion matrix, if desired.
    if show_confusion_matrix:
        print("Confusion Matrix:")
        plot_confusion_matrix(cls_pred=cls_pred)



#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    #----------------------------------------
    # version checking
    print(tf.__version__)
    # Load Data for CIFAR-10
    import cifar10
    from cifar10 import num_classes
    cifar10.data_path = "data/CIFAR-10/"
    cifar10.maybe_download_and_extract()
    class_names = cifar10.load_class_names()
    print(class_names)
    images_train, cls_train, labels_train = cifar10.load_training_data()
    images_test, cls_test, labels_test = cifar10.load_test_data()
    print("Size of:")
    print("- Training-set:\t\t{}".format(len(images_train)))
    print("- Test-set:\t\t{}".format(len(images_test)))
    #----------------------------------------
    # Plot a few images to see if data is correct
    # Get the first images from the test-set.
    images = images_test[0:9]
    # Get the true classes for those images.
    cls_true = cls_test[0:9]
    # Plot the images and labels using our helper-function above.
    plot_images(images=images, cls_true=cls_true, smooth=False)
    #----------------------------------------
    # Load inception model
    inception.data_dir = 'inception/'
    inception.maybe_download()
    model = inception.Inception()
    # Calculate Transfer-Values
    from inception import transfer_values_cache
    file_path_cache_train = os.path.join(cifar10.data_path, 'inception_cifar10_train.pkl')
    file_path_cache_test = os.path.join(cifar10.data_path, 'inception_cifar10_test.pkl')
    print("Processing Inception transfer-values for training-images ...")
    # Scale images because Inception needs pixels to be between 0 and 255,
    # while the CIFAR-10 functions return pixels between 0.0 and 1.0
    images_scaled = images_train * 255.0
    
    # If transfer-values have already been calculated then reload them,
    # otherwise calculate them and save them to a cache-file.
    transfer_values_train = transfer_values_cache(cache_path=file_path_cache_train,
                                                  images=images_scaled,
                                                  model=model)
    print("Processing Inception transfer-values for test-images ...")
    
    # Scale images because Inception needs pixels to be between 0 and 255,
    # while the CIFAR-10 functions return pixels between 0.0 and 1.0
    images_scaled = images_test * 255.0
    
    # If transfer-values have already been calculated then reload them,
    # otherwise calculate them and save them to a cache-file.
    transfer_values_test = transfer_values_cache(cache_path=file_path_cache_test,
                                                 images=images_scaled,
                                                 model=model)
    print ("the shape of transfer values of data in training: {0}".format(transfer_values_train.shape))
    print ("the shape of transfer values of data in testing: {0}".format(transfer_values_test.shape))
    plot_transfer_values(i=16)
    plot_transfer_values(i=17)
    #-----------------------------------------
    # Analysis of Transfer-Values using PCA
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    transfer_values = transfer_values_train[0:3000]
    cls = cls_train[0:3000]
    print(transfer_values.shape)
    transfer_values_reduced = pca.fit_transform(transfer_values)
    print(transfer_values_reduced.shape)
    plot_scatter(transfer_values_reduced, cls)
    #-----------------------------------------
    # Analysis of Transfer-Values using t-SNE
    from sklearn.manifold import TSNE
    pca = PCA(n_components=50)
    transfer_values_50d = pca.fit_transform(transfer_values)
    tsne = TSNE(n_components=2)
    transfer_values_reduced = tsne.fit_transform(transfer_values_50d)
    print(transfer_values_reduced.shape)
    plot_scatter(transfer_values_reduced, cls)
    # New Classifier in TensorFlow
    # Placeholder Variables
    transfer_len = model.transfer_len
    x = tf.placeholder(tf.float32, shape=[None, transfer_len], name='x')
    y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')
    y_true_cls = tf.argmax(y_true, dimension=1)
    # Neural Network
    # Wrap the transfer-values as a Pretty Tensor object.
    x_pretty = pt.wrap(x)
    
    with pt.defaults_scope(activation_fn=tf.nn.relu):
        y_pred, loss = x_pretty.\
            fully_connected(size=1024, name='layer_fc1').\
            softmax_classifier(num_classes=num_classes, labels=y_true)
    # Optimization Method
    global_step = tf.Variable(initial_value=0, name='global_step', trainable=False)
    optimizer = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(loss, global_step)
    # Classification Accuracy
    y_pred_cls = tf.argmax(y_pred, dimension=1)
    correct_prediction = tf.equal(y_pred_cls, y_true_cls)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    # TensorFlow Run
    # Create TensorFlow Session
    session = tf.Session()
    # Initialize Variables
    session.run(tf.global_variables_initializer())
    # Helper-function to get a random training-batch
    train_batch_size = 64
    #--------------------------------------
    # Result

    # Performance before any optimization
    print_test_accuracy(show_example_errors=False,
                        show_confusion_matrix=False)
    optimize(num_iterations=10000)
    print_test_accuracy(show_example_errors=True,
                        show_confusion_matrix=True)
    #--------------------------------------
    # Close TensorFlow Session
    
    # This has been commented out in case you want to modify and experiment
    # with the Notebook without having to restart it.
    model.close()
    session.close()
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
