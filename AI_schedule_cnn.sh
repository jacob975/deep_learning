#!/bin/bash

# Usage: AI_schedule_eq.sh [key word] [number of iterations]

# 20180412 version alpha 1
# The code work

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage:    ${0##*/} [key word] [number of iterations]"
    echo "Example : ${0##*/} MaxLoss15 5"
    exit 1
fi

keyword=${1}

sed_train_cnn_eq.py
vim option_train_cnn.txt

iter=1
while [ $iter -le ${2} ]
do
        # record when the program start
        # time stamp is used as identification
        timestamp=`date --rfc-3339=seconds`
        mkdir "${timestamp}_trained_by_${keyword}"
        sed_train_cnn_eq.py option_train_cnn.txt source_sed_${keyword}.txt source_id_${keyword}.txt source_coord_${keyword}.txt\
                        "${timestamp}_trained_by_${keyword}" > "${timestamp}_trained_by_${keyword}/Iters_log"
        (( iter++ ))
done
exit 0
