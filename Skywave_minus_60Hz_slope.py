# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:56:12 2015

@author: lenz
This code plots the skywaves associated with the biggest currents for 6
events. Skywave_plot_with_IRIG_LPF returns: moving_avg[0] (time list), 
moving_avg[1] (filtered skywave (moving average) list), and moving_avg[2] 
(UTC_time string)

[10:-10] is added when plotting to avoid showing the overshoot at the ends of
the waveforms causeed by the moving average filter
"""
from Skywaves_plot_with_IRIG_LPF import Skywave
from remove_60Hz_slope import remove_slope
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams.update({'font.size': 16})

x_min=0*1e6
x_max=0.00050*1e6

distance=208.9
dt_70km=(2*np.sqrt(70*70+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=70km
dt_80km=(2*np.sqrt(80*80+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=80km
dt_90km=(2*np.sqrt(90*90+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=90km
print("70km = %r, 80 km = %r, 90 km = %r (in microseconds)"%(dt_70km*1e6,dt_80km*1e6,dt_90km*1e6))

## Input Parameters ##
event=38
RS_number=3
Peak_current=15.4
RS_time=26.691097980
file_suffix=8

moving_avg=Skywave(event,RS_number,RS_time,file_suffix,x_max)

waveform=moving_avg[1][10:-10]
yoffset=np.mean(waveform[0:800])

## Remove 60 Hz slope ##
x0=moving_avg[0][10]
x1=moving_avg[0][4990] #500 us  = 5000 samples at 10MHz fs

y0=moving_avg[1][10]
y1=moving_avg[1][4990] 
m=(y1-y0)/(x1-x0)
b=-m*x0*y0

slope=m*moving_avg[0][10:-10]+b #y=mx+b
yoffset=yoffset+slope

plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset)
plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,linewidth=2.0)
plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-1,1],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-1,1],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-1,1],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-1,1],'--',linewidth=2.0) #time for 90 km h iono
plt.title("UF 15-"+str(event)+", RS #"+str(RS_number)+", Peak Current = "+str(Peak_current)+" kA")
plt.xlabel("UTC Time in microseconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)
#plt.ylim(-0.15,0.81)


plt.show()