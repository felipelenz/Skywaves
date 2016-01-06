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
import matplotlib.pyplot as plt
import numpy as np
import lecroy as lc
import matplotlib
matplotlib.rcParams.update({'font.size': 16})
plt.figure(figsize=(15.8,10.9))

date=82715
calfactor=19900.50
x_min=0*1e6
x_max=0.00050*1e6

yoffset=0.2
distance=208.9
dt_70km=(2*np.sqrt(70*70+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=70km
dt_80km=(2*np.sqrt(80*80+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=80km
dt_90km=(2*np.sqrt(90*90+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=90km
print("70km = %r, 80 km = %r, 90 km = %r (in microseconds)"%(dt_70km*1e6,dt_80km*1e6,dt_90km*1e6))


##UF 15-38. RS#2
##Plot channel-base current
#suffix26=0
#seg=1
#lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
#                        str(suffix26)+".trc"
#lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
#IIHI_time = lecroy_IIHI.get_seg_time()
#IIHI = lecroy_IIHI.get_segments()
#plt.subplot(321)
#plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
#plt.xlabel("Time ($\mu$s)")
#plt.ylabel("Channel-base Current (kA)")
#plt.xlim(0,500)
#plt.ylim(-1,22.5)
#plt.grid()
#plt.title("UF 15-38, RS#2, Peak Current = 21.5 kA")
#
#
#moving_avg=Skywave(38,2,26.579535265,8,x_max)
#plt.subplot(322)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#
### Remove 60 Hz slope ##
#x0=moving_avg[0][10]
#x1=moving_avg[0][4990] #500 us  = 5000 samples at 10MHz fs
#    
#y0=moving_avg[1][10]
#y1=moving_avg[1][4990] 
#m=(y1-y0)/(x1-x0)
#b=-m*x0*y0
#            
#slope=m*moving_avg[0][10:-10]+b #y=mx+b
#yoffset=yoffset+slope
#
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="Filtered signal",linewidth=2.0) #moving averaged skywave
##plt.plot(moving_avg[0][10:-10]*1e6+dt_90km*1e6,moving_avg[1][10:-10]-yoffset,label="Filtered signal",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',label="Time when signal raises 5 std. dev. from noise mean",linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',label="TOA for theoretical 70 km ionosphere height",linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',label="TOA for theoretical 80 km ionosphere height",linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',label="TOA for theoretical 90 km ionosphere height",linewidth=2.0) #time for 90 km h iono
#plt.title("UF 15-38, RS#2, Peak Current = 21.5 kA")
#plt.xlabel("UTC Time in microseconds after %s" %moving_avg[2])
#plt.grid()
#plt.xlim(x_min,x_max)
#plt.ylim(-0.11,0.9)
#plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
#plt.legend(bbox_to_anchor=(0., 1.5, 1., 0.2), loc=3,
#           ncol=3, mode="expand", borderaxespad=0.)
#           
##UF 15-39. RS#1
##Plot channel-base current
#suffix26=1
#seg=0
#lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
#                        str(suffix26)+".trc"
#lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
#IIHI_time = lecroy_IIHI.get_seg_time()
#IIHI = lecroy_IIHI.get_segments()
#plt.subplot(323)
#plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
#plt.xlabel("Time ($\mu$s)")
#plt.ylabel("Channel-base Current (kA)")
#plt.xlim(0,500)
#plt.ylim(-1,5.4)
#plt.grid()
#plt.title("UF 15-39, RS#1, Peak Current = 4.4 kA")
#
#moving_avg=Skywave(39,1,66.583436840,9,x_max)
#plt.subplot(324)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
### Remove 60 Hz slope ##
#x0=moving_avg[0][10]
#x1=moving_avg[0][4990] #500 us  = 5000 samples at 10MHz fs
#    
#y0=moving_avg[1][10]
#y1=moving_avg[1][4990] 
#m=(y1-y0)/(x1-x0)
#b=-m*x0*y0
#            
#slope=m*moving_avg[0][10:-10]+b #y=mx+b
#yoffset=yoffset+slope
#
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,linewidth=2.0)
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-0.13,0.47],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-0.13,0.47],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-0.13,0.47],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-0.13,0.47],'--',linewidth=2.0) #time for 90 km h iono
#plt.title("UF 15-39, RS#1, Peak Current = 4.4 kA")
#plt.xlabel("UTC Time in microseconds after %s" %moving_avg[2])
##plt.ylabel('Uncalibrated electric field')
#plt.grid()
#plt.xlim(x_min,x_max)
#plt.ylim(-0.05,0.48)
#plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
#
##UF15-40, RS#3
##Plot channel-base current
#suffix26=2
#seg=1
#lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
#                        str(suffix26)+".trc"
#lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
#IIHI_time = lecroy_IIHI.get_seg_time()
#IIHI = lecroy_IIHI.get_segments()
#plt.subplot(325)
#plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
#plt.xlabel("Time ($\mu$s)")
#plt.ylabel("Channel-base Current (kA)")
#plt.xlim(0,500)
#plt.ylim(-1,20.1)
#plt.grid()
#plt.title("UF 15-40, RS#3, Peak Current = 19.1 kA")
#
#moving_avg=Skywave(40,3,20.767465080,10,x_max)
#plt.subplot(326)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#
### Remove 60 Hz slope ##
#x0=moving_avg[0][10]
#x1=moving_avg[0][4990] #500 us  = 5000 samples at 10MHz fs
#    
#y0=moving_avg[1][10]
#y1=moving_avg[1][4990] 
#m=(y1-y0)/(x1-x0)
#b=-m*x0*y0
#            
#slope=m*moving_avg[0][10:-10]+b #y=mx+b
#yoffset=yoffset+slope
#
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,linewidth=2.0)
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-1,1],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-1,1],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-1,1],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-1,1],'--',linewidth=2.0) #time for 90 km h iono
#plt.title("UF 15-40, RS#3, Peak Current = 19.1 kA")
#plt.xlabel("UTC Time in microseconds after %s" %moving_avg[2])
#plt.grid()
#plt.xlim(x_min,x_max)
#plt.ylim(-0.15,0.81)
#plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")

#UF 15-41, RS#1
suffix26=3
seg=0
lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
                        str(suffix26)+".trc"
lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
IIHI_time = lecroy_IIHI.get_seg_time()
IIHI = lecroy_IIHI.get_segments()
plt.subplot(321)
plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Channel-base Current (kA)")
plt.xlim(0,500)
plt.ylim(-1,14.7)
plt.grid()
plt.title("UF 15-41, RS#1, Peak Current = 13.7 kA")

moving_avg=Skywave(41,1,57.298446790,11,x_max)
plt.subplot(322)
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

plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,linewidth=2.0)
plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-1,1],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-1,1],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-1,1],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-1,1],'--',linewidth=2.0) #time for 90 km h iono
plt.title("UF 15-41, RS#1, Peak Current = 13.7 kA")
plt.xlabel("UTC Time in microseconds after %s" %moving_avg[2])
plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min,x_max)
plt.ylim(-0.12,0.52)

#UF 15-42, RS#4
suffix26=4
seg=2
lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
                        str(suffix26)+".trc"
lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
IIHI_time = lecroy_IIHI.get_seg_time()
IIHI = lecroy_IIHI.get_segments()
plt.subplot(323)
plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Channel-base Current (kA)")
plt.xlim(0,500)
plt.ylim(-1,23.5)
plt.grid()
plt.title("UF 15-42, RS#4, Peak Current = 22.5 kA")

moving_avg=Skywave(42,4,43.058185590,12,x_max)
plt.subplot(324)
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

plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,linewidth=2.0)
plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-1,1],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-1,1],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-1,1],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-1,1],'--',linewidth=2.0) #time for 90 km h iono
plt.title("UF 15-42, RS#4, Peak Current = 22.5 kA")
plt.xlabel("UTC Time in microseconds after %s" %moving_avg[2])
plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min,x_max)
plt.ylim(-0.1,0.82)

#UF 15-42, RS#4
suffix26=5
seg=3
lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
                        str(suffix26)+".trc"
lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
IIHI_time = lecroy_IIHI.get_seg_time()
IIHI = lecroy_IIHI.get_segments()
plt.subplot(325)
plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Channel-base Current (kA)")
plt.xlim(0,500)
plt.ylim(-1,21.5)
plt.grid()
plt.title("UF 15-43, RS#4, Peak Current = 20.5 kA")

moving_avg=Skywave(43,4,23.293418545,13,x_max)
plt.subplot(326)
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

plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,linewidth=2.0)
plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-1,1],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-1,1],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-1,1],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-1,1],'--',linewidth=2.0) #time for 90 km h iono
plt.title("UF 15-43, RS#4, Peak Current = 20.5 kA")
plt.xlabel("UTC Time in microseconds after %s" %moving_avg[2])
plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min,x_max)
plt.ylim(-.13,0.78)

plt.show()