#!/bin/bash
# The program is used to save common data arrangements

# Usage: arrange_data.sh [options]

# 20180719
# The code works

# check arguments
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [option]"
    echo "Available options: ELAIS_N1u_OPHu_CHA_II, ELAIS_N1_OPH_CHA_II, ELAIS_N1ui_OPHui_CHA_IIi, ELAIS_N1i_OPHi_CHA_IIi, ELAIS_N1ui, ELAIS_N1u, ELAIS_N1i, ELAIS_N1, OPHui, OPHu, OPHi, OPH, SERui, SERi, SERu, SER, PERui, PERu, PERi, PER, CHA_IIi, CHA_II, LUP_Ii, LUP_I, LUP_IIIi, LUP_III, LUP_IVi, LUP_IV"
    exit 1
fi

# Load arguments
option=${1}


if [ "${option}" = "ELAIS_N1ui_OPHui_CHA_IIi" ]; then
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
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_star_WSA.csv ELAIS_N1_2mass/star_2mass.dat ELAIS_N1_star_sed.dat
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_gala_WSA.csv ELAIS_N1_2mass/gala_2mass.dat ELAIS_N1_gala_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_star_WSA.csv OPH_2mass/star_2mass.dat OPH_star_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_gala_WSA.csv OPH_2mass/gala_2mass.dat OPH_gala_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_ysos_WSA.csv OPH_2mass/ysos_2mass.dat OPH_ysos_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/star_2mass.dat CHA_II_star_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/gala_2mass.dat CHA_II_gala_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/ysos_2mass.dat CHA_II_ysos_sed.dat
    echo done
    # Make an extinction map
    echo "Make an extinction map."
    calculate_extinction.py OPH_star_coord.dat OPH_star_sed_twomass_mag.txt OPH_star_sed_err_twomass_mag.txt WD55B 6
    mv star_Av.dat OPH_star_Av.dat
    calculate_extinction.py CHA_II_star_coord.dat CHA_II_star_sed_twomass_mag.txt CHA_II_star_sed_err_twomass_mag.txt WD55B 3
    mv star_Av.dat CHA_II_star_Av.dat
    calculate_extinction.py ELAIS_N1_star_coord.txt ELAIS_N1_star_sed_twomass_mag.txt ELAIS_N1_star_sed_err_twomass_mag.txt WD55B 4.5
    mv star_Av.dat ELAIS_N1_star_Av.dat
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss OPH_star_emap_360arcsec.txt OPH_star_sed_u.txt OPH_star_Av.dat OPH_star_coord.dat
    remove_Av.py ukidss OPH_star_emap_360arcsec.txt OPH_gala_sed_u.txt skip OPH_gala_coord.dat
    remove_Av.py ukidss OPH_star_emap_360arcsec.txt OPH_ysos_sed_u.txt skip OPH_ysos_coord.dat
    echo "OPH done."
    remove_Av.py ukidss CHA_II_star_emap_180arcsec.txt CHA_II_star_sed_u.txt CHA_II_star_Av.dat CHA_II_star_coord.dat
    remove_Av.py ukidss CHA_II_star_emap_180arcsec.txt CHA_II_gala_sed_u.txt skip CHA_II_gala_coord.dat
    remove_Av.py ukidss CHA_II_star_emap_180arcsec.txt CHA_II_ysos_sed_u.txt skip CHA_II_ysos_coord.dat
    echo "CHA_II done."
    remove_Av.py ukidss ELAIS_N1_star_emap_270arcsec.txt ELAIS_N1_star_sed_u.txt ELAIS_N1_star_Av.dat ELAIS_N1_star_coord.txt
    remove_Av.py ukidss ELAIS_N1_star_emap_270arcsec.txt ELAIS_N1_gala_sed_u.txt skip ELAIS_N1_gala_coord.txt
    echo "ELAIS N1 done."
    # stack all data
    echo "Stack all data"
    cat ELAIS_N1_star_sed_u_intrinsic.txt OPH_star_sed_u_intrinsic.txt CHA_II_star_sed_u_intrinsic.txt > star_sed_u_intrinsic.txt
    cat ELAIS_N1_gala_sed_u_intrinsic.txt OPH_gala_sed_u_intrinsic.txt CHA_II_gala_sed_u_intrinsic.txt > gala_sed_u_intrinsic.txt
    cat OPH_ysos_sed_u_intrinsic.txt CHA_II_ysos_sed_u_intrinsic.txt > ysos_sed_u_intrinsic.txt
    cat ELAIS_N1_star_coord.txt OPH_star_coord.dat CHA_II_star_coord.dat > star_coord.txt
    cat ELAIS_N1_gala_coord.txt OPH_gala_coord.dat CHA_II_gala_coord.dat > gala_coord.txt
    cat OPH_ysos_coord.dat CHA_II_ysos_coord.dat > ysos_coord.txt
    cat ELAIS_N1_star_tracer.dat OPH_star_tracer.dat CHA_II_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat OPH_gala_tracer.dat CHA_II_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat CHA_II_ysos_tracer.dat > ysos_tracer.dat
    echo done
    exit 0
fi

if [ "${option}" = "ELAIS_N1u_OPHu_CHA_II" ]; then
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
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_star_WSA.csv ELAIS_N1_2mass/star_2mass.dat ELAIS_N1_star_sed.dat
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_gala_WSA.csv ELAIS_N1_2mass/gala_2mass.dat ELAIS_N1_gala_sed.dat
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

if [ "${option}" = "ELAIS_N1i_OPHi_CHA_IIi" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-CHA_II-HREL.tbl star
    get_catalog.sh catalog-CHA_II-HREL.tbl galaxy
    get_catalog.sh catalog-CHA_II-HREL.tbl yso
    mv star_sed.dat CHA_II_star_sed.dat
    mv star_tracer.dat CHA_II_star_tracer.dat
    mv star_coord.dat CHA_II_star_coord.dat
    mv star_Av.dat CHA_II_star_Av.dat
    mv gala_coord.dat CHA_II_gala_coord.dat
    mv gala_sed.dat CHA_II_gala_sed.dat
    mv gala_tracer.dat CHA_II_gala_tracer.dat
    mv gala_Av.dat CHA_II_gala_Av.dat
    mv ysos_coord.dat CHA_II_ysos_coord.dat
    mv ysos_sed.dat CHA_II_ysos_sed.dat
    mv ysos_tracer.dat CHA_II_ysos_tracer.dat
    mv ysos_Av.dat CHA_II_ysos_Av.dat
    echo "CHA_II done."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    mv gala_coord.dat OPH_gala_coord.dat
    mv gala_sed.dat OPH_gala_sed.dat
    mv gala_tracer.dat OPH_gala_tracer.dat
    mv gala_Av.dat OPH_gala_Av.dat
    mv star_coord.dat OPH_star_coord.dat
    mv star_sed.dat OPH_star_sed.dat
    mv star_tracer.dat OPH_star_tracer.dat
    mv star_Av.dat OPH_star_Av.dat
    mv ysos_coord.dat OPH_ysos_coord.dat
    mv ysos_sed.dat OPH_ysos_sed.dat
    mv ysos_tracer.dat OPH_ysos_tracer.dat
    mv ysos_Av.dat OPH_ysos_Av.dat
    echo "OPH done."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    mv star_coord.txt ELAIS_N1_star_coord.txt
    mv star_sed.dat ELAIS_N1_star_sed.dat
    mv star_tracer.dat ELAIS_N1_star_tracer.dat
    mv star_Av.dat ELAIS_N1_star_Av.dat
    mv gala_coord.txt ELAIS_N1_gala_coord.txt
    mv gala_sed.dat ELAIS_N1_gala_sed.dat
    mv gala_tracer.dat ELAIS_N1_gala_tracer.dat
    mv gala_Av.dat ELAIS_N1_gala_Av.dat
    echo "ELAIS N1 done."
    # replace old data with ukidss data and 2mass data
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py DXS skip ELAIS_N1_2mass/star_2mass.dat ELAIS_N1_star_sed.dat
    replace_jhk_with_ukidss.py DXS skip ELAIS_N1_2mass/gala_2mass.dat ELAIS_N1_gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/star_2mass.dat OPH_star_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/gala_2mass.dat OPH_gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/ysos_2mass.dat OPH_ysos_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/star_2mass.dat CHA_II_star_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/gala_2mass.dat CHA_II_gala_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/ysos_2mass.dat CHA_II_ysos_sed.dat
    echo done
    # Make an extinction map
    echo "Make an extinction map."
    calculate_extinction.py OPH_star_coord.dat OPH_star_sed_twomass_mag.txt OPH_star_sed_err_twomass_mag.txt WD55B 6
    calculate_extinction.py CHA_II_star_coord.dat CHA_II_star_sed_twomass_mag.txt CHA_II_star_sed_err_twomass_mag.txt WD55B 3
    calculate_extinction.py ELAIS_N1_star_coord.txt ELAIS_N1_star_sed_twomass_mag.txt ELAIS_N1_star_sed_err_twomass_mag.txt WD55B 4.5
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss OPH_star_emap_360arcsec.txt OPH_star_sed_u.txt OPH_star_Av.dat OPH_star_coord.dat
    remove_Av.py ukidss OPH_star_emap_360arcsec.txt OPH_gala_sed_u.txt skip OPH_gala_coord.dat
    remove_Av.py ukidss OPH_star_emap_360arcsec.txt OPH_ysos_sed_u.txt skip OPH_ysos_coord.dat
    echo "OPH done."
    remove_Av.py ukidss CHA_II_star_emap_180arcsec.txt CHA_II_star_sed_u.txt CHA_II_star_Av.dat CHA_II_star_coord.dat
    remove_Av.py ukidss CHA_II_star_emap_180arcsec.txt CHA_II_gala_sed_u.txt skip CHA_II_gala_coord.dat
    remove_Av.py ukidss CHA_II_star_emap_180arcsec.txt CHA_II_ysos_sed_u.txt skip CHA_II_ysos_coord.dat
    echo "CHA_II done."
    remove_Av.py ukidss ELAIS_N1_star_emap_270arcsec.txt ELAIS_N1_star_sed_u.txt ELAIS_N1_star_Av.dat ELAIS_N1_star_coord.txt
    remove_Av.py ukidss ELAIS_N1_star_emap_270arcsec.txt ELAIS_N1_gala_sed_u.txt skip ELAIS_N1_gala_coord.txt
    echo "ELAIS N1 done."
    # stack all data
    echo "Stack all data"
    cat ELAIS_N1_star_sed_u_intrinsic.txt OPH_star_sed_u_intrinsic.txt CHA_II_star_sed_u_intrinsic.txt > star_sed_u_intrinsic.txt
    cat ELAIS_N1_gala_sed_u_intrinsic.txt OPH_gala_sed_u_intrinsic.txt CHA_II_gala_sed_u_intrinsic.txt > gala_sed_u_intrinsic.txt
    cat OPH_ysos_sed_u_intrinsic.txt CHA_II_ysos_sed_u_intrinsic.txt > ysos_sed_u_intrinsic.txt
    cat ELAIS_N1_star_coord.txt OPH_star_coord.dat CHA_II_star_coord.dat > star_coord.txt
    cat ELAIS_N1_gala_coord.txt OPH_gala_coord.dat CHA_II_gala_coord.dat > gala_coord.txt
    cat OPH_ysos_coord.dat CHA_II_ysos_coord.dat > ysos_coord.txt
    cat ELAIS_N1_star_tracer.dat OPH_star_tracer.dat CHA_II_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat OPH_gala_tracer.dat CHA_II_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat CHA_II_ysos_tracer.dat > ysos_tracer.dat
    echo done
    exit 0
fi

if [ "${option}" = "ELAIS_N1_OPH_CHA_II" ]; then
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

if [ "${option}" = "OPHui" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    echo "OPH done."
    # replace old data with ukidss data and 2mass data
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_star_WSA.csv OPH_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_gala_WSA.csv OPH_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_ysos_WSA.csv OPH_2mass/ysos_2mass.dat ysos_sed.dat
    echo done
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 6
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_360arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_360arcsec.txt gala_sed_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_360arcsec.txt ysos_sed_u.txt skip ysos_coord.dat
    echo "done."
    exit 0
fi

if [ "${option}" = "OPHu" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    echo "OPH done."
    # replace old data with ukidss data and 2mass data
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_star_WSA.csv OPH_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_gala_WSA.csv OPH_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_GCS_source_table_ysos_WSA.csv OPH_2mass/ysos_2mass.dat ysos_sed.dat
    echo done
    exit 0
fi

if [ "${option}" = "OPHi" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data."
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 6
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_360arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_360arcsec.txt gala_sed_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_360arcsec.txt ysos_sed_u.txt skip ysos_coord.dat
    echo "done."
    exit 0
fi

if [ "${option}" = "OPH" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    echo "OPH done."
    # convert 2MASS band system to UKIDSS band system 
    echo "Convert 2MASS band system to UKIDSS band system"
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip OPH_2mass/ysos_2mass.dat ysos_sed.dat
    echo done
    exit 0
fi

if [ "${option}" = "ELAIS_N1ui" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    echo done
    # replace old data with ukidss data and 2mass data
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_star_WSA.csv ELAIS_N1_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_gala_WSA.csv ELAIS_N1_2mass/gala_2mass.dat gala_sed.dat
    echo done
    # Make an extinction map
    echo "Make an extinction map."
    calculate_extinction.py star_coord.txt star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 4.5
    echo "done."
    # Do extinction correction with extinction map
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_270arcsec.txt star_sed_u.txt star_Av.dat star_coord.txt
    remove_Av.py ukidss star_emap_270arcsec.txt gala_sed_u.txt skip gala_coord.txt
    echo "done."
    exit 0
fi

if [ "${option}" = "ELAIS_N1i" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    echo "done."
    # convert 2MASS band system to UKIDSS band system 
    echo "Convert 2MASS band system to UKIDSS band system"
    replace_jhk_with_ukidss.py DXS skip ELAIS_N1_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py DXS skip ELAIS_N1_2mass/gala_2mass.dat gala_sed.dat
    echo done
    # Make an extinction map
    echo "Make an extinction map."
    calculate_extinction.py star_coord.txt star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 4.5
    echo "done."
    # Do extinction correction with extinction map
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_270arcsec.txt star_sed_u.txt star_Av.dat star_coord.txt
    remove_Av.py ukidss star_emap_270arcsec.txt gala_sed_u.txt skip gala_coord.txt
    echo "done."
    exit 0
fi

if [ "${option}" = "ELAIS_N1" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    echo "done."
    # convert 2MASS band system to UKIDSS band system 
    echo "Convert 2MASS band system to UKIDSS band system"
    replace_jhk_with_ukidss.py DXS skip ELAIS_N1_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py DXS skip ELAIS_N1_2mass/gala_2mass.dat gala_sed.dat
    echo done
    exit 0
fi

if [ "${option}" = "ELAIS_N1u" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    echo done
    # replace old data with ukidss data and 2mass data
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_star_WSA.csv ELAIS_N1_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py DXS ELAIS_N1_DXS_source_table_gala_WSA.csv ELAIS_N1_2mass/gala_2mass.dat gala_sed.dat
    echo done
    exit 0
fi

if [ "${option}" = "SERui" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-SER-HREL.tbl star
    get_catalog.sh catalog-SER-HREL.tbl galaxy
    get_catalog.sh catalog-SER-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data."
    replace_jhk_with_ukidss.py GPS SER_ukidss/SER_GPS_source_table_star_WSA.csv SER_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GPS SER_ukidss/SER_GPS_source_table_gala_WSA.csv SER_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GPS SER_ukidss/SER_GPS_source_table_ysos_WSA.csv SER_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 2
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_120arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_120arcsec.txt gala_sed_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_120arcsec.txt ysos_sed_u.txt skip ysos_coord.dat
    echo "done."
    exit 0
fi

if [ "${option}" = "SERi" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-SER-HREL.tbl star
    get_catalog.sh catalog-SER-HREL.tbl galaxy
    get_catalog.sh catalog-SER-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data."
    replace_jhk_with_ukidss.py GPS skip SER_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GPS skip SER_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GPS skip SER_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 2
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_120arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_120arcsec.txt gala_sed_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_120arcsec.txt ysos_sed_u.txt skip ysos_coord.dat
    echo "done."
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

if [ "${option}" = "PERui" ]; then
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
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 4 
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_240arcsec.txt star_sed_u_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_240arcsec.txt gala_sed_u_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_240arcsec.txt ysos_sed_u_u.txt skip ysos_coord.dat
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

if [ "${option}" = "PERi" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-PER-HREL.tbl star
    get_catalog.sh catalog-PER-HREL.tbl galaxy
    get_catalog.sh catalog-PER-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data."
    replace_jhk_with_ukidss.py GCS skip PER_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip PER_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip PER_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 4 
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_240arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_240arcsec.txt gala_sed_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_240arcsec.txt ysos_sed_u.txt skip ysos_coord.dat
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

if [ "${option}" = "CHA_IIi" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-CHA_II-HREL.tbl star
    get_catalog.sh catalog-CHA_II-HREL.tbl galaxy
    get_catalog.sh catalog-CHA_II-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data."
    replace_jhk_with_ukidss.py GCS skip CHA_II_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip CHA_II_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip CHA_II_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 2 
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_120arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_120arcsec.txt gala_sed_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_120arcsec.txt ysos_sed_u.txt skip ysos_coord.dat
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

if [ "${option}" = "LUP_Ii" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-LUP_I-HREL.tbl star
    get_catalog.sh catalog-LUP_I-HREL.tbl galaxy
    get_catalog.sh catalog-LUP_I-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data."
    replace_jhk_with_ukidss.py GCS skip LUP_I_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_I_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_I_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 3 
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_180arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_180arcsec.txt gala_sed_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_180arcsec.txt ysos_sed_u.txt skip ysos_coord.dat
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

if [ "${option}" = "LUP_IIIi" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-LUP_III-HREL.tbl star
    get_catalog.sh catalog-LUP_III-HREL.tbl galaxy
    get_catalog.sh catalog-LUP_III-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data."
    replace_jhk_with_ukidss.py GCS skip LUP_III_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_III_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_III_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 2.5 
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_150arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_150arcsec.txt gala_sed_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_150arcsec.txt ysos_sed_u.txt skip ysos_coord.dat
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

if [ "${option}" = "LUP_IVi" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-LUP_IV-HREL.tbl star
    get_catalog.sh catalog-LUP_IV-HREL.tbl galaxy
    get_catalog.sh catalog-LUP_IV-HREL.tbl yso
    echo "done."
    echo "Replace JHK with UKIDSS data."
    replace_jhk_with_ukidss.py GCS skip LUP_IV_2mass/star_2mass.dat star_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_IV_2mass/gala_2mass.dat gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_IV_2mass/ysos_2mass.dat ysos_sed.dat
    echo "done."
    echo "Make an extinction map."
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 2.5 
    echo "done."
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_150arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_150arcsec.txt gala_sed_u.txt skip gala_coord.dat
    remove_Av.py ukidss star_emap_150arcsec.txt ysos_sed_u.txt skip ysos_coord.dat
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
echo "Available options: ELAIS_N1u_OPHu_CHA_II, ELAIS_N1_OPH_CHA_II, ELAIS_N1ui_OPHui_CHA_IIi, ELAIS_N1i_OPHi_CHA_IIi, ELAIS_N1ui, ELAIS_N1u, ELAIS_N1i, ELAIS_N1, OPHui, OPHu, OPHi, OPH, SERui, SERi, SERu, SER, PERui, PERu, PERi, PER, CHA_IIi, CHA_II, LUP_Ii, LUP_I, LUP_IIIi, LUP_III, LUP_IVi, LUP_IV"
exit 1
