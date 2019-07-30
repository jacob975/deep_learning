#!/usr/bin/python3
'''
Abstract:
    This is a program to convert .dat files to npy files
Usage:
    dat2npy.py [option file] [file name 1] [file name 2] [file name 3] ...
    
    [option file]:
        All setting is saved in there.
        Please check before execution.
    [file name]:
        The file you want to processed.
        The first will be labeded as 0, the second will be labeded as 1, so as on.
Example:

    You have a data file "Toy.dat", "Toy2.dat", and "Toy3.dat"

    Then, do this cmd.
    $ dat2npy.py
    the option file will give to you
    $ dat2npy.py [option files] Toy1.dat Toy2.dat Toy3.dat

Editor:
    Jacob975

20180123
####################################
update log
20180123 version alpha 1
    Now it works, the code can convert both source and label into tensorflow readable
20180124 version alpha 2
    1. Now feature, you can choose processing label or data by argv.
    2. Now the data will be normalized.
20180301 version alpha 3
    1. You can choose how many zero will be tolerated.
20180306 version alpha 4
    1. no argv for data mod and label mod anymore, for replacement, the code will generate label with data process.
    2. now you can process a sequence of data with label in order.
20180320 version alpha 5 
    1. add a tracer to dat data set
20180322 version alpha 6
    1. rename tracer
20180323 version alpha 7:
    1. rearrange the tracer
20180414 version alpha 8:
    1. denote no-observation as -9.99+e02
    2. rename func nozero_filter as no_observation_filter
20180415 version alpha 9:
    1. denote no-observation as 0 instead of -9.99+e02, if you need -9.99e+02, please use dat2npy_const.py
20180430 version alpha 10:
    1. This program become a prototype
    2. the default setting of no observation and no detections is 0, 0
20180530 version alpha 11:
    1. add a new func to save coord infomations
20180531 version alpha 12:
    1. all dat2npy programs are collected into the ensemble version
20180912 version alpha 13:
    1. Update the mask system, using a series of number represent the mask instead of key words.
20181031 version alpha 14:
    1. Update the description in the header.
20181113 version alpha 15:
    1. All arguments now are save in a file.
20181118 version alpha 16:
    1. Add quality flag
20181220 version alpha 17:
    1. Add Av tracking
'''
import time
import re           # this is used to apply multiple spliting
import numpy as np
from sys import argv
from dat2npy_lib import mask, normalize, no_observation_filter_eq_0, read_well_known_data, select_high_flux_error_correlated_source
from input_lib import option_dat2npy as option_files

def SEDname2other_name(name_dat_file, keyword, subtitle):
    position = name_dat_file.find(keyword)
    if position >= 0:
        new_name = '{0}{1}_{2}.dat'.format(name_dat_file[:position], keyword, subtitle)
        print (new_name)
        return 0, new_name
    return 1, ''

#--------------------------------------------
# main code
if __name__ == "__main__":
    VERBOSE = 0
    # measure times
    start_time = time.time()
    # initialize
    option_file = option_files()
    #----------------------------------
    # Check and load argv
    if len(argv) < 3:
        print ("Error! The number of argument is wrong")
        print ("Usage: dat2npy_ensemble.py [option file] [dat files]")
        print ("Please write down the options in option_dat2npy.txt before execution.")
        option_file.create()
        exit()
    option_file_name = argv[1]
    data_name_list = argv[2:]
    mask_code, \
    number_of_lost, \
    do_normalization, \
    consider_error, \
    high_flux_error_correlation, \
    upperlimit_num_sources, \
    do_extinction, \
    do_HL2013 = option_file.load(option_file_name)
    
    number_of_lost = int(number_of_lost)
    print ('mask code: {0}'.format(mask_code))
    print ('number_of_lost: {0}'.format(number_of_lost))
    print ('do normalization: {0}'.format(do_normalization))
    print ('consider error: {0}'.format(consider_error))
    print ("data to be processed: {0}".format(data_name_list))
    #-----------------------------------
    # how many element in a data vector
    data_width = 16
    if consider_error == 'yes':
        data_width = 16
    elif consider_error == 'no':
        data_width = 8
    # Load data, label, tracer, quality flag, and coordinate
    sum_data = [[] for x in range(data_width)]
    sum_label = [[] for x in range(data_width)]
    sum_tracer = [[] for x in range(data_width)]
    sum_coord = [[] for x in range(data_width)]
    sum_quality = [[] for x in range(data_width)]
    sum_Av = [[] for x in range(data_width)]
    sum_HL2013 = [[] for x in range(data_width)]
    num_sources = np.zeros((data_width, len(data_name_list)), dtype = int)
    for ind, data_name in enumerate(data_name_list, start = 0):
        print ("##############################")
        print ("data name = {0}".format(data_name))
        print ("label = {0}".format(ind))
        # Load data
        str_data = read_well_known_data(data_name)
        # Load tracer, coord, Q flag, and Av table.
        keywords = ['star', 'gala', 'ysos']
        name_tracer = ''
        name_coord = ''
        name_quality = ''
        name_Av = ''
        name_HL2013 = '' 
        for key in keywords:
            # Tracer
            failure, tmp_name_tracer = SEDname2other_name(data_name, key, 'tracer')
            if not failure:
                name_tracer = tmp_name_tracer
            # Coordinate
            failure, tmp_name_coord = SEDname2other_name(data_name, key, 'coord')
            if not failure:
                name_coord = tmp_name_coord
            # Q flag
            failure, tmp_name_quality =  SEDname2other_name(data_name, key, 'Q')
            if not failure:
                name_quality = tmp_name_quality
            # Av
            if do_extinction == 'yes': 
                failure, tmp_name_Av = SEDname2other_name(data_name, key, 'Av') 
                if not failure:
                    name_Av = tmp_name_Av
            # HL 2013
            if do_HL2013 == 'yes':
                failure, tmp_name_HL2013 = SEDname2other_name(data_name, key, 'HL2013_label')
                if not failure:
                    name_HL2013 = tmp_name_HL2013
        tracer = np.loadtxt(name_tracer, dtype = object)
        coord = np.loadtxt(name_coord)
        quality = np.loadtxt(name_quality, dtype = str)
        extinction = None
        if do_extinction == 'yes': extinction = np.loadtxt(name_Av)
        if do_HL2013 == 'yes': HL2013 = np.loadtxt(name_HL2013)
        # Convert the format from str to float
        data = np.array(str_data, dtype = float)
        # Mask low flux error correlated sources.
        if high_flux_error_correlation == 'yes':
            exclusion = select_high_flux_error_correlated_source(data)
            data = data[~exclusion]
            tracer = tracer[~exclusion]
            coord = coord[~exclusion]
            quality = quality[~exclusion]
            if do_extinction == 'yes': extinction = extinction[~exclusion]
            if do_HL2013 == 'yes': HL2013 = HL2013[~exclusion]
        # Mask specified bands
        data_n = mask(data, mask_code)
        # Mask error or not
        if consider_error == 'no':
            data_n = data_n[:,:8]
        # Do normalization
        if do_normalization == 'yes':
            data_n = normalize(data_n)
        elif do_normalization == 'no':
            pass 
        # remove all nan value
        nan_filter = np.isnan(data_n[:,0])
        data_n = data_n[~nan_filter]
        tracer = tracer[~nan_filter]
        coord  = coord[~nan_filter]
        quality = quality[~nan_filter]
        if do_extinction == 'yes': extinction = extinction[~nan_filter]
        if do_HL2013 == 'yes': HL2013 = HL2013[~nan_filter]
        # no observation filter
        # i is the tolarence of loss in a single datum
        for i in range(data_width):
            data_n_z, _filter= no_observation_filter_eq_0(data_n, i, data_width)
            tracer_outp = np.where(_filter == 1.0)
            coord_outp = coord[_filter]
            quality_outp = quality[_filter]
            extinction_outp = None
            HL2013_outp = None
            if do_extinction == 'yes': extinction_outp = extinction[_filter]
            if do_HL2013 == 'yes': HL2013_outp = HL2013[_filter]
            num_sources[i, ind] = len(data_n_z)
            print ("MaxLoss = {0}, number of data = {1}".format(i, len(data_n_z)))
            # Generate labels
            label_z = np.array([ind for x in range(len(data_n_z)) ])
            label_z_f = [[0 for k in range(3)] for j in range(len(label_z))]
            for u in range(len(label_z_f)):
                label_z_f[u][int(label_z[u])] = 1
            #-----------------------------------------------------
            # stack them
            sum_data[i] = np.append(sum_data[i], data_n_z)
            sum_label[i] = np.append(sum_label[i], label_z_f)
            sum_tracer[i] = np.append(sum_tracer[i], tracer_outp)
            sum_quality[i] = np.append(sum_quality[i], quality_outp)
            sum_coord[i] = np.append(sum_coord[i], coord_outp)
            if do_extinction == 'yes': sum_Av[i] = np.append(sum_Av[i], extinction_outp)
            if do_HL2013 == 'yes': sum_HL2013[i] = np.append(sum_HL2013[i], HL2013_outp)
            #-----------------------------------------------------
    # save data, number of sources in different selection, label, tracer, and coordinate
    print ("###############################")
    print ("save data, label, tracer, quality flag, and coordinate")
    np.savetxt("num_sources.txt", num_sources, fmt = '%d', header = "Star Gala YSOs")
    for i in range(data_width):
        # reshape the data because np.append smooth the array.
        sum_data[i] = np.reshape(sum_data[i], (-1, data_width))
        sum_label[i] = np.reshape(sum_label[i], (-1, 3))
        sum_coord[i] = np.reshape(sum_coord[i], (-1, 2))
        sum_quality[i] = np.reshape(sum_quality[i], (-1,8))
        if do_extinction == 'yes': sum_Av[i] = np.reshape(sum_Av[i], (-1, 2))
        if int(upperlimit_num_sources) != 0 and int(upperlimit_num_sources) < len(sum_data[i]):
            randomize = np.arange(len(sum_data[i]))
            np.random.shuffle(randomize)
            sum_data[i] = sum_data[i][randomize[:int(upperlimit_num_sources)]]
            sum_label[i] = sum_label[i][randomize[:int(upperlimit_num_sources)]]
            sum_coord[i] = sum_coord[i][randomize[:int(upperlimit_num_sources)]]
            sum_tracer[i] = sum_tracer[i][randomize[:int(upperlimit_num_sources)]]
            sum_quality[i] = sum_quality[i][randomize[:int(upperlimit_num_sources)]]
            if do_extinction == 'yes': sum_Av[i] = sum_Av[i][randomize[:int(upperlimit_num_sources)]]
            if do_HL2013 == 'yes': sum_HL2013[i] = sum_HL2013[i][randomize[:int(upperlimit_num_sources)]]
        print ("number of data with MaxLoss {0} = {1}".format(i, len(sum_data[i])))
        if i == number_of_lost:
            np.savetxt("source_sed_MaxLoss{0}.txt".format(i), sum_data[i])
            np.savetxt("source_id_MaxLoss{0}.txt".format(i), sum_label[i])
            np.savetxt("source_tracer_MaxLoss{0}.txt".format(i), sum_tracer[i], fmt = '%s')
            np.savetxt("source_Q_MaxLoss{0}.txt".format(i), sum_quality[i], fmt ='%s')
            np.savetxt("source_coord_MaxLoss{0}.txt".format(i), sum_coord[i])
            if do_extinction == 'yes': np.savetxt("source_Av_MaxLoss{0}.txt".format(i), sum_Av[i])
            if do_HL2013 == 'yes': np.savetxt("source_HL2013_MaxLoss{0}.txt".format(i), sum_HL2013[i])
    #-----------------------------------
    # measuring time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
