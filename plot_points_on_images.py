#!/usr/bin/python3
'''
Abstract:
    This is a program to test how to plot points on images
Usage:
    plot_points_on_images.py [name of image] [name of regions file]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180525
####################################
update log
'''
import time
import os
from sys import argv

def plot_point_on_ds9(name_image, name_regions_file):
    # convert region file from XY to ds9/fortran
    cmd =   "ds9 {0}\
            -regions format xy \
            -regions system wcs \
            -regions sky fk5 \
            -regions load {1} \
            -regions select all \
            -regions format ds9 \
            -regions save {2}.reg \
            -exit ".format(name_image, name_regions_file, name_regions_file[:-4])
    os.system(cmd)
    # set boxcircle size 1
    cmd = "sed -i -e 's/boxcircle/boxcircle 2/g' {0}.reg".format(name_regions_file[:-4])
    os.system(cmd)
    # display
    cmd =   "ds9 -zscale {0} \
            -regions format ds9 \
            -regions load {1}.reg \
            -zoom to fit \
            -saveimage png {1}.png&".format(name_image, name_regions_file[:-4])
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
    if len(argv) != 3:
        print ("Error!\nUsage: plot_points_on_images.py [name of image] [name of regions file]")
        exit()
    name_image = argv[1]
    name_regions_file = argv[2]
    # plot points on images
    plot_point_on_ds9(name_image, name_regions_file)
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
