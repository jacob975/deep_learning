#!/bin/bash

# Usage: print_coords.sh [working directory] [key word]

# 20180531 version alpha 1
# The code work

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage:    ${0##*/} [working directory] [key word]"
    echo "Example : ${0##*/} . MaxLoss15"
    exit 1
fi

WORK_DIR=${1}
keyword=${2}

# print coordinates of data in each elements.
iter=0
while [ $iter -le 2 ]
do
    jter=0
    while [ $jter -le 2 ]
    do
        echo "###############"
        echo "print_coords.py ${WORK_DIR} ${keyword} ${iter} ${jter}"
        print_coords.py "${WORK_DIR}" "${keyword}" ${iter} ${jter}
        ((jter++))
    done
    ((iter++))
done

# print coordinates of data of each columns and rows.
_true=0
while [ $_true -le 2 ]
do
    cat coords_test_${_true}_0.txt coords_test_${_true}_1.txt coords_test_${_true}_2.txt \
    > coords_test_true_${_true}.txt
    ((_true++))
done
pred=0
while [ $pred -le 2 ]
do
    cat coords_test_0_${pred}.txt coords_test_1_${pred}.txt coords_test_2_${pred}.txt \
    > coords_test_pred_${pred}.txt
    ((pred++))
done
# print coordinates of diagonal terms and non-diagonal terms
# diagonal terms
cat coords_test_0_0.txt coords_test_1_1.txt coords_test_2_2.txt \
    > coords_test_diag.txt
# non-diagonal terms
cat coords_test_0_1.txt coords_test_0_2.txt coords_test_1_0.txt \
    coords_test_1_2.txt coords_test_2_0.txt coords_test_2_1.txt \
    > coords_test_nondiag.txt
