# deep learning
I study on how to apply deep_learning on astronomy.

# preparation
The module you need
1. tensorflow
2. sklearn
3. tkinter
4. IPython
5. prettytensor
4. TBA

If you want to install tensorflow with gpu compiled version, you need
1. bazel

The git you need
1. TensorFlow-Tutorials

# tutorial I have practiced
```bash
TensorFlow-Tutorials/01_Simple_Linear_Model.ipynb

TensorFlow-Tutorials/02_Convolutional_Neural_Network.ipynb

TensorFlow-Tutorials/03_PrettyTensor.ipynb

TensorFlow-Tutorials/04_Save_Restore.ipynb

TensorFlow-Tutorials/05_Ensemble_Learning.ipynb

TensorFlow-Tutorials/06_CIFAR-10.ipynb

TensorFlow-Tutorials/07_Inception_Model.ipynb
```

# How to train AI?

Usage:
```sed_04_64_8.py [source] [id]```

# The product of training an AI

+ `yyyy-mm-dd hh:mm:ss+UTC_trained_by_MaxLoss15`
  + test
    + tracer	        // tracer index
    + labels		    // true label
    + data set		    // data
  - training
    + tracer            // tracer index
    + labels            // true label
    + data set          // data
  - validation
    + tracer             // tracer index
    + labels            // true label
    + data set          // data
  + cls true of test                        // predicted label of test set
  + cls pred of test                        // true label of test set
  + checkpoint_AI_64_8_`file_name`          // this is AI

# How to make a prediction on dataset with trained AI?

Usage:
```sed_test_AI_64_8.py [source] [id] [directory] [AI]```

# The product of prediction

+ `AI_yyyy-mm-dd hh:mm:ss+UTC_trained_by_MaxLoss15_test_on_MaxLoss15`
  + test
    + tracer            // tracer index
    + labels            // true label
    + data set          // data
  + cls true of test                        // predicted label of test set
  + cls pred of test                        // true label of test set
  + result_of_AI_test

# Tracer tree

https://github.com/jacob975/deep_learning/data_selection.png
https://github.com/jacob975/deep_learning/data_tracer.png
