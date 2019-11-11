#!/bin/bash

# Usage: AI_schedule_eq.sh [key word] [number of iterations]

# 20180412 version alpha 1
# The code work

# 20190529 version alpha 2
# Using main name to replace keyword, and the function become more flexible.

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage:    ${0##*/} [sed name] [label name] [coord_name] [number of iterations]"
    echo "Example : ${0##*/} sed.txt label.txt coord.txt 5"
    exit 1
fi

sed_name=${1}
label_name=${2}
coord_name=${3}


sed_train_cnn.py
vim option_train.txt

iter=1
while [ $iter -le ${4} ]
do
        # record when the program start
        # time stamp is used as identification
        timestamp=`date --rfc-3339=seconds`
        mkdir "${timestamp}_trained"
        sed_train_cnn.py option_train.txt ${sed_name} ${label_name} ${coord_name}\
                        "${timestamp}_trained" > "${timestamp}_trained/Iters_log"
        (( iter++ ))
done
exit 0
