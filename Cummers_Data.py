# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 11:32:13 2016

@author: lenz
"""
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from Skywaves_plot_with_IRIG_LPF import Skywave
import matplotlib
matplotlib.rcParams.update({'font.size': 16})
plt.figure(figsize=(15.8,10.9))
fs=10e6

date=82715
calfactor=19900.50 #for plotting current
x_min=0*1e6
x_max=0.00050*1e6

yoffset=0.2
distance=208.9 #kilometers
dt_70km=(2*np.sqrt(70*70+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=70km
dt_80km=(2*np.sqrt(80*80+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=80km
dt_90km=(2*np.sqrt(90*90+(distance/2)*(distance/2))-distance)/2.99e5 #time delay of the first skywave for ionospheric reflection height=90km
print("70km = %5.2f, 80 km = %5.2f, 90 km = %5.2f (in microseconds)"%(dt_70km*1e6,dt_80km*1e6,dt_90km*1e6))

# Remove 60 Hz slope ##                  
def remove_60Hz_slope(moving_avg,yoffset):
    x0=moving_avg[0][10]
    x1=moving_avg[0][4990] #500 us  = 5000 samples at 10MHz fs
    
    y0=moving_avg[1][10]
    y1=moving_avg[1][4990] 
    m=(y1-y0)/(x1-x0)
#    m=m/moving_avg[8] #account for GW amplitude normalization
    b=-m*x0*y0
            
    slope=m*moving_avg[0][10:-10]+b #y=mx+b
    modified_yoffset=yoffset+slope
    
    return modified_yoffset

def process_and_plot(moving_avg):
    waveform=moving_avg[1][10:8000] #500 us of e-field data
    first_time=moving_avg[0][10]*1e6 #first sample of the waveform above
    yoffset=np.mean(waveform[0:800]) #find the DC offset during noise window
    
    modified_yoffset=remove_60Hz_slope(moving_avg, yoffset) #remove 60Hz slope

    t_peak=(np.argmax(waveform-modified_yoffset[10:8000]))*(1/fs)*1e6 #find GW peak
    t_start=moving_avg[5]*1e6 #This sets GW to t=0 based on 4 sigma from noise
    adjust_peaks_in_time=t_peak-t_start+first_time #This sets GW to t=0 by alligning GW peaks
    
    time_list=moving_avg[0][10:8000]*1e6-t_start-adjust_peaks_in_time
    data_list=waveform-modified_yoffset[10:8000]
    
    return time_list, data_list, t_start


cummers_data=sio.loadmat('FIT_LF_20150827_232426.mat')
time=cummers_data['FIT_LF_20150827_232426_Time_Sec']
data=cummers_data['FIT_LF_20150827_232426_Bphi_nT']

#dt=0.056626370 #UF 15-38, RS#2
dt=0 #UF 15-38, RS#1
plt.plot((time[0]-26.523-dt)*1e6-500-242.53,(1/0.85)*data[0]/(np.max(data[0])),\
        linewidth=2.0,color=[1,0,0],label="DUKE LF $B_\phi$ Data at 250 km")
plt.xlabel('Time ($\mu$s)')# after 23:24:26.5801')
plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
plt.xlim(-90,410)
if dt==0:
    plt.title("UF 15-38, RS#1")
    moving_avg=Skywave(38,1,26.522908895,8,x_max,10)  #UF 15-38. RS#1
else:
    plt.title("UF 15-38, RS#2")
    moving_avg=Skywave(38,2,26.579535265,8,x_max,10) #UF 15-38. RS#2 *


time, data, t_start = process_and_plot(moving_avg)
plt.plot(time,data/(np.max(data)),linewidth=2.0,\
         color=[0,0,1],label="UF Wideband $E_z$ Data at 209 km") #moving averaged skywave
plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 90 km h iono
plt.legend()
plt.grid()

plt.show()
 