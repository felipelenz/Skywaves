# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 14:49:18 2016

@author: lenz
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 13:34:44 2016

@author: lenz
"""
import numpy as np
from scipy import signal as sigs

def filter_VE(data):
    f=np.linspace(0,1,50000)
    a = np.ones(50000)
    
    #Switching power supply frequency (~290 KHz)
    a[2850:2950] =0
    
    #1.49 MHz
    a[14850:14950]=0
    
    #AM 1.37 MHz
    a[13650:13750] = 0
    
    #80 m Ham band (3.97 MHz)
    a[39650:39750] = 0
    
    #80 m Ham band (4 MHz)
    a[39950:40050]= 0
    
    a[-1]=0
    
    b=sigs.firwin2(3000,f,a)
    [h, fpoints] = sigs.freqz(b, 1, 50000,10E6)
    
    #Run the FIR filter
    vec = sigs.lfilter(b,1,data)
    return vec