#!/bin/bash

# check arguments
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [file1] [file2]"
    echo "Available options: ${available_sources}"
    exit 1
fi

file1=$1
file2=$2

awk 'FNR==NR{a[$1];next}($1 in a){print}' ${file1} ${file2}
