#!/usr/bin/python3
'''
Abstract:
    This is a program for plotting the color color diagram of given sources. 
    So far it is only available for sptizer
Usage:
    cc_diag.py [option ccdiag] [Sp] [Q] [spitzer sed]
    option ccdiag: The file describe the options.
    Sp: source type
    spitzer sed: the SED of spitzer observation.
Output:
    1. The plot of color-color diagram 
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20190623
####################################
update log
20190623 version alpha 1
    1. The code works.
'''
import time
import numpy as np
from sys import argv
import convert_lib
from convert_JHK_from_twomass_to_ukidss import mjy_to_mag
from matplotlib import pyplot as plt
from input_lib import option_ccdiag
from functools import reduce

class band_manager():
    def __init__(self, band_name):
        if band_name == 'N':
            self.mag = np.zeros((len(sed_array), 2))
            self.index_detected = np.arange(len(sed_array))
        elif band_name == 'max':
            band_col = np.argmax(sed_array[:,:5], axis = 1)
            band_col_flux = np.array(list(enumerate(band_col)))
            band_col_err = np.array(list(enumerate(band_col+8)))
            flux = np.transpose(np.array([  sed_array[band_col_flux[:,0], band_col_flux[:,1]], 
                                            sed_array[band_col_err[:,0], band_col_err[:,1]]]))
            # Warning!!!!!!!!!!!!
            # That could not be band_3
            self.mag = mjy_to_mag(flux, band_name_3, SCAO_system)
            self.index_detected = np.where(Q_array[band_col_flux[:,0], band_col_flux[:,1]] != 'U')[0]
        else:
            band_col = np.where(SCAO_bands == band_name)[0][0]
            flux = np.transpose(np.array([sed_array[:,band_col], sed_array[:,band_col+8]]))
            self.mag = mjy_to_mag(flux, band_name, SCAO_system)
            self.index_detected = np.where(Q_array[:,band_col] != 'U')[0]
        return


#--------------------------------------------
# Main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    stu = option_ccdiag()
    if len(argv) != 5:
        print ("The number of arguments is wrong.")
        print ("Usage: cc_diag.py [option ccdiag] [Sp] [Q] [spitzer sed]")
        print ("Please check the option file before run it.")
        stu.create()
        exit(1)
    option_file_name = argv[1]
    source_type_filename = argv[2]
    Q_filename = argv[3]
    sed_filename = argv[4]
    band_name_1, band_name_2, band_name_3, band_name_4 = stu.load(option_file_name)
    print ('The plot is {0} - {1} vs. {2} - {3}'.format(band_name_3,
                                                        band_name_4,
                                                        band_name_1, 
                                                        band_name_2))
    #-----------------------------------
    # Initialize
    SCAO_bands =np.array([  'J', 
                            'H', 
                            'K', 
                            'IR1', 
                            'IR2', 
                            'IR3', 
                            'IR4',
                            'MP1'])
    SCAO_system = convert_lib.set_SCAO()
    #-----------------------------------
    # Load SED flux data from files.
    source_type_array = np.loadtxt(source_type_filename)
    source_type = np.argmax(source_type_array, axis = 1)
    Q_array = np.loadtxt(Q_filename, dtype = str)
    sed_array = np.loadtxt(sed_filename)
    #-----------------------------------
    # Convert from flux to mag
    band_1 = band_manager(band_name_1)
    band_2 = band_manager(band_name_2)
    band_3 = band_manager(band_name_3)
    band_4 = band_manager(band_name_4)
    mag_1 = band_1.mag
    mag_2 = band_2.mag
    mag_3 = band_3.mag
    mag_4 = band_4.mag
    index_detected_1 = band_1.index_detected
    index_detected_2 = band_2.index_detected
    index_detected_3 = band_3.index_detected
    index_detected_4 = band_4.index_detected
    index_detected_all = reduce(np.intersect1d,(index_detected_1,
                                                index_detected_2,
                                                index_detected_3,
                                                index_detected_4))
    # Select only detected sources.
    color_1 = mag_1[:,0] - mag_2[:,0]
    color_2 = mag_3[:,0] - mag_4[:,0]
    # Denote the source with source types
    index_star = np.where(source_type == 0)[0]
    index_star_detected = np.intersect1d(index_star, index_detected_all)
    index_gala = np.where(source_type == 1)[0]
    index_gala_detected = np.intersect1d(index_gala, index_detected_all)
    index_ysos = np.where(source_type == 2)[0]
    index_ysos_detected = np.intersect1d(index_ysos, index_detected_all)
    # Plot the result
    plt.scatter(color_1[index_star_detected],
                color_2[index_star_detected], 
                color = 'gray',
                s = 2,
                label = 'star')
    plt.scatter(color_1[index_gala_detected],
                color_2[index_gala_detected], 
                color = 'b',
                s = 2,
                label = 'galaxy')
    plt.scatter(color_1[index_ysos_detected],
                color_2[index_ysos_detected], 
                color = 'g',
                s = 2,
                label = 'YSO')
    plt.xlabel('{0} - {1}'.format(band_name_1, band_name_2))
    plt.ylabel('{0} - {1}'.format(band_name_3, band_name_4))
    #plt.gca().invert_yaxis()
    #plt.xlim(-1, 4)
    #plt.ylim(-5, 6)
    plt.legend()
    # Name the result plot
    if band_name_2 == 'N':
        x_name = band_name_1
    else:
        x_name = '{0}-{1}'.format(band_name_1, band_name_2)

    if band_name_4 == 'N':
        y_name = band_name_3
    else:
        y_name = '{0}-{1}'.format(band_name_3, band_name_4)
        
    plt.savefig('cc_diag_{0}_vs_{1}.png'.format(y_name,
                                                x_name))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
