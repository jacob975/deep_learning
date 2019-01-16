# Purpose
Classify the identities of sources in c2d legacy catalog using SED data and our trained-AI.

# Preparation
The module you need
1. tensorflow
2. sklearn
3. tkinter
4. IPython
5. prettytensor (No need in the future)
4. TBA

# How to train our AI?
1. Getting SED data of sources in c2d legacy catalog, and also corresponding data from 2MASS or UKIDSS catalog.
2. ```arrange_data.sh```
  + This program is used to pick SED data from c2d legacy catalog based on some selection, e.g.:
    + source_type
    + ability of extinction correction
    + data quality
    + TBA
  + The program will generate several available options for you.
3. ```arrange_data.sh [option]```
  + The option could be the one of the regions in c2d legacy survey.
  + ```i``` means the program will do extinction correction.
  + ```slct``` means the program will select data only could be done by extinction correction.
  + ```u``` means UKIDSS data will be used to replace data in JHK bands.
  + e.g. PERui means the program takes data in PER region, uses UKIDSS data to replace data in JHK bands, and do extinction correction.
4. ```dat2npy_ensemble.py```
  + The program will generate an option file for you, you should edit that file and go on.
5. ```dat2npy_ensemble.py [option file] [SED data 1] [SED data 2] [SED data 3] ...and so on```
  + The program will further select and modify the data, e.g.:
    + normalize or not
    + pick error or not
    + the tolerance of the number of lost data.
    + The upper limit of the number of data.
    + TBA
6. Optional: ```mask_bands.py [mask code] [SED data]```
  + This is a program to mask data in some bands by 0.
7. Optional: ```mask_ul.py [upper limit table] [SED data]```
  + This is a program to mask data which are upper limit.
8. ```AI_schedule_wopt.sh MaxLoss[number] [iteration]```
  + Train AIs by SED data which tolerate ```[number]``` of lost data points, and repeat by ```[iteration]``` times, ```[iteration]``` AIs will be generated.
9. In previoud program, all logs and corresponding SED data will be saved in a folder name as the following.
  + `yyyy-mm-dd hh:mm:ss+UTC_trained_by_MaxLoss15`
    + test
      + tracer	        // tracer index
      + labels		    // true label
      + data set		    // data
    + training
      + tracer            // tracer index
      + labels            // true label
      + data set          // data
    + validation
      + tracer             // tracer index
      + labels            // true label
      + data set          // data
    + checkpoint_AI_64_8_`file_name`          // All the parameters of AI
# How to test our AI on SED data.
10. Find SED data which are not included in previous steps.
11. Repeat 1~7 using test data.
12. ```make_prediction_wopt.sh [DIR where AI saved] [Keyword of AI] [keyword of dataset]```
  + This is the program for testing AI.
  + ```[DIR where AI saved]``` means the absolute of relative directory of our trained-AI
  + ```[Keyword of AI]``` should be ```MaxLoss[number]``` of AI.
  + ```[Keyword of dataset]``` should be ```MaxLoss[number]``` of testing SED data.
13. In previoud program, all logs and corresponding SED data will be saved in a folder name as the following.
  + `AI_yyyy-mm-dd hh:mm:ss+UTC_trained_by_MaxLoss15_test_on_MaxLoss15`
    + test
      + tracer            // tracer index
      + labels            // true label
      + data set          // data
    + cls true of test                        // predicted label of test set
    + cls pred of test                        // true label of test set
    + result_of_AI_test
14. ```print_test_result.py [keyword of dataset]```
  + This program is used to print the confusion matrixes, recall-rate, and precision, ... several statistial result.
  + ```[Keyword of dataset]``` should be ```MaxLoss[number]``` of testing SED data.

# Tracer tree
https://github.com/jacob975/deep_learning/data_selection.png
https://github.com/jacob975/deep_learning/data_tracer.png
