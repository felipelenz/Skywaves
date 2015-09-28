# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:56:12 2015

@author: lenz
"""
from Skywaves_plot_with_IRIG_LPF import Skywave
import matplotlib.pyplot as plt

moving_avg=Skywave(38,2,26.579535265,8)
plt.subplot(6,1,1)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-38, RS#2, Peak Current = 21.5 kA")
plt.xlim(0,0.00035)

moving_avg=Skywave(39,1,66.583436840,9)
plt.subplot(6,1,2)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-39, RS#1, Peak Current = 4.4 kA")
plt.xlim(0,0.00035)

moving_avg=Skywave(40,3,20.767465080,10)
plt.subplot(6,1,3)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-40, RS#3, Peak Current = 19.1 kA")
plt.xlim(0,0.00035)

moving_avg=Skywave(41,1,57.298446790,11)
plt.subplot(6,1,4)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-41, RS#1, Peak Current = 13.7 kA")
plt.xlim(0,0.00035)

moving_avg=Skywave(42,4,43.058185590,12)
plt.subplot(6,1,5)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-42, RS#4, Peak Current = 22.5 kA")
plt.xlim(0,0.00035)

moving_avg=Skywave(43,4,23.293418545,13)
plt.subplot(6,1,6)
plt.plot(moving_avg[0][10:-10],moving_avg[1][10:-10])
plt.title("UF 15-43, RS#4, Peak Current = 20.5 kA")
plt.xlabel("Time (s)")
plt.xlim(0,0.00035)

plt.show()