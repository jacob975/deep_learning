#!/bin/bash
# The program is used to save common data arrangements

# Usage: arrange_data.sh [options]

# 20180719
# The code works

# check arguments
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [option]"
    echo "Available options: data_Au_OPHu_CHA_II, data_A_OPH_CHA_II, SERu, SER, PERu, PER, CHA_II, LUP_I, LUP_III, LUP_IV"
    exit 1
fi

# Load arguments
option=${1}

if [ "${option}" = "data_Au_OPHu_CHA_II" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-CHA_II-HREL.tbl star
    get_catalog.sh catalog-CHA_II-HREL.tbl galaxy
    get_catalog.sh catalog-CHA_II-HREL.tbl yso
    mv star_sed.dat CHA_II_star_sed.dat
    mv star_tracer.dat CHA_II_star_tracer.dat
    mv star_coord.dat CHA_II_star_coord.dat
    mv gala_coord.dat CHA_II_gala_coord.dat
    mv gala_sed.dat CHA_II_gala_sed.dat
    mv gala_tracer.dat CHA_II_gala_tracer.dat
    mv ysos_coord.dat CHA_II_ysos_coord.dat
    mv ysos_sed.dat CHA_II_ysos_sed.dat
    mv ysos_tracer.dat CHA_II_ysos_tracer.dat
    echo "CHA_II done."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    mv gala_coord.dat OPH_gala_coord.dat
    mv gala_sed.dat OPH_gala_sed.dat
    mv gala_tracer.dat OPH_gala_tracer.dat
    mv star_coord.dat OPH_star_coord.dat
    mv star_sed.dat OPH_star_sed.dat
    mv star_tracer.dat OPH_star_tracer.dat
    mv ysos_coord.dat OPH_ysos_coord.dat
    mv ysos_sed.dat OPH_ysos_sed.dat
    mv ysos_tracer.dat OPH_ysos_tracer.dat
    echo "OPH done."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    mv star_coord.txt ELAIS_N1_star_coord.txt
    mv star_sed.dat ELAIS_N1_star_sed.dat
    mv star_tracer.dat ELAIS_N1_star_tracer.dat
    mv gala_coord.txt ELAIS_N1_gala_coord.txt
    mv gala_sed.dat ELAIS_N1_gala_sed.dat
    mv gala_tracer.dat ELAIS_N1_gala_tracer.dat
    echo "ELAIS N1 done."
    # replace old data with ukidss data and 2mass data
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_star_WSA.csv ELAIS_N1_2mass/star_2mass.txt ELAIS_N1_star_sed.dat
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_gala_WSA.csv ELAIS_N1_2mass/gala_2mass.txt ELAIS_N1_gala_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_star_WSA.csv OPH_2mass/star_2mass.dat OPH_star_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_gala_WSA.csv OPH_2mass/gala_2mass.dat OPH_gala_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_ysos_WSA.csv OPH_2mass/ysos_2mass.dat OPH_ysos_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/star_2mass.dat CHA_II_star_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/gala_2mass.dat CHA_II_gala_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/ysos_2mass.dat CHA_II_ysos_sed.dat
    echo done
    # stack all data
    echo "Stack all data"
    cat ELAIS_N1_star_sed_u.txt OPH_star_sed_u.txt CHA_II_star_sed_u.txt > star_sed_u.txt
    cat ELAIS_N1_gala_sed_u.txt OPH_gala_sed_u.txt CHA_II_gala_sed_u.txt > gala_sed_u.txt
    cat OPH_ysos_sed_u.txt CHA_II_ysos_sed_u.txt > ysos_sed_u.txt
    cat ELAIS_N1_star_coord.txt OPH_star_coord.dat CHA_II_star_coord.dat > star_coord.txt
    cat ELAIS_N1_gala_coord.txt OPH_gala_coord.dat CHA_II_gala_coord.dat > gala_coord.txt
    cat OPH_ysos_coord.dat CHA_II_ysos_coord.dat > ysos_coord.txt
    cat ELAIS_N1_star_tracer.dat OPH_star_tracer.dat CHA_II_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat OPH_gala_tracer.dat CHA_II_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat CHA_II_ysos_tracer.dat > ysos_tracer.dat
    echo done
    exit 0
fi

if [ "${option}" = "data_A_OPH_CHA_II" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-CHA_II-HREL.tbl star
    get_catalog.sh catalog-CHA_II-HREL.tbl galaxy
    get_catalog.sh catalog-CHA_II-HREL.tbl yso
    mv star_sed.dat CHA_II_star_sed.dat
    mv star_tracer.dat CHA_II_star_tracer.dat
    mv star_coord.dat CHA_II_star_coord.dat
    mv gala_coord.dat CHA_II_gala_coord.dat
    mv gala_sed.dat CHA_II_gala_sed.dat
    mv gala_tracer.dat CHA_II_gala_tracer.dat
    mv ysos_coord.dat CHA_II_ysos_coord.dat
    mv ysos_sed.dat CHA_II_ysos_sed.dat
    mv ysos_tracer.dat CHA_II_ysos_tracer.dat
    echo "CHA_II done."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    mv gala_coord.dat OPH_gala_coord.dat
    mv gala_sed.dat OPH_gala_sed.dat
    mv gala_tracer.dat OPH_gala_tracer.dat
    mv star_coord.dat OPH_star_coord.dat
    mv star_sed.dat OPH_star_sed.dat
    mv star_tracer.dat OPH_star_tracer.dat
    mv ysos_coord.dat OPH_ysos_coord.dat
    mv ysos_sed.dat OPH_ysos_sed.dat
    mv ysos_tracer.dat OPH_ysos_tracer.dat
    echo "OPH done."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    mv star_coord.txt ELAIS_N1_star_coord.txt
    mv star_sed.dat ELAIS_N1_star_sed.dat
    mv star_tracer.dat ELAIS_N1_star_tracer.dat
    mv gala_coord.txt ELAIS_N1_gala_coord.txt
    mv gala_sed.dat ELAIS_N1_gala_sed.dat
    mv gala_tracer.dat ELAIS_N1_gala_tracer.dat
    echo "ELAIS N1 done."
    # convert 2MASS band system to UKIDSS band system 
    echo "Convert 2MASS band system to UKIDSS band system"
    replace_jhk_with_ukidss.py DXS skip ELAIS_N1_2mass/star_2mass.dat ELAIS_N1_star_sed.dat
    replace_jhk_with_ukidss.py DXS skip ELAIS_N1_2mass/gala_2mass.dat ELAIS_N1_gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/star_2mass.dat OPH_star_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/gala_2mass.dat OPH_gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/ysos_2mass.dat OPH_ysos_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/star_2mass.dat CHA_II_star_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/gala_2mass.dat CHA_II_gala_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/ysos_2mass.dat CHA_II_ysos_sed.dat
    echo done
    # stack all data
    echo "Stack all data"
    cat ELAIS_N1_star_sed_u.txt OPH_star_sed_u.txt CHA_II_star_sed_u.txt > star_sed_u.txt
    cat ELAIS_N1_gala_sed_u.txt OPH_gala_sed_u.txt CHA_II_gala_sed_u.txt > gala_sed_u.txt
    cat OPH_ysos_sed_u.txt CHA_II_ysos_sed_u.txt > ysos_sed_u.txt
    cat ELAIS_N1_star_coord.txt OPH_star_coord.dat CHA_II_star_coord.dat > star_coord.txt
    cat ELAIS_N1_gala_coord.txt OPH_gala_coord.dat CHA_II_gala_coord.dat > gala_coord.txt
    cat OPH_ysos_coord.dat CHA_II_ysos_coord.dat > ysos_coord.txt
    cat ELAIS_N1_star_tracer.dat OPH_star_tracer.dat CHA_II_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat OPH_gala_tracer.dat CHA_II_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat CHA_II_ysos_tracer.dat > ysos_tracer.dat
    echo done
    exit 0
fi

if [ "${option}" = "SERu" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-SER-HREL.tbl star
    get_catalog.sh catalog-SER-HREL.tbl galaxy
    get_catalog.sh catalog-SER-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py GPS SER_ukidss/SER_GPS_source_table_star_WSA.csv SER_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GPS SER_ukidss/SER_GPS_source_table_gala_WSA.csv SER_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GPS SER_ukidss/SER_GPS_source_table_ysos_WSA.csv SER_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    exit 0
fi

if [ "${option}" = "SER" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-SER-HREL.tbl star
    get_catalog.sh catalog-SER-HREL.tbl galaxy
    get_catalog.sh catalog-SER-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py GPS skip SER_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GPS skip SER_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GPS skip SER_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    exit 0
fi

if [ "${option}" = "PERu" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-PER-HREL.tbl star
    get_catalog.sh catalog-PER-HREL.tbl galaxy
    get_catalog.sh catalog-PER-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py GCS PER_ukidss/PER_GCS_source_table_star_WSA.csv PER_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS PER_ukidss/PER_GCS_source_table_gala_WSA.csv PER_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS PER_ukidss/PER_GCS_source_table_ysos_WSA.csv PER_2mass/ysos_2mass.dat ysos_sed.dat
    replace_jhk_with_ukidss.py GPS PER_ukidss/PER_GPS_source_table_star_WSA.csv skip star_sed_u.txt
    replace_jhk_with_ukidss.py GPS PER_ukidss/PER_GPS_source_table_gala_WSA.csv skip gala_sed_u.txt
    replace_jhk_with_ukidss.py GPS PER_ukidss/PER_GPS_source_table_ysos_WSA.csv skip ysos_sed_u.txt
    echo "done."
    exit 0
fi

if [ "${option}" = "PER" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-PER-HREL.tbl star
    get_catalog.sh catalog-PER-HREL.tbl galaxy
    get_catalog.sh catalog-PER-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py GCS skip PER_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip PER_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip PER_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    exit 0
fi

if [ "${option}" = "CHA_II" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-CHA_II-HREL.tbl star
    get_catalog.sh catalog-CHA_II-HREL.tbl galaxy
    get_catalog.sh catalog-CHA_II-HREL.tbl yso
    echo "done."
    # convert 2MASS band system to UKIDSS band system 
    echo "Convert 2MASS band system to UKIDSS band system"
    replace_jhk_with_ukidss.py GCS skip CHA_II_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip CHA_II_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip CHA_II_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    exit 0
fi

if [ "${option}" = "LUP_I" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-LUP_I-HREL.tbl star
    get_catalog.sh catalog-LUP_I-HREL.tbl galaxy
    get_catalog.sh catalog-LUP_I-HREL.tbl yso
    echo "done."
    # convert 2MASS band system to UKIDSS band system 
    echo "Convert 2MASS band system to UKIDSS band system"
    replace_jhk_with_ukidss.py GCS skip LUP_I_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_I_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_I_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    exit 0
fi

if [ "${option}" = "LUP_III" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-LUP_III-HREL.tbl star
    get_catalog.sh catalog-LUP_III-HREL.tbl galaxy
    get_catalog.sh catalog-LUP_III-HREL.tbl yso
    echo "done."
    # convert 2MASS band system to UKIDSS band system 
    echo "Convert 2MASS band system to UKIDSS band system"
    replace_jhk_with_ukidss.py GCS skip LUP_III_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_III_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_III_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    exit 0
fi

if [ "${option}" = "LUP_IV" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-LUP_IV-HREL.tbl star
    get_catalog.sh catalog-LUP_IV-HREL.tbl galaxy
    get_catalog.sh catalog-LUP_IV-HREL.tbl yso
    echo "done."
    # convert 2MASS band system to UKIDSS band system 
    echo "Convert 2MASS band system to UKIDSS band system"
    replace_jhk_with_ukidss.py GCS skip LUP_IV_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_IV_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_IV_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    exit 0
fi


echo "No match parameters"
echo "Available options: data_Au_OPHu_CHA_II, data_A_OPH_CHA_II, SERu, SER, PERu, PER, CHA_II, LUP_I, LUP_III, LUP_IV"
exit 1
