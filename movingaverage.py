# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:51:35 2016

@author: lenz
This code takes the moving average of a signal. The inputs are the data (interval)
and the number of points of the moving average window (window_size). The outputs
are the moving averaged data and the filter delay in seconds.
"""

import numpy as np
#########################
# Moving Average Filter #
#########################
def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    filter_delay=((window_size-1)/2)*1/10e6
    return np.convolve(interval, window, mode='valid') ,filter_delay