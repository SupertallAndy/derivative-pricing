# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:58:13 2018

@author: fangqiheng
"""

'''
key assumption: for each day the stock price will change M=120 times and we look at the ending price
'''
import numpy as np
from math import exp,sqrt
import matplotlib.pyplot as plt

r = 0.03 #risk-free rate
v = 0.2 #volitility
q = 0 #dividend rate
t = 0.5
k1 = 100
k2 = 110
s = 100
percentage = 10
M = 120 #assume that stock price changes 120 times a day
times = 1000 #run how many times

def range_accrue(r,v,q,t,k1,k2,s,percentage,M,times):
    trading_days = int(252*t)
    dt = t/(trading_days*M)
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
                for i in range(M):
                    random_seed = np.random.lognormal((r-q-v*v*0.5)*dt,v*sqrt(dt))
                    k *= random_seed
                #print(k)
                if k >= k1 and k <= k2:
                    count += 1
                path.append(k)
        payoff_list.append(count/trading_days*percentage)
        result.append(path)

    price = exp(-r*t) * np.average(payoff_list)
    #print('the price of the range_accrue is:', price)
    return price

#range_accrue(0.03,0.3,0,0.5,100,110,100,10,120,1000)

def theta(r,v,q,k1,k2,s,percentage,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    t = lower_bound
    while t <= upper_bound:
        x_axis.append(t)        
        price.append(range_accrue(r,v,q,t,k1,k2,s,percentage,M,times))
        t += step  
    plt.subplot(211)
    plt.plot(x_axis,price)
    plt.title('Greeks of range accrue')
    plt.grid(True)
    plt.xlabel('maturity')
    plt.ylabel('price')
    plt.tight_layout()

def vega(r,q,t,k1,k2,s,percentage,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    v = lower_bound
    while v <= upper_bound:
        x_axis.append(v)        
        price.append(range_accrue(r,v,q,t,k1,k2,s,percentage,M,times))
        v += step  
    plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('volatility')
    plt.ylabel('price')

def upper_limit(r,v,q,t,k1,s,percentage,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    k2 = lower_bound
    while k2 <= upper_bound:
        x_axis.append(k2)        
        price.append(range_accrue(r,v,q,t,k1,k2,s,percentage,M,times))
        k2 += step  
    plt.subplot(211)
    plt.title('sensitivity of range')
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('upper_limit')
    plt.ylabel('price')
    plt.tight_layout()

def lower_limit(r,v,q,t,k2,s,percentage,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    k1 = lower_bound
    while k1 <= upper_bound:
        x_axis.append(k1)        
        price.append(range_accrue(r,v,q,t,k1,k2,s,percentage,M,times))
        k1 += step  
    plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('lower_limit')
    plt.ylabel('price')

def adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T):
    return S * Cash_percent + S * (1-Cash_percent) *(F+D)/I *exp(-r*T)

def adjusted_rangeaccrue(S,Cash_percent,F,D,I,r,T,K1,K2,sigma,M,times):
    S_0 = adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T)
    return range_accrue(r,sigma,D,T,K1,K2,S_0, 10, M,times)

def basis_to_price(S,Cash_percent,D,I,r,T,K1,K2,sigma,M,times,lower,upper,step):
    x_axis = []
    price = []
    v = lower
    while v >= upper:
        x_axis.append(v)
        F = I + v        
        price.append(adjusted_rangeaccrue(S,Cash_percent,F,D,I,r,T,K1,K2,sigma,M,times))
        v += step  
    #plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('basis')
    plt.ylabel('price')
'''
basis_to_price(95,0.0121,0,3500,0.02,0.25,100,110,0.2,120,100000,-5,-50,-5)
basis_to_price(100,0.0121,0,3500,0.02,0.25,100,110,0.2,120,100000,-5,-50,-5)
basis_to_price(105,0.0121,0,3500,0.02,0.25,100,110,0.2,120,100000,-5,-50,-5)
basis_to_price(110,0.0121,0,3500,0.02,0.25,100,110,0.2,120,100000,-5,-50,-5)
basis_to_price(115,0.0121,0,3500,0.02,0.25,100,110,0.2,120,100000,-5,-50,-5)
'''

def new_greek(Cash_percent,D,I,r,T,K1,K2,sigma,M,times,lower,upper,step):
    x_axis = []
    greek = []
    s = lower
    while s <= upper:
        d = adjusted_rangeaccrue(s,Cash_percent,I-5,D,I,r,T,K1,K2,sigma,M,times)-adjusted_rangeaccrue(s,Cash_percent,I-50,D,I,r,T,K1,K2,sigma,M,times)
        d /= 45
        x_axis.append(s)
        greek.append(d)
        s += step
    plt.subplot(211)
    plt.plot(x_axis,greek)
    plt.grid(True)
    plt.xlabel('spot price')
    plt.ylabel('greek')

def delta(Cash_percent,D,I,r,T,K1,K2,sigma,M,times,lower,upper,step):
    x_axis = []
    delta = []
    s = lower
    while s <= upper:
        d = adjusted_rangeaccrue(s+1,Cash_percent,I-5,D,I,r,T,K1,K2,sigma,M,times)-adjusted_rangeaccrue(s-1,Cash_percent,I-50,D,I,r,T,K1,K2,sigma,M,times)
        d /= 2
        x_axis.append(s)
        delta.append(d)
        s += step
    plt.subplot(212)
    plt.plot(x_axis,delta)
    plt.grid(True)
    plt.xlabel('spot price')
    plt.ylabel('delta')

new_greek(0.0121,0,3500,0.02,0.25,90,110,0.2,100,1000,80,120,5)
delta(0.0121,0,3500,0.02,0.25,90,110,0.2,100,1000,80,120,5)
#upper_limit(0.03,0.3,0,0.5,100,100,10,120,1000,110,130,1)  
#lower_limit(0.03,0.3,0,0.5,110,100,10,120,1000,80,100,1)  
#theta(0.03,0.3,0,100,110,95,10,120,1000,1/12,1,1/12) 
#vega(0.03,0,0.5,100,110,95,10,120,1000,0.05,1,0.05)   
