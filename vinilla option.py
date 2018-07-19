# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 10:13:55 2018

@author: fangqiheng
"""
#mu=(r-v*v/2)*t, tau=v*v*t
import numpy as np
from math import exp,sqrt
import matplotlib.pyplot as plt
'''
r = int(input('please type in the risk-free rate:'))
v = int(input('please type in the volitility:'))
u = int(input('please type in the dividend rate:'))
t = int(input('please type in the maturity:'))
k = int(input('please type in the strike price:'))
s = int(input('please type in the current stock price:'))
'''
r = 0.03
v = 0.2 #volitility
q = 0 #dividend rate
t = 0.5 #unit:year
k = 100
s = 100
M = 100 #step
times = 1000 #run how many times
dt = t/M

result = []
for i in range(times):
    path = []
    for j in range(M):
        if j == 0:
            path.append(s)
        else:
            random_seed = np.random.lognormal((r-q-v*v*0.5)*dt,v*sqrt(dt))
            path.append(path[j-1] * random_seed)
    result.append(path)

c = exp(-r*t)*np.sum([max(path[-1]-k,0) for path in result])/times
p = exp(-r*t)*np.sum([max(k-path[-1],0) for path in result])/times
print('the price of the call option is:', c)
print('the price of the put option is:', p)

'''
plt.figure(figsize=(10,7))
plt.grid(True)
plt.xlabel('Time step')
plt.ylabel('index level')
for i in range(30):
    plt.plot(result[i])
'''    



