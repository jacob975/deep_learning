#!/usr/bin/python3
'''
Abstract:
    This is a program for convert units 
    ukirt: mJy, Jy, mag supported
Usage:
    1. Choose a python file you like
    2. Write down "import convert_lib" some where
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180502
####################################
update log
20180502 version alpha 1
    1. the code work
20180531 version alpha 2
    1. add a group of funcs for converting between pixel and wcs
    but they haven't been tested.
20180604 version alpha 3
    1. update the parameter of system.
20190731 verision alpha 4
    1. Add an ensemble convertor from 2mag to Umag.
    2. Add an ensemble convertor from mjy to mag.
    3. Add an ensemble convertor from mag to mjy.
'''
import numpy as np

####################################
from uncertainties import unumpy, ufloat
# How to cite this package
# If you use this package for a publication (in a journal, on the web, etc.), 
# please cite it by including as much information as possible from the following: 
# Uncertainties: a Python package for calculations with uncertainties, Eric O. LEBIGOT, 
# http://pythonhosted.org/uncertainties/. Adding the version number is optional.
####################################


####################################
# Convert quantities between magnitude and Jy
# Those convert function comes from: http://ssc.spitzer.caltech.edu/warmmission/propkit/pet/magtojy/index.html
# Hint: 1 Jy = 1000 mJy
#       Jy is a unit of flux density

# the properties of bands in ukirt
# example key : [band, wavelength, zeropoint]
# 20180604
# I find that band J is inconsistent with 2mass, so I modified the zeropoint of band J.

# This is copy from paper "Hewett, P. C. et al. 2006" 

def set_ukirt():
    # system    key: [name, middle wavelength, F_0]
    ukirt_system = {'u' : ["u", 0.3546, 1545],\
                    'g' : ["g", 0.4670, 3991],\
                    'r' : ["r", 0.6156, 3174],\
                    'i' : ["i", 0.7471, 2593],\
                    'z' : ["z", 0.8918, 2222],\
                    'Z' : ["Z", 0.8817, 2232],\
                    'Y' : ["Y", 1.0305, 2026],\
                    'J' : ["J", 1.2483, 1530],\
                    'H' : ["H", 1.6313, 1019],\
                    'K' : ["K", 2.2010, 631] }
    return ukirt_system

# This is copy from https://www.ipac.caltech.edu/2mass/releases/allsky/doc/sec6_4a.html
def set_twomass():
    # system    key: [name, middle wavelength, F_0]
    twomass_system = {  'J' : ["J", 1.235, 1594],\
                        'H' : ["H", 1.662, 1024],\
                       'Ks' : ["Ks", 2.159, 666.7] }
    return twomass_system

# This is copy from a paper "Wright et al. 2010"
def set_wise():
    # system    key: [name, middle wavelength, F_0]
    wise_system = { 'W1' : ["W1", 3.3526, 306.681],\
                    'W2' : ["W2", 4.6028, 170.663],\
                    'W3' : ["W3", 11.5608,29.0448],\
                    'W4' : ["W4", 22.0883, 8.2839]}
    return wise_system

# This is copy from papers "Reach et al. 2005"(IRAC) 
# and the website https://irsa.ipac.caltech.edu/data/SPITZER/docs/mips/mipsinstrumenthandbook/49/ (MIPS) 
def set_spitzer():
    # system    key: [name, middle wavelength, F_0]
    spitzer_system = {  'IR1': ["IR1", 3.550, 280.9],\
                        'IR2': ["IR2", 4.493, 179.7],\
                        'IR3': ["IR3", 5.731, 115.0],\
                        'IR4': ["IR4", 7.872, 64.13],\
                        'MP1': ["MP1", 23.68, 7.17 ],\
                        'MP2': ["MP2", 71.42, 0.778],\
                        'MP3': ["MP3", 155.9, 0.159],\
                        }
    return spitzer_system

# This is the system describe our SCAO dataset, contains J, H, K from UKIDSS, and  IR1, IR2, IR3, IR4, MP1 from spitzer.
def set_SCAO():
    # system    key: [name, middle wavelength, F_0]
    SCAO_system = { 'J' : ["J", 1.2483, 1530],\
                    'H' : ["H", 1.6313, 1019],\
                    'K' : ["K", 2.2010, 631],\
                    'IR1': ["IR1", 3.550, 280.9],\
                    'IR2': ["IR2", 4.493, 179.7],\
                    'IR3': ["IR3", 5.731, 115.0],\
                    'IR4': ["IR4", 7.872, 64.13],\
                    'MP1': ["MP1", 23.68, 7.17 ],\
                        }
    return SCAO_system
    

def Jy_to_mJy_noerr(flux_density):
    return 1000 * flux_density

def mJy_to_Jy_noerr(flux_density):
    return flux_density / 1000

def mag_to_Jy_noerr(zeropoint, magnitude):
    flux_density = zeropoint * np.power( 10.0, -0.4 * magnitude )
    return flux_density

def Jy_to_mag_noerr(zeropoint, flux_density):
    magnitude = -2.5 * ( np.log(flux_density) - np.log(zeropoint) )/ np.log(10.0)
    return magnitude

def mag_to_mJy_noerr(zeropoint, magnitude):
    flux_density = mag_to_Jy_noerr(zeropoint, magnitude)
    flux_density = Jy_to_mJy_noerr(flux_density)
    return flux_density

def mJy_to_mag_noerr(zeropoint, flux_density):
    flux_density = mJy_to_Jy_noerr(flux_density)
    magnitude = Jy_to_mag_noerr(zeropoint, flux_density)
    return magnitude
#-----------------------------------------------------
# convertion with error

def Jy_to_mJy(flux_density, err_flux_density):
    return 1000 * flux_density, 1000* err_flux_density

def mJy_to_Jy(flux_density, err_flux_density):
    return flux_density / 1000, err_flux_density / 1000

def mag_to_Jy(zeropoint, magnitude, err_magnitude):
    flux_density = zeropoint * np.power( 10.0, -0.4 * magnitude )
    err_flux_density = np.abs(np.divide(err_magnitude * np.log(10.0) * flux_density, 2.5))
    return flux_density, err_flux_density

def Jy_to_mag(zeropoint, flux_density, err_flux_density):
    magnitude = -2.5 * ( np.log(flux_density) - np.log(zeropoint) )/ np.log(10.0)
    err_magnitude = np.abs(np.divide(-2.5 * err_flux_density, flux_density * np.log(10.0))) 
    return magnitude, err_magnitude

def mag_to_mJy(zeropoint, magnitude, err_magnitude):
    flux_density, err_flux_density = mag_to_Jy(zeropoint, magnitude, err_magnitude)
    flux_density, err_flux_density = Jy_to_mJy(flux_density, err_flux_density)
    return flux_density, err_flux_density

def mJy_to_mag(zeropoint, flux_density, err_flux_density):
    flux_density, err_flux_density = mJy_to_Jy(flux_density, err_flux_density)
    magnitude, err_magnitude = Jy_to_mag(zeropoint, flux_density, err_flux_density)
    return magnitude, err_magnitude

######################################################
# The lazy version of converter

def ensemble_mag_to_mjy(mags, band, system):
    # initialize variables
    j_mjy = []
    err_j_mjy = []
    print("{1}, zeropoint: {0} Jy".format(system[band][2], band))
    for i in range(len(mags)):
        # If no observation, 0 or -infinty will be givne, put 0 as the value
        if mags[i,0] == 0 or mags[i,1] == 0:
            mjy = err_mjy = 0.0
        elif mags[i,0] < -100 or mags[i,0] < -100:
            mjy = err_mjy = 0.0
        # Convert
        else:
            mjy, err_mjy = mag_to_mJy(system[band][2], mags[i,0], mags[i,1])
        j_mjy.append(mjy)
        err_j_mjy.append(err_mjy)
    # Remove exotic answers
    j_mjy = np.nan_to_num(j_mjy)
    err_j_mjy = np.nan_to_num(err_j_mjy)
    j_mjy = np.transpose(np.stack((j_mjy, err_j_mjy)))
    return np.array(j_mjy)

# This function for converting mini Janskey to magnitude
def ensemble_mjy_to_mag(mjys, band, system):
    # initialize variables
    j_mag = []
    err_j_mag = []
    print("{1}, zeropoint: {0} Jy".format(system[band][2], band))
    for i in range(len(mjys)):
        # If no observation, put 0 as value.
        if mjys[i,0] == 0 or mjys[i,1] == 0:
            mag = err_mag = 0.0
        # Convert
        else:
            mag, err_mag = mJy_to_mag(system[band][2], mjys[i,0], mjys[i,1])
        j_mag.append(mag)
        err_j_mag.append(err_mag)
    # Remove exotic answers
    j_mag = np.nan_to_num(j_mag)
    err_j_mag = np.nan_to_num(err_j_mag)
    j_mag = np.transpose(np.stack((j_mag, err_j_mag)))
    return np.array(j_mag)

######################################################
# Convert quantities between 2MASS mag system and UKIRT mag system

class TWOMASS_to_UKIDSS():
    def __init__(self, J2, H2, K2):
        # Load data from 2MASS
        self.J2 = J2
        self.H2 = H2
        self.K2 = K2
        # Data type of J2, H2, and K2 must be uncertainties.unumpy.
        self.Jw = self.getJw_base_on_J2_H2()
        self.Hw = self.getHw_base_on_J2_H2()
        self.Kw = self.getKw_base_on_J2_K2()
        return
    def getJw_base_on_J2_H2(self):
        Jw = self.J2 - 0.065 * (self.J2 - self.H2)
        return Jw
    def getHw_base_on_J2_H2(self):
        Hw = self.H2 + 0.070 * (self.J2 - self.H2) - 0.030
        return Hw
    def getKw_base_on_J2_K2(self):
        Kw = self.K2 - 0.010 * (self.J2 - self.K2)
        return Kw

def ensemble_two2u(J2mag, H2mag, K2mag):
    # Convert from 2MASSmag to UKIDSSmag
    JUmag = []
    HUmag = []
    KUmag = []
    for i in range(len(J2mag)):
        # Initialzed
        J2mag_u = None
        H2mag_u = None
        K2mag_u = None
        # Selection
        # ignore the detections with less -100.
        if J2mag[i,0] < -100 or J2mag[i,1] < -100:
            J2mag_u = ufloat(0,0)
        else:
            J2mag_u = ufloat(J2mag[i,0], J2mag[i,1])
        if H2mag[i,0] < -100 or H2mag[i,1] < -100:
            H2mag_u = ufloat(0,0)
        else:
            H2mag_u = ufloat(H2mag[i,0], H2mag[i,1])
        if K2mag[i,0] < -100 or K2mag[i,1] < -100:
            K2mag_u = ufloat(0,0)
        else:
            K2mag_u = ufloat(K2mag[i,0], K2mag[i,1])
        TwotoU = TWOMASS_to_UKIDSS(J2mag_u, H2mag_u, K2mag_u)
        if (J2mag_u.n != 0.0) and (H2mag_u.n != 0.0):
            JUmag_u = TwotoU.Jw
            HUmag_u = TwotoU.Hw
        else:
            JUmag_u = ufloat(0.0, 0.0)
            HUmag_u = ufloat(0.0, 0.0)
        if (J2mag_u.n != 0.0) and (K2mag_u.n != 0.0):
            KUmag_u = TwotoU.Kw
        else:
            KUmag_u = ufloat(0.0, 0.0)
        # Append the result to list
        JUmag.append(JUmag_u)
        HUmag.append(HUmag_u)
        KUmag.append(KUmag_u)
    # Return a list which are formated in uncertainties nparray.
    return JUmag, HUmag, KUmag

# this function is used to convert the unit from magnitude to mini Janskey
# take j band as example
def ensemble_mag_to_mjy_ufloat(bands, band, system):
    # initialize variables
    mjy_array = []
    err_mjy_array = []
    # Convert from mag to mjy
    for i in range(len(bands)):
        # If the source is not observed.
        if bands[i].n == 0 or bands[i].s == 0:
            mjy = err_mjy = 0.0
        elif bands[i].n < -100 or bands[i].s < -100:
            mjy = err_mjy = 0.0
        
        else:
            mjy, err_mjy = mag_to_mJy(system[band][2], bands[i].n, bands[i].s)
        mjy_array.append(mjy)
        err_mjy_array.append(err_mjy)
    mjy_array = np.nan_to_num(mjy_array)
    err_mjy_array = np.nan_to_num(err_mjy_array)
    return np.array(mjy_array), np.array(err_mjy_array)

#-----------------------------------------------------
# This def is used to fill up empty error with median one.
def fill_up_error(bands):
    # load data
    flux_with_error = bands[(bands[:,1] != 0.0),0]
    bands_with_error = bands[(bands[:,1] != 0.0)]
    # find the upper bond of flux with error
    flux_with_error = np.sort(flux_with_error)
    flux_upper_bond = flux_with_error[-1]
    # if flux over upper bond of flux with error, abandom that data.
    # if flux is below the upper bond of flux with error, replace error with median
    bands[(bands[:,1] == 0) & (bands[:,0] != 0.0) & (bands[:,0] > flux_upper_bond), 0] = 0.0
    index_of_bands_below_upper_bond_without_error = np.where( (bands[:,1] == 0.0) \
                                                            & (bands[:,0] != 0.0))
    for index in index_of_bands_below_upper_bond_without_error[0]:
        candidates = bands_with_error[(bands_with_error[:,0] < bands[index, 0] + 0.115) \
                                    & (bands_with_error[:,0] > bands[index, 0] - 0.115), 1]
        bands[index, 1] = np.median(candidates)
    return bands

def fill_up_flux_error(bands):
    # Make sure data format
    bands = np.array(bands, dtype = float)
    # load data
    flux_with_error =  bands[(bands[:,1] != 0.0), 0]
    bands_with_error = bands[(bands[:,1] != 0.0)]
    # find the upper bond of flux with error
    flux_with_error = np.sort(flux_with_error)
    flux_upper_bond = flux_with_error[-1]
    # if flux over upper bond of flux with error, abandom that data.
    # if flux is below the upper bond of flux with error, replace error with median
    bands[(bands[:,1] == 0) & (bands[:,0] != 0.0) & (bands[:,0] > flux_upper_bond), 0] = 0.0
    index_of_bands_below_upper_bond_without_error = np.where( (bands[:,1] == 0.0) \
                                                            & (bands[:,0] != 0.0))
    for index in index_of_bands_below_upper_bond_without_error[0]:
        candidates = bands_with_error[(bands_with_error[:,0] < bands[index, 0]*1.115) \
                                    & (bands_with_error[:,0] > bands[index, 0]*0.885), 1]
        bands[index, 1] = np.median(candidates)
    return bands
