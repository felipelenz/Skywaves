# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 16:13:52 2016
Crosscorrelate subsequent return strokes in the same flash
read_DBY is an updated version of Skywaves_plot_with_IRIG_LPF, but the
UTC time reference output was done much more carefully. 
@author: lenz
"""

from read_DBY import read_DBY
import matplotlib.pyplot as plt
import scipy.signal as ss
from scipy.fftpack import fft
import numpy as np

# Remove 60 Hz slope ##                  
def remove_60Hz_slope(data,x_max):
    #Because moving averaging introduces discontinuities on the edges of the
    #curve, we choose to ignore the first 10 samples in the beggining and at 
    #the end of the curve. 10 samples at 0.1us/sample is 1us, 1 us in the 
    #beggining and 1 us in the end, thus UTC_time needs to be updated to
    #UTC_time + 1 us, when we plot the new data
    fs=10e6
    Ts=1/fs
    
    first_sample=10
    last_sample=x_max/Ts-10
    
    x0=data[0][first_sample]
    x1=data[0][last_sample] #500 us  = 5000 samples at 10MHz fs
    
    y0=data[1][first_sample]
    y1=data[1][last_sample] 
    m=(y1-y0)/(x1-x0)
    b=-m*x0*y0
        
    slope=m*data[0][10:-10]+b #y=mx+b
    yoffset=np.mean(data[1][first_sample:first_sample+300])
    modified_yoffset=yoffset+slope
    
    processed_data=data[1][10:-10]-modified_yoffset #data without 60 Hz
    processed_time=data[0][10:-10]
    
    #adjust UTC reference time to account for ignoring the first 10 samples
    timestamp=data[11]
    reference_UTC_seconds=data[12]
    UTC_reference_time = "%r:%r:%11.9f" %(timestamp.hour,timestamp.minute,reference_UTC_seconds+first_sample*Ts)
    return processed_time, processed_data, UTC_reference_time

#########################
# Moving Average Filter #
#########################
def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, mode='valid') 

def chop_gw_ir(remove_60Hz_slope_output):
    gw_ir_ref=2200 #we define this sample number to be the point where groundwave 
               #becomes skywave. This point doesn't need to be very well defined
               #we just put it here to make the code cleaner
    gw_time=remove_60Hz_slope_output[0][1:gw_ir_ref]
    gw_data=remove_60Hz_slope_output[1][1:gw_ir_ref]
    ir_time=remove_60Hz_slope_output[0][gw_ir_ref:-1]
    ir_data=remove_60Hz_slope_output[1][gw_ir_ref:-1]
    return gw_time,gw_data,ir_time,ir_data
    
x_max=450e-6
gw_ir_ref=2200 #we define this sample number to be the point where groundwave 
               #becomes skywave. This point doesn't need to be very well defined
               #we just put it here to make the code cleaner
UF_1538_1=read_DBY(38,1,26.522908895,8,x_max,10)
processed_UF_1538_1=remove_60Hz_slope(UF_1538_1,x_max)
gw_time,gw_data,ir_time,ir_data=chop_gw_ir(processed_UF_1538_1)

UF_1538_1_gw_time=gw_time
UF_1538_1_gw=gw_data
UF_1538_1_ir_time=ir_time
UF_1538_1_ir=ir_data

plt.plot(UF_1538_1_ir_time,UF_1538_1_ir)

UF_1538_1_ir_time=movingaverage(UF_1538_1_ir_time,50)
UF_1538_1_ir=movingaverage(UF_1538_1_ir,50)

plt.plot(UF_1538_1_gw_time,UF_1538_1_gw)
plt.plot(UF_1538_1_ir_time,UF_1538_1_ir)
plt.show()
def take_fft(data):
    # Number of sample points
    N = len(data)
    fs=10e6
    # sample spacing
    T = 1/fs
    y = data
    yf = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    mag = 20*np.log10(np.abs(yf[0:N/2]))
    mag_2 = 2.0/N * np.abs(yf[0:N/2])
    phase = np.unwrap(np.angle(yf[0:N/2]))*190/np.pi
    return xf, mag, mag_2 , phase


gw_fft=take_fft(UF_1538_1_gw)
ir_fft=take_fft(UF_1538_1_ir)

#plt.subplot(211)
#plt.plot(gw_fft[0], gw_fft[1],label='groundwave')
#plt.plot(ir_fft[0], ir_fft[1],label='skywave')
#plt.xlabel('Frequency (Hz)')
#plt.ylabel('Magnitude (dB)')
#plt.xscale('log')
#plt.grid()
#
#plt.subplot(212)
plt.plot(gw_fft[0], gw_fft[2],label='groundwave')
plt.plot(ir_fft[0], ir_fft[2],label='skywave')

plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.xscale('log')
plt.yscale('log')
plt.grid()
plt.legend(loc=3)

#plt.subplot(212)
#plt.plot(gw_fft[0], gw_fft[3])
#plt.plot(ir_fft[0], ir_fft[3])
#
#plt.xlabel('Frequency (Hz)')
#plt.ylabel('Phase (degrees)')
#plt.xscale('log')
#plt.grid()
plt.show()