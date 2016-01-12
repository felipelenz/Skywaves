# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:56:12 2015

@author: lenz
This code plots the skywaves associated with the biggest currents for 6
events with the peak of the ground waves set to t=0. If adjust_peaks_in_time
is set to 0, the GWs are aligned in time t=0 for when the e-field raises above
4 sigma of the noise window

[10:-10] is added when plotting to avoid showing the overshoot at the ends of
the waveforms causeed by the moving average filter
"""
from Skywaves_plot_with_IRIG_LPF import Skywave
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams.update({'font.size': 16})
plt.figure(figsize=(15.8,10.9))
fs=10e6

date=82715
calfactor=19900.50 #for plotting current
x_min=0*1e6
x_max=0.00050*1e6

yoffset=0.2
distance=208.9 #kilometers
dt_70km=(2*np.sqrt(70*70+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=70km
dt_80km=(2*np.sqrt(80*80+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=80km
dt_90km=(2*np.sqrt(90*90+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=90km
print("70km = %5.2f, 80 km = %5.2f, 90 km = %5.2f (in microseconds)"%(dt_70km*1e6,dt_80km*1e6,dt_90km*1e6))

# Remove 60 Hz slope ##                  
def remove_60Hz_slope(moving_avg,yoffset):
    x0=moving_avg[0][10]
    x1=moving_avg[0][4990] #500 us  = 5000 samples at 10MHz fs
    
    y0=moving_avg[1][10]
    y1=moving_avg[1][4990] 
    m=(y1-y0)/(x1-x0)
#    m=m/moving_avg[8] #account for GW amplitude normalization
    b=-m*x0*y0
            
    slope=m*moving_avg[0][10:-10]+b #y=mx+b
    modified_yoffset=yoffset+slope
    
    return modified_yoffset

def process_and_plot(moving_avg):
    waveform=moving_avg[1][10:4990] #500 us of e-field data
    first_time=moving_avg[0][10]*1e6 #first sample of the waveform above
    yoffset=np.mean(waveform[0:800]) #find the DC offset during noise window
    
    modified_yoffset=remove_60Hz_slope(moving_avg, yoffset) #remove 60Hz slope

    t_peak=(np.argmax(waveform-modified_yoffset[10:4990]))*(1/fs)*1e6 #find GW peak
    t_start=moving_avg[5]*1e6 #This sets GW to t=0 based on 4 sigma from noise
    adjust_peaks_in_time=t_peak-t_start+first_time #This sets GW to t=0 by alligning GW peaks
    
    time_list=moving_avg[0][10:4990]*1e6-t_start-adjust_peaks_in_time
    data_list=waveform-modified_yoffset[10:4990]
    
    return time_list, data_list, t_start
    
#UF 15-38. RS#2
moving_avg=Skywave(38,2,26.579535265,8,x_max)
time, data, t_start = process_and_plot(moving_avg)
plt.plot(time,data,linewidth=2.0,color=[0,0,1],label="UF 15-38, RS#2") #moving averaged skywave
    
#UF 15-39. RS#1
moving_avg=Skywave(39,1,66.583436840,9,x_max)
time, data, t_start = process_and_plot(moving_avg)
plt.plot(time,data,linewidth=2.0,color=[1/6,5/6,1],label="UF 15-39, RS#1") #moving averaged skywave

#UF15-40, RS#3
moving_avg=Skywave(40,3,20.767465080,10,x_max)
time, data, t_start = process_and_plot(moving_avg)
plt.plot(time,data,linewidth=2.0,color=[2/6,4/6,1],label="UF 15-40, RS#3")

#UF 15-41, RS#1
moving_avg=Skywave(41,1,57.298446790,11,x_max)
time, data, t_start = process_and_plot(moving_avg)
plt.plot(time,data,linewidth=2.0,color=[3/6,3/6,1],label="UF 15-41, RS#1")

#UF 15-42, RS#4
moving_avg=Skywave(42,4,43.058185590,12,x_max)
time, data, t_start = process_and_plot(moving_avg)
plt.plot(time,data,linewidth=2.0,color=[4/6,2/6,1],label="UF 15-42, RS#4")

#UF 15-43, RS#4
moving_avg=Skywave(43,4,23.293418545,13,x_max)
time, data, t_start = process_and_plot(moving_avg)
plt.plot(time,data,linewidth=2.0,color=[5/6,1/6,1],label="UF 15-43, RS#4")

plt.plot([0,0],[-1,1],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1],'--',linewidth=2.0) #time for 90 km h iono
plt.title("Ground-wave peaks are time-alligned to t=0")
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Amplitude normalized E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min-t_start,x_max-t_start)
plt.ylim(-.15,0.95)
plt.legend()

plt.show()

