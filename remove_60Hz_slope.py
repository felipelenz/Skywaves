# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:48:23 2016

@author: lenz
This code removes the 60 Hz slope for electric field DBY data. It does so by
taking the first and the last samples of the signal, finding the slope of the 
line connecting these two points and removing that slope from the original data

It returns the processed time and data alongside with the corrected UTC 
reference time
"""
import numpy as np
#################
# Remove 60 Hz #
################             
def remove_60Hz_slope(data,x_max):
    #Because moving averaging introduces discontinuities on the edges of the
    #curve, we choose to ignore the first 10 samples in the beggining and at 
    #the end of the curve. 10 samples at 0.1us/sample is 1us, 1 us in the 
    #beggining and 1 us in the end, thus UTC_time needs to be updated to
    #UTC_time + 1 us, when we plot the new data
    fs=10e6
    Ts=1/fs
    
    first_sample=10
    last_sample=x_max/Ts-10
    
    x0=data[0][first_sample]
    x1=data[0][last_sample] #500 us  = 5000 samples at 10MHz fs
    
    y0=data[1][first_sample]
    y1=data[1][last_sample] 
    m=(y1-y0)/(x1-x0)
    b=-m*x0*y0
        
    slope=m*data[0][10:-10]+b #y=mx+b
    yoffset=np.mean(data[1][first_sample:first_sample+300])
    modified_yoffset=yoffset+slope
    
    processed_data=data[1][10:-10]-modified_yoffset #data without 60 Hz
    processed_time=data[0][10:-10]
    
    #adjust UTC reference time to account for ignoring the first 10 samples
    timestamp=data[11]
    reference_UTC_seconds=data[12]
    UTC_reference_time = "%r:%r:%11.9f" %(timestamp.hour,timestamp.minute,reference_UTC_seconds+first_sample*Ts)
    return processed_time, processed_data, UTC_reference_time
