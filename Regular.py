# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 22:01:41 2021

@author: LIU KANG
"""

###Due to Kang LIU 2021.06.04##################


import numpy as np
import statsmodels.api as sm
from scipy.signal import find_peaks


#def first_index(y):
#    i = 0
#    p = np.mean(y)
#    while y[i]>p:
#        i = i+ 1
#    return i
 
#def first_index(y):
#    i = np.argmin(y)
#    return i

       

def First_derive(y):
    z = np.zeros([len(y),])
    for i in range(len(y)-1):
        z[i] = y[i+1]-y[i]
    return z


def Second_derivate(y,ratio,frequency):
    n = len(y)
    m = np.round(ratio*n)
    m=int(m)
    z = np.zeros([n,])
    for i in range(m,n-int(frequency+1)):
        z[i] = np.max([(y[i+2] + y[i] - 2*y[i+1])/2, (y[i+1] + y[i-1] - 2*y[i])/2, (y[i] + y[i-2] - 2*y[i-1])/2])
    return z


def Periode(y, num=10, dis=100):
    ff = sm.tsa.acf(y, nlags=len(y))
    peaks, _ = find_peaks(ff,distance=dis)
    peak_dict = {}
    for p in peaks:
        peak_dict[p] = ff[p]
    a = sorted(peak_dict.items(), key=lambda x: x[1], reverse=True)
    previous = np.array(sorted(a[:num]))[:,0]
    return  np.int(np.median(np.diff(previous)))
    
    

def Regular(x_r, tresh=0.7, ratio=0.2, n=10, d=100, scale=1.2, frequency=1400):
    periode = np.int(scale*Periode(x_r, num=n, dis=d))
    x_new = np.zeros(frequency)
    if periode>frequency:
        periode = frequency
    I_r = np.where(Second_derivate(x_r,ratio,frequency) < tresh*np.min(Second_derivate(x_r,ratio,frequency)))[0]
    xm = np.median(x_r[I_r])
    x_mid = I_r[ np.argmin( abs(x_r[I_r]-xm) )] 
    #x_opt = x_mid + first_index(x_r[x_mid:x_mid+int(periode-1)])
    x_opt = x_mid
    #dx_mid = First_derive(x_r[x_mid:x_mid+int(frequency-1)])
    #x_opt = np.argmin(np.where(dx_mid<0)) + x_mid
    x_new[0:periode] = x_r[(x_opt):(x_opt+periode)]
    return x_new