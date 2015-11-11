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
from Skywaves_plot_general import Natural_Skywaves
from remove_60Hz_slope import remove_slope
from geopy.distance import great_circle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
#from pylab import *
matplotlib.rcParams.update({'font.size': 16})

x_min=0*1e6
x_max=0.5

#distance=208.9
#dt_70km=(2*np.sqrt(70*70+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=70km
#dt_80km=(2*np.sqrt(80*80+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=80km
#dt_90km=(2*np.sqrt(90*90+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=90km
#print("70km = %r, 80 km = %r, 90 km = %r (in microseconds)"%(dt_70km*1e6,dt_80km*1e6,dt_90km*1e6))

## Input Parameters ##
RS_time=34.0
date=11072015
fs=10e6
suffix=1206
DBY_station=(28.462991, -80.707441)
NLDN_flash=(27.566,-81.851)#(29.265,-79.649)
Peak_Current=-42

Horizontal_Distance=great_circle(DBY_station, NLDN_flash).meters
Horizontal_Distance_km=Horizontal_Distance/1000

angle=np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))
angle_deg=angle*180/np.pi
angle_deg=int(angle_deg*10)/10
print("angle= %f degrees" %angle_deg )
print("Distance from the flash= %f km" %Horizontal_Distance_km)

time,skywave,UTC_time,t0=Natural_Skywaves(RS_time,date,fs,suffix,Horizontal_Distance,x_max)
plt.plot(time,skywave)
plt.show()
m,b,x0,xf=remove_slope(time,skywave,fs,t0)

yoffset=np.mean(skywave[int(x0*fs):int(x0*fs)+800])
#
### Remove 60 Hz slope ##
#x0=time[0]
#x1=time[-1] #500 us  = 5000 samples at 10MHz fs
#    
#y0=skywave[0]
#y1=skywave[-1] 
#m=(y1-y0)/(x1-x0)
#b=-m*x0*y0
        
slope=m*time+b #y=mx+b
yoffset=yoffset+slope

plt.figure(figsize=(11,8.5))
plt.plot(time,skywave-yoffset,linewidth=2.0)
#plt.plot(time*1e6,yoffset,linewidth=2.0)
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-1,1],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-1,1],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-1,1],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-1,1],'--',linewidth=2.0) #time for 90 km h iono

plt.title("Date: "+str(date)+" \n Horizontal Distance= "+str(int(Horizontal_Distance_km))+" km, angle= "+str(angle_deg)+" deg \n Peak Current= "+str(Peak_Current)+" kA")
plt.xlabel("UTC Time in seconds after %s" %UTC_time)
plt.grid()
plt.xlim(x0,xf)

plt.savefig('Date= '+str(date)+' D= '+str(int(Horizontal_Distance_km))+' km, angle= '+str(angle_deg)+' deg, Peak Current= '+str(Peak_Current)+' kA.pdf', dpi = 300)
#    #plt.ylim(-0.15,0.81)
#
#
plt.show()
#    fig_title=["UF 15-"+str(event)+", RS #"+str(RS_number[i])+".png"]
#    savefig('fig_title')