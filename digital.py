# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:13:33 2018

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
s = 100
payoff = 1
M = 10 #step
times = 10 #run how many times

def digital(r,v,q,t,k,s,payoff,M,times):
    dt = t/M
    summation = 0 #np.zeros_like(s)
    for i in range(times): 
        for j in range(M):            
            random_seed = np.random.lognormal((r-q-v*v*0.5)*dt,v*sqrt(dt))
            s *= random_seed
        if s>k:
            summation += payoff                
        #difference = s - k
        #mask=np.zeros_like(difference)
        #mask[difference>0]=10
        #summation += mask
    summation/=times
    summation*=exp(-r*t)
    return summation

def digitial_from_github(r,v,q,t,k,s,payoff,M,times):
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
    return d
    
#print(digital(0.02,0.2,0,0.25,100,100,10,1000,10000))
#print(digitial_from_github(0.02,0.2,0,0.25,100,100,10,100,10000))
def theta(r,v,q,k,s,payoff,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    t = lower_bound
    while t <= upper_bound:
        x_axis.append(t)        
        price.append(digital(r,v,q,t,k,s,payoff,M,times))
        t += step  
    plt.subplot(211)
    plt.plot(x_axis,price)
    plt.title('Greeks of otm digital option')
    plt.grid(True)
    plt.xlabel('maturity')
    plt.ylabel('price')
    plt.tight_layout()

def vega(r,q,t,k,s,payoff,M,times,lower_bound,upper_bound,step):
    x_axis = []
    price = []
    v = lower_bound
    while v <= upper_bound:
        x_axis.append(v)        
        price.append(digital(r,v,q,t,k,s,payoff,M,times))
        v += step  
    plt.subplot(212)
    plt.plot(x_axis,price)
    plt.grid(True)
    plt.xlabel('volatility')
    plt.ylabel('price')

def adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T):
    return S * Cash_percent + S * (1-Cash_percent) *(F+D)/I *exp(-r*T)

def adjusted_digital(S,Cash_percent,F,D,I,r,T,K,sigma,payoff,M,times):
    S_0 = adjusted_underlying_asset(S,Cash_percent,F,D,I,r,T)
    return digitial_from_github(r,sigma,D,T,K,S_0,payoff,M,times)

#digital(r,v,q,t,k,s,payoff,M,times)   

def basis_to_price(S,Cash_percent,D,I,r,T,K,sigma,payoff,M,times,lower,upper,step):
    x_axis = []
    price = []
    v = lower
    while v >= upper:
        x_axis.append(v)
        F = I + v        
        price.append(adjusted_digital(S,Cash_percent,F,D,I,r,T,K,sigma,payoff,M,times))
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
    #print(X,Y)
    #Z = np.sqrt(X ** 2 + Y ** 2)
    Z = adjusted_digital(100,0.0121,3500+X,0,3500,0.02,22/365,Y,0.2,10,100,1000)
    
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
    
    plt.show()
'''
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.5,0.2,10,100,10000,-5,-50,-5)
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.4,0.2,10,100,10000,-5,-50,-5)
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.6,0.2,10,100,10000,-5,-50,-5)
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.3,0.2,10,100,10000,-5,-50,-5)
basis_to_price(2.5,0.0121,0,3500,0.02,0.25,2.7,0.2,10,100,10000,-5,-50,-5)
'''

def new_greek(Cash_percent,D,I,r,T,K,sigma,payoff,M,times,lower,upper,step):
    x_axis = []
    greek = []
    s = lower
    while s <= upper:
        d = adjusted_digital(s,Cash_percent,I-5,D,I,r,T,K,sigma,payoff,M,times)-adjusted_digital(s,Cash_percent,I-50,D,I,r,T,K,sigma,payoff,M,times)
        d /= 45
        x_axis.append(s)
        greek.append(d)
        s += step
    plt.subplot(211)
    plt.plot(x_axis,greek)
    plt.grid(True)
    plt.xlabel('spot price')
    plt.ylabel('greek')

def delta(Cash_percent,D,I,r,T,K,sigma,payoff,M,times,lower,upper,step):
    x_axis = []
    delta = []
    s = lower
    while s <= upper:
        d = adjusted_digital(s+1,Cash_percent,I-5,D,I,r,T,K,sigma,payoff,M,times)-adjusted_digital(s-1,Cash_percent,I-50,D,I,r,T,K,sigma,payoff,M,times)
        d /= 2
        x_axis.append(s)
        delta.append(d)
        s += step
    plt.subplot(212)
    plt.plot(x_axis,delta)
    plt.grid(True)
    plt.xlabel('spot price')
    plt.ylabel('delta')

new_greek(0.0121,0,3500,0.02,0.25,100,0.2,10,100,10000,80,120,5)
delta(0.0121,0,3500,0.02,0.25,100,0.2,10,100,10000,80,120,5)
#theta(0.03,0.3,0,100,80,1,100,1000,1/12,1,1/12)
#vega(0.03,0,0.5,100,80,1,100,1000,0.12,0.4,0.02)      
