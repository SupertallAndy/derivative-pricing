# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:30:20 2018

@author: fangqiheng
"""
import numpy as np
from math import exp,sqrt
import matplotlib.pyplot as plt
r = 0.03 #risk-free rate
v = 0.2 #volitility
q = 0 #dividend rate
t = 0.5 #unit:year
k = 100
knock_out = 110
s = 100
M = 100 #step
times = 1000 #run how many times
dt = t/M

result = []
for i in range(times):
    path = []
    path.append(s)
    for i in range(M-1):
        path.append(0)
    for j in range(1,M):        
        random_seed = np.random.lognormal((r-q-v*v*0.5)*dt,v*sqrt(dt))
        path[j] = path[j-1] * random_seed
        if path[j] > knock_out:
            result.append(path)
            break            
    result.append(path)

sharkfin = exp(-r*t)*np.sum([max(path[-1]-k,0) for path in result])/times
print('the price of the sharkfin is:', sharkfin)