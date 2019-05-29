#!/bin/bash

# Usage: AI_schedule_eq.sh [key word] [number of iterations]

# 20180412 version alpha 1
# The code work

# 20190529 version alpha 2
# Using main name to replace keyword, and the function become more flexible.

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage:    ${0##*/} [main name] [number of iterations]"
    echo "Example : ${0##*/} spitzer 5"
    exit 1
fi

main_name=${1}

sed_train_dnn.py
vim option_train.txt

iter=1
while [ $iter -le ${2} ]
do
        # record when the program start
        # time stamp is used as identification
        timestamp=`date --rfc-3339=seconds`
        mkdir "${timestamp}_trained_${main_name}"
        sed_train_dnn.py option_train.txt ${main_name}_sed.txt ${main_name}_c2d2007_Sp.txt ${main_name}_coord.txt\
                        "${timestamp}_trained_${main_name}" > "${timestamp}_trained_${main_name}/Iters_log"
        (( iter++ ))
done
exit 0
