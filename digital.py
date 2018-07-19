# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:13:33 2018

@author: fangqiheng
"""

r = 0.03 #risk-free rate
v = 0.2 #volitility
q = 0 #dividend rate
t = 0.5 #unit:year
k = 100
s = 100
payoff = 1
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

summation = 0
for path in result:
    if path[-1] > k:
        summation += payoff
d = exp(-r*t)* (summation/times)
print('the price of the digital is:', d)