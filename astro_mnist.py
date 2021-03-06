#!/usr/bin/python3
# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Functions for downloading and reading MNIST data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip

import numpy
from six.moves import xrange  # pylint: disable=redefined-builtin

from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import random_seed
from tensorflow.python.platform import gfile

# CVDF mirror of http://yann.lecun.com/exdb/mnist/
DEFAULT_SOURCE_URL = 'https://storage.googleapis.com/cvdf-datasets/mnist/'


def _read32(bytestream):
  dt = numpy.dtype(numpy.uint32).newbyteorder('>')
  return numpy.frombuffer(bytestream.read(4), dtype=dt)[0]

def dense_to_one_hot(labels_dense, num_classes):
  """Convert class labels from scalars to one-hot vectors."""
  num_labels = labels_dense.shape[0]
  index_offset = numpy.arange(num_labels) * num_classes
  labels_one_hot = numpy.zeros((num_labels, num_classes))
  labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
  return labels_one_hot

class DataSet(object):

  def __init__(self,
               images,
               labels,
               fake_data=False,
               one_hot=False,
               dtype=dtypes.float32,
               reshape=True,
               seed=None):
    """Construct a DataSet.
    one_hot arg is used only if fake_data is true.  `dtype` can be either
    `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
    `[0, 1]`.  Seed arg provides for convenient deterministic testing.
    """
    seed1, seed2 = random_seed.get_seed(seed)
    # If op level seed is not set, use whatever graph level seed is returned
    numpy.random.seed(seed1 if seed is None else seed2)
    dtype = dtypes.as_dtype(dtype).base_dtype
    if dtype not in (dtypes.uint8, dtypes.float32):
      raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
                      dtype)
    if fake_data:
      self._num_examples = 10000
      self.one_hot = one_hot
    else:
      assert images.shape[0] == labels.shape[0], (
          'images.shape: %s labels.shape: %s' % (images.shape, labels.shape))
      self._num_examples = images.shape[0]

      # Convert shape from [num examples, rows, columns, depth]
      # to [num examples, rows*columns] (assuming depth == 1)
      if reshape:
        assert images.shape[3] == 1
        images = images.reshape(images.shape[0],
                                images.shape[1] * images.shape[2])
      if dtype == dtypes.float32:
        # Convert from [0, 255] -> [0.0, 1.0].
        images = images.astype(numpy.float32)
    self._images = images
    self._labels = labels
    self._epochs_completed = 0
    self._index_in_epoch = 0

  @property
  def images(self):
    return self._images

  @property
  def labels(self):
    return self._labels

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_completed(self):
    return self._epochs_completed

#--------------------
  def next_proper_batch(self, batch_size, label):
    cls_label = numpy.argmax(self.labels, axis = 1)
    # Select the source match the label
    bool_candidates = cls_label == label
    # Count the number of source I pick.
    num_candidates = numpy.sum(bool_candidates)
    # Create a random index for the sources I pick.
    perm = numpy.arange(num_candidates)
    numpy.random.shuffle(perm)
    # Get the data and labels of sources.
    source_candidates = self.images[bool_candidates]
    source_candidates = source_candidates[perm]
    label_arr = numpy.array([ i == label for i in range(3)])
    label_candidates = numpy.array([label_arr for i in range(num_candidates)])
    return source_candidates[:batch_size], label_candidates[:batch_size]

  def next_batch(self, batch_size, fake_data=False, shuffle=True, equal = False):
    # Equal means I pick the same number of sources from different labels.
    if equal:
      equal_batch_size = batch_size//3
      star_source, star_labels = self.next_proper_batch(equal_batch_size, label = 0)
      gala_source, gala_labels = self.next_proper_batch(equal_batch_size, label = 1) 
      ysos_source, ysos_labels = self.next_proper_batch(equal_batch_size, label = 2)
      source = numpy.concatenate((star_source, gala_source, ysos_source), axis = 0)
      labels = numpy.concatenate((star_labels, gala_labels, ysos_labels), axis = 0)
      # Shuffle the source I pick
      perm = numpy.arange(len(source))
      numpy.random.shuffle(perm)
      source = source[perm]
      labels = labels[perm]
      return source, labels
    """Return the next `batch_size` examples from this data set."""
    if fake_data:
      fake_image = [1] * 784
      if self.one_hot:
        fake_label = [1] + [0] * 9
      else:
        fake_label = 0
      return [fake_image for _ in xrange(batch_size)], [
          fake_label for _ in xrange(batch_size)
      ]
    start = self._index_in_epoch
    # Shuffle for the first epoch
    if self._epochs_completed == 0 and start == 0 and shuffle:
      perm0 = numpy.arange(self._num_examples)
      numpy.random.shuffle(perm0)
      self._images = self.images[perm0]
      self._labels = self.labels[perm0]
    # Go to the next epoch
    if start + batch_size > self._num_examples:
      # Finished epoch
      self._epochs_completed += 1
      # Get the rest examples in this epoch
      rest_num_examples = self._num_examples - start
      images_rest_part = self._images[start:self._num_examples]
      labels_rest_part = self._labels[start:self._num_examples]
      # Shuffle the data
      if shuffle:
        perm = numpy.arange(self._num_examples)
        numpy.random.shuffle(perm)
        self._images = self.images[perm]
        self._labels = self.labels[perm]
      # Start next epoch
      start = 0
      self._index_in_epoch = batch_size - rest_num_examples
      end = self._index_in_epoch
      images_new_part = self._images[start:end]
      labels_new_part = self._labels[start:end]
      return numpy.concatenate((images_rest_part, images_new_part), axis=0) , numpy.concatenate((labels_rest_part, labels_new_part), axis=0)
    else:
      self._index_in_epoch += batch_size
      end = self._index_in_epoch
      return self._images[start:end], self._labels[start:end]

class shuffled_tracer:
    def __init__(self, train, validation, test):
        self.train = train
        self.validation = validation
        self.test = test
        return

def read_data_sets(images_name,
                   labels_name,
                   coords_name,
                   fake_data=False,
                   one_hot=False,
                   dtype=dtypes.float32,
                   reshape=True,
                   # Total size are 10
                   train_weight = 7,
                   validation_weight=1,
                   test_weight = 0,
                   seed=None):

  # load data, label, and coords
  images = numpy.loadtxt(images_name)
  images = images.reshape((len(images), len(images[0]), 1, 1))
  labels = numpy.loadtxt(labels_name)
  coords = numpy.loadtxt(coords_name)
  '''
  if not 0 <= validation_size <= len(images):
    raise ValueError('Validation size should be between 0 and {}. Received: {}.'.format(len(images), validation_size))
  '''
  # shuffle the data
  randomize = numpy.arange(len(images))
  numpy.random.shuffle(randomize)
  images = images[randomize]
  labels = labels[randomize]
  coords = coords[randomize]
  # distribute data, label, and coord into three dataset
  total_weight = train_weight + validation_weight + test_weight
  train_size = int(len(images) * train_weight/total_weight)
  validation_size = int(len(images) * validation_weight/total_weight)
  test_size = int(len(images) * test_weight/total_weight)
  validation_images = images[:validation_size]
  validation_labels = labels[:validation_size]
  validation_coords = coords[:validation_size]
  test_images = images[validation_size:validation_size + test_size]
  test_labels = labels[validation_size:validation_size + test_size]
  test_coords = coords[validation_size:validation_size + test_size]
  train_images = images[validation_size + test_size:]
  train_labels = labels[validation_size + test_size:]
  train_coords = coords[validation_size + test_size:]
  options = dict(dtype=dtype, reshape=reshape, seed=seed)
  # generate shuffled coords
  coords = shuffled_tracer(train_coords, validation_coords, test_coords)
  # generate shuffled tracer
  train_shuffle = numpy.array(randomize[validation_size + test_size:])
  validation_shuffle = numpy.array(randomize[:validation_size])
  test_shuffle = numpy.array(randomize[validation_size:validation_size + test_size])
  tracer = shuffled_tracer(train_shuffle, validation_shuffle, test_shuffle)
  # generate data and index
  train = DataSet(train_images, train_labels, **options)
  validation = DataSet(validation_images, validation_labels, **options)
  test = DataSet(test_images, test_labels, **options)
    
  return base.Datasets(train=train, validation=validation, test=test), tracer, coords
