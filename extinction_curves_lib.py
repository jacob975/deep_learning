#!/usr/bin/python3
'''
Abstract:
    This is a program to save the parameters of extinction curves. 
Usage:
    extinction_curves_lib.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180104
####################################
update log
20180813 version alpha 1
    1. The code works    
'''
#----------------------------------------------------
# Milky Way, R_V = 3.1: Weingartner & Draine (2001) 
# Milky Way size distribution for R_V=3.1 with C/H = b_C = 60 ppm in log-normal size dists.
# For 2MASS, IRAC, and MIPS
#       [      index of index of       ]
#       [band ,flux    ,err_flux, C_av ]
WD_31B=[['J'  ,0       ,8       ,0.2939],
        ['H'  ,1       ,9       ,0.1847],
        ['K'  ,2       ,10      ,0.1193],
        ['IR1',3       ,11      ,0.0462],
        ['IR2',4       ,12      ,0.0301],
        ['IR3',5       ,13      ,0.0200],
        ['IR4',6       ,14      ,0.0302],
        ['MP1',7       ,15      ,0.0195]]
#----------------------------------------------------
# Milky Way, R_V = 5.5: Weingartner & Draine (2001)
# Milky Way size distribution "B" for R_V=5.5 with C/H = b_C = 30 ppm in log-normal size dists.
# For 2MASS, IRAC, and MIPS
#               [      index of index of       ]
#               [band ,flux    ,err_flux, C_av ]
WD_55B_twomass=[['J'  ,0       ,8       ,0.2738],
                ['H'  ,1       ,9       ,0.1619],
                ['K'  ,2       ,10      ,0.1117],
                ['IR1',3       ,11      ,0.0660],
                ['IR2',4       ,12      ,0.0541],
                ['IR3',5       ,13      ,0.0441],
                ['IR4',6       ,14      ,0.0502],
                ['MP1',7       ,15      ,0.0258]]
#----------------------------------------------------
# Milky Way, R_V = 5.5: Weingartner & Draine (2001)
# Milky Way size distribution "B" for R_V=5.5 with C/H = b_C = 30 ppm in log-normal size dists.
# For 2MASS, IRAC, and MIPS
#              [      index of index of       ]
#              [band ,flux    ,err_flux, C_av ]
WD_55B_ukidss=[['J'  ,0       ,8       ,0.2683],
               ['H'  ,1       ,9       ,0.1670],
               ['K'  ,2       ,10      ,0.1093],
               ['IR1',3       ,11      ,0.0660],
               ['IR2',4       ,12      ,0.0541],
               ['IR3',5       ,13      ,0.0441],
               ['IR4',6       ,14      ,0.0502],
               ['MP1',7       ,15      ,0.0258]]
#----------------------------------------------------
# From TH Heish in zeus
# /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/Old/New_version/calculate_distance_and_Remove_Av.py
# For 2MASS, IRAC, and MIPS
#              [      index of index of       ]
#              [band ,flux    ,err_flux, C_av ]
THHeish_WD_55=[['J'  ,0       ,8       ,0.2741],
               ['H'  ,1       ,9       ,0.1622],
               ['K'  ,2       ,10      ,0.1119],
               ['IR1',3       ,11      ,0.0671],
               ['IR2',4       ,12      ,0.0543],
               ['IR3',5       ,13      ,0.0444],
               ['IR4',6       ,14      ,0.0463],
               ['MP1',7       ,15      ,0.0259]]
