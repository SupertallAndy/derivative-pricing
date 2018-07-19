# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:58:13 2018

@author: fangqiheng
"""

'''
key assumption: for each day the stock price will change 120 times and we look at the ending price
'''
import numpy as np
from math import exp,sqrt
import matplotlib.pyplot as plt
r = 0.03 #risk-free rate
v = 0.2 #volitility
q = 0 #dividend rate
trading_days = 252
lower_bound = 100
upper_bound = 110
s = 100
percentage = 0.1
times = 1000 #run how many times
dt = t/M
result = []
payoff_list = []
for i in range(times):
    count = 0
    path = []    
    for j in range(trading_days+1):
        if j == 0:
            path.append(s)
        else:
            k = path[j-1]
            for i in range(120):
                random_seed = np.random.lognormal((r-q-v*v*0.5)*dt,v*sqrt(dt))
                k *= random_seed
            #print(k)
            if k >= lower_bound and k <= upper_bound:
                count += 1
            path.append(k)
    payoff_list.append(count/trading_days*percentage)
    result.append(path)

#print(count)
range_accrue = exp(-r*t) * np.average(payoff_list)
print('the price of the range_accrue is:', range_accrue)
