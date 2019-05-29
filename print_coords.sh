#!/bin/bash
# The program is used to generate a list of coordinates of certain sources.
# In 3x3 SCAO confusion matrix
# The program create a list for each element contains coordinates of data belonged that element.
# Usage: print_coords.sh [working directory] [key word]

# 20180531 version alpha 1
# The code work
# 20180605 version alpha 2
# Add a func to print coordinates of high reliable sources only.

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage:    ${0##*/} [working directory] [key word]"
    echo "Example : ${0##*/} . MaxLoss15"
    exit 1
fi

WORK_DIR=${1}
main_name=${2}

# print coordinates of data in each elements.
iter=0
while [ $iter -le 2 ]
do
    jter=0
    while [ $jter -le 2 ]
    do
        echo "###############"
        echo "print_coords.py ${WORK_DIR} ${main_name} ${iter} ${jter}"
        print_coords.py "${WORK_DIR}" "${main_name}" ${iter} ${jter}
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
    cat coords_test_HR_${_true}_0.txt coords_test_HR_${_true}_1.txt coords_test_HR_${_true}_2.txt \
    > coords_test_true_HR_${_true}.txt
    ((_true++))
done
pred=0
while [ $pred -le 2 ]
do
    cat coords_test_0_${pred}.txt coords_test_1_${pred}.txt coords_test_2_${pred}.txt \
    > coords_test_pred_${pred}.txt
    cat coords_test_HR_0_${pred}.txt coords_test_HR_1_${pred}.txt coords_test_HR_2_${pred}.txt \
    > coords_test_HR_pred_${pred}.txt
    ((pred++))
done
# print coordinates of diagonal terms and non-diagonal terms
# diagonal terms
cat coords_test_HR_0_0.txt coords_test_HR_1_1.txt coords_test_HR_2_2.txt \
    > coords_test_HR_diag.txt
cat coords_test_0_0.txt coords_test_1_1.txt coords_test_2_2.txt \
    > coords_test_diag.txt
# non-diagonal terms
cat coords_test_0_1.txt coords_test_0_2.txt coords_test_1_0.txt \
    coords_test_1_2.txt coords_test_2_0.txt coords_test_2_1.txt \
    > coords_test_nondiag.txt
cat coords_test_HR_0_1.txt coords_test_HR_0_2.txt coords_test_HR_1_0.txt \
    coords_test_HR_1_2.txt coords_test_HR_2_0.txt coords_test_HR_2_1.txt \
    > coords_test_HR_nondiag.txt
