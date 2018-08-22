# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 10:21:23 2018

@author: fangqiheng
"""
import numpy as np
from math import log, sqrt, exp,pi
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def bsm_call_value(S_0, K, T, r, sigma):
    #S_0 = float(S_0)
    #print(S_0.shape)    
    #print(K.shape)
    d_1 = (np.log(S_0 / K) + (r + 0.5 *sigma **2) *T)/(sigma * sqrt(T))
    d_2 = (np.log(S_0 / K) + (r - 0.5 *sigma **2) *T)/(sigma * sqrt(T))
    C_0 = (S_0 * stats.norm.cdf(d_1, 0.0, 1.0) - K * exp(-r * T) * stats.norm.cdf(d_2, 0.0, 1.0))
    return C_0

def adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T):
    return S * Cash_percent + S * (1-Cash_percent) *(F+D)/I *exp(-r*T)

def pricing(S,Cash_percent,F,D,I,r,T,K,sigma):
    S_0 = adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T)
    return bsm_call_value(S_0, K, T, r, sigma)

def basis_to_price(S,Cash_percent,D,I,r,T,K,sigma,lower,upper,step):
    x_axis = []
    price = []
    v = lower
    while v >= upper:
        x_axis.append(v)
        F = I + v        
        price.append(pricing(S,Cash_percent,F,D,I,r,T,K,sigma))
        v += step  
    #plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('basis')
    plt.ylabel('price')

def threeDplot():
    fig = plt.figure()
    ax = Axes3D(fig)
    
    X = np.arange(-50,-5,5)
    Y = np.arange(80,120,5)
    X, Y = np.meshgrid(X, Y)
    #Z = np.sqrt(X ** 2 + Y ** 2)
    Z = pricing(100,0.0121,3500+X,0,3500,0.02,22/365,Y,0.2)
    
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
    
    plt.show()

basis_to_price(100,0.0121,0,3500,0.02,0.25,100,0.2,-5,-50,-5)
basis_to_price(95,0.0121,0,3500,0.02,0.25,100,0.2,-5,-50,-5)
basis_to_price(105,0.0121,0,3500,0.02,0.25,100,0.2,-5,-50,-5)
basis_to_price(110,0.0121,0,3500,0.02,0.25,100,0.2,-5,-50,-5)
basis_to_price(115,0.0121,0,3500,0.02,0.25,100,0.2,-5,-50,-5)
#basis_to_price(2.595,0.0121,0,3500,0.02,22/365,2.4,0.2,-5,-50,-5)
#print(pricing(2.595,0.0121,3504,0,3510,0.02,22/365,2.4,0.2))
