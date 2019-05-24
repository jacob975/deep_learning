#!/bin/bash
# 
# Abstract:
#     This is a program for retrieve data from the WISE allwise table. 
# Usage:
#     get_wise.sh [input wise table] 
# Output:
#       1. The SEDs of sources.
#       2. The coordinates of sources.
#       3. The Quality label of sources.
# Editor:
#     Jacob975
# 
# ##################################
# #   Python3                      #
# #   This code is made in python3 #
# ##################################
# 
# 20190522
# ####################################
# update log
# 20190522 version alpha 1
#   The code works 
# 20190524 version alpha 2
#   Correct the comments, name the output files by the original name. 
#-------------------

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [file name]"
    exit 1
fi

awk -F "|" '{print  $17"|" $21"|" $25"|" $29"|" \
                    $18"|" $22"|" $26"|" $30}' ${1} > ${1}_sed.dat
awk -F "|" '{print $60}' ${1} > ${1}_Q.dat
awk -F "|" '{print $2" "$3 }' ${1} > ${1}_coord.dat
#awk -F "|" '{print FNR }' ${1} > wise_tracer.dat
exit 0
    
