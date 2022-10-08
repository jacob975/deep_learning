# Purpose
Classify the identities of sources in c2d legacy catalog using SED data and our trained-AI.

# Publications
Chiu, Y.-L. et al. (2021). “Searching for young stellar objects through SEDs by machine learning”. In: Astronomy and Computing 36, p. 100470. issn: 2213-1337. doi: https://doi.org/10.1016/j.ascom.2021.100470. url: https://www.sciencedirect.com/science/article/pii/S221313372100024X.

# Preparation
The module you need
1. tensorflow
2. sklearn
3. tkinter
4. IPython

# How to train our AI?
1. Getting SED data of sources in c2d legacy catalog, and also corresponding data from 2MASS or UKIDSS catalog.
2. ```arrange_data.sh [option]```
  + This program is used to pick source from c2d legacy catalog based the following selections:
    + SED data in band J, H, K, IRAC 1, 2, 3, 4, and MIPS 1, respectively.
    + Source_type, including star, galaxies, and YSOc(s)
    + Data quality
  + Type ```arrange_data.sh``` and hit enter, it will show you available options
  + The option could be the one of the regions in c2d legacy survey.
    + ```i``` means the program will do extinction correction.
    + ```slct``` means the program will select data only could be done by extinction correction.
    + ```u``` means UKIDSS data will be used to replace data in JHK bands.
    + e.g. PERui means the program takes data in PER region, uses UKIDSS data to replace data in JHK bands, and do extinction correction.
3. ```dat2npy_ensemble.py [option file] [SED data 1] [SED data 2] [SED data 3] ...and so on```
  + This program is used to do data preparation. The program will further select and modify the data with the following options:
    + Mask certain bands. In this case, the specified bands been excluded will not be read and neither be counted into the number of lost detections.
    + The tolerance of the number of lost detection for a SED. The source will be eliminated with the higher number of lost detections.
    + Normalize the SEDs or not.
    + Consider the error of SEDs or not.
    + The upper limit of the number of sources.
    + Only select the sources with high error-flux correlation or not only.
    + Included Av, HL 2013 label, or Evans 2009 label.
  + Type ```dat2npy_ensemble.py``` and hit enter, it will show you available options and generate an option file for you, you should edit that file and then go on.
4. Optional: ```mask_bands.py [mask code] [SED data]```
  + This is a program to mask the certain bands.
5. Optional: ```mask_ul.py [Q flag table] [SED data]```
  + This is a program to replace the upper limits with a lowest detectable value of that band based on the given SED list.
6. Optional: ```exclude_exXUS.py [Q flag table] [SED data]```
  + This is a program to exclude the sources with upper limits, no detection, or saturations.
# Subroutine 1: Make a prediction on part of sources in the dataset.
Please follow the step 7, step 8.
7. ```AI_schedule_cnn.sh [main name] [number of iterations]```
  + Train our models by SED data, and repeat by ```[iteration]``` times, ```[iteration]``` number of models will be generated.
  + You can pick  ```AI_schedule_dnn.sh``` with the same arguments as well.
8. In previoud program, all logs and corresponding SED data will be saved in a folder name as the following.
  + `yyyy-mm-dd hh:mm:ss+UTC_trained_by_[main_name]`
    + checkpoint_AI_64_8_`main_name`_sed        // All the parameters of our model.
    + Iters_log                             // The log file of the status of our models.
    + training
      + coordinates
      + Source types
      + SEDs (called set)
      + Tracers
    + validation
      + coordinates
      + Source types
      + SEDs (called set)
      + Tracers
# Subroutine 2: Make a prediction on all sources in the dataset.
9. Please move all file start with ```source``` to another folder.
10. ```generate_appendix.py [label table] [number of partitions]```
  + This is a program for seperate the given files into N sub sets.
  + For example, please type ```generate_appendix.py source_id_MaxLoss0.txt 5```, then the program will show the number of source for each source type and for each sub-set.
  + The program wait for you until you type in the name of a file which will be seperated in to N sub sets.
11. Go to the directory ```./part1_train```, and train your model with the data inside using step 7. Please do this for all folder ```part%d_train```.
# How to test our well-trained model on SED data?
12. Perparing SEDs which are not included in training sets either validation sets in previous steps.
13. Repeat step 1 ~ 6 on test data.
14. ```make_prediction_cnn.sh [DIR where AI saved] [main_name of AI] [main_name of dataset]```
  + This is the program for testing AI.
  + ```[DIR where AI saved]``` means the absolute of relative directory of our trained-AI
  + You should pick ```make_prediction_dnn.sh``` if you train your models using ```AI_schedule_dnn.sh```.
15. In previoud program, all logs and corresponding SED data will be saved in a folder name as the following.
  + `AI_yyyy-mm-dd hh:mm:ss+UTC_trained_by_[main_name of AI]_test_on_[main_name of test data]`
    + result_of_AI_test                     // The log file from testing programs.
    + test
      + cls true of test                    // predicted label of test set
      + cls pred of test                    // actual label of test set
      + The probabilities of each actual label of each source.
      + The propabilities of each predicted label of each source.
      + coordinates
      + SEDs (called set)
      + Tracers
16. ```print_test_result.py [main_name of dataset]```
  + This program is used to print the confusion matrixes, recall-rate, and precision, ... several statistial result.
