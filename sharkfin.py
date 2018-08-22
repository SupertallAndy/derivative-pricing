# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:30:20 2018

@author: fangqiheng
"""
import numpy as np
from math import exp,sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

r = 0.03 #risk-free rate
v = 0.2 #volitility
q = 0 #dividend rate
t = 0.5 #unit:year
k = 100
knock_out = 110
s = 100
M = 100 #step
times = 1000 #run how many times

def sharkfin(r,v,q,t,k,knock_out,s,M,times):
    dt = t/M
    knock_out_matrix = knock_out * np.ones_like(s)
    summation = np.zeros_like(s)
    for i in range(times):  
        zero = np.ones_like(s)
        for j in range(M):        
            random_seed = np.random.lognormal((r-q-v*v*0.5)*dt,v*sqrt(dt))
            s *= random_seed
            z = s-knock_out_matrix
            #temp_mask = np.ones_like(s)
            zero[z>0] = 0
        s = s-k
        s[s<0]=0
        summation += s * zero 
    summation/=times
    summation*=exp(-r*t)
    return summation

def sharkfin_from_github(r,v,q,t,k,knock_out,s,M,times):
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
    return sharkfin
    
    
def theta(r,v,q,k,knock_out,s,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    t = lower_bound
    while t <= upper_bound:
        x_axis.append(t)        
        price.append(sharkfin(r,v,q,t,k,knock_out,s,M,times))
        t += step  
    plt.subplot(211)
    plt.plot(x_axis,price)
    plt.title('Greeks of sharkfin')
    plt.grid(True)
    plt.xlabel('maturity')
    plt.ylabel('price')
    plt.tight_layout()

def vega(r,q,t,k,knock_out,s,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    v = lower_bound
    while v <= upper_bound:
        x_axis.append(v)        
        price.append(sharkfin(r,v,q,t,k,knock_out,s,M,times))
        v += step  
    plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('volatility')
    plt.ylabel('price')

def adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T):
    return S * Cash_percent + S * (1-Cash_percent) *(F+D)/I *exp(-r*T)

def adjusted_sharkfin(S,Cash_percent,F,D,I,r,T,K,sigma,knock_out,M,times):
    S_0 = adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T)
    return sharkfin_from_github(r,sigma,D,T,K,knock_out,S_0,M,times)

def basis_to_price(S,Cash_percent,D,I,r,T,K,sigma,knock_out,M,times,lower,upper,step):
    x_axis = []
    price = []
    v = lower
    while v >= upper:
        x_axis.append(v)
        F = I + v        
        price.append(adjusted_sharkfin(S,Cash_percent,F,D,I,r,T,K,sigma,knock_out,M,times))
        v += step  
    #plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('basis')
    plt.ylabel('price')

def threeDplot():
    fig = plt.figure()
    ax = Axes3D(fig)
    #basis_to_price(100,0.0121,0,3500,0.02,22/365,100,0.2,110,100,100000,-5,-50,-5)
    
    X = np.arange(-50,-5,5)
    Y = np.arange(80,120,5)
    X, Y = np.meshgrid(X, Y)
    
    Z = adjusted_sharkfin(S=100,Cash_percent=0.0121,F=3500+X,D=0,I=3500,r=0.03,T=22/365,K=Y,sigma=0.2,knock_out=130,M=100,times=1000)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
    
    plt.show()
'''
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.5,0.2,3.5,100,10000,-5,-50,-5)
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.6,0.2,3.5,100,10000,-5,-50,-5)
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.7,0.2,3.5,100,10000,-5,-50,-5)
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.3,0.2,3.5,100,10000,-5,-50,-5)
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.4,0.2,4.5,100,10000,-5,-50,-5)
'''
def new_greek(Cash_percent,D,I,r,T,K,sigma,kock_out,M,times,lower,upper,step):
    x_axis = []
    greek = []
    s = lower
    while s <= upper:
        d = adjusted_sharkfin(s,Cash_percent,I-5,D,I,r,T,K,sigma,kock_out,M,times)-adjusted_sharkfin(s,Cash_percent,I-50,D,I,r,T,K,sigma,kock_out,M,times)
        d /= 45
        x_axis.append(s)
        greek.append(d)
        s += step
    plt.subplot(211)
    plt.plot(x_axis,greek)
    plt.grid(True)
    plt.xlabel('spot price')
    plt.ylabel('greek')

def delta(Cash_percent,D,I,r,T,K,sigma,kock_out,M,times,lower,upper,step):
    x_axis = []
    delta = []
    s = lower
    while s <= upper:
        d = adjusted_sharkfin(s+1,Cash_percent,I-5,D,I,r,T,K,sigma,kock_out,M,times)-adjusted_sharkfin(s-1,Cash_percent,I-50,D,I,r,T,K,sigma,kock_out,M,times)
        d /= 2
        x_axis.append(s)
        delta.append(d)
        s += step
    plt.subplot(212)
    plt.plot(x_axis,delta)
    plt.grid(True)
    plt.xlabel('spot price')
    plt.ylabel('delta')

new_greek(0.0121,0,3500,0.02,0.25,100,0.2,130,100,10000,80,120,5)
delta(0.0121,0,3500,0.02,0.25,100,0.2,130,100,10000,80,120,5)
#theta(0.03,0.3,0,100,110,95,100,10000,1/12,1,1/12)    
#vega(0.03,0,0.5,100,110,95,100,10000,0.05,1,0.05)  

