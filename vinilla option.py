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
r = 0.03 #risk-free rate
v = 0.2 #volitility
q = 0 #dividend rate
t = 0.5 #unit:year
k = 100
s = 100
M = 100 #step
times = 1000 #run how many times


def vanilla_pricing(r,v,q,t,k,s,M,times):   
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
    #print('the price of the call option is:', c)
    #print('the price of the put option is:', p)
    return c,p

#by default, the range of stock price is 80 -120 
def delta(r,v,q,t,k,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    s = lower_bound
    while s <= upper_bound:   
        x_axis.append(s)        
        price.append(vanilla_pricing(r,v,q,t,k,s,M,times)[0])
        s += step  
    plt.plot(x_axis,price)
    return x_axis,price

def gamma(r,v,q,t,k,M,times,lower_bound,upper_bound,step):
    x_axis,price = delta(r,v,q,t,k,M,times,lower_bound,upper_bound,step)    
    difference = []
    for i in range(1,len(price)):
        difference.append(price[i]-price[i-1])
    plt.plot(x_axis[1:],difference)

def theta(r,v,q,k,s,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    t = lower_bound
    while t <= upper_bound:
        x_axis.append(t)        
        price.append(vanilla_pricing(r,v,q,t,k,s,M,times)[0])
        t += step
    plt.subplot(211)
    plt.plot(x_axis,price)
    plt.title('Greeks of bull spread')
    plt.grid(True)
    plt.xlabel('maturity')
    plt.ylabel('price')
    plt.tight_layout()

def vega(r,q,t,k,s,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    v = lower_bound
    while v <= upper_bound:
        x_axis.append(v)        
        price.append(vanilla_pricing(r,v,q,t,k,s,M,times)[0])
        v += step  
    plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('volatility')
    plt.ylabel('price')

#vega(0.03,0,0.5,100,100,100,1000,0.05,1,0.05)   
#theta(0.03,0.3,0,100,100,100,1000,1/12,1,1/12)    
print(vanilla_pricing(0.03,0.4,0,0.5,100,100,100,100000))
#v1 = vanilla_pricing(0.03,0.4,0,0.5,100,100,100,1000)[0] - vanilla_pricing(0.03,0.4,0,0.5,110,100,100,1000)[0]
#v2 = vanilla_pricing(0.03,0.5,0,0.5,100,100,100,1000)[0] - vanilla_pricing(0.03,0.5,0,0.5,110,100,100,1000)[0]
#v3 = vanilla_pricing(0.03,0.8,0,0.5,100,100,100,1000)[0] - vanilla_pricing(0.03,0.8,0,0.5,110,100,100,1000)[0]
#print(v1,v2,v3)
#delta(0.03,0.3,0,0.5,100,100,1000,80,120,0.5)
#gamma(0.03,0.3,0,0.5,100,100,1000,60,140,0.5)
'''
plt.figure(figsize=(10,7))
plt.grid(True)
plt.xlabel('Time step')
plt.ylabel('index level')
for i in range(30):
    plt.plot(result[i])
'''




