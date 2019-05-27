#!/bin/bash
# 
# Abstract:
#     This is a program for retrieve data from the GCQE WISE-allwise table. 
# Usage:
#     get_wise_GCQE.sh [input wise table] 
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
# 20190527
# ####################################
# update log
# 20190527 version alpha 1
#   The code works 
#-------------------

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [file name]"
    exit 1
fi

awk  '{print  $12" " $16" " $20" " $24" " \
              $13" " $17" " $21" " $25}' ${1} > ${1::-4}_sed.dat
awk  '{print $41}' ${1} > ${1::-4}_Q.dat
awk  '{print $4" "$5 }' ${1} > ${1::-4}_coord.dat
#awk -F "|" '{print FNR }' ${1} > wise_tracer.dat
exit 0
