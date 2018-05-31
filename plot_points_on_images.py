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
    # using ds9 to display
    cmd =   "ds9 -zscale {0} \
            -regions color red \
            -regions format xy \
            -regions system wcs \
            -regions sky fk5 \
            -regions load {1} \
            -zoom to fit &".format(name_image, name_regions_file)
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