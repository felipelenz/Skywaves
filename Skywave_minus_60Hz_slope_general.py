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
matplotlib.rcParams.update({'font.size': 16})

x_min=0*1e6
x_max=0.3


## Input Parameters ##
RS_time=12.4#From NLDN
date=11072015
fs=10e6
suffix=2588
DBY_station=(0,0)#(28.462991, -80.707441) #Latitude, Longitude
NLDN_flash=(1,0)#(29.119,-80.122) #From NLDN
Peak_Current=-24#From NLDN

# Code starts here
Horizontal_Distance=great_circle(DBY_station, NLDN_flash).meters
Horizontal_Distance_km=Horizontal_Distance/1000

distance=Horizontal_Distance_km
# Time delay of the first skywave for three ionospheric reflection heights:
# 70 km, 80 km, and 90 km
dt_70km=(2*np.sqrt(70*70+(distance/2)*(distance/2))-distance)/2.99e5 
dt_80km=(2*np.sqrt(80*80+(distance/2)*(distance/2))-distance)/2.99e5 
dt_90km=(2*np.sqrt(90*90+(distance/2)*(distance/2))-distance)/2.99e5
print("70km = %r, 80 km = %r, 90 km = %r (in microseconds)"
      %(dt_70km*1e6,dt_80km*1e6,dt_90km*1e6))

# The logic below is necessary to account for the horizontal angle between
# the antenna and the NLDN reported latitude and Longitude
# North is 0 deg, East is 90 deg, South is 180 deg and West is 270 deg
# NE Quadrant
if NLDN_flash[0]>DBY_station[0] and NLDN_flash[1]>DBY_station[1]:
    angle=np.pi/2-np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))
# SE Quadrant
elif NLDN_flash[0]<DBY_station[0] and NLDN_flash[1]>DBY_station[1]:
    angle=np.pi/2-np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))
# SW Quadrant
elif NLDN_flash[0]<DBY_station[0] and NLDN_flash[1]<DBY_station[1]:
    angle=3*np.pi/2-np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))
# NW Quadrant
elif NLDN_flash[0]>DBY_station[0] and NLDN_flash[1]<DBY_station[1]:
    angle=3*np.pi/2-np.arctan((NLDN_flash[0]-DBY_station[0])/(NLDN_flash[1]-DBY_station[1]))
# North
elif NLDN_flash[0]>DBY_station[0] and NLDN_flash[1]==DBY_station[1]:
    angle=0
# East    
elif NLDN_flash[0]==DBY_station[0] and NLDN_flash[1]>DBY_station[1]:
    angle=np.pi/2
# South
elif NLDN_flash[0]<DBY_station[0] and NLDN_flash[1]==DBY_station[1]:
    angle=np.pi
# West
elif NLDN_flash[0]==DBY_station[0] and NLDN_flash[1]<DBY_station[1]:
    angle=3*np.pi/2

angle_deg=angle*180/np.pi
angle_deg=int(angle_deg*10)/10
print("Horizontal angle= %f degrees" %angle_deg )
print("Distance from the flash= %f km" %Horizontal_Distance_km)

parameter=Natural_Skywaves(RS_time,date,fs,suffix,Horizontal_Distance,x_max)
time=parameter[0]
skywave=parameter[1]
UTC_time=parameter[2]
t0=parameter[3]
initial_timestamp=parameter[4]

m,b,x0,xf,slope0=remove_slope(time,skywave,fs)


slope=m*time+b #y=mx+b

##sine=-0.2*np.sin(2*np.pi*59.5*time)
#plt.figure(figsize=(11,8.5))
#plt.plot(time,skywave+yoffset,linewidth=2.0)
##plt.plot(time,sine,'r',linewidth=2.0)
##plt.plot(time*1e6,yoffset,linewidth=2.0)

print("index0 = %r, indexf = %r" %(x0*fs,x0*fs))
y=skywave[x0*fs:xf*fs]

t_max=np.argmax(y)
y_topeak=y[0:t_max]

noise_window=y[0:1200]
yoffset=np.mean(y[0:1200])
sigma=np.std(noise_window)
mean=np.mean(noise_window)

min_ind=np.argmax(np.abs(1.0/((mean+3*sigma)-y_topeak)))   
min_time=min_ind/fs
print('GW Start=%r'%min_time)

time=time-x0
plt.figure(figsize=(11,8.5))
plt.plot(time,skywave-slope-slope0,linewidth=2.0)
plt.xlim(x0-x0,xf-x0)
plt.show()

var = input('Please manual offset: ')
plt.figure(figsize=(11,8.5))
plt.plot(time,skywave-slope-slope0-float(var),linewidth=2.0)
plt.plot([min_time,min_time],[-20,20],'--',linewidth=2.0) #beginning time
plt.plot([min_time+dt_70km,min_time+dt_70km],[-20,20],'--',linewidth=2.0) #70 km iono
plt.plot([min_time+dt_80km,min_time+dt_80km],[-20,20],'--',linewidth=2.0) #80 km iono
plt.plot([min_time+dt_90km,min_time+dt_90km],[-20,20],'--',linewidth=2.0) #90 km iono

plt.title("File# "+str(suffix)+" Date: "+str(date)+" \n Horizontal Distance= "
          +str(int(Horizontal_Distance_km))+" km, angle= "+str(angle_deg)
          +" deg \n Peak Current= "+str(Peak_Current)+" kA")
plt.xlabel("UTC Time in seconds after %s" %UTC_time)
plt.grid()
plt.xlim(x0-x0,xf-x0)
plt.tight_layout()
plt.savefig('File#'+str(suffix)+' Date= '+str(date)
            +' (Lat '+str(NLDN_flash[0])+',Long '+str(NLDN_flash[1])
            +')D= '+str(int(Horizontal_Distance_km))+' km, angle= '
            +str(angle_deg)+' deg, Peak Current= '
            +str(Peak_Current)+' kA.pdf', dpi = 300)
plt.show()
