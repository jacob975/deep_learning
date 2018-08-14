#!/bin/bash

# The code for generate data form c2d project table

#20180414 version alpha 1
# example file name: /mazu/users/Jacob975/c2d/OPH/CATALOGS/catalog-OPH-HREL.tbl

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0} [file name] [argument]"
    echo "arguments: star, galaxy, yso. others"
    exit 1
fi

case ${2} in
    "star")
        awk '$15~/star/ && $15!~/dust/ \
            {print "["$22"," $26"," $30"," $42"," $60"," $78"," $96"," $114"," \
            $23"," $27"," $31"," $43"," $61"," $79"," $97"," $115"],"}' ${1} > star_sed.dat
        awk '$15~/star/ && $15!~/dust/ {print FNR }' ${1} > star_tracer.dat
        awk '$15~/star/ && $15!~/dust/ {print $3" "$5 }' ${1} > star_coord.dat
        awk '$15~/star/ && $15!~/dust/ {print $16" "$17 }' ${1} > star_Av.dat
        exit 0
        ;;
    
    "galaxy")
        awk '$15~/Galc/  \
            {print "["$22"," $26"," $30"," $42"," $60"," $78"," $96"," $114"," \
            $23"," $27"," $31"," $43"," $61"," $79"," $97"," $115"],"}' ${1} > gala_sed.dat
	    awk '$15~/Galc/   {print FNR }' ${1} > gala_tracer.dat
        awk '$15~/Galc/ {print $3" "$5 }' ${1} > gala_coord.dat
        awk '$15~/Galc/ {print $16" "$17 }' ${1} > gala_Av.dat
        exit 0
        ;;
    "yso")
        awk '$15~/YSOc/  \
            {print "["$22"," $26"," $30"," $42"," $60"," $78"," $96"," $114"," \
            $23"," $27"," $31"," $43"," $61"," $79"," $97"," $115"],"}' ${1} > ysos_sed.dat
        awk '$15~/YSOc/  {print FNR}' ${1} > ysos_tracer.dat
        awk '$15~/YSOc/  {print $3" "$5}' ${1} > ysos_coord.dat
        awk '$15~/YSOc/  {print $16" "$17}' ${1} > ysos_Av.dat
        exit 0
        ;;
    "others")
        awk '$15~/red/|| $15~/rising/ || $15~/falling/ || $15~/cup-up/ || $15~/cup-down/ || $15~/flat/ \
            {print "["$22"," $26"," $30"," $42"," $60"," $78"," $96"," $114"," $23"," \
            $27"," $31"," $43"," $61"," $79"," $97"," $115"],"}' ${1} > othr_sed.dat 
        awk '$15~/red/|| $15~/rising/ || $15~/falling/ || $15~/cup-up/ || $15~/cup-down/ || $15~/flat/ \
            {print FNR}' ${1} > othr_tracer.dat
        awk '$15~/red/|| $15~/rising/ || $15~/falling/ || $15~/cup-up/ || $15~/cup-down/ || $15~/flat/ \
            {print $3" "$5}' ${1} > othr_coord.dat
        exit 0
        ;;
    *)
        echo wrong argument
        echo "arguments: star, galaxy, yso. others"
        exit 1
esac
