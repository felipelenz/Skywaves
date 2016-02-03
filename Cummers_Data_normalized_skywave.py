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

def process_and_plotv2(moving_avg):
    waveform=moving_avg[1][10:4990] #500 us of e-field data
    raw_waveform=moving_avg[10][10:4990] #500 us of e-field data
    
    first_time=moving_avg[0][10]*1e6 #first sample of the waveform above
    yoffset=np.mean(waveform[0:800]) #find the DC offset during noise window
    
    modified_yoffset=remove_60Hz_slope(moving_avg, yoffset) #remove 60Hz slope

    t_peak=(np.argmax(waveform-modified_yoffset[10:4990]))*(1/fs)*1e6 #find GW peak
    raw_t_peak=(np.argmax(raw_waveform-modified_yoffset[10:4990]))*(1/fs)*1e6 #find GW peak
    t_start=moving_avg[5]*1e6 #This sets GW to t=0 based on 4 sigma from noise
    adjust_peaks_in_time=t_peak-t_start+first_time #This sets GW to t=0 by alligning GW peaks
    raw_adjust_peaks_in_time=raw_t_peak-t_start+first_time #This sets GW to t=0 by alligning GW peaks
    
    time_list=moving_avg[0][10:4990]*1e6-t_start-adjust_peaks_in_time
    data_list=waveform-modified_yoffset[10:4990]
    raw_data_list=raw_waveform-modified_yoffset[10:4990]
    raw_time_list=moving_avg[0][10:4990]*1e6-t_start-raw_adjust_peaks_in_time
    return time_list, data_list, t_start, raw_time_list, raw_data_list
    
def apply_two_filters(moving_avg_gw,moving_avg_ir):
    
    #The code plots Fig. 1 of the Paper
    time, data, t_start,raw_time_list,raw_data_list = process_and_plotv2(moving_avg_gw)
    time2, data2, t_start2,raw_time_list2,raw_data_list2 = process_and_plotv2(moving_avg_ir)
    time_gw=time[:2380]
    data_gw=data[:2380]
    time_ir=time2[2370:]
    data_ir=data2[2370:]
    return time_gw, data_gw, time_ir, data_ir, raw_time_list, raw_data_list, t_start 

#UF 15-38
cummers_data=sio.loadmat('FIT_LF_20150827_232426.mat')
time=cummers_data['FIT_LF_20150827_232426_Time_Sec']
data=cummers_data['FIT_LF_20150827_232426_Bphi_nT']

dt=0.056626370 #UF 15-38, RS#2
#dt=0 #UF 15-38, RS#1
plt.plot((time[0]-26.523-dt)*1e6-500-242.53,data[0]/np.max(data[0])/0.321,\
        linewidth=2.0,color=[1,0,0],label="DUKE LF $B_\phi$ Data at 250 km")
plt.xlabel('Time ($\mu$s)')# after 23:24:26.5801')
plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
plt.xlim(100,300)
if dt==0:
    plt.title("UF 15-38, RS#1")
    moving_avg=Skywave(38,1,26.522908895,8,x_max,50)  #UF 15-38. RS#1
else:
    plt.title("UF 15-38, RS#2")
    moving_avg=Skywave(38,2,26.579535265,8,x_max,50) #UF 15-38. RS#2 *


time, data, t_start = process_and_plot(moving_avg)
plt.plot(time,data/np.max(data)/0.260,linewidth=2.0,\
         color=[0,0,1],label="UF Wideband $E_z$ Data at 209 km") #moving averaged skywave
plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.legend()
plt.grid()
##
#plt.show()

##UF 15-39, RS#1
#cummers_data=sio.loadmat('FIT_LF_20150827_233206.mat')
#time=cummers_data['FIT_LF_20150827_233206_Time_Sec']
#data=cummers_data['FIT_LF_20150827_233206_Bphi_nT']
#manual_norm_factor=0.2467
#plt.plot((time[0]-6.58427)*1e6-0.988,data[0]/np.max(data[0])/manual_norm_factor,\
#        linewidth=2.0,color=[1,0,0],label="DUKE LF $B_\phi$ Data at 250 km")
#plt.xlabel('Time ($\mu$s)')# after 23:24:26.5801')
#plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
##
##Plot DBY Data
#moving_avg_gw=Skywave(39,1,66.583436840,9,x_max,10)   
#moving_avg_ir=Skywave(39,1,66.583436840,9,x_max,50) 
#
#temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
#time_gw=temp[0]
#data_gw=temp[1]
#time_ir=temp[2]
#data_ir=temp[3]
#raw_time_list=temp[4]
#raw_data_list=temp[5]
#t_start=temp[6]
#
#
#plt.plot(time_gw,data_gw/np.max(data_ir),linewidth=2.0,color=[0,0,1],label="UF Wideband $E_z$ Data at 209 km") #moving averaged skywave
#plt.plot(time_ir, data_ir/np.max(data_ir),linewidth=2.0,color=[0,0,1]) #moving averaged skywave
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.title("Event UF 15-39, 1st Return Stroke")
##plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
##plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#plt.legend()
#plt.title("UF 15-39, RS#1")
#plt.grid()
#plt.xlim(100,300)
##plt.ylim(-.4,1.1)
##
##plt.show()


##UF 15-39, RS#2
#cummers_data=sio.loadmat('FIT_LF_20150827_233206.mat')
#time=cummers_data['FIT_LF_20150827_233206_Time_Sec']
#data=cummers_data['FIT_LF_20150827_233206_Bphi_nT']
#manual_norm_factor=0.038
#plt.plot((time[0]-6.58427)*1e6-0.988-3116-10.959,data[0]/np.max(data[0])/manual_norm_factor,\
#         linewidth=2.0,color=[1,0,0],label="DUKE LF $B_\phi$ Data at 250 km")
#plt.xlabel('Time ($\mu$s)')# after 23:24:26.5801')
#plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
##
##Plot DBY Data
#moving_avg_gw=Skywave(39,2,66.586552840,9,x_max,10)   
#moving_avg_ir=Skywave(39,2,66.586552840,9,x_max,50) 
#
#temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
#time_gw=temp[0]
#data_gw=temp[1]
#time_ir=temp[2]
#data_ir=temp[3]
#raw_time_list=temp[4]
#raw_data_list=temp[5]
#t_start=temp[6]
#
#
#plt.plot(time_gw,data_gw/np.max(data_ir),linewidth=2.0,color=[0,0,1],label="UF Wideband $E_z$ Data at 209 km") #moving averaged skywave
#plt.plot(time_ir, data_ir/np.max(data_ir),linewidth=2.0,color=[0,0,1]) #moving averaged skywave
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.title("Event UF 15-39, 2nd Return Stroke")
###plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
###plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#plt.legend()
#plt.title("UF 15-39, RS#2")
#plt.grid()
#plt.xlim(100,300)
#plt.ylim(-.4,1.1)
#
##plt.show()

##UF 15-40, RS#2
#cummers_data=sio.loadmat('FIT_LF_20150827_234120.mat')
#time=cummers_data['FIT_LF_20150827_234120_Time_Sec']
#data=cummers_data['FIT_LF_20150827_234120_Bphi_nT']
#manual_norm_factor=0.212
#plt.plot((time[0]-20.746971600)*1e6-833.393,data[0]/np.max(data[0])/manual_norm_factor,\
#        linewidth=2.0,color=[1,0,0],label="DUKE LF $B_\phi$ Data at 250 km")
#plt.xlabel('Time ($\mu$s)')# after 23:24:26.5801')
#plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#
##Plot DBY Data
#moving_avg_gw=Skywave(40,2,20.746971600,10,x_max,10)   
#moving_avg_ir=Skywave(40,2,20.746971600,10,x_max,50) 
#
#temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
#time_gw=temp[0]
#data_gw=temp[1]
#time_ir=temp[2]
#data_ir=temp[3]
#raw_time_list=temp[4]
#raw_data_list=temp[5]
#t_start=temp[6]
#
#
#plt.plot(time_gw,data_gw/np.max(data_ir),linewidth=2.0,color=[0,0,1],label="UF Wideband $E_z$ Data at 209 km") #moving averaged skywave
#plt.plot(time_ir, data_ir/np.max(data_ir),linewidth=2.0,color=[0,0,1]) #moving averaged skywave
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.title("Event UF 15-40, 2nd Return Stroke")
###plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
###plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#plt.legend()
#plt.title("UF 15-40, RS#2")
#plt.grid()
#plt.xlim(100,300)
#plt.ylim(-.4,1.1)
##
###plt.show()

##UF 15-40, RS#3
#cummers_data=sio.loadmat('FIT_LF_20150827_234120.mat')
#time=cummers_data['FIT_LF_20150827_234120_Time_Sec']
#data=cummers_data['FIT_LF_20150827_234120_Bphi_nT']
#manual_norm_factor=0.2745
#plt.plot((time[0]-20.7683)*1e6+1.005,data[0]/np.max(data[0])/manual_norm_factor,\
#        linewidth=2.0,color=[1,0,0],label="DUKE LF $B_\phi$ Data at 250 km")
#plt.xlabel('Time ($\mu$s)')# after 23:24:26.5801')
#plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#
##Plot DBY Data
#moving_avg_gw=Skywave(40,3,20.767465080,10,x_max,10)   
#moving_avg_ir=Skywave(40,3,20.767465080,10,x_max,50) 
#
#temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
#time_gw=temp[0]
#data_gw=temp[1]
#time_ir=temp[2]
#data_ir=temp[3]
#raw_time_list=temp[4]
#raw_data_list=temp[5]
#t_start=temp[6]
#
#
#plt.plot(time_gw,data_gw/np.max(data_ir),linewidth=2.0,color=[0,0,1],label="UF Wideband $E_z$ Data at 209 km") #moving averaged skywave
#plt.plot(time_ir, data_ir/np.max(data_ir),linewidth=2.0,color=[0,0,1]) #moving averaged skywave
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.title("Event UF 15-40, 3rd Return Stroke")
###plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
###plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#plt.legend()
#plt.title("UF 15-40, RS#3")
#plt.grid()
#plt.xlim(100,300)
#plt.ylim(-.4,1.1)
##
##plt.show()

##UF 15-41, RS#1
#cummers_data=sio.loadmat('FIT_LF_20150827_234357.mat')
#time=cummers_data['FIT_LF_20150827_234357_Time_Sec']
#data=cummers_data['FIT_LF_20150827_234357_Bphi_nT']
#manual_norm_factor=0.432
#plt.plot((time[0]-57.2993)*1e6+20,data[0]/np.max(data[0])/manual_norm_factor,\
#         linewidth=2.0,color=[1,0,0],label="DUKE LF $B_\phi$ Data at 250 km")
#plt.xlabel('Time ($\mu$s)')# after 23:24:26.5801')
#plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#
##Plot DBY Data
#moving_avg_gw=Skywave(41,1,57.298446790,11,x_max,10)   
#moving_avg_ir=Skywave(41,1,57.298446790,11,x_max,50) 
#
#temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
#time_gw=temp[0]
#data_gw=temp[1]
#time_ir=temp[2]
#data_ir=temp[3]
#raw_time_list=temp[4]
#raw_data_list=temp[5]
#t_start=temp[6]
#
#
#plt.plot(time_gw,data_gw/np.max(data_ir),linewidth=2.0,color=[0,0,1],label="UF Wideband $E_z$ Data at 209 km") #moving averaged skywave
#plt.plot(time_ir, data_ir/np.max(data_ir),linewidth=2.0,color=[0,0,1]) #moving averaged skywave
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.title("Event UF 15-41, 1st Return Stroke")
##plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
#plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#plt.legend()
#plt.title("UF 15-41, RS#1")
#plt.grid()
#plt.xlim(100,300)
#plt.ylim(-.4,1.1)
#
#plt.show()


##UF 15-42, RS#4
#cummers_data=sio.loadmat('FIT_LF_20150827_234743.mat')
#time=cummers_data['FIT_LF_20150827_234743_Time_Sec']
#data=cummers_data['FIT_LF_20150827_234743_Bphi_nT']
#manual_norm_factor=0.233
#plt.plot((time[0]-43.059)*1e6-20.005,data[0]/np.max(data[0])/manual_norm_factor,\
#        linewidth=2.0,color=[1,0,0],label="DUKE LF $B_\phi$ Data at 250 km")
#plt.xlabel('Time ($\mu$s)')# after 23:24:26.5801')
#plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#
##Plot DBY Data
#moving_avg_gw=Skywave(42,4,43.058185590,12,x_max,10)   
#moving_avg_ir=Skywave(42,4,43.058185590,12,x_max,50) 
#
#temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
#time_gw=temp[0]
#data_gw=temp[1]
#time_ir=temp[2]
#data_ir=temp[3]
#raw_time_list=temp[4]
#raw_data_list=temp[5]
#t_start=temp[6]
#
#
#plt.plot(time_gw,data_gw/np.max(data_ir),linewidth=2.0,color=[0,0,1],label="UF Wideband $E_z$ Data at 209 km") #moving averaged skywave
#plt.plot(time_ir, data_ir/np.max(data_ir),linewidth=2.0,color=[0,0,1]) #moving averaged skywave
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.title("Event UF 15-42, 4th Return Stroke")
###plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
###plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#plt.legend()
#plt.title("UF 15-42, RS#4")
#plt.grid()
#plt.xlim(100,300)
#plt.ylim(-.4,1.1)

#plt.show()


##UF 15-43, RS#4
#cummers_data=sio.loadmat('FIT_LF_20150827_235323.mat')
#time=cummers_data['FIT_LF_20150827_235323_Time_Sec']
#data=cummers_data['FIT_LF_20150827_235323_Bphi_nT']
#
#manual_norm_factor=0.2177
#plt.plot((time[0]-23.2943)*1e6+46.02,data[0]/np.max(data[0])/manual_norm_factor,\
#        linewidth=2.0,color=[1,0,0],label="DUKE LF $B_\phi$ Data at 250 km")
#plt.xlabel('Time ($\mu$s)')# after 23:24:26.5801')
#
##Plot DBY Data
#moving_avg_gw=Skywave(43,4,23.293418545,13,x_max,10)   
#moving_avg_ir=Skywave(43,4,23.293418545,13,x_max,50)
#
#temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
#time_gw=temp[0]
#data_gw=temp[1]
#time_ir=temp[2]
#data_ir=temp[3]
#raw_time_list=temp[4]
#raw_data_list=temp[5]
#t_start=temp[6]
#
#
#plt.plot(time_gw,data_gw/np.max(data_ir),linewidth=2.0,color=[0,0,1],label="UF Wideband $E_z$ Data at 209 km") #moving averaged skywave
#plt.plot(time_ir, data_ir/np.max(data_ir),linewidth=2.0,color=[0,0,1]) #moving averaged skywave
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.title("Event UF 15-43, 4th Return Stroke")
##plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
#plt.ylabel('Amplitude normalized E (blue) and B (red) fields')
#plt.legend()
#plt.title("UF 15-43, RS#4")
#plt.grid()
#plt.xlim(100,300)
#plt.ylim(-.4,1.1)

plt.show()