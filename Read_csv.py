# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 16:02:11 2016
This code uses the .csv file created in Skywaves.py and plot the magnitude and
phase of the fft. Inputs to this code are filename and title_string
@author: lenz
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack
plt.figure(figsize=(8.5,11))
fs=10e6

filename1='UF 15-43, RS4 (Ez, DBY) (raw).csv'
filename2='UF 15-43, RS4 (Ez, DBY).csv'
title_string='UF15-43, RS#4'
def fft_plot(filename):
    
    f = open(filename)
    csv_f = csv.reader(f)
    
    time=[]
    data=[]
    for column in csv_f:
        time.append(column[0])
        data.append(column[1])
    
   
    data_array=np.asarray(data)
    
    data_FFT=scipy.fftpack.fft(data_array)
    N=len(data_array)
    xf=np.linspace(0.0,(N-1)*fs/N,N)
    return time,data,xf,data_FFT
    
 
time,data,xf,data_FFT=fft_plot(filename1)
plt.subplot(311)
plt.plot(time,data,label='raw data')
plt.xlabel('Time($\mu s$)')
plt.ylabel('Uncalibrated $E_z$ from DBY')
plt.title(title_string)

plt.subplot(312)
plt.plot(xf*1e-6,20*np.log10(abs(data_FFT)),label='raw data')
plt.xlabel('Frequency (MHz)')
plt.ylabel('FFT Magnitude (dB)')
plt.xlim(0,fs*1e-6/2)

plt.subplot(313)
Phase=np.unwrap(np.angle(data_FFT))
plt.plot(xf*1e-6,Phase*180/np.pi,label='raw data')
plt.xlabel('Frequency (MHz)')
plt.ylabel('FFT Phase (degrees)')
plt.xlim(0,fs*1e-6/2)
plt.plot()
#plt.show()

time,data,xf,data_FFT=fft_plot(filename2)
plt.subplot(311)
plt.plot(time,data,'r',label='processed data')
plt.xlabel('Time($\mu s$)')
plt.ylabel('Uncalibrated $E_z$ from DBY')
plt.title(title_string)
plt.legend()

plt.subplot(312)
plt.plot(xf*1e-6,20*np.log10(abs(data_FFT)),'r',label='processed data')
plt.xlabel('Frequency (MHz)')
plt.ylabel('FFT Magnitude (dB)')
plt.xlim(0,fs*1e-6/2)
plt.legend()

plt.subplot(313)
Phase=np.unwrap(np.angle(data_FFT))
plt.plot(xf*1e-6,Phase*180/np.pi,'r',label='processed data')
plt.xlabel('Frequency (MHz)')
plt.ylabel('FFT Phase (degrees)')
plt.xlim(0,fs*1e-6/2)
plt.plot()
plt.legend(loc=4)
plt.show()
