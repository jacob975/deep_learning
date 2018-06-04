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
# Convert quantities between magnitude and Jy
# Those convert function comes from: http://ssc.spitzer.caltech.edu/warmmission/propkit/pet/magtojy/index.html
# Hint: 1 Jy = 1000 mJy
#       Jy is a unit of flux density

# the properties of bands in ukirt
# example key : [band, wavelength, zeropoint]
# 20180604
# I find that band J is inconsistent with 2mass, so I modified the zeropoint of band J.
def set_ukirt():
    ukirt_system = {'V' : ["V", 0.5556, 3540] , 'I' : ["I", 0.90, 2250] , 'J' : ["J", 1.25, 1500] , 'H' : ["H", 1.65, 1020] ,\
                    'K' : ["K", 2.20, 657] , 'L' : ["L", 3.45, 290] , 'Lprime' : ["Lprime", 3.80, 252], 'M' : ["M", 4.80, 163] ,\
                    'N' : ["N", 10.1, 39.8], 'Q' : ["Q", 20.0, 10.4] }
    return ukirt_system
'''
# This is copy from http://ssc.spitzer.caltech.edu/warmmission/propkit/pet/magtojy/
def set_ukirt():
    ukirt_system = {'V' : ["V", 0.5556, 3540] , 'I' : ["I", 0.90, 2250] , 'J' : ["J", 1.25, 1600] , 'H' : ["H", 1.65, 1020] ,\
                    'K' : ["K", 2.20, 657] , 'L' : ["L", 3.45, 290] , 'Lprime' : ["Lprime", 3.80, 252], 'M' : ["M", 4.80, 163] ,\
                    'N' : ["N", 10.1, 39.8], 'Q' : ["Q", 20.0, 10.4] }
    return ukirt_system
'''
def set_2mass():
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
    upper_flux_density = zeropoint * np.power(10.0, -0.4 * (magnitude - err_magnitude))
    err_flux_density = upper_flux_density - flux_density
    return flux_density, err_flux_density

def Jy_to_mag(zeropoint, flux_density, err_flux_density):
    magnitude = -2.5 * ( np.log(flux_density) - np.log(zeropoint) )/ np.log(10.0)
    upper_magnitude = -2.5 * ( np.log(flux_density - err_flux_density) - np.log(zeropoint) )/ np.log(10.0)
    err_magnitude = upper_magnitude - magnitude
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
# Convert quantities between pixel and wcs
def pix2wcs(radec, name_image):
    hdulist = pyfits.open(name_image)
    wcs = pywcs.WCS(hdulist[0].header)
    pix = wcs.wcs_sky2pix(radec, 1)
    return pix

def wcs2wpix(pix, name_image):
    hdulist = pyfits.open(name_image)
    wcs = pywcs.WCS(hdulist[0].header)
    radec = wcs.pix2wcs_sky(pix, 1)
    return radec
