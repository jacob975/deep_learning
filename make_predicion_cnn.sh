#!/bin/bash

# code for test AI

# Usage: make_prediction.sh [DIR where AI saved] [keyword of AI] [keyword of dataset]

# 20180413 version alpha 1
# The code work

# 20180425 version alpha 2
# Set keyword of AI and keyword of dataset respectively.

# check arguments
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [DIR where AI saved] [keyword of AI] [keyword of dataset]"
    echo "Example: ${0##*/} . 0 MaxLoss15"
    exit 1
fi
# Initialize the format of your datasets.
sed_test_cnn.py
vim option_train_cnn.txt

# Initialize variables
iters=0
AI_POOL=${1}
keyword_AI=${2}
keyword_set=${3}

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
    mkdir -p "AI_${AI_NAME}_test_on_${keyword_set}"
    if [ "${keyword_AI}" -eq "0" ];then
        echo "MaxLoss${iters}"
        sed_test_cnn.py option_train_cnn.txt \
                        source_sed_${keyword_set}.txt source_id_${keyword_set}.txt source_coord_${keyword_set}.txt \
                        "AI_${AI_NAME}_test_on_${keyword_set}"\
                        "${each}checkpoint_AI_64_8_source_sed_MaxLoss${iters}" \
                        > "AI_${AI_NAME}_test_on_${keyword_set}/result_of_AI_test"
        ((iters++))
    else
        sed_test_cnn.py option_train_cnn.txt \
                        source_sed_${keyword_set}.txt source_id_${keyword_set}.txt source_coord_${keyword_set}.txt\
                        "AI_${AI_NAME}_test_on_${keyword_set}"\
                        "${each}checkpoint_AI_64_8_source_sed_${keyword_AI}" \
                        > "AI_${AI_NAME}_test_on_${keyword_set}/result_of_AI_test"
    fi
done
exit 0