#!/bin/bash

# The code for generate data form SWIRE project ELAIS N1 table

#20180501 version alpha 1
# the code work

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [argument]"
    echo "arguments: star, galaxy, yso"
    exit 1
fi

case ${1} in
    "star")
        awk '$17~/star/ && $17!~/dust/ \
            {print "["$34"," $55"," $76"," $97"," $118"," $139"," $160"," $181"," \
            $35"," $56"," $77"," $98"," $119"," $140"," $161"," $182"],"}' catalog-SWIRE-v3.tbl > star_sed.dat
        awk '$17~/star/ && $17!~/dust/ {print FNR }' catalog-SWIRE-v3.tbl > star_tracer.dat
        exit 0
        ;;
    
    "galaxy")
        awk '$17~/Galc/ \
            {print "["$34"," $55"," $76"," $97"," $118"," $139"," $160"," $181"," \
            $35"," $56"," $77"," $98"," $119"," $140"," $161"," $182"],"}' catalog-SWIRE-v3.tbl > galaxy_sed.dat
	    awk '$17~/Galc/   {print FNR }' catalog-SWIRE-v3.tbl > galaxy_tracer.dat
        exit 0
        ;;
    "yso")
        # save YSOc sed data with error recorded
        mkdir -p yso_lab
        cp apjs_no_header.txt yso_lab
        cd yso_lab
        cut -c6-14 apjs_no_header.txt > J
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' J > J_0
        cut -c16-26 apjs_no_header.txt > e_J
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_J > e_J_0
        cut -c28-36 apjs_no_header.txt > H
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' H > H_0
        cut -c38-46 apjs_no_header.txt > e_H
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_H > e_H_0
        cut -c48-55 apjs_no_header.txt > K
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' K > K_0
        cut -c57-64 apjs_no_header.txt > e_K
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_K > e_K_0
        cut -c66-74 apjs_no_header.txt > I1
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' I1 > I1_0
        cut -c76-84 apjs_no_header.txt > e_I1
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_I1 > e_I1_0
        cut -c86-93 apjs_no_header.txt > I2
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' I2 > I2_0
        cut -c95-103 apjs_no_header.txt > e_I2
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_I2 > e_I2_0
        cut -c105-113 apjs_no_header.txt > I3
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' I3 > I3_0
        cut -c115-122 apjs_no_header.txt > e_I3
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_I3 > e_I3_0
        cut -c124-131 apjs_no_header.txt > I4
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' I4 > I4_0
        cut -c133-140 apjs_no_header.txt > e_I4
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_I4 > e_I4_0
        cut -c142-148 apjs_no_header.txt > M1
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' M1 > M1_0
        cut -c150-157 apjs_no_header.txt > e_M1
        awk '{if ($1>0)  print $1; else print "0.00e+00"}' e_M1 > e_M1_0
        paste J_0 H_0 K_0 I1_0 I2_0 I3_0 I4_0 M1_0 e_J_0 e_H_0 e_K_0 e_I1_0 e_I2_0 e_I3_0 e_I4_0 e_M1_0 > apjs_yso.txt
        awk '{print "["$1"," $2"," $3"," $4"," $5"," $6"," $7"," $8"," $9"," $10"," $11"," $12"," $13"," $14"," $15"," $16"],"}' apjs_yso.txt > apjs_yso_sed.dat
        cp apjs_yso_sed.dat ../yso_sed.dat
        cd ..        
        awk '{print NR}' yso_sed.dat > yso_tracer.dat
        exit 0
        ;;
    *)
        echo wrong argument
        echo "arguments: star, galaxy, yso"
        exit 1
esac
