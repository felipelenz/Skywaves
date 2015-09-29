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

x_min=0
x_max=0.00050
moving_avg=Skywave(38,2,26.579535265,8,x_max)
plt.subplot(6,1,1)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-38, RS#2, Peak Current = 21.5 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)

moving_avg=Skywave(39,1,66.583436840,9,x_max)
plt.subplot(6,1,2)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-39, RS#1, Peak Current = 4.4 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)

moving_avg=Skywave(40,3,20.767465080,10,x_max)
plt.subplot(6,1,3)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-40, RS#3, Peak Current = 19.1 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)

moving_avg=Skywave(41,1,57.298446790,11,x_max)
plt.subplot(6,1,4)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-41, RS#1, Peak Current = 13.7 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)

moving_avg=Skywave(42,4,43.058185590,12,x_max)
plt.subplot(6,1,5)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-42, RS#4, Peak Current = 22.5 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)

moving_avg=Skywave(43,4,23.293418545,13,x_max)
plt.subplot(6,1,6)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-43, RS#4, Peak Current = 20.5 kA")
plt.xlabel("UTC Time in seconds after %s" %moving_avg[2])
plt.grid()
plt.xlim(x_min,x_max)

plt.show()