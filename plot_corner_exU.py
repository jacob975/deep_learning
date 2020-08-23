#!/usr/bin/python3
'''
Abstract:
    This is a program for plotting the corner plot of given band index. 
Usage:
    plot_corner_exU.py [band index code] [sed table] [cls table] [Q table]
    e.g. $plot_corner_exU.py 678 sed_table.txt cls_table.txt Q_table.txt
    A corner plot of band 6, 7, and 8 will be returned.
Output:
    1. The figure of corner diagram.
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

def adjust_ax(inp_axes, row_i, col_i):
    # Adjust the panel
    inp_ax = inp_axes[row_i, col_i]
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
        print ("Usage: plot_corner_exU.py [band index code] [sed table] [cls table] [Q table]")
        print ("Example: plot_corner_exU.py 678 sed_table.txt cls_table.txt Q_table.txt")
        exit()
    band_index_code = argv[1]
    sed_table_name = argv[2]
    cls_table_name = argv[3]
    Q_table_name = argv[4]
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
    Q_table = np.loadtxt(Q_table_name, dtype = str)
    index_star = cls_table == 0
    index_gala = cls_table == 1
    index_ysos = cls_table == 2
    # Load sed data
    num_index = len(band_index_code)
    data_index_list = []
    data_list = []
    data_name_list = []
    for c in band_index_code:
        tmp_index = 'f{0}'.format(c)
        tmp_data, tmp_name = load_flux_color(tmp_index, sed_table)
        data_index_list.append(tmp_index)
        data_list.append(tmp_data)
        data_name_list.append(tmp_name)
    #-----------------------------------
    # Plot the color-color diagram
    print("Plot the diagram")
    fig, axes = plt.subplots(
        num_index, num_index,
        figsize = (10,10),
    )
    # Adjust the panel style
    fig.suptitle('Corner plot')
    plt.subplots_adjust(wspace=0, hspace=0)
    band_index_str_list = (list(band_index_code))
    for i in range(num_index):
        for j in range(num_index):
            # Plot the histogram
            if i == j:
                axes[i,j].invert_xaxis() 
                axes[i,j].hist(
                    data_list[i][(index_star) & (Q_table[:,int(band_index_str_list[i])-1] != 'U') ],
                    50,
                    normed = 1,
                    facecolor = "b",
                    edgecolor = 'None',
                    alpha = 0.3,
                    zorder = 100,
                ) 
                axes[i,j].hist(
                    data_list[i][(index_gala) & (Q_table[:,int(band_index_str_list[i])-1] != 'U')],
                    50,
                    normed = 1,
                    facecolor = "g",
                    edgecolor = 'None',
                    alpha = 0.3,
                    zorder = 100,
                ) 
                axes[i,j].hist(
                    data_list[i][(index_ysos) & (Q_table[:,int(band_index_str_list[i])-1] != 'U')],
                    50,
                    normed = 1,
                    facecolor = "r",
                    edgecolor = 'None',
                    alpha = 0.3,
                    zorder = 100,
                )
            # Plot the mag-mag diagram
            elif i > j:
                axes[i,j].invert_xaxis() 
                axes[i,j].invert_yaxis() 
                adjust_ax(axes, i, j)
                axes[i,j].scatter(
                    data_list[j][(index_star) & (Q_table[:,int(band_index_str_list[i])-1] != 'U') & (Q_table[:,int(band_index_str_list[j])-1] != 'U')],
                    data_list[i][(index_star) & (Q_table[:,int(band_index_str_list[i])-1] != 'U') & (Q_table[:,int(band_index_str_list[j])-1] != 'U')], 
                    color = 'b',
                    s = 1,
                )
                axes[i,j].scatter(
                    data_list[j][(index_gala) & (Q_table[:,int(band_index_str_list[i])-1] != 'U') & (Q_table[:,int(band_index_str_list[j])-1] != 'U')],
                    data_list[i][(index_gala) & (Q_table[:,int(band_index_str_list[i])-1] != 'U') & (Q_table[:,int(band_index_str_list[j])-1] != 'U')], 
                    color = 'g',
                    s = 1,
                )
                axes[i,j].scatter(
                    data_list[j][(index_ysos) & (Q_table[:,int(band_index_str_list[i])-1] != 'U') & (Q_table[:,int(band_index_str_list[j])-1] != 'U')],
                    data_list[i][(index_ysos) & (Q_table[:,int(band_index_str_list[i])-1] != 'U') & (Q_table[:,int(band_index_str_list[j])-1] != 'U')], 
                    color = 'r',
                    s = 1,
                )
            elif i < j:
                axes[i,j].set_visible(False)
    # Set labels visibilities
    for i in range(num_index):
        for j in range(num_index):
            if i == len(band_index_code)-1: 
                axes[i,j].set_xlabel(
                    data_name_list[j],
                )
            else:
                axes[i,j].tick_params(axis='x', colors='None')
            if j == 0:
                axes[i,j].set_ylabel(
                    data_name_list[i],
                )
            else:
                axes[i,j].tick_params(axis='y', colors='None')


    plt.savefig(
        "corner_f{0}_exU.png".format(
            band_index_code, 
        ), 
        dpi = 200)
    plt.close()
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
