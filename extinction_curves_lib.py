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
#       [      index of index of       ]
#       [band ,flux    ,err_flux, C_av ]
WD_31B=[['J'  ,21      ,22      ,0.2939],
        ['H'  ,25      ,26      ,0.1847],
        ['K'  ,29      ,30      ,0.1193],
        ['IR1',41      ,42      ,0.0462],
        ['IR2',59      ,60      ,0.0301],
        ['IR3',77      ,78      ,0.0200],
        ['IR4',95      ,96      ,0.0302],
        ['MP1',113     ,114     ,0.0195]]
#----------------------------------------------------
# Milky Way, R_V = 5.5: Weingartner & Draine (2001)
# Milky Way size distribution "B" for R_V=5.5 with C/H = b_C = 30 ppm in log-normal size dists.
#       [      index of index of       ]
#       [band ,flux    ,err_flux, C_av ]
WD_55B=[['J'  ,21      ,22      ,0.2738],
        ['H'  ,25      ,26      ,0.1619],
        ['K'  ,29      ,30      ,0.1117],
        ['IR1',41      ,42      ,0.0660],
        ['IR2',59      ,60      ,0.0541],
        ['IR3',77      ,78      ,0.0441],
        ['IR4',95      ,96      ,0.0502],
        ['MP1',113     ,114     ,0.0258]]
#----------------------------------------------------
# From TH Heish
#       [      index of index of       ]
#       [band ,flux    ,err_flux, C_av ]
THHeish_WD_55=[['J'  ,21    ,22      ,0.2741],
               ['H'  ,25    ,26      ,0.1622],
               ['K'  ,29    ,30      ,0.1119],
               ['IR1',41    ,42      ,0.0671],
               ['IR2',59    ,60      ,0.0543],
               ['IR3',77    ,78      ,0.0444],
               ['IR4',95    ,96      ,0.0463],
               ['MP1',113   ,114     ,0.0259]]
