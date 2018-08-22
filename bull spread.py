# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 16:53:23 2018

@author: fangqiheng
"""
import numpy as np
from math import exp,sqrt,log
from scipy import stats
import matplotlib.pyplot as plt

r = 0.03 #risk-free rate
v = 0.2 #volitility
q = 0 #dividend rate
t = 0.5 #unit:year
k1 = 100
k2 = 110
s = 100
M = 100 #step
times = 1000 #run how many times

def bsm_call_value(S_0, K, T, r, sigma):
    S_0 = float(S_0)
    d_1 = (log(S_0 / K) + (r + 0.5 *sigma **2) *T)/(sigma * sqrt(T))
    d_2 = (log(S_0 / K) + (r - 0.5 *sigma **2) *T)/(sigma * sqrt(T))
    C_0 = (S_0 * stats.norm.cdf(d_1, 0.0, 1.0) - K * exp(-r * T) * stats.norm.cdf(d_2, 0.0, 1.0))
    return C_0

def bull_spread_formula(S_0, K1, K2, T, r, sigma):
    return bsm_call_value(S_0, K1, T, r, sigma) - bsm_call_value(S_0, K2, T, r, sigma)

def bull_spread(r,v,q,t,k1,k2,s,M,times):
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
        if path[-1] > k2:
            summation += k2-s
        elif path[-1] > k1:
            summation += path[-1] - k1
    b = exp(-r*t) * (summation/times)
    #print('the price of the bullspread is:', b)
    return b

def theta(r,v,q,k1,k2,s,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    t = lower_bound
    while t <= upper_bound:
        x_axis.append(t)        
        price.append(bull_spread(r,v,q,t,k1,k2,s,M,times))
        t += step 
    #print(price)
    plt.subplot(211)
    plt.plot(x_axis,price)
    plt.title('Greeks of bull spread')
    plt.grid(True)
    plt.xlabel('maturity')
    plt.ylabel('price')
    plt.tight_layout()

def vega(r,q,t,k1,k2,s,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    v = lower_bound
    while v <= upper_bound:
        x_axis.append(v)        
        price.append(bull_spread(r,v,q,t,k1,k2,s,M,times))
        v += step  
    #plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('volatility')
    plt.ylabel('price')

def adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T):
    return S * Cash_percent + S * (1-Cash_percent) *(F+D)/I *exp(-r*T)

def pricing(S,Cash_percent,F,D,I,r,T,K,sigma):
    if F+D > I or T < 3/365:
        return bsm_call_value(S, K, T, r, sigma)
    else:
        S_0 = adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T)
        return bsm_call_value(S_0, K, T, r, sigma)

def basis_to_price(S,Cash_percent,D,I,r,T,K1,K2,sigma,lower,upper,step):
    x_axis = []
    price = []
    v = lower
    while v >= upper:
        x_axis.append(v)
        F = I + v        
        price.append(pricing(S,Cash_percent,F,D,I,r,T,K1,sigma)-pricing(S,Cash_percent,F,D,I,r,T,K2,sigma))
        v += step  
    #plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('basis')
    plt.ylabel('price')

basis_to_price(100,0.0121,0,3500,0.02,0.25,100,110,0.2,-5,-50,-5)
basis_to_price(95,0.0121,0,3500,0.02,0.25,100,110,0.2,-5,-50,-5)
basis_to_price(105,0.0121,0,3500,0.02,0.25,100,110,0.2,-5,-50,-5)
basis_to_price(110,0.0121,0,3500,0.02,0.25,100,110,0.2,-5,-50,-5)
basis_to_price(115,0.0121,0,3500,0.02,0.25,100,110,0.2,-5,-50,-5)

#theta(0.03,0.3,0,100,110,100,100,10000,1/12,1,1/12)
#vega(0.03,0,0.5,100,110,100,100,10000,0.05,1,0.05)
