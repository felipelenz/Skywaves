# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:56:12 2015

@author: lenz
"""
from Skywaves_plot_with_IRIG_LPF import Skywave
import matplotlib.pyplot as plt

moving_avg=Skywave(38,2,26.579535265)
plt.plot(moving_avg[0],moving_avg[1])
plt.show()