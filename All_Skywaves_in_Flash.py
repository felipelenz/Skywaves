# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 15:12:02 2015

@author: lenz
"""

from Skywaves_plot_with_IRIG_LPF import Skywave
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams.update({'font.size': 22})

date=82715
calfactor=19900.50

x_min=0*1e6
x_max=0.00050*1e6

distance=208.9
dt_70km=(2*np.sqrt(70*70+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=70km
dt_80km=(2*np.sqrt(80*80+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=80km
dt_90km=(2*np.sqrt(90*90+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=90km

#UF 15-38, RS#1
#moving_avg=Skywave(38,1,26.522908895,8,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_reference=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-38, RS#1, Peak Current = 15.1 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.1,0.66)


#moving_avg=Skywave(38,2,26.579535265,8,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-38, RS#2, Peak Current = 21.5 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono

#moving_avg=Skywave(38,3,26.691097980,8,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-38, RS#3, Peak Current = 15.4 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.06,0.46)


#moving_avg=Skywave(38,4,26.734557870,8,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-38, RS#4, Peak Current = 12.6 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.07,0.4)


#moving_avg=Skywave(38,5,26.764446000,8,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-38, RS#5, Peak Current = 6.1 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.03,0.16)
#plt.ylim(-0.1,0.9)
#
#UF 15-39
#moving_avg=Skywave(39,1,66.583436840,9,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-39, RS#1, Peak Current = 4.4 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.1,0.45)

#moving_avg=Skywave(39,3,66.633136315,9,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-39, RS#3, Peak Current = 5.1 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.07,0.3)

#moving_avg=Skywave(39,5,66.671758785,9,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-39, RS#5, Peak Current = 8.6 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.02,0.3)
#plt.ylim(-0.11,0.47)


#UF 15-40
#moving_avg=Skywave(40,2,20.746971600,10,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-40, RS#2, Peak Current = 14 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.11,0.61)

#moving_avg=Skywave(40,3,20.767465080,10,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-40, RS#3, Peak Current = 19.1 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.1,0.8)
#plt.ylim(-0.11,0.8)

#UF 15-41
#moving_avg=Skywave(41,1,57.298446790,11,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-41, RS#1, Peak Current = 13.7 kA",linewidth=2.0) #moving averaged skywave

#moving_avg=Skywave(41,2,57.373669615,11,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-41, RS#2, Peak Current = 11.1 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.03,0.4)

#moving_avg=Skywave(41,3,57.405116910,11,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-41, RS#3, Peak Current = 11 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.03,0.37)

#moving_avg=Skywave(41,4,57.555913445,11,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-41, RS#4, Peak Current = 11.4 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.03,0.32)
#plt.ylim(-0.12,0.5)
##
#UF 15-42
#moving_avg=Skywave(42,1,42.712899355,12,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-42, RS#1, Peak Current = 7.9 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.05,0.31)
#
#moving_avg=Skywave(42,3,42.862766400,12,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-42, RS#3, Peak Current = 13 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.05,0.43)

#moving_avg=Skywave(42,4,43.058185590,12,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-42, RS#4, Peak Current = 22.5 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.11,0.8)

#moving_avg=Skywave(42,5,43.338093110,12,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-42, RS#5, Peak Current = 14.3 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.05,0.36)
#
#moving_avg=Skywave(42,6,43.366312590,12,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-42, RS#6, Peak Current = 16.5 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.05,0.55)
#plt.ylim(-0.11,0.8)

###UF 15-43
#moving_avg=Skywave(43,1,22.706011205,13,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-43, RS#1, Peak Current = 14.8 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.15,0.64)

#moving_avg=Skywave(43,2,22.934697575,13,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-43, RS#2, Peak Current = 14.2 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.12,0.55)
#
#moving_avg=Skywave(43,3,23.157666725,13,x_max)
#waveform=moving_avg[1][10:-10]
#yoffset=np.mean(waveform[0:800])
#t_start=moving_avg[5]*1e6
#plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-43, RS#3, Peak Current = 17.6 kA",linewidth=2.0) #moving averaged skywave
#plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
#plt.ylim(-0.08,0.55)

#UF 15-43, RS#4
moving_avg=Skywave(43,4,23.293418545,13,x_max)
waveform=moving_avg[1][10:-10]
yoffset=np.mean(waveform[0:800])
t_start=moving_avg[5]*1e6
plt.plot(moving_avg[0][10:-10]*1e6,moving_avg[1][10:-10]-yoffset,label="UF 15-43, RS#4, Peak Current = 20.5 kA",linewidth=2.0) #moving averaged skywave
#The next line plots the flipped waveform with the peaks alligned. We do this
# to see if any of the wave characteristics of the GW and IR align well
#plt.plot(moving_avg[0][10:-10]*1e6+250-53,-(moving_avg[1][10:-10]-yoffset),linewidth=2.0)
plt.plot([moving_avg[5]*1e6,moving_avg[5]*1e6],[-.2,1.2],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(moving_avg[5]+dt_70km)*1e6,(moving_avg[5]+dt_70km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(moving_avg[5]+dt_80km)*1e6,(moving_avg[5]+dt_80km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(moving_avg[5]+dt_90km)*1e6,(moving_avg[5]+dt_90km)*1e6],[-.2,1.2],'--',linewidth=2.0) #time for 90 km h iono
plt.ylim(-0.15,0.75)

plt.xlim(x_min,x_max)
plt.grid()
plt.legend()
plt.xlabel("Time ($\mu$s)")
plt.show()