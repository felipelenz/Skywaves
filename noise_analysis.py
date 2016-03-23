# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:24:41 2015

@author: lenz
"""
import numpy as np
from pylab import show, ginput, plot
import matplotlib.pyplot as plt

def noise_analysis(x,y,fs,t0): #t0 is the pretrigger! 
    fig=plt.figure()
    ax=fig.add_subplot(111)
    
    
    ax.plot(x,y)
    temp=[]
    
    def onclick(event):
        print('I pressed g')
        if event.key == "g":
            xx = ginput(3)    
            temp.append(xx)
    cid = fig.canvas.mpl_connect('key_press_event', onclick)

    show()
#    print("Please click")

    xx = temp[0]
#    print(temp)
#    print("clicked",xx)
    sampling_time=1/fs
    t0=xx[0][0]
    t0_noise=np.int(xx[0][0]/sampling_time)-t0/sampling_time
    tf_noise=np.int(xx[1][0]/sampling_time)-t0/sampling_time
    t_end=np.int(xx[2][0]/sampling_time)-t0/sampling_time
    print(t0_noise,tf_noise,t_end)
    
    noise_data_window=y[t0_noise:tf_noise]
    plt.plot(x[t0_noise:tf_noise],noise_data_window,'g')
    plt.show()
    
    y_to_end=y[t0_noise:t_end]
    plt.plot(x[t0_noise:t_end],y_to_end,'r')
    plt.show()
    
    
    t_max=np.argmax(y_to_end)
    y_topeak=y_to_end[0:t_max]
    plt.plot(y_topeak,'b')
    plt.show()
    
    y_afterpeak=y[t_max:-1]
    plt.plot(y_afterpeak,'m')
    plt.show()
    
    noise_data_window=y[t0_noise:tf_noise]
    sigma=np.std(noise_data_window)
    mean=np.mean(noise_data_window)

    min_ind=np.argmax(np.abs(1.0/((mean+3*sigma)-y_topeak)))
    min_ampl=y_topeak[min_ind]
    max_ampl=np.max(y_topeak)
    curve_peak=y_topeak[-1]-mean
    y_ampl=max_ampl-min_ampl
   
    five_percent_ind=np.argmax(np.abs(1.0/((0.05*y_ampl+min_ampl)-y_topeak))) 
    ten_percent_ind=np.argmax(np.abs(1.0/((0.1*y_ampl+min_ampl)-y_topeak)))  
    twenty_percent_ind=np.argmax(np.abs(1.0/((0.2*y_ampl+min_ampl)-y_topeak))) 
    fifty_percent_ind=np.argmax(np.abs(1.0/((0.5*y_ampl+min_ampl)-y_topeak))) 
    fifty_percent_afterpeak_ind=np.argmax(np.abs(1.0/((0.5*y_ampl+min_ampl)-y_afterpeak))) + t_max
    eighty_percent_ind=np.argmax(np.abs(1.0/((0.8*y_ampl+min_ampl)-y_topeak))) 
    ninety_percent_ind=np.argmax(np.abs(1.0/((0.9*y_ampl+min_ampl)-y_topeak))) 
    risetime_90_10=ninety_percent_ind-ten_percent_ind
    risetime_90_10_time=risetime_90_10*sampling_time  
    
    five_percent_to_peak_time=(t_max-five_percent_ind)*sampling_time
    half_width_time=(fifty_percent_afterpeak_ind-fifty_percent_ind)*sampling_time
    print("standard deviation= %.4f noise mean= %.4f"%(sigma,mean))
    print("10-90 risetime (sec)=%r"%risetime_90_10_time)
    print("5-peak risetime (sec)=%r"%five_percent_to_peak_time)
    print("half peak width (sec)=%r"%half_width_time)
    plt.plot(x,y, 'b', \
    x[t0_noise:tf_noise],y[t0_noise:tf_noise], 'g', \
    [x[0],x[-1]],[mean,mean], 'r', \
    [x[0],x[-1]],[mean+sigma,mean+sigma], '--r', \
    [x[0],x[-1]],[mean-sigma,mean-sigma], '--r', \
    x[min_ind],y[min_ind],'*g',\
    x[five_percent_ind],y[five_percent_ind],'oy',\
    [x[ten_percent_ind],x[ninety_percent_ind]],[y[ten_percent_ind],y[ninety_percent_ind]], 'or',\
    [x[fifty_percent_ind],x[fifty_percent_afterpeak_ind]],[y[fifty_percent_ind],y[fifty_percent_afterpeak_ind]],'oc')
    plt.show()
    
    return risetime_90_10_time, ten_percent_ind, min_ind, y_ampl, mean,\
    twenty_percent_ind, fifty_percent_ind, eighty_percent_ind,\
    ninety_percent_ind, risetime_90_10, curve_peak, t_max