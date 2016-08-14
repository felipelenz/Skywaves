# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 13:34:44 2016

@author: lenz
"""
import numpy as np
from scipy import signal as sigs

def filter_DBY(data):
    f=np.linspace(0,1,50000)
    a = np.ones(50000)

    
    #Switching power supply frequency (~290 KHz)
    a[2850:2950]=0
    
    #AM 540 KHz
    a[5350:5450] = 0
    
    #AM 580 KHz
    a[5750:5850] =0
    
    #AM 740 KHz
    a[7350:7450] = 0
    
    #AM 810 KHz
    a[8050:8150] =0
    
    #AM 840 KHz
    a[8350:8450] =0
    
    #AM 920 KHz
    a[9150:9250] =0
    
    #AM 990 KHz
    a[9850:9950] =0
    
    #AM 1030 KHz
    a[10250:10350] = 0
    
    #AM 1060 KHz
    a[10550:10650] = 0
    
    #AM 1180 KHz
    a[11750:11850] = 0
    
    #AM 1240 KHz
    a[12350:12450] =0
    
    #AM 1300 KHz
    a[12950:13050] = 0
    
    #AM 1350 KHz
    a[13450:13550] = 0
    
    #AM 1510 KHz
    a[15050:15150] = 0
    
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