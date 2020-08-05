#!/usr/bin/python3
'''
Abstract:
    This is a program for plotting the color-color diagram for given sources.
Usage:
    plot_ccdiag.py [band index 1] [band index 2] [sed table] [cls table]
    The band index can be like: f8, c67.
    The first char indicate this is a flux or color, and the number shows which bands are going to be used.
    c67 means this is a color for band 6 divied by band 7.
Output:
    1. The figure of color-color diagram.
Editor:
    Jacob975
##################################
#   Python3                      #
#   This code is made in python3 #
##################################
20200805
##################1##################
update log
2020085 version alpha 1
    1. The code works.
'''
import time
import numpy as np
from sys import argv
from matplotlib import pyplot as plt
from convert_lib import set_SCAO, mJy_to_mag_noerr

def load_flux_color(band_index, sed_table):
    outp = None
    # For Flux
    if band_index[0] == 'f':
        seq1 = int(band_index[1]) - 1
        flux1 = sed_table[:, seq1]
        mag1 = mJy_to_mag_noerr(
            SCAO_system[bands[seq1]][2],
            flux1
        )
        outp = mag1
        out_name = "{0} (mag)".format(SCAO_system[bands[seq1]][0])
    # FOr Color
    elif band_index[0] == 'c':
        seq1 = int(band_index[1]) - 1
        seq2 = int(band_index[2]) - 1
        flux1 = sed_table[:, seq1]
        flux2 = sed_table[:, seq2]
        mag1 = mJy_to_mag_noerr(
            SCAO_system[bands[seq1]][2],
            flux1
        )
        mag2 = mJy_to_mag_noerr(
            SCAO_system[bands[seq2]][2],
            flux2
        )
        outp = mag1 - mag2
        out_name = "{0} - {1} (mag)".format(
            SCAO_system[bands[seq1]][0],
            SCAO_system[bands[seq2]][0]
        )
    return outp, out_name

def adjust_ax(inp_ax):
    # Adjust the panel
    #inp_ax.set_ylim(-2, 4)
    inp_ax.grid(True)
    inp_ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        direction='in'
    )
    inp_ax.tick_params(
        axis='y',          # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        direction='in'
    )
    inp_ax.set_xlabel(x_name)
    inp_ax.set_ylabel(y_name)
    

#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 5:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_ccdiag.py [band/color index 1] [band/color index 2] [sed table] [cls table]")
        print ("Example: plot_ccdiag.py c67 f8 sed_table.txt")
        exit()
    band_index_1 = argv[1]
    band_index_2 = argv[2]
    sed_table_name = argv[3]
    cls_table_name = argv[4]
    #-----------------------------------
    # Initialize the band system
    SCAO_system = set_SCAO()
    bands = [
        'J', 
        'H', 
        'K', 
        'IR1', 
        'IR2', 
        'IR3', 
        'IR4', 
        'MP1'
    ]
    #-----------------------------------
    # Load data
    print("Load data")
    sed_table = np.loadtxt(sed_table_name)
    cls_table = np.loadtxt(cls_table_name, dtype = int)
    index_star = np.where(cls_table == 0)[0]
    index_gala = np.where(cls_table == 1)[0]
    index_ysos = np.where(cls_table == 2)[0]
    x_data, x_name = load_flux_color(band_index_1, sed_table)
    y_data, y_name = load_flux_color(band_index_2, sed_table)
    #-----------------------------------
    # Plot the color-color diagram
    print("Plot the diagram")
    fig, axes = plt.subplots(
        2, 2,
        sharex = True,
        sharey = True,
    )
    # 1st panel
    axes[0,0].scatter(
        x_data[index_star], 
        y_data[index_star],
        color = 'b',
        s = 1,
    )
    axes[0,0].scatter(
        x_data[index_gala], 
        y_data[index_gala],
        color = 'g',
        s = 1,
    )
    axes[0,0].scatter(
        x_data[index_ysos], 
        y_data[index_ysos],
        color = 'r',
        s = 1,
    )
    # 2nd panel
    axes[0,1].scatter(
        x_data[index_star], 
        y_data[index_star],
        color = 'b',
        s = 1,
    )
    # 3rd panel
    axes[1,0].scatter(
        x_data[index_gala], 
        y_data[index_gala],
        color = 'g',
        s = 1,
    )
    # 4rd panel
    axes[1,1].scatter(
        x_data[index_ysos], 
        y_data[index_ysos],
        color = 'r',
        s = 1,
    )
    # Adjust the panel
    adjust_ax(axes[0,0])
    adjust_ax(axes[0,1])
    adjust_ax(axes[1,0])
    adjust_ax(axes[1,1])
    plt.savefig("Plot_test.png", dpi = 200)
    plt.close()
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
