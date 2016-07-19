# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:48:47 2015

@author: lenz
read_DBY is an updated version of Skywaves_plot_with_IRIG_LPF, but the
UTC time reference output was done much more carefully. 

###########
# Inputs: #
###########

event= event number (e.g. 38)
RS_number= return stroke number (e.g. 2)
RS_time=seconds of the XLI time stamp (for trigger lightning) this time can 
be found in the triggered lightning reports (e.g. 26.579535265)
suffix=last two digits of file name
x_max=time window of the data
filterwindow=number of samples used in the moving average filtering routine

############
# Outputs: #
############
moving_avg[0]=time list 
moving_avg[1]=filtered skywave (moving average) list
moving_avg[2]=UTC_time string

"""
from __future__ import division
import lecroy as lc
import numpy as np
import matplotlib.pyplot as plt
import IRIGA

fs=10e6

def read_skywaves_2016(station,year,date,event,RS_number,RS_time,suffix,x_max,filterwindow): 
    ####################
    # Input Parameters #
    ####################
#    fs=10e6 #sampling rate
#    event=43 #event name
#    RS_number=4 #return stroke number
#    RS_time=23.293418545 #seconds of the XLI time stamp (for trigger lightning) 
    #                        #this time can be found in the triggered lightning reports
#    x_max=500e-6 #xlim max for plotting the skywaves
#    suffix=13
    DBY_distance=209e3 #209 km
    VE_distance=302.5e3 #302.5 km
    GL_distance=50e3

    if station == "VE":
        distance=VE_distance
    elif station == "DBY":
        distance=DBY_distance
    elif station == "GL":
        distance=GL_distance
        
    c=2.99e8 #m/s
    
    ##############
    # Read Files #
    ##############
    #import IRIG file
#    if suffix <=9:
    lecroy_fileName_IRIG = "/Volumes/Promise 12TB RAID5/"+str(year)+" Data/0"+str(date)+"/"+str(station)+"/C2"+str(station)+"0000"+str(suffix)+".trc"
    lecroy_IRIG= lc.lecroy_data(lecroy_fileName_IRIG)
    segments_IRIG = lecroy_IRIG.get_segments()
    
    #read IRIG file and print time stamp
    timestamp,t = IRIGA.IRIGA_signal(segments_IRIG[0], fs, year=year)
    print('time stamp from IRIGA: %s' %timestamp)
    
    #import skywaves data
    lecroy_fileName_data = "/Volumes/Promise 12TB RAID5/"+str(year)+" Data/0"+str(date)+"/"+str(station)+"/C1"+str(station)+"0000"+str(suffix)+".trc"
    lecroy_data= lc.lecroy_data(lecroy_fileName_data)
    segments_data = lecroy_data.get_segments()
  
    GW_propagation_delay=distance/c
    
    ##ICLRT XLi + propagation delay
    UTC_time_at_station=RS_time+GW_propagation_delay - 80e-6 #The -80us accounts for some data to be displayed before the groundwave
    
    ##This is the time t is referred to, i.e., t[0] is 0 seconds after reference_UTC_seconds 
    reference_UTC_seconds=timestamp.second+timestamp.microsecond/1e6
    UTC_reference_time= "%r:%r:%r" %(timestamp.hour,timestamp.minute,reference_UTC_seconds)
    
    ##Find the index in the t array closest to the UTC_time_at_DBY
    n0=np.argmax(np.abs(1.0/(t+reference_UTC_seconds-UTC_time_at_station))) 
    
    ##This will shift the data[n0] to t=0 
    shift_to_0=t[n0]
    UTC_reference_time= "%r:%r:%11.9f" %(timestamp.hour,timestamp.minute,reference_UTC_seconds+shift_to_0)
    
    ##The data window is from n0 to nf, nf being x_max in seconds. Here we have a 500us window if x_max is set to 500e-6
    nf=n0+x_max*fs 
    
    time=t[n0:nf]-shift_to_0
    Ez_data=segments_data[0][n0:nf]
    
    print('UTC reference time: %s' %UTC_reference_time)
#    plt.plot(time*1e6,Ez_data)
#    plt.xlabel('UTC time in microseconds after %s' %UTC_reference_time)
#    plt.show()
    
    ##############################################
    ## Resample to 1MHz (Cummer's sampling rate) #
    ##############################################
    #Ez_data=ss.resample(Ez_data,x_max/1e-6)
    #time=ss.resample(time,x_max/1e-6)
    #plt.plot(time,Ez_data)
    #plt.show()
    
    #########################
    # Moving Average Filter #
    #########################
    def movingaverage(interval, window_size):
        window= np.ones(int(window_size))/float(window_size)
        return np.convolve(interval, window, mode='same')
    
    Moving_Average_Ez=movingaverage(Ez_data,filterwindow)

    ####################
    # Measure Risetime #
    ####################
    def noise_analysis(x,y,fs,t0):
    #        plot(x,y)
    #        print("Please click")
    #        xx = ginput(3)
        xx=[0,0.00006,0.000095] #just for this application! 
        sampling_time=1/fs
    
        t0_noise=np.int(xx[0]/sampling_time)-t0/sampling_time #xx[0][0] when ginput is being used
        tf_noise=np.int(xx[1]/sampling_time)-t0/sampling_time #xx[1][0] when ginput is being used
        t_end=np.int(xx[2]/sampling_time)-t0/sampling_time #xx[2][0] when ginput is being used        
    #        show()  
        
        t_max=np.argmax(y[0:t_end])
        y_topeak=y[0:t_max]
        y_afterpeak=y[t_max:-1]
        noise_data_window=y_topeak[t0_noise:tf_noise]
        sigma=np.std(noise_data_window)
        mean=np.mean(noise_data_window)
    
        min_ind=np.argmax(np.abs(1.0/((mean+4*sigma)-y_topeak)))   
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
#        plt.plot(x,y, 'b', \
#        x[t0_noise:tf_noise],y[t0_noise:tf_noise], 'g', \
#        [x[0],x[-1]],[mean,mean], 'r', \
#        [x[0],x[-1]],[mean+sigma,mean+sigma], '--r', \
#        [x[0],x[-1]],[mean-sigma,mean-sigma], '--r', \
#        x[min_ind],y[min_ind],'og',\
#        x[five_percent_ind],y[five_percent_ind],'oy',\
#        [x[ten_percent_ind],x[ninety_percent_ind]],[y[ten_percent_ind],y[ninety_percent_ind]], 'or',\
#        [x[fifty_percent_ind],x[fifty_percent_afterpeak_ind]],[y[fifty_percent_ind],y[fifty_percent_afterpeak_ind]],'oc')
#        plt.show()
        
        return risetime_90_10_time, ten_percent_ind, min_ind, y_ampl, mean,\
        twenty_percent_ind, fifty_percent_ind, eighty_percent_ind,\
        ninety_percent_ind, risetime_90_10, curve_peak, t_max, five_percent_to_peak_time
        
        
    #    time2=time-group_delay
    #    LPF_skywave = noise_analysis(time2,filtered_skywave,10e6,0)
    #    print("LPF 10-90 risetime = %r" %LPF_skywave[0])
    #    
    MovAvg_skywave = noise_analysis(time[10:-10],Moving_Average_Ez[10:-10],fs,0) 
    risetime_10_90=MovAvg_skywave[0]
    ten_percent_level=MovAvg_skywave[1]*(1/fs)
    ground_wave_start=MovAvg_skywave[2]*(1/fs)
    ground_wave_ampl=MovAvg_skywave[3]
    ground_wave_max=MovAvg_skywave[10]
    ground_wave_time_peak=MovAvg_skywave[11]*(1/fs)
    min_ampl=MovAvg_skywave[4]
    five_percent_to_peak_time=MovAvg_skywave[12]
    print("Moving Average 10-90 risetime = %r" %MovAvg_skywave[0])
    
    time=time+ground_wave_start
    reference_UTC_seconds=reference_UTC_seconds+shift_to_0-ground_wave_start
    UTC_reference_time = "%r:%r:%11.9f" %(timestamp.hour,timestamp.minute,reference_UTC_seconds)
    #    unfiltered = noise_analysis(time,skywave,10e6,0)
    #    print("Unfiltered 10-90 risetime = %r" %unfiltered[0])
    
    return time, Moving_Average_Ez, UTC_reference_time, risetime_10_90, ten_percent_level,\
    ground_wave_start, ground_wave_ampl, min_ampl, ground_wave_max, ground_wave_time_peak,\
    Ez_data, timestamp, reference_UTC_seconds,five_percent_to_peak_time