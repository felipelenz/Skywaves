# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:04:08 2016

@author: lenz
Takes the xcorr between data 1 and data 2, plots xcorr and returns the lag time
from xcorr operation
"""
import matplotplib.pyplot as plt
import numpy as np
#XCORR CODE:
def xcorr(time1,time2,data1,data2):
    xcorr=np.correlate(data1/np.max(data1),data2/np.max(data2),'full')
    xcorr_delay=np.argmax(xcorr)-(xcorr.size-1)/2 #this delay is how much one skywave is shifted relative to another. It must, however, be referenced to the same feature of the groundwave, i.e. GW peak
    xcorr_delay=xcorr_delay*(1/10e6)
    print(xcorr_delay)
    
    plt.plot(time1,data1/np.max(data1),label='data1')
    plt.plot(time2,data2/np.max(data2),label='data2')
    plt.show()
    plt.legend()
    plt.grid()
    
    plt.plot(time1-xcorr_delay,data1/np.max(data1),label='data1')
    plt.plot(time2,data2/np.max(data2),label='data2')
    plt.show()
    
    plt.plot(xcorr)
    plt.show()
    plt.grid()
    print("sampling time")
    print(time1[1]-time1[0])
    print(time2[43]-time2[42])