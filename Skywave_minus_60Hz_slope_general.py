# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:56:12 2015

@author: lenz
This code plots the skywaves from natural lightning NLDN data
Skywave_plot_general returns: time, skywave,UTC_time,t0 

It also removes the 60 Hz slope
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


## Input Parameters ##
RS_time=56.3 #From NLDN
date=11072015
fs=10e6
suffix=1244
DBY_station=(28.462991, -80.707441)
NLDN_flash=(27.679,-81.966) #From NLDN
Peak_Current=-16 #From NLDN

# Code starts here
Horizontal_Distance=great_circle(DBY_station, NLDN_flash).meters
Horizontal_Distance_km=Horizontal_Distance/1000

angle=np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))
angle_deg=angle*180/np.pi
angle_deg=int(angle_deg*10)/10
print("angle= %f degrees" %angle_deg )
print("Distance from the flash= %f km" %Horizontal_Distance_km)

time,skywave,UTC_time,t0=Natural_Skywaves(RS_time,date,fs,suffix,Horizontal_Distance,x_max)

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

plt.title("Date: "+str(date)+" \n Horizontal Distance= "+str(int(Horizontal_Distance_km))+" km, angle= "+str(angle_deg)+" deg \n Peak Current= "+str(Peak_Current)+" kA")
plt.xlabel("UTC Time in seconds after %s" %UTC_time)
plt.grid()
plt.xlim(x0,xf)
plt.tight_layout()
plt.savefig('Date= '+str(date)+' (Lat '+str(NLDN_flash[0])+',Long '+str(NLDN_flash[1])+')D= '+str(int(Horizontal_Distance_km))+' km, angle= '+str(angle_deg)+' deg, Peak Current= '+str(Peak_Current)+' kA.pdf', dpi = 300)
plt.show()
