#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

# Now let's generate this with one of the Markov Chain Monte Carlo methods called Metropolis Hastings algorithm
# Our assumed transition probabilities would follow normal distribution X2 ~ N(X1, Covariance = [[0.2, 0], [0, 0.2]])

import time
start_time = time.time()
# Set up constants and initial variable conditions
num_samples = 100000
prob_density = 0
## Plan is to sample from a Bivariate Gaussian Distribution with mean (0, 0) and covariance of 0.7 between the two variables
mean = np.array([0, 0])
cov = np.array([[1, -0.7], [-0.7, 1]])
cov1 = np.matrix(cov)
mean1 = np.matrix(mean)
x_list, y_list = [], []
accepted_samples_count = 0
## Normalizer of the Probability distribution
## This is not actually required since we are taking ratio of probabilities for inference
normalizer = np.sqrt(((2*np.pi)**2)*np.linalg.det(cov))
## Start with initial Point (0, 0)
x_initial, y_initial = 0, 0
x1, y1 = x_initial, y_initial

for i in range(num_samples):
    ## Set up the Conditional Probability distribution, taking the existing point
    ## as the mean and a small variance = 0.2 so that points near the existing point
    ## have a high chance of getting sampled.
    mean_trans = np.array([x1, y1])
    cov_trans = np.array([[0.2, 0], [0, 0.2]])
    x2, y2 = np.random.multivariate_normal(mean_trans, cov_trans).T
    X = np.array([x2, y2])
    X2 = np.matrix(X)
    X1 = np.matrix(mean_trans)
    ## Compute the probability density of the existing point and the new sampled point
    mahalnobis_dist2 = (X2 - mean1)*np.linalg.inv(cov)*(X2 - mean1).T
    prob_density2 = (1/float(normalizer))*np.exp(-0.5*mahalnobis_dist2)
    mahalnobis_dist1 = (X1 - mean1)*np.linalg.inv(cov)*(X1 - mean1).T
    prob_density1 = (1/float(normalizer))*np.exp(-0.5*mahalnobis_dist1)
    ## This is the heart of the algorithm. Comparing the ration of probability density of the new 
    ## point and the existing point(acceptance_ratio) and selecting the new point if it is to have more probability
    ## density. If it has less probability it is randomly selected with the probability of getting
    ## selected being proportional to hte ration of the acceptance ratio
    acceptance_ratio = prob_density2[0, 0] / float(prob_density1[0, 0])
    if (acceptance_ratio >= 1 ) | ((acceptance_ratio < 1) and (acceptance_ratio >= np.random.uniform(0, 1))):
        x_list.append(x2)
        y_list.append(y2)
        x1 = x2
        y1 = y2
        accepted_samples_count += 1
end_time = time.time()
print("Time taken to sample {0} points ==> {1}  seconds".format(accepted_samples_count, end_time - start_time))
print("Acceptance ratio ===> {0}".format(accepted_samples_count/100000))
## Time to display the samples generated
plt.xlabel('X')
plt.ylabel('Y')
plt.scatter(x_list, y_list, color = 'red', alpha = 0.1)
print("Mean of the Sampled Points\n{0} {1}".format(np.mean(x_list), np.mean(y_list)))
print("Covariance matrix of the Sampled Points\n{0}".format(np.cov(x_list, y_list)))
plt.show()
