#!/bin/bash
# 
# Abstract:
#     This is a program for matching the sources in ALLWISE catalogue and c2d+SWIRE catalogue. 
# Usage:
#     match_sp_wise.py [spitzer coord] [wise coord]
# Output:
#     1. coordinates of matched sources
#     2. coordinates of un-matched sources
# Editor:
#     Jacob975
# 
# ##################################
# #   Python3                      #
# #   This code is made in python3 #
# ##################################
# 
# 20180104
# ####################################
# update log
# 20190522 version alpha 1
#   This is the program for getting data from wise-allwise catalogues 
#-------------------

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0} [file name]"
    exit 1
fi

awk '{print "["$22"," $26"," $30"," $42"," $60"," $78"," $96"," $114"," \
    $23"," $27"," $31"," $43"," $61"," $79"," $97"," $115"],"}' ${1} > wise_sed.dat
awk '{print $25" " $29" " $33" " $45" " $63" " $81" " $99" " $117}' ${1} > wise_Q.dat
awk '{print FNR }' ${1} > wise_tracer.dat
awk '{print $3" "$5 }' ${1} > wise_coord.dat
exit 0
    
