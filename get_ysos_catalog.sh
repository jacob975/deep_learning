#!/bin/bash

# This is a program for rearrange the Evans YSOs list to the program-easy-to-read format.

# 20181003 version alpha 1
#   The code works.

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [YSO_m1.txt] [YSO_m2.txt]"
    exit 1
fi

#-----------------------------------------------
# Load variables
mkdir -p yso_lab
YSO_m1=${1}
YSO_m2=${2}
cp $YSO_m1 yso_lab
cp $YSO_m2 yso_lab
cd yso_lab
# Get YSOs sed data with error recorded
cut -c6-14 $YSO_m2 > J
awk '{if ($1>0)  print $1; else print "0.00e+00"}' J > J_0
cut -c16-26 $YSO_m2 > e_J
awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_J > e_J_0
cut -c28-36 $YSO_m2 > H
awk '{if ($1>0)  print $1; else print "0.00e+00"}' H > H_0
cut -c38-46 $YSO_m2 > e_H
awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_H > e_H_0
cut -c48-55 $YSO_m2 > K
awk '{if ($1>0)  print $1; else print "0.00e+00"}' K > K_0
cut -c57-64 $YSO_m2 > e_K
awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_K > e_K_0
cut -c66-74 $YSO_m2 > I1
awk '{if ($1>0)  print $1; else print "0.00e+00"}' I1 > I1_0
cut -c76-84 $YSO_m2 > e_I1
awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_I1 > e_I1_0
cut -c86-93 $YSO_m2 > I2
awk '{if ($1>0)  print $1; else print "0.00e+00"}' I2 > I2_0
cut -c95-103 $YSO_m2 > e_I2
awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_I2 > e_I2_0
cut -c105-113 $YSO_m2 > I3
awk '{if ($1>0)  print $1; else print "0.00e+00"}' I3 > I3_0
cut -c115-122 $YSO_m2 > e_I3
awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_I3 > e_I3_0
cut -c124-131 $YSO_m2 > I4
awk '{if ($1>0)  print $1; else print "0.00e+00"}' I4 > I4_0
cut -c133-140 $YSO_m2 > e_I4
awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_I4 > e_I4_0
cut -c142-148 $YSO_m2 > M1
awk '{if ($1>0)  print $1; else print "0.00e+00"}' M1 > M1_0
cut -c150-157 $YSO_m2 > e_M1
awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_M1 > e_M1_0
paste J_0 H_0 K_0 I1_0 I2_0 I3_0 I4_0 M1_0 e_J_0 e_H_0 e_K_0 e_I1_0 e_I2_0 e_I3_0 e_I4_0 e_M1_0 > apjs_yso.txt
awk '{print $1"\t" $2"\t" $3"\t" $4"\t" $5"\t" $6"\t" $7"\t" $8"\t" $9"\t" $10"\t" $11"\t" $12"\t" $13"\t" $14"\t" $15"\t" $16}' apjs_yso.txt > apjs_yso_sed.dat
cp apjs_yso_sed.dat ../ysos_sed.dat
# Create coordinates
cut -c15-16 $YSO_m1 > yso_RA_h
cut -c17-18 $YSO_m1 > yso_RA_m
cut -c19-23 $YSO_m1 > yso_RA_s

cut -c25-26 $YSO_m1 > yso_DEC_d
cut -c27-28 $YSO_m1 > yso_DEC_m
cut -c29-32 $YSO_m1 > yso_DEC_s
echo 'Cut finished'
paste yso_RA_h yso_RA_m yso_RA_s yso_DEC_d yso_DEC_m yso_DEC_s > temp_ysos_coord.dat
awk '{print $1"h"$2"m"$3"s "$4"d"$5"m"$6"s"}' temp_ysos_coord.dat > ysos_coord.dat
hms2deg.py ysos_coord.dat
cp ysos_coord.dat ../ysos_coord.dat
cd ..
# Create tracer 
awk '{print NR}' ysos_sed.dat > ysos_tracer.dat
exit 0
