#!/usr/bin/python3
'''
Abstract:
    This is a program for plot the signal noise ratio of incorrectly predicted sources.
Usage:
    print_incorrect.py [keyword] [DIR where AI saved]
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181106
####################################
update log
20181106 version alpha 1
    1. the code works
'''
import numpy as np
import time
import os
from sys import argv
from load_lib import load_cls_true, load_labels_pred, load_coords, load_arrangement, confusion_matrix_infos, cross_confusion_matrix_infos
import glob
import matplotlib.pyplot as plt

def find_corresponding_sed(coords, ref_coords, ref_sed):
    sed_corresponding = []
    for coord in coords:
        sed_corresponding.append(ref_sed[ref_coords[:,0] == coord[0]])
    sed_corresponding_array = np.array(sed_corresponding).reshape(-1, 16)
    return sed_corresponding_array

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Check argv
    if len(argv) != 3:
        print ("Error\nUsage: print_incorrect.py [keywords] [DIR where AI saved]")
        print ("Example: print_incorrect.py MaxLoss15 data_A/alice")
        exit()
    # Load arguments
    keyword = argv[1]
    ai_alice = argv[2]
    work_dir = os.getcwd()
    #----------------------------------------
    # Load prediction 1 and true labels
    print ("AI DIR = {0}".format(ai_alice))
    os.chdir(ai_alice)
    data_list = glob.glob("AI*test_on*{0}".format(keyword))
    ensemble_cls_true = None
    ensemble_coords = None
    alice_labels_pred_set = []
    for directory in data_list:
        print ('Loading {0}'.format(directory))
        print ('--- Load tracer of the random generator ---')
        # load tracer
        failure, data, tracer = load_arrangement(keyword, directory)
        print ('--- Load prediction labels---')
        # load label_pred
        failure, labels_pred = load_labels_pred(keyword, directory)
        if not failure:
            temp_labels_pred =  [ value for _,value in sorted(zip(tracer.test, labels_pred))]
            alice_labels_pred_set.append(temp_labels_pred)
        print ('--- Load catalog labels ---')
        # load cls_true
        failure, cls_true = load_cls_true(keyword, directory)
        if not failure:
            if ensemble_cls_true == None:
                ensemble_cls_true = [ value for _,value in sorted(zip(tracer.test, cls_true))]
        print ('--- Load coordinates of sources ---')
        # load coord
        failure, coords = load_coords(keyword, directory)
        if not failure:
            if ensemble_coords == None:
                ensemble_coords = [ value for _,value in sorted(zip(tracer.test, coords.test))]

    alice_labels_pred_set = np.array(alice_labels_pred_set)
    ensemble_coords = np.array(ensemble_coords)
    alice_ensemble_labels_pred = np.mean(alice_labels_pred_set, axis = 0)
    alice_ensemble_cls_pred = np.argmax(alice_ensemble_labels_pred, axis = 1)
    ensemble_cls_true = np.array(ensemble_cls_true)
    alice_infos = confusion_matrix_infos(ensemble_cls_true, alice_ensemble_labels_pred)
    # Pick the coordinates of incorrectly predicted sources.
    index_incorrect_star = np.where((ensemble_cls_true == 0) & (alice_ensemble_cls_pred != 0))
    index_incorrect_gala = np.where((ensemble_cls_true == 1) & (alice_ensemble_cls_pred != 1))
    index_incorrect_ysos = np.where((ensemble_cls_true == 2) & (alice_ensemble_cls_pred != 2))
    coords_incorrect_star = ensemble_coords[index_incorrect_star]
    coords_incorrect_gala = ensemble_coords[index_incorrect_gala]
    coords_incorrect_ysos = ensemble_coords[index_incorrect_ysos]
    os.chdir('..')
    #-----------------------------------
    # Load tables contain original data
    try:
        star_sed_table = np.loadtxt('{0}/star_sed_u_u.txt'.format(ai_alice))
    except:
        star_sed_table = np.loadtxt('{0}/star_sed_u.txt'.format(ai_alice))
    try:
        gala_sed_table = np.loadtxt('{0}/gala_sed_u_u.txt'.format(ai_alice))
    except:
        gala_sed_table = np.loadtxt('{0}/gala_sed_u.txt'.format(ai_alice))
    try:
        ysos_sed_table = np.loadtxt('{0}/ysos_sed_u_u.txt'.format(ai_alice))
    except:
        ysos_sed_table = np.loadtxt('{0}/ysos_sed_u.txt'.format(ai_alice))
    star_coord_table = np.loadtxt('{0}/star_coord.dat'.format(ai_alice))
    gala_coord_table = np.loadtxt('{0}/gala_coord.dat'.format(ai_alice))
    ysos_coord_table = np.loadtxt('{0}/ysos_coord.dat'.format(ai_alice))
    # Find the corresponding sed via matching coordinates.
    sed_incorrect_star = find_corresponding_sed(coords_incorrect_star, star_coord_table, star_sed_table)
    sed_incorrect_gala = find_corresponding_sed(coords_incorrect_gala, gala_coord_table, gala_sed_table)
    sed_incorrect_ysos = find_corresponding_sed(coords_incorrect_ysos, ysos_coord_table, ysos_sed_table)
    sed_tables = [sed_incorrect_star, sed_incorrect_gala, sed_incorrect_ysos]
    label_name = ['star', 'gala', 'ysos']
    band_name = ['J', 'H', 'K', 'IRAC1', 'IRAC2', 'IRAC3', 'IRAC4', 'MIPS1']
    ratio = [0, 0, 0, 0.047, 0.047, 0.047, 0.047, 0.095]
    #-----------------------------------
    # Plot the ratio
    for i in range(len(sed_tables)):
        fig, axs = plt.subplots(3, 3, figsize = (12, 12), sharex = 'all', sharey = 'all')
        plt.suptitle("{0}_incorrect_{1}".format(ai_alice, label_name[i]), fontsize=28)
        axs = axs.ravel()
        for j in range(len(sed_tables[i][0])//2):
            axs[j].set_title(band_name[j])
            axs[j].set_ylabel('uncertainties(mJy)')
            axs[j].set_xlabel('flux(mJy)')
            axs[j].grid(True)
            axs[j].set_yscale("log", nonposx='clip')
            axs[j].set_xscale('log', nonposy='clip')
            axs[j].set_ylim(ymin = 1e-3, ymax = 1e4)
            axs[j].set_xlim(xmin = 1e-3, xmax = 1e4)
            axs[j].scatter(sed_tables[i][:,j], sed_tables[i][:,j+8], s = 5, marker = '+' )
            if ratio[j] != 0:
                axs[j].plot([0.01, 2000], [0.01*ratio[j], 2000*ratio[j]], 'r-', label = r'$\frac{N}{S}$ = %.4f' % ratio[j])
            axs[j].legend()
        plt.savefig('incorrect_{0}_signal_noise_relation.png'.format(label_name[i]))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
