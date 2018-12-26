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
    ukirt_system = {'u' : ["u", 0.3546, 1545] ,\
                    'g' : ["g", 0.4670, 3991] ,\
                    'r' : ["r", 0.6156, 3174] ,\
                    'i' : ["i", 0.7471, 2593] ,\
                    'z' : ["z", 0.8918, 2222] ,\
                    'Z' : ["Z", 0.8817, 2232] ,\
                    'Y' : ["Y", 1.0305, 2026] ,\
                    'J' : ["J", 1.2483, 1530] ,\
                    'H' : ["H", 1.6313, 1019] ,\
                    'K' : ["K", 2.2010, 631] }
    return ukirt_system

# This is copy from https://www.ipac.caltech.edu/2mass/releases/allsky/doc/sec6_4a.html
def set_twomass():
    twomass_system = { 'J' : ["J", 1.235, 1594] , 'H' : ["H", 1.662, 1024] , 'Ks' : ["Ks", 2.159, 666.7] }
    return twomass_system

def Jy_to_mJy(flux_density):
    return 1000 * flux_density

def mJy_to_Jy(flux_density):
    return flux_density / 1000

def mag_to_Jy(zeropoint, magnitude):
    flux_density = zeropoint * np.power( 10.0, -0.4 * magnitude )
    return flux_density

def Jy_to_mag(zeropoint, flux_density):
    magnitude = -2.5 * ( np.log(flux_density) - np.log(zeropoint) )/ np.log(10.0)
    return magnitude

def mag_to_mJy(zeropoint, magnitude):
    flux_density = mag_to_Jy(zeropoint, magnitude)
    flux_density = Jy_to_mJy(flux_density)
    return flux_density

def mJy_to_mag(zeropoint, flux_density):
    flux_density = mJy_to_Jy(flux_density)
    magnitude = Jy_to_mag(zeropoint, flux_density)
    return magnitude
#-----------------------------------------------------
# convertion with error

def Jy_to_mJy(flux_density, err_flux_density):
    return 1000 * flux_density, 1000* err_flux_density

def mJy_to_Jy(flux_density, err_flux_density):
    return flux_density / 1000, err_flux_density / 1000

def mag_to_Jy(zeropoint, magnitude, err_magnitude):
    flux_density = zeropoint * np.power( 10.0, -0.4 * magnitude )
    err_flux_density = np.divide(err_magnitude * np.log(10.0) * flux_density, 2.5)
    return flux_density, err_flux_density

def Jy_to_mag(zeropoint, flux_density, err_flux_density):
    magnitude = -2.5 * ( np.log(flux_density) - np.log(zeropoint) )/ np.log(10.0)
    err_magnitude = np.divide(-2.5 * err_flux_density, flux_density * np.log(10.0)) 
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
    index_of_bands_below_upper_bond_without_error = np.where((bands[:,1] == 0.0) & (bands[:,0] != 0.0))
    for index in index_of_bands_below_upper_bond_without_error[0]:
        candidates = bands_with_error[(bands_with_error[:,0] < bands[index, 0] + 0.115)  & (bands_with_error[:,0] > bands[index, 0] - 0.115), 1]
        bands[index, 1] = np.median(candidates)
    return bands
