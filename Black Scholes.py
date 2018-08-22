# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 17:18:11 2018

@author: fangqiheng
"""

from math import log, sqrt, exp,pi
from scipy import stats
import matplotlib.pyplot as plt

def bsm_call_value(S_0, K, T, r, sigma):
    S_0 = float(S_0)
    d_1 = (log(S_0 / K) + (r + 0.5 *sigma **2) *T)/(sigma * sqrt(T))
    d_2 = (log(S_0 / K) + (r - 0.5 *sigma **2) *T)/(sigma * sqrt(T))
    C_0 = (S_0 * stats.norm.cdf(d_1, 0.0, 1.0) - K * exp(-r * T) * stats.norm.cdf(d_2, 0.0, 1.0))
    return C_0

def vega(S_0, K1, K2, T, r, lower, upper, step):
    k = lower
    price = []
    vol =[]
    while k <= upper:
        vol.append(k)
        price.append(bsm_call_value(S_0, K1, T, r, k)-bsm_call_value(S_0, K2, T, r, k))
        k += step
    plt.plot(vol,price)
    plt.grid(True)

def derivative(S_0, K, T, r, lower, upper):
    k = lower
    derivative = []
    vol =[]
    while k <= upper:
        vol.append(k)
        d_1 = (log(S_0 / K) + (r + 0.5 *k **2) *T)/(k * sqrt(T))
        d_1_derivative = sqrt(T)/2 - (log(S_0 / K)+r*T)/(k*k*sqrt(T))
        vega_to_vol = s*sqrt(T)*1/sqrt(2*pi)*exp(-0.5*d_1*d_1)*(-d_1)*d_1_derivative
        vega_to_s = 1/sqrt(2*pi)*exp(-0.5*d_1*d_1)*(sqrt(T)-d_1/k)
        derivative.append(vega_to_s)
        k += 0.01
    plt.plot(vol,derivative)
    plt.grid(True)

#derivative(100, 100, 1, 0, 0.1, 0.7)
#derivative(100, 110, 1, 0, 0.1, 0.7)

def vega_to_strike_price(s, T, r, sigma, lower, upper):
    K = lower
    derivative = []
    strike_price =[]
    while K <= upper:
        strike_price.append(K)
        d_1 = (log(s / K) + (r + 0.5 * sigma **2) *T)/(sigma * sqrt(T))
        d_1_derivative = sqrt(T)/2 - (log(s / K)+r*T)/(sigma*sigma*sqrt(T))
        #vega_to_vol = s*sqrt(T)*1/sqrt(2*pi)*exp(-0.5*d_1*d_1)*(-d_1)*d_1_derivative
        #vega_to_s = 1/sqrt(2*pi)*exp(-0.5*d_1*d_1)*(sqrt(T)-d_1/sigma)
        vega_to_k = 1/sqrt(2*pi)*exp(-0.5*d_1*d_1)*s*d_1/(K*sigma)
        derivative.append(vega_to_k)
        K += 1
    plt.plot(strike_price,derivative)
    plt.grid(True)

vega_to_strike_price(100, 1, 0, 0.6, 80, 130)


    

#vega(100, 100, 110, 0.5, 0.03, 0.1, 0.9, 0.1)
'''    
v1 = bsm_call_value(100, 100, 0.5, 0.03, 0.2) - bsm_call_value(100, 110, 0.5, 0.03, 0.2) 
v2 = bsm_call_value(100, 100, 0.5, 0.03, 0.3) - bsm_call_value(100, 110, 0.5, 0.03, 0.3)
v3 = bsm_call_value(100, 100, 0.5, 0.03, 0.4) - bsm_call_value(100, 110, 0.5, 0.03, 0.4)
v4 = bsm_call_value(100, 100, 0.5, 0.03, 0.5) - bsm_call_value(100, 110, 0.5, 0.03, 0.5)
v5 = bsm_call_value(100, 100, 0.5, 0.03, 0.6) - bsm_call_value(100, 110, 0.5, 0.03, 0.6)
v6 = bsm_call_value(100, 100, 0.5, 0.03, 0.7) - bsm_call_value(100, 110, 0.5, 0.03, 0.7)
v7 = bsm_call_value(100, 100, 0.5, 0.03, 0.8) - bsm_call_value(100, 110, 0.5, 0.03, 0.8)
print(v1,v2,v3,v4,v5,v6,v7)
'''
