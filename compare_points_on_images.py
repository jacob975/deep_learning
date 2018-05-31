#!/usr/bin/python3
'''
Abstract:
    This is a program to test how to plot points on images
Usage:
    compare_points_on_images.py [name of image] [name of regions file A] [name of regions file B]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180531
####################################
update log
'''
import time
import os
from sys import argv

def compare_point_on_ds9(name_image, name_regions_file_A, name_regions_file_B):
    # convert region file A from XY to ds9/fortran
    cmd =   "ds9 {0}\
            -regions format xy \
            -regions system wcs \
            -regions sky fk5 \
            -regions load {1} \
            -regions select all \
            -regions format ds9 \
            -regions save {2}.reg \
            -exit ".format(name_image, name_regions_file_A, name_regions_file_A[:-4])
    os.system(cmd)
    # set boxcircle size 1
    cmd = "sed -i -e 's/boxcircle/boxcircle 2/g' {0}.reg".format(name_regions_file_A[:-4])
    os.system(cmd)
    # convert region file B from XY to ds9/fortran
    cmd =   "ds9 {0}\
            -regions format xy \
            -regions system wcs \
            -regions sky fk5 \
            -regions load {1} \
            -regions select all \
            -regions format ds9 \
            -regions save {2}.reg \
            -exit ".format(name_image, name_regions_file_B, name_regions_file_B[:-4])
    os.system(cmd)
    # set boxcircle size 1
    cmd = "sed -i -e 's/boxcircle/boxcircle 2/g' {0}.reg".format(name_regions_file_B[:-4])
    os.system(cmd)
    cmd = "sed -i -e 's/green/red/g' {0}.reg".format(name_regions_file_B[:-4])
    os.system(cmd)
    # display
    cmd =   "ds9 -zscale {0} \
            -regions format ds9 \
            -regions load {1}.reg \
            -regions load {2}.reg \
            -zoom to fit &".format(name_image, name_regions_file_A[:-4], name_regions_file_B[:-4])
    os.system(cmd)
    return

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 4:
        print ("Error!\nUsage: compare_points_on_images.py [name of image] [name of regions file A] [name of regions file B]")
        exit()
    name_image = argv[1]
    name_regions_file_A = argv[2]
    name_regions_file_B = argv[3]
    # plot points on images
    compare_point_on_ds9(name_image, name_regions_file_A, name_regions_file_B)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
