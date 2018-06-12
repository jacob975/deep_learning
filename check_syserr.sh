#!/bin/bash
# The program is used to check the systematic error between UKIDSS and 2MASS. 
# Executing the following processes : 1. replacing jhk bands data in 2mass with data jhk bands in ukidss
# and then 2. test the systematic error

# Usage: make_prediction.sh [DIR where AI saved] [keyword of AI] [keyword of dataset]

# 20180611 version alpha 1
# The code works

# check arguments
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [label of ukidss survey] [label of regions]" 
    echo "Available ukidss survey: DXS, GCS, GPS"
    echo "Available regions: ELAIS_N1, CHA_II, LUP_I, LUP_III, LUP_IV, OPH, PER, SER"
    echo "Example: ${0##*/} GCS OPH"
    exit 1
fi

# initialize variables
iters=0
name_ukidss_survey=${1}
name_region=${2}
declare -a arr=("star" "gala" "ysos")

for label in "${arr[@]}"
do

    # make replacement
    replace_jhk_with_ukidss_${name_ukidss_survey}.py ${name_region}_${name_ukidss_survey}_source_table_${label}_WSA.csv ${label}_sed.dat
    # plot systematic error with the label "${label}, gala, and ysos"
    take_jhk_from_dat.py ${label}_sed_u.npy
    take_jhk_from_dat.py ${label}_sed.dat
    take_jhk_from_ukidss_${name_ukidss_survey}.py ${name_region}_${name_ukidss_survey}_source_table_${label}_WSA.csv ${label}
    systematic_error.py ${label}_sed_j.txt ${label}_sed_u_j.txt
    systematic_error.py ${label}_sed_h.txt ${label}_sed_u_h.txt
    systematic_error.py ${label}_sed_k.txt ${label}_sed_u_k.txt
    if [ "${name_ukidss_survey}" == "GCS" ]; then
        systematic_error.py ${label}_sed_j.txt ukidss_j_${label}.txt
        systematic_error.py ${label}_sed_h.txt ukidss_h_${label}.txt
        systematic_error.py ${label}_sed_k.txt ukidss_k1_${label}.txt
        systematic_error.py ${label}_sed_k.txt ukidss_k2_${label}.txt
        plot_compare_histograms.py ${label}_sed_j.txt ukidss_j_${label}.txt
        plot_compare_histograms.py ${label}_sed_h.txt ukidss_h_${label}.txt
        plot_compare_histograms.py ${label}_sed_k.txt ukidss_k1_${label}.txt
        plot_compare_histograms.py ${label}_sed_k.txt ukidss_k2_${label}.txt
    elif [ "${name_ukidss_survey}" == "DXS" ]; then
        systematic_error.py ${label}_sed_j.txt ukidss_j_${label}.txt
        systematic_error.py ${label}_sed_h.txt ukidss_h_${label}.txt
        systematic_error.py ${label}_sed_k.txt ukidss_k_${label}.txt
        plot_compare_histograms.py ${label}_sed_j.txt ukidss_j_${label}.txt
        plot_compare_histograms.py ${label}_sed_h.txt ukidss_h_${label}.txt
        plot_compare_histograms.py ${label}_sed_k.txt ukidss_k_${label}.txt
    elif [ "${name_ukidss_survey}" == "GPS" ]; then
        systematic_error.py ${label}_sed_j.txt ukidss_j_${label}.txt
        systematic_error.py ${label}_sed_h.txt ukidss_h1_${label}.txt
        systematic_error.py ${label}_sed_h.txt ukidss_h2_${label}.txt
        systematic_error.py ${label}_sed_k.txt ukidss_k1_${label}.txt
        systematic_error.py ${label}_sed_k.txt ukidss_k2_${label}.txt
        plot_compare_histograms.py ${label}_sed_j.txt ukidss_j_${label}.txt
        plot_compare_histograms.py ${label}_sed_h.txt ukidss_h1_${label}.txt
        plot_compare_histograms.py ${label}_sed_h.txt ukidss_h2_${label}.txt
        plot_compare_histograms.py ${label}_sed_k.txt ukidss_k1_${label}.txt
        plot_compare_histograms.py ${label}_sed_k.txt ukidss_k2_${label}.txt
    fi
done
