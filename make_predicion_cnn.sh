#!/bin/bash

# code for test AI

# Usage: make_prediction.sh [DIR where AI saved] [keyword of AI] [keyword of dataset]

# 20180413 version alpha 1
# The code work

# 20180425 version alpha 2
# Set keyword of AI and keyword of dataset respectively.

# 20180529 version alpha 3
# Using main name to replace the keywords, and the fucntions become more flexible.
# check arguments
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [DIR where AI saved] [sed name] [label name] [coord name]"
    echo "Example: ${0##*/} . sed.txt label.txt coord.txt"
    exit 1
fi
# Initialize the format of your datasets.
sed_test_cnn.py
vim option_test.txt

# Initialize variables
AI_POOL=${1}
sed_name=${2}
label_name=${3}
coord_name=${4}

echo "AI saved directory going to test:"
for each in ${AI_POOL}/20*/;
do
    # ${each##*/} means only take the last word of $each
    # ${each::-1} means take $each but the last latter. 
    FULL_AI_NAME=${each:0:${#each} - 1}
    AI_NAME=${FULL_AI_NAME##*/}
    echo "##############"
    echo "AI under test: ${AI_NAME}"

    # create a directory to save result of testing
    mkdir -p "AI_${AI_NAME}_test_on_testset"
    sed_test_cnn.py option_test.txt \
                    ${sed_name} ${label_name} ${coord_name} \
                    "AI_${AI_NAME}_test_on_testset"\
                    "${each}checkpoint" \
                    > "AI_${AI_NAME}_test_on_testset/result_of_AI_test"

done
exit 0
