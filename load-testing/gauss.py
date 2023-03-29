
# █▀█ ▄▀█ █▄░█ █▀▄ █▀█ █▀▄▀█   █▀▀ ▄▀█ █░█ █▀ █▀
# █▀▄ █▀█ █░▀█ █▄▀ █▄█ █░▀░█   █▄█ █▀█ █▄█ ▄█ ▄█

import random 
import matplotlib.pyplot as plt 
import numpy as np
import scipy.stats as stats
import math   
from locust import HttpUser, TaskSet, between, constant
# store the random numbers in a list 
nums = [] 
mu = 5 # expected value
sigma = 1

x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma), label=f'σ={sigma}, μ={mu}')
plt.xlabel('z-score')
plt.ylabel('Probability density')
plt.legend()
plt.show()

gen = lambda instance: random.gauss(mu, sigma) 

for i in range(10000): 
    temp = gen(i)
    nums.append(temp) 

# plotting a graph 
plt.hist(nums, bins = 200) 
plt.xlabel('values')
plt.show()

