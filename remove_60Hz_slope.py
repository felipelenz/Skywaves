# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:24:41 2015

@author: lenz

This code asks the user to select the beginning and the end of the waveform 
then returns the the slope equation y=mx+b and the user limit inputs
"""
import numpy as np
from pylab import show, ginput, plot
import matplotlib.pyplot as plt

def remove_slope(x,y,fs,t0): #t0 is the pretrigger! 
    fig=plt.figure()
    ax=fig.add_subplot(111)
    
    
    ax.plot(x,y)
    temp=[]
    
    def onclick(event):
        print('I pressed g')
        if event.key == "g":
            xx = ginput(2)    
            temp.append(xx)
    cid = fig.canvas.mpl_connect('key_press_event', onclick)

    show()
#    print("Please click")

    xx = temp[0]
#    print(temp)
#    print("clicked",xx)
    sampling_time=1/fs
    x0=xx[0][0]
    y0=xx[0][1]
    
    x1=xx[1][0]
    y1=xx[1][1]
    print(x0,x1,y0,y1)
    
    m=(y1-y0)/(x1-x0)
    b=-m*x0*y0
    
    print('y='+str(m)+'x+'+str(b))
    slope=m*(x-t0)+b
    
    n0=x0/sampling_time
    n1=x1/sampling_time
    plot(x,y, 'b', \
    [x[n0],x[n1]],[y[n0],y[n1]], 'or', \
    x,slope,'g')
    show()
    
    return m,b,x0,x1