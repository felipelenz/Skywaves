# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:48:47 2015

@author: lenz
This code finds skywaves that happened at a specified (input) UTC time,
applies two filters to the data (low pass and moving average), the measures
the risetime of the signal.
"""
from __future__ import division
import lecroy as lc
import numpy as np
import matplotlib.pyplot as plt
import IRIGA
from pylab import ginput, plot, show
from scipy.signal import butter, lfilter

####################
# Input Parameters #
####################
fs=10e6 #sampling rate
event=38 #event name
RS_number=2 #return stroke number
RS_time=26.579535265 #seconds of the XLI time stamp (for trigger lightning) 
                    #this time can be found in the triggered lightning reports
x_max=0.00035 #xlim max for plotting the skywaves

##############
# Read Files #
##############
#import IRIG file
lecroy_fileName_DBY_IRIG = "/Volumes/Promise 12TB RAID5/2015 Data/082715/DBY Data/C2DBY00008.trc"
lecroy_DBY_IRIG= lc.lecroy_data(lecroy_fileName_DBY_IRIG)
seg_time_DBY_IRIG = lecroy_DBY_IRIG.get_seg_time()
segments_DBY_IRIG = lecroy_DBY_IRIG.get_segments()

#read IRIG file and print time stamp
timestamp,t =IRIGA.IRIGA_signal(segments_DBY_IRIG[0], fs, year=2015)
print(timestamp)

#import skywaves data
lecroy_fileName_DBY = "/Volumes/Promise 12TB RAID5/2015 Data/082715/DBY Data/C1DBY00008.trc"
lecroy_DBY= lc.lecroy_data(lecroy_fileName_DBY)
seg_time_DBY = lecroy_DBY.get_seg_time()
segments_DBY = lecroy_DBY.get_segments()

t0=RS_time-(timestamp.second+timestamp.microsecond/1e6)+200e3/2.99e8
t0=round(t0*1e9)/1e9
tf=t0+0.5
n0=int((t0-0.5)*fs)
nf=int(tf*fs)
#plt.plot([0,0],[-1,1],t[n0:nf]-t0,segments_DBY[0][n0:nf])
#plt.xlabel('UTC Time in seconds after '+str(timestamp.hour)+':'+str(timestamp.minute)+':'+str(round((timestamp.second+timestamp.microsecond/1e6+t0)*1e9)/1e9))
#plt.xlim(0,x_max)
#plt.title("UF 15-"+str(event)+ " return stroke #"+str(RS_number) )
#plt.grid()
#plt.show()

skywave=segments_DBY[0][n0:nf];
time=t[n0:nf]-t0;

#chop lists
time=time[int(0.5*fs):int((x_max+0.5)*fs)]
skywave=skywave[int(0.5*fs):int((x_max+0.5)*fs)]
#plt.plot(time,skywave)
#plt.xlim(0,x_max)
#plt.show()

##################################
# take the FFT of skywave signal #
##################################
#skywave_FFT=np.fft.fft(skywave,n=None,axis=-1)
#n=int(len(skywave_FFT))
#freq=[]
#for a in range(0,n):
#    freq.append(a*(fs/n)) #Create frequency list
#plt.plot(freq,20*np.log10(np.abs(skywave_FFT))) #plot magnitude of FFT
#plt.xlabel('Frequency (Hz)')
#plt.ylabel('Magnitude (dB)')
#plt.grid()
#plt.show()

########################
# Low Pass Filter data #
########################
def butter_lowpass(cutoff, fs, order=6):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Filter requirements.
order = 6
fs = 10e6      # sample rate, Hz
cutoff = 0.9e6  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

## Plot the frequency response.
#w, h = freqz(b, a, worN=8000)
#plt.subplot(2, 1, 1)
#plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
#plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
#plt.axvline(cutoff, color='k')
#plt.xlim(0, 0.5*fs)
#plt.title("Lowpass Filter Frequency Response")
#plt.xlabel('Frequency [Hz]')
#plt.grid()

# Filter the data, and plot both the original and filtered signals.
filtered_skywave = butter_lowpass_filter(skywave, cutoff, fs, order)
group_delay=.6e-6
plt.plot(time, skywave, 'b-', label='data')
plt.plot(time-group_delay, filtered_skywave, 'r-', linewidth=2, label='low pass filtered data')
plt.xlim(0,x_max)
plt.title("UF 15-"+str(event)+ " return stroke #"+str(RS_number) )
plt.xlabel('UTC Time in seconds after '+str(timestamp.hour)+':'+str(timestamp.minute)+':'+str(round((timestamp.second+timestamp.microsecond/1e6+t0)*1e9)/1e9))
plt.grid()

#########################
# Moving Average Filter #
#########################
def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')
    
avg_skywave=movingaverage(skywave,10)
plt.plot(time, avg_skywave,'g',linewidth=2, label='moving average data')
plt.legend()
plt.show()

####################
# Measure Risetime #
####################
def noise_analysis(x,y,fs,t0):
    
    plot(x,y)
    print("Please click")
    xx = ginput(3)
    sampling_time=1/fs
    t0_noise=np.int(xx[0][0]/sampling_time)-t0/sampling_time
    tf_noise=np.int(xx[1][0]/sampling_time)-t0/sampling_time
    t_end=np.int(xx[2][0]/sampling_time)-t0/sampling_time
    show()  
    
    t_max=np.argmax(y[0:t_end])
    y_topeak=y[0:t_max]
    noise_data_window=y_topeak[t0_noise:tf_noise]
    sigma=np.std(noise_data_window)
    mean=np.mean(noise_data_window)

    min_ind=np.argmax(np.abs(1.0/((mean+3*sigma)-y_topeak)))   
    min_ampl=y_topeak[min_ind]
    max_ampl=np.max(y_topeak)
    y_ampl=max_ampl-min_ampl
   
    ten_percent_ind=np.argmax(np.abs(1.0/((0.1*y_ampl+min_ampl)-y_topeak)))  
    twenty_percent_ind=np.argmax(np.abs(1.0/((0.2*y_ampl+min_ampl)-y_topeak))) 
    fifty_percent_ind=np.argmax(np.abs(1.0/((0.5*y_ampl+min_ampl)-y_topeak))) 
    eighty_percent_ind=np.argmax(np.abs(1.0/((0.8*y_ampl+min_ampl)-y_topeak))) 
    ninety_percent_ind=np.argmax(np.abs(1.0/((0.9*y_ampl+min_ampl)-y_topeak))) 
    risetime_90_10=ninety_percent_ind-ten_percent_ind
    risetime_90_10_time=risetime_90_10*sampling_time  
    
    print("standard deviation= %.4f noise mean= %.4f"%(sigma,mean))
    plot(x,y, 'b', \
    x[t0_noise:tf_noise],y[t0_noise:tf_noise], 'g', \
    [x[0],x[-1]],[mean,mean], 'r', \
    [x[0],x[-1]],[mean+sigma,mean+sigma], '--r', \
    [x[0],x[-1]],[mean-sigma,mean-sigma], '--r', \
    [x[min_ind],x[ten_percent_ind],x[ninety_percent_ind]],[y[min_ind],y[ten_percent_ind],y[ninety_percent_ind]], 'or')
    show()
    
    return risetime_90_10_time,ten_percent_ind,twenty_percent_ind,fifty_percent_ind,eighty_percent_ind,ninety_percent_ind,risetime_90_10
    
time2=time-group_delay
LPF_skywave = noise_analysis(time2,filtered_skywave,10e6,0)
print("LPF 10-90 risetime = %r" %LPF_skywave[0])

MovAvg_skywave = noise_analysis(time,avg_skywave,10e6,0)
print("Moving Average 10-90 risetime = %r" %MovAvg_skywave[0])

unfiltered = noise_analysis(time,skywave,10e6,0)
print("Unfiltered 10-90 risetime = %r" %unfiltered[0])