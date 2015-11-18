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
x_max=0.3


## Input Parameters ##
RS_time=47.1#From NLDN
date=11072015
fs=10e6
suffix=1211
DBY_station=(28.462991, -80.707441)
NLDN_flash=(27.681,-81.919) #From NLDN
Peak_Current=-30 #From NLDN

# Code starts here
Horizontal_Distance=great_circle(DBY_station, NLDN_flash).meters
Horizontal_Distance_km=Horizontal_Distance/1000

RS_time=RS_time+Horizontal_Distance/2.99e8
print('RS_time=%r' %RS_time)

distance=Horizontal_Distance_km
dt_70km=(2*np.sqrt(70*70+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=70km
dt_80km=(2*np.sqrt(80*80+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=80km
dt_90km=(2*np.sqrt(90*90+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=90km
print("70km = %r, 80 km = %r, 90 km = %r (in microseconds)"%(dt_70km*1e6,dt_80km*1e6,dt_90km*1e6))

if NLDN_flash[0]>DBY_station[0] and NLDN_flash[1]>DBY_station[1]:
    angle=np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))
elif NLDN_flash[0]>DBY_station[0] and NLDN_flash[1]<DBY_station[1]:
    angle=np.pi+np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))
elif NLDN_flash[0]<DBY_station[0] and NLDN_flash[1]<DBY_station[1]:
    angle=np.pi+np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))
elif NLDN_flash[0]<DBY_station[0] and NLDN_flash[1]>DBY_station[1]:
    angle=2*np.pi+np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))

angle_deg=angle*180/np.pi
angle_deg=int(angle_deg*10)/10
print("angle= %f degrees" %angle_deg )
print("Distance from the flash= %f km" %Horizontal_Distance_km)

Horizontal_Distance=0
time,skywave,UTC_time,t0,initial_timestamp=Natural_Skywaves(RS_time,date,fs,suffix,Horizontal_Distance,x_max)
print(UTC_time)
m,b,x0,xf,slope0=remove_slope(time,skywave,fs,t0)

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
slope

##sine=-0.2*np.sin(2*np.pi*59.5*time)
#plt.figure(figsize=(11,8.5))
#plt.plot(time,skywave+yoffset,linewidth=2.0)
##plt.plot(time,sine,'r',linewidth=2.0)
##plt.plot(time*1e6,yoffset,linewidth=2.0)
y=skywave

t_max=np.argmax(y)
y_topeak=y[0:t_max]

noise_window=y[0:1200]
yoffset=np.mean(y[0:1200])
sigma=np.std(noise_window)
mean=np.mean(noise_window)

min_ind=np.argmax(np.abs(1.0/((mean+5*sigma)-y_topeak)))   
min_time=min_ind/fs+x0
print('GW Start=%r'%min_time)


plt.figure(figsize=(11,8.5))
plt.plot(time,skywave-slope+slope0,linewidth=2.0)
plt.xlim(x0,xf)
plt.show()

var = input('Please manual offset: ')
plt.figure(figsize=(11,8.5))
plt.plot(time,skywave-slope+slope0-float(var),linewidth=2.0)
plt.plot([min_time,min_time],[-2,2],'--',linewidth=2.0) #beginning time
plt.plot([min_time+dt_70km,min_time+dt_70km],[-2,2],'--',linewidth=2.0) #70 km iono
plt.plot([min_time+dt_80km,min_time+dt_80km],[-2,2],'--',linewidth=2.0) #80 km iono
plt.plot([min_time+dt_90km,min_time+dt_90km],[-2,2],'--',linewidth=2.0) #90 km iono

plt.title("File# "+str(suffix)+" Date: "+str(date)+" \n Horizontal Distance= "+str(int(Horizontal_Distance_km))+" km, angle= "+str(angle_deg)+" deg \n Peak Current= "+str(Peak_Current)+" kA")
plt.xlabel("UTC Time in seconds after %s" %UTC_time)
plt.grid()
plt.xlim(x0,xf)
plt.tight_layout()
plt.savefig('File#'+str(suffix)+' Date= '+str(date)+' (Lat '+str(NLDN_flash[0])+',Long '+str(NLDN_flash[1])+')D= '+str(int(Horizontal_Distance_km))+' km, angle= '+str(angle_deg)+' deg, Peak Current= '+str(Peak_Current)+' kA.pdf', dpi = 300)
plt.show()
