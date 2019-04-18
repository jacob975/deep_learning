#!/bin/bash
# The program is used to save common data arrangements

# Usage: arrange_data.sh [options]

# 20180719
# The code works

available_sources=\
' ELAIS_N1u_OPHu_CHA_II,'\
' ELAIS_N1_OPH_CHA_II,'\
' ELAIS_N1ui_OPHui_CHA_IIi,'\
' ELAIS_N1i_OPHi_CHA_IIi,'\
' ELAIS_N1u_OPHu_CHA_II_slctEC,'\
' ELAIS_N1ui,'\
' ELAIS_N1u,'\
' ELAIS_N1i,'\
' ELAIS_N1,'\
' OPHui,'\
' OPHu,'\
' OPHi,'\
' OPH,'\
' SERui,'\
' SERi,'\
' SERu,'\
' SER,'\
' SERu_slct,'\
' PERui,'\
' PERu_slctEC,'\
' PERu,'\
' PERi,'\
' PER,'\
' CHA_IIi,'\
' CHA_II,'\
' CHA_II_slctEC,'\
' LUP_Ii,'\
' LUP_I,'\
' LUP_I_slctEC,'\
' LUP_IIIi,'\
' LUP_III_slctEC,'\
' LUP_III,'\
' LUP_IVi,'\
' LUP_IV_slctEC,'\
' LUP_IV,'\
' ALLu,'

# check arguments
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [option]"
    echo "Available options: ${available_sources}"
    exit 1
fi

# Load arguments
option=${1}

if [ "${option}" = "ALLu" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-CHA_II-HREL.tbl star
    get_catalog.sh catalog-CHA_II-HREL.tbl galaxy
    get_catalog.sh catalog-CHA_II-HREL.tbl yso
    mv star_sed.dat CHA_II_star_sed.dat
    mv star_tracer.dat CHA_II_star_tracer.dat
    mv star_coord.dat CHA_II_star_coord.dat
    mv star_Q.dat CHA_II_star_Q.dat
    mv gala_coord.dat CHA_II_gala_coord.dat
    mv gala_sed.dat CHA_II_gala_sed.dat
    mv gala_tracer.dat CHA_II_gala_tracer.dat
    mv gala_Q.dat CHA_II_gala_Q.dat
    mv ysos_coord.dat CHA_II_ysos_coord.dat
    mv ysos_sed.dat CHA_II_ysos_sed.dat
    mv ysos_tracer.dat CHA_II_ysos_tracer.dat
    mv ysos_Q.dat CHA_II_ysos_Q.dat
    echo "CHA_II done."
    get_catalog.sh catalog-LUP_I-HREL.tbl star
    get_catalog.sh catalog-LUP_I-HREL.tbl galaxy
    get_catalog.sh catalog-LUP_I-HREL.tbl yso
    mv star_sed.dat LUP_I_star_sed.dat
    mv star_tracer.dat LUP_I_star_tracer.dat
    mv star_coord.dat LUP_I_star_coord.dat
    mv star_Q.dat LUP_I_star_Q.dat
    mv gala_coord.dat LUP_I_gala_coord.dat
    mv gala_sed.dat LUP_I_gala_sed.dat
    mv gala_tracer.dat LUP_I_gala_tracer.dat
    mv gala_Q.dat LUP_I_gala_Q.dat
    mv ysos_coord.dat LUP_I_ysos_coord.dat
    mv ysos_sed.dat LUP_I_ysos_sed.dat
    mv ysos_tracer.dat LUP_I_ysos_tracer.dat
    mv ysos_Q.dat LUP_I_ysos_Q.dat
    echo "LUP_I done."
    get_catalog.sh catalog-LUP_III-HREL.tbl star
    get_catalog.sh catalog-LUP_III-HREL.tbl galaxy
    get_catalog.sh catalog-LUP_III-HREL.tbl yso
    mv star_sed.dat LUP_III_star_sed.dat
    mv star_tracer.dat LUP_III_star_tracer.dat
    mv star_coord.dat LUP_III_star_coord.dat
    mv star_Q.dat LUP_III_star_Q.dat
    mv gala_coord.dat LUP_III_gala_coord.dat
    mv gala_sed.dat LUP_III_gala_sed.dat
    mv gala_tracer.dat LUP_III_gala_tracer.dat
    mv gala_Q.dat LUP_III_gala_Q.dat
    mv ysos_coord.dat LUP_III_ysos_coord.dat
    mv ysos_sed.dat LUP_III_ysos_sed.dat
    mv ysos_tracer.dat LUP_III_ysos_tracer.dat
    mv ysos_Q.dat LUP_III_ysos_Q.dat
    echo "LUP_III done."
    get_catalog.sh catalog-LUP_IV-HREL.tbl star
    get_catalog.sh catalog-LUP_IV-HREL.tbl galaxy
    get_catalog.sh catalog-LUP_IV-HREL.tbl yso
    mv star_sed.dat LUP_IV_star_sed.dat
    mv star_tracer.dat LUP_IV_star_tracer.dat
    mv star_coord.dat LUP_IV_star_coord.dat
    mv star_Q.dat LUP_IV_star_Q.dat
    mv gala_coord.dat LUP_IV_gala_coord.dat
    mv gala_sed.dat LUP_IV_gala_sed.dat
    mv gala_tracer.dat LUP_IV_gala_tracer.dat
    mv gala_Q.dat LUP_IV_gala_Q.dat
    mv ysos_coord.dat LUP_IV_ysos_coord.dat
    mv ysos_sed.dat LUP_IV_ysos_sed.dat
    mv ysos_tracer.dat LUP_IV_ysos_tracer.dat
    mv ysos_Q.dat LUP_IV_ysos_Q.dat
    echo "LUP_IV done."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    mv gala_coord.dat OPH_gala_coord.dat
    mv gala_sed.dat OPH_gala_sed.dat
    mv gala_tracer.dat OPH_gala_tracer.dat
    mv gala_Q.dat OPH_gala_Q.dat
    mv star_coord.dat OPH_star_coord.dat
    mv star_sed.dat OPH_star_sed.dat
    mv star_tracer.dat OPH_star_tracer.dat
    mv star_Q.dat OPH_star_Q.dat
    mv ysos_coord.dat OPH_ysos_coord.dat
    mv ysos_sed.dat OPH_ysos_sed.dat
    mv ysos_tracer.dat OPH_ysos_tracer.dat
    mv ysos_Q.dat OPH_ysos_Q.dat
    echo "OPH done."
    get_catalog.sh catalog-PER-HREL.tbl star
    get_catalog.sh catalog-PER-HREL.tbl galaxy
    get_catalog.sh catalog-PER-HREL.tbl yso
    mv star_sed.dat PER_star_sed.dat
    mv star_tracer.dat PER_star_tracer.dat
    mv star_coord.dat PER_star_coord.dat
    mv star_Q.dat PER_star_Q.dat
    mv gala_coord.dat PER_gala_coord.dat
    mv gala_sed.dat PER_gala_sed.dat
    mv gala_tracer.dat PER_gala_tracer.dat
    mv gala_Q.dat PER_gala_Q.dat
    mv ysos_coord.dat PER_ysos_coord.dat
    mv ysos_sed.dat PER_ysos_sed.dat
    mv ysos_tracer.dat PER_ysos_tracer.dat
    mv ysos_Q.dat PER_ysos_Q.dat
    echo "PER done."
    get_catalog.sh catalog-SER-HREL.tbl star
    get_catalog.sh catalog-SER-HREL.tbl galaxy
    get_catalog.sh catalog-SER-HREL.tbl yso
    mv star_sed.dat SER_star_sed.dat
    mv star_tracer.dat SER_star_tracer.dat
    mv star_coord.dat SER_star_coord.dat
    mv star_Q.dat SER_star_Q.dat
    mv gala_coord.dat SER_gala_coord.dat
    mv gala_sed.dat SER_gala_sed.dat
    mv gala_tracer.dat SER_gala_tracer.dat
    mv gala_Q.dat SER_gala_Q.dat
    mv ysos_coord.dat SER_ysos_coord.dat
    mv ysos_sed.dat SER_ysos_sed.dat
    mv ysos_tracer.dat SER_ysos_tracer.dat
    mv ysos_Q.dat SER_ysos_Q.dat
    echo "SER done."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    mv star_coord.dat ELAIS_N1_star_coord.dat
    mv star_sed.dat ELAIS_N1_star_sed.dat
    mv star_tracer.dat ELAIS_N1_star_tracer.dat
    mv star_Q.dat ELAIS_N1_star_Q.dat
    mv gala_coord.dat ELAIS_N1_gala_coord.dat
    mv gala_sed.dat ELAIS_N1_gala_sed.dat
    mv gala_tracer.dat ELAIS_N1_gala_tracer.dat
    mv gala_Q.dat ELAIS_N1_gala_Q.dat
    echo "ELAIS N1 done."
    # replace old data with ukidss data and 2mass data
    echo "Replace JHK with UKIDSS data"
    replace_jhk_with_ukidss.py DXS ELAIS_N1_ukidss/ELAIS_N1_DXS_source_table_star_WSA.csv ELAIS_N1_2mass/star_2mass.dat ELAIS_N1_star_sed.dat
    replace_jhk_with_ukidss.py DXS ELAIS_N1_ukidss/ELAIS_N1_DXS_source_table_gala_WSA.csv ELAIS_N1_2mass/gala_2mass.dat ELAIS_N1_gala_sed.dat
    
    replace_jhk_with_ukidss.py GCS OPH_ukidss/OPH_GCS_source_table_star_WSA.csv OPH_2mass/star_2mass.dat OPH_star_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_ukidss/OPH_GCS_source_table_gala_WSA.csv OPH_2mass/gala_2mass.dat OPH_gala_sed.dat
    replace_jhk_with_ukidss.py GCS OPH_ukidss/OPH_GCS_source_table_ysos_WSA.csv OPH_2mass/ysos_2mass.dat OPH_ysos_sed.dat
    
    replace_jhk_with_ukidss.py GPS SER_ukidss/SER_GPS_source_table_star_WSA.csv SER_2mass/star_2mass.dat SER_star_sed.dat
    replace_jhk_with_ukidss.py GPS SER_ukidss/SER_GPS_source_table_gala_WSA.csv SER_2mass/gala_2mass.dat SER_gala_sed.dat
    replace_jhk_with_ukidss.py GPS SER_ukidss/SER_GPS_source_table_ysos_WSA.csv SER_2mass/ysos_2mass.dat SER_ysos_sed.dat
    
    replace_jhk_with_ukidss.py GCS PER_ukidss/PER_GCS_source_table_star_WSA.csv PER_2mass/star_2mass.dat PER_star_sed.dat
    replace_jhk_with_ukidss.py GCS PER_ukidss/PER_GCS_source_table_gala_WSA.csv PER_2mass/gala_2mass.dat PER_gala_sed.dat
    replace_jhk_with_ukidss.py GCS PER_ukidss/PER_GCS_source_table_ysos_WSA.csv PER_2mass/ysos_2mass.dat PER_ysos_sed.dat
    replace_jhk_with_ukidss.py GPS PER_ukidss/PER_GPS_source_table_star_WSA.csv skip PER_star_sed_u.txt
    replace_jhk_with_ukidss.py GPS PER_ukidss/PER_GPS_source_table_gala_WSA.csv skip PER_gala_sed_u.txt
    replace_jhk_with_ukidss.py GPS PER_ukidss/PER_GPS_source_table_ysos_WSA.csv skip PER_ysos_sed_u.txt
    
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/star_2mass.dat CHA_II_star_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/gala_2mass.dat CHA_II_gala_sed.dat
    replace_jhk_with_ukidss.py DXS skip CHA_II_2mass/ysos_2mass.dat CHA_II_ysos_sed.dat
    
    replace_jhk_with_ukidss.py GCS skip LUP_I_2mass/star_2mass.dat LUP_I_star_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_I_2mass/gala_2mass.dat LUP_I_gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_I_2mass/ysos_2mass.dat LUP_I_ysos_sed.dat
    
    replace_jhk_with_ukidss.py GCS skip LUP_III_2mass/star_2mass.dat LUP_III_star_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_III_2mass/gala_2mass.dat LUP_III_gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_III_2mass/ysos_2mass.dat LUP_III_ysos_sed.dat
    
    replace_jhk_with_ukidss.py GCS skip LUP_IV_2mass/star_2mass.dat LUP_IV_star_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_IV_2mass/gala_2mass.dat LUP_IV_gala_sed.dat
    replace_jhk_with_ukidss.py GCS skip LUP_IV_2mass/ysos_2mass.dat LUP_IV_ysos_sed.dat
    echo done
    # stack all data
    echo "Stack all data"
    cat ELAIS_N1_star_sed_u.txt \
        OPH_star_sed_u.txt \
        SER_star_sed_u.txt \
        PER_star_sed_u_u.txt \
        CHA_II_star_sed_u.txt \
        LUP_I_star_sed_u.txt \
        LUP_III_star_sed_u.txt \
        LUP_IV_star_sed_u.txt > star_sed_u.txt
    cat ELAIS_N1_gala_sed_u.txt \
        OPH_gala_sed_u.txt \
        SER_gala_sed_u.txt \
        PER_gala_sed_u_u.txt \
        CHA_II_gala_sed_u.txt \
        LUP_I_gala_sed_u.txt \
        LUP_III_gala_sed_u.txt \
        LUP_IV_gala_sed_u.txt > gala_sed_u.txt
    cat OPH_ysos_sed_u.txt \
        SER_ysos_sed_u.txt \
        PER_ysos_sed_u_u.txt \
        CHA_II_ysos_sed_u.txt \
        LUP_I_ysos_sed_u.txt \
        LUP_III_ysos_sed_u.txt \
        LUP_IV_ysos_sed_u.txt > ysos_sed_u.txt
    cat ELAIS_N1_star_coord.dat \
        OPH_star_coord.dat \
        SER_star_coord.dat \
        PER_star_coord.dat \
        CHA_II_star_coord.dat \
        LUP_I_star_coord.dat \
        LUP_III_star_coord.dat \
        LUP_IV_star_coord.dat > star_coord.dat
    cat ELAIS_N1_gala_coord.dat \
        OPH_gala_coord.dat \
        SER_gala_coord.dat \
        PER_gala_coord.dat \
        CHA_II_gala_coord.dat \
        LUP_I_gala_coord.dat \
        LUP_III_gala_coord.dat \
        LUP_IV_gala_coord.dat > gala_coord.dat
    cat OPH_ysos_coord.dat \
        SER_ysos_coord.dat \
        PER_ysos_coord.dat \
        CHA_II_ysos_coord.dat \
        LUP_I_ysos_coord.dat \
        LUP_III_ysos_coord.dat \
        LUP_IV_ysos_coord.dat > ysos_coord.dat
    cat ELAIS_N1_star_tracer.dat \
        OPH_star_tracer.dat \
        SER_star_tracer.dat \
        PER_star_tracer.dat \
        CHA_II_star_tracer.dat \
        LUP_I_star_tracer.dat \
        LUP_III_star_tracer.dat \
        LUP_IV_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat \
        OPH_gala_tracer.dat \
        SER_gala_tracer.dat \
        PER_gala_tracer.dat \
        CHA_II_gala_tracer.dat \
        LUP_I_gala_tracer.dat \
        LUP_III_gala_tracer.dat \
        LUP_IV_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat \
        SER_ysos_tracer.dat \
        PER_ysos_tracer.dat \
        CHA_II_ysos_tracer.dat \
        LUP_I_ysos_tracer.dat \
        LUP_III_ysos_tracer.dat \
        LUP_IV_ysos_tracer.dat > ysos_tracer.dat
    cat ELAIS_N1_star_Q.dat \
        OPH_star_Q.dat \
        SER_star_Q.dat \
        PER_star_Q.dat \
        CHA_II_star_Q.dat \
        LUP_I_star_Q.dat \
        LUP_III_star_Q.dat \
        LUP_IV_star_Q.dat > star_Q.dat
    cat ELAIS_N1_gala_Q.dat \
        OPH_gala_Q.dat \
        SER_gala_Q.dat \
        PER_gala_Q.dat \
        CHA_II_gala_Q.dat \
        LUP_I_gala_Q.dat \
        LUP_III_gala_Q.dat \
        LUP_IV_gala_Q.dat > gala_Q.dat
    cat OPH_ysos_Q.dat \
        SER_ysos_Q.dat \
        PER_ysos_Q.dat \
        CHA_II_ysos_Q.dat \
        LUP_I_ysos_Q.dat \
        LUP_III_ysos_Q.dat \
        LUP_IV_ysos_Q.dat > ysos_Q.dat
    
    cat HL_2013/HL_ELAIS_N1_gala_label.txt \
        HL_2013/HL_OPH_gala_label.txt \
        HL_2013/HL_SER_gala_label.txt \
        HL_2013/HL_PER_gala_label.txt \
        HL_2013/HL_CHA_II_gala_label.txt \
        HL_2013/HL_LUP_I_gala_label.txt \
        HL_2013/HL_LUP_III_gala_label.txt \
        HL_2013/HL_LUP_IV_gala_label.txt > HL_gala_label.dat
    cat HL_2013/HL_ELAIS_N1_star_label.txt \
        HL_2013/HL_OPH_star_label.txt \
        HL_2013/HL_SER_star_label.txt \
        HL_2013/HL_PER_star_label.txt \
        HL_2013/HL_CHA_II_star_label.txt \
        HL_2013/HL_LUP_I_star_label.txt \
        HL_2013/HL_LUP_III_star_label.txt \
        HL_2013/HL_LUP_IV_star_label.txt > HL_star_label.dat
    cat HL_2013/HL_OPH_ysos_label.txt \
        HL_2013/HL_SER_ysos_label.txt \
        HL_2013/HL_PER_ysos_label.txt \
        HL_2013/HL_CHA_II_ysos_label.txt \
        HL_2013/HL_LUP_I_ysos_label.txt \
        HL_2013/HL_LUP_III_ysos_label.txt \
        HL_2013/HL_LUP_IV_ysos_label.txt > HL_ysos_label.dat
    echo done
    exit 0
fi

if [ "${option}" = "ELAIS_N1ui_OPHui_CHA_IIi" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-CHA_II-HREL.tbl star
    get_catalog.sh catalog-CHA_II-HREL.tbl galaxy
    get_catalog.sh catalog-CHA_II-HREL.tbl yso
    mv star_sed.dat CHA_II_star_sed.dat
    mv star_tracer.dat CHA_II_star_tracer.dat
    mv star_coord.dat CHA_II_star_coord.dat
    mv star_Q.dat CHA_II_star_Q.dat
    mv gala_coord.dat CHA_II_gala_coord.dat
    mv gala_sed.dat CHA_II_gala_sed.dat
    mv gala_tracer.dat CHA_II_gala_tracer.dat
    mv gala_Q.dat CHA_II_gala_Q.dat
    mv ysos_coord.dat CHA_II_ysos_coord.dat
    mv ysos_sed.dat CHA_II_ysos_sed.dat
    mv ysos_tracer.dat CHA_II_ysos_tracer.dat
    mv ysos_Q.dat CHA_II_ysos_Q.dat
    echo "CHA_II done."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    mv gala_coord.dat OPH_gala_coord.dat
    mv gala_sed.dat OPH_gala_sed.dat
    mv gala_tracer.dat OPH_gala_tracer.dat
    mv gala_Q.dat OPH_gala_Q.dat
    mv star_coord.dat OPH_star_coord.dat
    mv star_sed.dat OPH_star_sed.dat
    mv star_tracer.dat OPH_star_tracer.dat
    mv star_Q.dat OPH_star_Q.dat
    mv ysos_coord.dat OPH_ysos_coord.dat
    mv ysos_sed.dat OPH_ysos_sed.dat
    mv ysos_tracer.dat OPH_ysos_tracer.dat
    mv ysos_Q.dat OPH_ysos_Q.dat
    echo "OPH done."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    mv star_coord.dat ELAIS_N1_star_coord.dat
    mv star_sed.dat ELAIS_N1_star_sed.dat
    mv star_tracer.dat ELAIS_N1_star_tracer.dat
    mv star_Q.dat ELAIS_N1_star_Q.dat
    mv gala_coord.dat ELAIS_N1_gala_coord.dat
    mv gala_sed.dat ELAIS_N1_gala_sed.dat
    mv gala_tracer.dat ELAIS_N1_gala_tracer.dat
    mv gala_Q.dat ELAIS_N1_gala_Q.dat
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
    calculate_extinction.py CHA_II_star_coord.dat CHA_II_star_sed_twomass_mag.txt CHA_II_star_sed_err_twomass_mag.txt WD55B 3
    calculate_extinction.py ELAIS_N1_star_coord.dat ELAIS_N1_star_sed_twomass_mag.txt ELAIS_N1_star_sed_err_twomass_mag.txt WD55B 4.5
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
    remove_Av.py ukidss ELAIS_N1_star_emap_270arcsec.txt ELAIS_N1_star_sed_u.txt ELAIS_N1_star_Av.dat ELAIS_N1_star_coord.dat
    remove_Av.py ukidss ELAIS_N1_star_emap_270arcsec.txt ELAIS_N1_gala_sed_u.txt skip ELAIS_N1_gala_coord.dat
    echo "ELAIS N1 done."
    # stack all data
    echo "Stack all data"
    cat ELAIS_N1_star_sed_u_intrinsic.txt OPH_star_sed_u_intrinsic.txt CHA_II_star_sed_u_intrinsic.txt > star_sed_u_intrinsic.txt
    cat ELAIS_N1_gala_sed_u_intrinsic.txt OPH_gala_sed_u_intrinsic.txt CHA_II_gala_sed_u_intrinsic.txt > gala_sed_u_intrinsic.txt
    cat OPH_ysos_sed_u_intrinsic.txt CHA_II_ysos_sed_u_intrinsic.txt > ysos_sed_u_intrinsic.txt
    cat ELAIS_N1_star_coord.dat OPH_star_coord.dat CHA_II_star_coord.dat > star_coord.dat
    cat ELAIS_N1_gala_coord.dat OPH_gala_coord.dat CHA_II_gala_coord.dat > gala_coord.dat
    cat OPH_ysos_coord.dat CHA_II_ysos_coord.dat > ysos_coord.dat
    cat ELAIS_N1_star_tracer.dat OPH_star_tracer.dat CHA_II_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat OPH_gala_tracer.dat CHA_II_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat CHA_II_ysos_tracer.dat > ysos_tracer.dat
    cat ELAIS_N1_star_Q.dat OPH_star_Q.dat CHA_II_star_Q.dat > star_Q.dat
    cat ELAIS_N1_gala_Q.dat OPH_gala_Q.dat CHA_II_gala_Q.dat > gala_Q.dat
    cat OPH_ysos_Q.dat CHA_II_ysos_Q.dat > ysos_Q.dat
    echo done
    exit 0
fi


if [ "${option}" = "ELAIS_N1u_OPHu_CHA_II_slctEC" ]; then
    # Cut data from dataset
    echo "Cut data from catalog."
    get_catalog.sh catalog-CHA_II-HREL.tbl star
    get_catalog.sh catalog-CHA_II-HREL.tbl galaxy
    get_catalog.sh catalog-CHA_II-HREL.tbl yso
    mv star_sed.dat CHA_II_star_sed.dat
    mv star_tracer.dat CHA_II_star_tracer.dat
    mv star_coord.dat CHA_II_star_coord.dat
    mv star_Q.dat CHA_II_star_Q.dat
    mv gala_coord.dat CHA_II_gala_coord.dat
    mv gala_sed.dat CHA_II_gala_sed.dat
    mv gala_tracer.dat CHA_II_gala_tracer.dat
    mv gala_Q.dat CHA_II_gala_Q.dat
    mv ysos_coord.dat CHA_II_ysos_coord.dat
    mv ysos_sed.dat CHA_II_ysos_sed.dat
    mv ysos_tracer.dat CHA_II_ysos_tracer.dat
    mv ysos_Q.dat CHA_II_ysos_Q.dat
    echo "CHA_II done."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    mv gala_coord.dat OPH_gala_coord.dat
    mv gala_sed.dat OPH_gala_sed.dat
    mv gala_tracer.dat OPH_gala_tracer.dat
    mv gala_Q.dat OPH_gala_Q.dat
    mv star_coord.dat OPH_star_coord.dat
    mv star_sed.dat OPH_star_sed.dat
    mv star_tracer.dat OPH_star_tracer.dat
    mv star_Q.dat OPH_star_Q.dat
    mv ysos_coord.dat OPH_ysos_coord.dat
    mv ysos_sed.dat OPH_ysos_sed.dat
    mv ysos_tracer.dat OPH_ysos_tracer.dat
    mv ysos_Q.dat OPH_ysos_Q.dat
    echo "OPH done."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    mv star_coord.dat ELAIS_N1_star_coord.dat
    mv star_sed.dat ELAIS_N1_star_sed.dat
    mv star_tracer.dat ELAIS_N1_star_tracer.dat
    mv star_Q.dat ELAIS_N1_star_Q.dat
    mv gala_coord.dat ELAIS_N1_gala_coord.dat
    mv gala_sed.dat ELAIS_N1_gala_sed.dat
    mv gala_tracer.dat ELAIS_N1_gala_tracer.dat
    mv gala_Q.dat ELAIS_N1_gala_Q.dat
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
    # Select sources with the extinction correction.
    echo "Select sources with the extinction correction"
    select_data.py filter ELAIS_N1_star_sed_u.txt ../prototype_EC/ELAIS_N1_star_sed_u_index_of_no_Av.txt
    select_data.py filter ELAIS_N1_gala_sed_u.txt ../prototype_EC/ELAIS_N1_gala_sed_u_index_of_no_Av.txt
    select_data.py filter ELAIS_N1_star_coord.dat ../prototype_EC/ELAIS_N1_star_sed_u_index_of_no_Av.txt
    select_data.py filter ELAIS_N1_gala_coord.dat ../prototype_EC/ELAIS_N1_gala_sed_u_index_of_no_Av.txt
    select_data.py filter ELAIS_N1_star_tracer.dat ../prototype_EC/ELAIS_N1_star_sed_u_index_of_no_Av.txt
    select_data.py filter ELAIS_N1_gala_tracer.dat ../prototype_EC/ELAIS_N1_gala_sed_u_index_of_no_Av.txt
    select_data.py filter ELAIS_N1_star_Q.dat ../prototype_EC/ELAIS_N1_star_sed_u_index_of_no_Av.txt
    select_data.py filter ELAIS_N1_gala_Q.dat ../prototype_EC/ELAIS_N1_gala_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_star_sed_u.txt ../prototype_EC/OPH_star_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_gala_sed_u.txt ../prototype_EC/OPH_gala_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_ysos_sed_u.txt ../prototype_EC/OPH_ysos_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_star_coord.dat ../prototype_EC/OPH_star_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_gala_coord.dat ../prototype_EC/OPH_gala_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_ysos_coord.dat ../prototype_EC/OPH_ysos_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_star_tracer.dat ../prototype_EC/OPH_star_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_gala_tracer.dat ../prototype_EC/OPH_gala_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_ysos_tracer.dat ../prototype_EC/OPH_ysos_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_star_Q.dat ../prototype_EC/OPH_star_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_gala_Q.dat ../prototype_EC/OPH_gala_sed_u_index_of_no_Av.txt
    select_data.py filter OPH_ysos_Q.dat ../prototype_EC/OPH_ysos_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_star_sed_u.txt ../prototype_EC/CHA_II_star_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_gala_sed_u.txt ../prototype_EC/CHA_II_gala_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_ysos_sed_u.txt ../prototype_EC/CHA_II_ysos_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_star_coord.dat ../prototype_EC/CHA_II_star_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_gala_coord.dat ../prototype_EC/CHA_II_gala_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_ysos_coord.dat ../prototype_EC/CHA_II_ysos_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_star_tracer.dat ../prototype_EC/CHA_II_star_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_gala_tracer.dat ../prototype_EC/CHA_II_gala_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_ysos_tracer.dat ../prototype_EC/CHA_II_ysos_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_star_Q.dat ../prototype_EC/CHA_II_star_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_gala_Q.dat ../prototype_EC/CHA_II_gala_sed_u_index_of_no_Av.txt
    select_data.py filter CHA_II_ysos_Q.dat ../prototype_EC/CHA_II_ysos_sed_u_index_of_no_Av.txt
    echo done
    # stack all data
    echo "Stack all data"
    cat ELAIS_N1_star_sed_u.txt OPH_star_sed_u.txt CHA_II_star_sed_u.txt > star_sed_u.txt
    cat ELAIS_N1_gala_sed_u.txt OPH_gala_sed_u.txt CHA_II_gala_sed_u.txt > gala_sed_u.txt
    cat OPH_ysos_sed_u.txt CHA_II_ysos_sed_u.txt > ysos_sed_u.txt
    cat ELAIS_N1_star_coord.dat OPH_star_coord.dat CHA_II_star_coord.dat > star_coord.dat
    cat ELAIS_N1_gala_coord.dat OPH_gala_coord.dat CHA_II_gala_coord.dat > gala_coord.dat
    cat OPH_ysos_coord.dat CHA_II_ysos_coord.dat > ysos_coord.dat
    cat ELAIS_N1_star_tracer.dat OPH_star_tracer.dat CHA_II_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat OPH_gala_tracer.dat CHA_II_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat CHA_II_ysos_tracer.dat > ysos_tracer.dat
    cat ELAIS_N1_star_Q.dat OPH_star_Q.dat CHA_II_star_Q.dat > star_Q.dat
    cat ELAIS_N1_gala_Q.dat OPH_gala_Q.dat CHA_II_gala_Q.dat > gala_Q.dat
    cat OPH_ysos_Q.dat CHA_II_ysos_Q.dat > ysos_Q.dat
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
    mv star_Q.dat CHA_II_star_Q.dat
    mv gala_coord.dat CHA_II_gala_coord.dat
    mv gala_sed.dat CHA_II_gala_sed.dat
    mv gala_tracer.dat CHA_II_gala_tracer.dat
    mv gala_Q.dat CHA_II_gala_Q.dat
    mv ysos_coord.dat CHA_II_ysos_coord.dat
    mv ysos_sed.dat CHA_II_ysos_sed.dat
    mv ysos_tracer.dat CHA_II_ysos_tracer.dat
    mv ysos_Q.dat CHA_II_ysos_Q.dat
    echo "CHA_II done."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    mv gala_coord.dat OPH_gala_coord.dat
    mv gala_sed.dat OPH_gala_sed.dat
    mv gala_tracer.dat OPH_gala_tracer.dat
    mv gala_Q.dat OPH_gala_Q.dat
    mv star_coord.dat OPH_star_coord.dat
    mv star_sed.dat OPH_star_sed.dat
    mv star_tracer.dat OPH_star_tracer.dat
    mv star_Q.dat OPH_star_Q.dat
    mv ysos_coord.dat OPH_ysos_coord.dat
    mv ysos_sed.dat OPH_ysos_sed.dat
    mv ysos_tracer.dat OPH_ysos_tracer.dat
    mv ysos_Q.dat OPH_ysos_Q.dat
    echo "OPH done."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    mv star_coord.dat ELAIS_N1_star_coord.dat
    mv star_sed.dat ELAIS_N1_star_sed.dat
    mv star_tracer.dat ELAIS_N1_star_tracer.dat
    mv star_Q.dat ELAIS_N1_star_Q.dat
    mv gala_coord.dat ELAIS_N1_gala_coord.dat
    mv gala_sed.dat ELAIS_N1_gala_sed.dat
    mv gala_tracer.dat ELAIS_N1_gala_tracer.dat
    mv gala_Q.dat ELAIS_N1_gala_Q.dat
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
    cat ELAIS_N1_star_coord.dat OPH_star_coord.dat CHA_II_star_coord.dat > star_coord.dat
    cat ELAIS_N1_gala_coord.dat OPH_gala_coord.dat CHA_II_gala_coord.dat > gala_coord.dat
    cat OPH_ysos_coord.dat CHA_II_ysos_coord.dat > ysos_coord.dat
    cat ELAIS_N1_star_tracer.dat OPH_star_tracer.dat CHA_II_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat OPH_gala_tracer.dat CHA_II_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat CHA_II_ysos_tracer.dat > ysos_tracer.dat
    cat ELAIS_N1_star_Q.dat OPH_star_Q.dat CHA_II_star_Q.dat > star_Q.dat
    cat ELAIS_N1_gala_Q.dat OPH_gala_Q.dat CHA_II_gala_Q.dat > gala_Q.dat
    cat OPH_ysos_Q.dat CHA_II_ysos_Q.dat > ysos_Q.dat
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
    mv star_Q.dat CHA_II_star_Q.dat
    mv gala_coord.dat CHA_II_gala_coord.dat
    mv gala_sed.dat CHA_II_gala_sed.dat
    mv gala_tracer.dat CHA_II_gala_tracer.dat
    mv gala_Q.dat CHA_II_gala_Q.dat
    mv ysos_coord.dat CHA_II_ysos_coord.dat
    mv ysos_sed.dat CHA_II_ysos_sed.dat
    mv ysos_tracer.dat CHA_II_ysos_tracer.dat
    mv ysos_Q.dat CHA_II_ysos_Q.dat
    echo "CHA_II done."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    mv gala_coord.dat OPH_gala_coord.dat
    mv gala_sed.dat OPH_gala_sed.dat
    mv gala_tracer.dat OPH_gala_tracer.dat
    mv gala_Q.dat OPH_gala_Q.dat
    mv star_coord.dat OPH_star_coord.dat
    mv star_sed.dat OPH_star_sed.dat
    mv star_tracer.dat OPH_star_tracer.dat
    mv star_Q.dat OPH_star_Q.dat
    mv ysos_coord.dat OPH_ysos_coord.dat
    mv ysos_sed.dat OPH_ysos_sed.dat
    mv ysos_tracer.dat OPH_ysos_tracer.dat
    mv ysos_Q.dat OPH_ysos_Q.dat
    echo "OPH done."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    mv star_coord.dat ELAIS_N1_star_coord.dat
    mv star_sed.dat ELAIS_N1_star_sed.dat
    mv star_tracer.dat ELAIS_N1_star_tracer.dat
    mv star_Q.dat ELAIS_N1_star_Q.dat
    mv gala_coord.dat ELAIS_N1_gala_coord.dat
    mv gala_sed.dat ELAIS_N1_gala_sed.dat
    mv gala_tracer.dat ELAIS_N1_gala_tracer.dat
    mv gala_Q.dat ELAIS_N1_gala_Q.dat
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
    calculate_extinction.py ELAIS_N1_star_coord.dat ELAIS_N1_star_sed_twomass_mag.txt ELAIS_N1_star_sed_err_twomass_mag.txt WD55B 4.5
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
    remove_Av.py ukidss ELAIS_N1_star_emap_270arcsec.txt ELAIS_N1_star_sed_u.txt ELAIS_N1_star_Av.dat ELAIS_N1_star_coord.dat
    remove_Av.py ukidss ELAIS_N1_star_emap_270arcsec.txt ELAIS_N1_gala_sed_u.txt skip ELAIS_N1_gala_coord.dat
    echo "ELAIS N1 done."
    # stack all data
    echo "Stack all data"
    cat ELAIS_N1_star_sed_u_intrinsic.txt OPH_star_sed_u_intrinsic.txt CHA_II_star_sed_u_intrinsic.txt > star_sed_u_intrinsic.txt
    cat ELAIS_N1_gala_sed_u_intrinsic.txt OPH_gala_sed_u_intrinsic.txt CHA_II_gala_sed_u_intrinsic.txt > gala_sed_u_intrinsic.txt
    cat OPH_ysos_sed_u_intrinsic.txt CHA_II_ysos_sed_u_intrinsic.txt > ysos_sed_u_intrinsic.txt
    cat ELAIS_N1_star_coord.dat OPH_star_coord.dat CHA_II_star_coord.dat > star_coord.dat
    cat ELAIS_N1_gala_coord.dat OPH_gala_coord.dat CHA_II_gala_coord.dat > gala_coord.dat
    cat OPH_ysos_coord.dat CHA_II_ysos_coord.dat > ysos_coord.dat
    cat ELAIS_N1_star_tracer.dat OPH_star_tracer.dat CHA_II_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat OPH_gala_tracer.dat CHA_II_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat CHA_II_ysos_tracer.dat > ysos_tracer.dat
    cat ELAIS_N1_star_Q.dat OPH_star_Q.dat CHA_II_star_Q.dat > star_Q.dat
    cat ELAIS_N1_gala_Q.dat OPH_gala_Q.dat CHA_II_gala_Q.dat > gala_Q.dat
    cat OPH_ysos_Q.dat CHA_II_ysos_Q.dat > ysos_Q.dat
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
    mv star_Q.dat CHA_II_star_Q.dat
    mv gala_coord.dat CHA_II_gala_coord.dat
    mv gala_sed.dat CHA_II_gala_sed.dat
    mv gala_tracer.dat CHA_II_gala_tracer.dat
    mv gala_Q.dat CHA_II_gala_Q.dat
    mv ysos_coord.dat CHA_II_ysos_coord.dat
    mv ysos_sed.dat CHA_II_ysos_sed.dat
    mv ysos_tracer.dat CHA_II_ysos_tracer.dat
    mv ysos_Q.dat CHA_II_ysos_Q.dat
    echo "CHA_II done."
    get_catalog.sh catalog-OPH-HREL.tbl star
    get_catalog.sh catalog-OPH-HREL.tbl galaxy
    get_catalog.sh catalog-OPH-HREL.tbl yso
    mv gala_coord.dat OPH_gala_coord.dat
    mv gala_sed.dat OPH_gala_sed.dat
    mv gala_tracer.dat OPH_gala_tracer.dat
    mv gala_Q.dat OPH_gala_Q.dat
    mv star_coord.dat OPH_star_coord.dat
    mv star_sed.dat OPH_star_sed.dat
    mv star_tracer.dat OPH_star_tracer.dat
    mv star_Q.dat OPH_star_Q.dat
    mv ysos_coord.dat OPH_ysos_coord.dat
    mv ysos_sed.dat OPH_ysos_sed.dat
    mv ysos_tracer.dat OPH_ysos_tracer.dat
    mv ysos_Q.dat OPH_ysos_Q.dat
    echo "OPH done."
    get_catalog_data_A.sh star
    get_catalog_data_A.sh galaxy
    mv star_coord.dat ELAIS_N1_star_coord.dat
    mv star_sed.dat ELAIS_N1_star_sed.dat
    mv star_tracer.dat ELAIS_N1_star_tracer.dat
    mv star_Q.dat ELAIS_N1_star_Q.dat
    mv gala_coord.dat ELAIS_N1_gala_coord.dat
    mv gala_sed.dat ELAIS_N1_gala_sed.dat
    mv gala_tracer.dat ELAIS_N1_gala_tracer.dat
    mv gala_Q.dat ELAIS_N1_gala_Q.dat
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
    cat ELAIS_N1_star_coord.dat OPH_star_coord.dat CHA_II_star_coord.dat > star_coord.dat
    cat ELAIS_N1_gala_coord.dat OPH_gala_coord.dat CHA_II_gala_coord.dat > gala_coord.dat
    cat OPH_ysos_coord.dat CHA_II_ysos_coord.dat > ysos_coord.dat
    cat ELAIS_N1_star_tracer.dat OPH_star_tracer.dat CHA_II_star_tracer.dat > star_tracer.dat
    cat ELAIS_N1_gala_tracer.dat OPH_gala_tracer.dat CHA_II_gala_tracer.dat > gala_tracer.dat
    cat OPH_ysos_tracer.dat CHA_II_ysos_tracer.dat > ysos_tracer.dat
    cat ELAIS_N1_star_Q.dat OPH_star_Q.dat CHA_II_star_Q.dat > star_Q.dat
    cat ELAIS_N1_gala_Q.dat OPH_gala_Q.dat CHA_II_gala_Q.dat > gala_Q.dat
    cat OPH_ysos_Q.dat CHA_II_ysos_Q.dat > ysos_Q.dat
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
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 4.5
    echo "done."
    # Do extinction correction with extinction map
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_270arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_270arcsec.txt gala_sed_u.txt skip gala_coord.dat
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
    calculate_extinction.py star_coord.dat star_sed_twomass_mag.txt star_sed_err_twomass_mag.txt WD55B 4.5
    echo "done."
    # Do extinction correction with extinction map
    echo "Do extinction correction with extinction map."
    remove_Av.py ukidss star_emap_270arcsec.txt star_sed_u.txt star_Av.dat star_coord.dat
    remove_Av.py ukidss star_emap_270arcsec.txt gala_sed_u.txt skip gala_coord.dat
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


if [ "${option}" = "SERu_slct" ]; then
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
    # Select sources with the extinction correction.
    echo "Select sources with the extinction correction"
    select_data.py filter star_sed_u.txt ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_sed_u.txt ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_sed_u.txt ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_coord.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_coord.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_coord.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_tracer.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_tracer.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_tracer.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
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

if [ "${option}" = "PERu_slctEC" ]; then
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
    echo 'done.'
    # Select sources with the extinction correction.
    echo "Select sources with the extinction correction"
    select_data.py filter star_sed_u_u.txt ../prototype_EC/star_sed_u_u_index_of_no_Av.txt
    select_data.py filter gala_sed_u_u.txt ../prototype_EC/gala_sed_u_u_index_of_no_Av.txt
    select_data.py filter ysos_sed_u_u.txt ../prototype_EC/ysos_sed_u_u_index_of_no_Av.txt
    select_data.py filter star_coord.dat ../prototype_EC/star_sed_u_u_index_of_no_Av.txt
    select_data.py filter gala_coord.dat ../prototype_EC/gala_sed_u_u_index_of_no_Av.txt
    select_data.py filter ysos_coord.dat ../prototype_EC/ysos_sed_u_u_index_of_no_Av.txt
    select_data.py filter star_tracer.dat ../prototype_EC/star_sed_u_u_index_of_no_Av.txt
    select_data.py filter gala_tracer.dat ../prototype_EC/gala_sed_u_u_index_of_no_Av.txt
    select_data.py filter ysos_tracer.dat ../prototype_EC/ysos_sed_u_u_index_of_no_Av.txt
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

if [ "${option}" = "CHA_II_slctEC" ]; then
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
    # Select sources with the extinction correction.
    echo "Select sources with the extinction correction"
    select_data.py filter star_sed_u.txt ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_sed_u.txt ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_sed_u.txt ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_coord.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_coord.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_coord.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_tracer.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_tracer.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_tracer.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
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

if [ "${option}" = "LUP_I_slctEC" ]; then
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
    # Select sources with the extinction correction.
    echo "Select sources with the extinction correction"
    select_data.py filter star_sed_u.txt ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_sed_u.txt ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_sed_u.txt ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_coord.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_coord.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_coord.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_tracer.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_tracer.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_tracer.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
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

if [ "${option}" = "LUP_III_slctEC" ]; then
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
    # Select sources with the extinction correction.
    echo "Select sources with the extinction correction"
    select_data.py filter star_sed_u.txt ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_sed_u.txt ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_sed_u.txt ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_coord.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_coord.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_coord.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_tracer.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_tracer.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_tracer.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
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

if [ "${option}" = "LUP_IV_slctEC" ]; then
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
    # Select sources with the extinction correction.
    echo "Select sources with the extinction correction"
    select_data.py filter star_sed_u.txt ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_sed_u.txt ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_sed_u.txt ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_coord.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_coord.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_coord.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
    select_data.py filter star_tracer.dat ../prototype_EC/star_sed_u_index_of_no_Av.txt
    select_data.py filter gala_tracer.dat ../prototype_EC/gala_sed_u_index_of_no_Av.txt
    select_data.py filter ysos_tracer.dat ../prototype_EC/ysos_sed_u_index_of_no_Av.txt
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
echo "Available options: ${available_sources}"
exit 1
