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

x_min=0
x_max=0.00050

dt_70km=(2*np.sqrt(70*70+100*100)-200)/2.99e5 #time delay of the first skywave for ionospheric reflection height=70kn
dt_80km=(2*np.sqrt(80*80+100*100)-200)/2.99e5 #time delay of the first skywave for ionospheric reflection height=80kn


moving_avg=Skywave(38,2,26.579535265,8,x_max)
plt.subplot(6,1,1)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10],label="Filtered signal") #moving averaged skywave
plt.plot([moving_avg[5],moving_avg[5]],[0,1.2],label="Time when signal raises 5 std. dev. from noise mean") #time when skywave raises 3 std dev from mean noise
plt.plot([moving_avg[5]+dt_70km,moving_avg[5]+dt_70km],[0,1.2],label="TOA for theoretical 70 km ionosphere height") #time for 70 km h iono
plt.plot([moving_avg[5]+dt_80km,moving_avg[5]+dt_80km],[0,1.2],label="TOA for theoretical 80 km ionosphere height") #time for 80 km h iono
plt.title("UF 15-38, RS#2, Peak Current = 21.5 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)
plt.ylim(0,1.2)
plt.legend(bbox_to_anchor=(0., 1.5, 1., 0.2), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)


moving_avg=Skywave(39,1,66.583436840,9,x_max)
plt.subplot(6,1,2)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.plot([moving_avg[5],moving_avg[5]],[-0.5,0.2]) #time when skywave raises 3 std dev from mean noise
plt.plot([moving_avg[5]+dt_70km,moving_avg[5]+dt_70km],[-0.5,0.2]) #time for 70 km h iono
plt.plot([moving_avg[5]+dt_80km,moving_avg[5]+dt_80km],[-0.5,0.2]) #time for 80 km h iono
plt.title("UF 15-39, RS#1, Peak Current = 4.4 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)
plt.ylim(-0.5,0.2)

moving_avg=Skywave(40,3,20.767465080,10,x_max)
plt.subplot(6,1,3)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.plot([moving_avg[5],moving_avg[5]],[-0.6,0.4]) #time when skywave raises 3 std dev from mean noise
plt.plot([moving_avg[5]+dt_70km,moving_avg[5]+dt_70km],[-0.6,0.4]) #time for 70 km h iono
plt.plot([moving_avg[5]+dt_80km,moving_avg[5]+dt_80km],[-0.6,0.4]) #time for 80 km h iono
plt.title("UF 15-40, RS#3, Peak Current = 19.1 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)
plt.ylim(-0.6,0.4)

moving_avg=Skywave(41,1,57.298446790,11,x_max)
plt.subplot(6,1,4)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.plot([moving_avg[5],moving_avg[5]],[-0.2,0.5]) #time when skywave raises 3 std dev from mean noise
plt.plot([moving_avg[5]+dt_70km,moving_avg[5]+dt_70km],[-0.2,0.5]) #time for 70 km h iono
plt.plot([moving_avg[5]+dt_80km,moving_avg[5]+dt_80km],[-0.2,0.5]) #time for 80 km h iono
plt.title("UF 15-41, RS#1, Peak Current = 13.7 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)
plt.ylim(-0.2,0.5)

moving_avg=Skywave(42,4,43.058185590,12,x_max)
plt.subplot(6,1,5)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.plot([moving_avg[5],moving_avg[5]],[0.1,1.1]) #time when skywave raises 3 std dev from mean noise
plt.plot([moving_avg[5]+dt_70km,moving_avg[5]+dt_70km],[0.1,1.1]) #time for 70 km h iono
plt.plot([moving_avg[5]+dt_80km,moving_avg[5]+dt_80km],[0.1,1.1]) #time for 80 km h iono
plt.title("UF 15-42, RS#4, Peak Current = 22.5 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)
plt.ylim(0.1,1.1)

moving_avg=Skywave(43,4,23.293418545,13,x_max)
plt.subplot(6,1,6)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.plot([moving_avg[5],moving_avg[5]],[0.2,1.1]) #time when skywave raises 3 std dev from mean noise
plt.plot([moving_avg[5]+dt_70km,moving_avg[5]+dt_70km],[0.2,1.1]) #time for 70 km h iono
plt.plot([moving_avg[5]+dt_80km,moving_avg[5]+dt_80km],[0.2,1.1]) #time for 80 km h iono
plt.title("UF 15-43, RS#4, Peak Current = 20.5 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)
plt.ylim(0.2,1.1)

plt.show()