#!/usr/bin/python3
'''
Abstract:
    This is a program to exercise what I learned in CH4.
Usage:
    20180601_CH4_disorder_of_small_numbers.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20170601
####################################
update log
20180601 version alpha 1:
    1. The code works

'''
import numpy as np
from IPython.core.pylabtools import figsize
import matplotlib.pyplot as plt

figsize(12.5, 4)
import pymc as pm

# initialize
std_height = 15
mean_height = 150
n_counties = 50000
pop_generator = pm.rdiscrete_uniform
norm = pm.rnormal

# generate some artificial population numbers
population = pop_generator(100, 1500, size = n_counties)
average_across_county = np.zeros(n_counties)
for i in range(n_counties):
    # generate some individuals and take the mean
    average_across_county[i] = norm(mean_height, 1./std_height**2, size = population[i]).mean()

# locate the counties with the apparently most extreme average heights
i_min = np.argmin(average_across_county)
i_max = np.argmax(average_across_county)

# print the population size of 10 shortest counties and 10 talleset counties
print("Population sizes of 10 'shortest' counties:")
print(population[np.argsort(average_across_county)[:10]])
print("Population sizes of 10 'tallest' counties:")
print(population[np.argsort(-average_across_county)[:10]])

# plot population size versus recorded average
plt.scatter(population, average_across_county, alpha = 0.5, c = "#7A68A6")
plt.scatter([population[i_min], population[i_max]], [average_across_county[i_min], average_across_county[i_max]],
            s= 60, marker = "o", facecolors = "none", edgecolors = "#A60628", linewidths = 1.5, label = "extreme heights")
plt.xlim(100, 1500)
plt.title("Average height versus county population")
plt.xlabel("County population")
plt.ylabel("Average height in county")
plt.plot([100, 1500], [150, 150], color="k", label="true expected height", ls = "--")
plt.legend(scatterpoints = 1)
plt.show()
