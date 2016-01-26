# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:56:12 2015

@author: lenz
This code plots the skywaves associated with the biggest currents for 6
events. Skywave_plot_with_IRIG_LPF returns: moving_avg[0] (time list), 
moving_avg[1] (filtered skywave (moving average) list) and moving_avg[2] 
(UTC_time string), risetime_10_90, ten_percent_level, ground_wave_start,
ground_wave_ampl, and min_ampl

[10:-10] is added when plotting to avoid showing the overshoot at the ends of
the waveforms causeed by the moving average filter
"""
from Skywaves_plot_with_IRIG_LPF import Skywave
import matplotlib.pyplot as plt
import numpy as np
import lecroy as lc
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
    x1=moving_avg[0][500e-6*fs -10] #500 us  = 5000 samples at 10MHz fs
    
    y0=moving_avg[1][10]
    y1=moving_avg[1][500e-6*fs -10] 
    m=(y1-y0)/(x1-x0)
#    m=m/moving_avg[8] #account for GW amplitude normalization
    b=-m*x0*y0
            
    slope=m*moving_avg[0][10:-10]+b #y=mx+b
    modified_yoffset=yoffset+slope
    return modified_yoffset

def process_and_plot(moving_avg):
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

#UF 15-40, RS#3
moving_avg_gw=Skywave(40,3,20.767465080,10,x_max,10)
moving_avg_ir=Skywave(40,3,20.767465080,10,x_max,50)
def apply_two_filters(moving_avg_gw,moving_avg_ir):
    
    #The code plots Fig. 1 of the Paper
    time, data, t_start,raw_time_list,raw_data_list = process_and_plot(moving_avg_gw)
    time2, data2, t_start2,raw_time_list2,raw_data_list2 = process_and_plot(moving_avg_ir)
    time_gw=time[:2380]
    data_gw=data[:2380]
    time_ir=time2[2370:]
    data_ir=data2[2370:]
    return time_gw, data_gw, time_ir, data_ir, raw_time_list, raw_data_list, t_start 

##!!!!!!Plot Fig.1!!!!!!!
#temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
#time_gw=temp[0]
#data_gw=temp[1]
#time_ir=temp[2]
#data_ir=temp[3]
#raw_time_list=temp[4]
#raw_data_list=temp[5]
#
#plt.subplot(211)
#plt.plot(raw_time_list,raw_data_list,linewidth=2.0,color=[1,0,0],label="Raw UF 15-40, RS#3")
#plt.plot(time_gw,data_gw,linewidth=2.0,color=[0,0,1],label="Filtered UF 15-40, RS#3") #moving averaged skywave
#plt.plot(time_ir, data_ir,linewidth=2.0,color=[0,0,1]) #moving averaged skywave
#
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 90 km h iono
#plt.xlabel(moving_avg_gw[2])
#plt.legend()
#plt.grid()
#
#plt.subplot(223)
#plt.plot(raw_time_list,raw_data_list,linewidth=2.0,color=[1,0,0],label="Raw UF 15-40, RS#3")
#plt.plot(time_gw,data_gw,linewidth=2.0,color=[0,0,1],label="Filtered UF 15-40, RS#3") #moving averaged skywave
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.legend()
#plt.grid()
#plt.xlim(-10,40)
##plt.ylim(0,1.1)
#
#plt.subplot(224)
#plt.plot(raw_time_list,raw_data_list,linewidth=2.0,color=[1,0,0],label="Raw UF 15-40, RS#3")
#plt.plot(time_ir,data_ir,linewidth=2.0,color=[0,0,1],label="Filtered UF 15-40, RS#3") #moving averaged skywave
#plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
#plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 70 km h iono
#plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 80 km h iono
#plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 90 km h iono
#plt.legend()
#plt.xlim(180,240)
#plt.ylim(-0.12,0.28)
#plt.grid()
#
#plt.show()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!Plot Fig.2!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#UF 15-38, RS#1

#Plot channel-base current
suffix26=0
seg=0
lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
                        str(suffix26)+".trc"
lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
IIHI_time = lecroy_IIHI.get_seg_time()
IIHI = lecroy_IIHI.get_segments()
plt.subplot(321)
plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Channel-base Current (kA)")
plt.xlim(0,500)
plt.ylim(-1,16.1)
plt.grid()
plt.title("UF 15-38, RS#1, Peak Current = 15.1 kA")

#Plot DBY Data
moving_avg_gw=Skywave(38,1,26.522908895,8,x_max,10)   
moving_avg_ir=Skywave(38,1,26.522908895,8,x_max,50) 

temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
time_gw=temp[0]
data_gw=temp[1]
time_ir=temp[2]
data_ir=temp[3]
raw_time_list=temp[4]
raw_data_list=temp[5]
t_start=temp[6]

plt.subplot(322)
plt.plot(time_gw,data_gw,linewidth=2.0,color=[1/6,1,1],label="UF 15-38, RS#1") #moving averaged skywave
plt.plot(time_ir, data_ir,linewidth=2.0,color=[1/6,1,1]) #moving averaged skywave
plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 90 km h iono
plt.title("Event UF 15-38, 1st Return Stroke")
plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min-t_start,x_max-t_start)
plt.ylim(-0.11,0.9)

#UF 15-39, RS#1
#Plot channel-base current
suffix26=1
seg=0
lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
                        str(suffix26)+".trc"
lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
IIHI_time = lecroy_IIHI.get_seg_time()
IIHI = lecroy_IIHI.get_segments()
plt.subplot(323)
plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Channel-base Current (kA)")
plt.xlim(0,500)
plt.ylim(-1,5.4)
plt.grid()
plt.title("UF 15-39, RS#1, Peak Current = 4.4 kA")

#Plot DBY Data
moving_avg_gw=Skywave(39,1,66.583436840,9,x_max,10)   
moving_avg_ir=Skywave(39,1,66.583436840,9,x_max,50) 

temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
time_gw=temp[0]
data_gw=temp[1]
time_ir=temp[2]
data_ir=temp[3]
raw_time_list=temp[4]
raw_data_list=temp[5]
t_start=temp[6]

plt.subplot(324)
plt.plot(time_gw,data_gw,linewidth=2.0,color=[2/6,5/6,1],label="UF 15-39, RS#1") #moving averaged skywave
plt.plot(time_ir, data_ir,linewidth=2.0,color=[2/6,5/6,1]) #moving averaged skywave
plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 90 km h iono
plt.title("Event UF 15-39, 1st Return Stroke")
plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min-t_start,x_max-t_start)
plt.ylim(-0.05,0.48)

#UF 15-40, RS#3
#Plot channel-base current
suffix26=2
seg=1
lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
                        str(suffix26)+".trc"
lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
IIHI_time = lecroy_IIHI.get_seg_time()
IIHI = lecroy_IIHI.get_segments()
plt.subplot(325)
plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Channel-base Current (kA)")
plt.xlim(0,500)
plt.ylim(-1,20.1)
plt.grid()
plt.title("UF 15-40, RS#3, Peak Current = 19.1 kA")

#Plot DBY Data
moving_avg_gw=Skywave(40,3,20.767465080,10,x_max,10)   
moving_avg_ir=Skywave(40,3,20.767465080,10,x_max,50) 

temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
time_gw=temp[0]
data_gw=temp[1]
time_ir=temp[2]
data_ir=temp[3]
raw_time_list=temp[4]
raw_data_list=temp[5]
t_start=temp[6]

plt.subplot(326)
plt.plot(time_gw,data_gw,linewidth=2.0,color=[3/6,4/6,1],label="UF 15-40, RS#3") #moving averaged skywave
plt.plot(time_ir, data_ir,linewidth=2.0,color=[3/6,4/6,1]) #moving averaged skywave
plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 90 km h iono
plt.title("Event UF 15-40, 3rd Return Stroke")
plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min-t_start,x_max-t_start)
plt.ylim(-0.09,0.81)
plt.show()

#UF 15-41, RS#1
#Plot channel-base current
suffix26=3
seg=0
lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
                        str(suffix26)+".trc"
lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
IIHI_time = lecroy_IIHI.get_seg_time()
IIHI = lecroy_IIHI.get_segments()
plt.subplot(321)
plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Channel-base Current (kA)")
plt.xlim(0,500)
plt.ylim(-1,14.7)
plt.grid()
plt.title("UF 15-41, RS#1, Peak Current = 13.7 kA")

#Plot DBY Data
moving_avg_gw=Skywave(41,1,57.298446790,11,x_max,10)   
moving_avg_ir=Skywave(41,1,57.298446790,11,x_max,50) 

temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
time_gw=temp[0]
data_gw=temp[1]
time_ir=temp[2]
data_ir=temp[3]
raw_time_list=temp[4]
raw_data_list=temp[5]
t_start=temp[6]

plt.subplot(322)
plt.plot(time_gw,data_gw,linewidth=2.0,color=[4/6,3/6,1],label="UF 15-41, RS#1") #moving averaged skywave
plt.plot(time_ir, data_ir,linewidth=2.0,color=[4/6,3/6,1]) #moving averaged skywave
plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 90 km h iono
plt.title("Event UF 15-41, 1st Return Stroke")
plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min-t_start,x_max-t_start)
plt.ylim(-0.12,0.52)


#UF 15-42, RS#4
#Plot channel-base current
suffix26=4
seg=2
lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
                        str(suffix26)+".trc"
lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
IIHI_time = lecroy_IIHI.get_seg_time()
IIHI = lecroy_IIHI.get_segments()
plt.subplot(323)
plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Channel-base Current (kA)")
plt.xlim(0,500)
plt.ylim(-1,23.5)
plt.grid()
plt.title("UF 15-42, RS#4, Peak Current = 22.5 kA")

#Plot DBY Data
moving_avg_gw=Skywave(42,4,43.058185590,12,x_max,10)   
moving_avg_ir=Skywave(42,4,43.058185590,12,x_max,50) 

temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
time_gw=temp[0]
data_gw=temp[1]
time_ir=temp[2]
data_ir=temp[3]
raw_time_list=temp[4]
raw_data_list=temp[5]
t_start=temp[6]

plt.subplot(324)
plt.plot(time_gw,data_gw,linewidth=2.0,color=[5/6,2/6,1],label="UF 15-42, RS#4") #moving averaged skywave
plt.plot(time_ir, data_ir,linewidth=2.0,color=[5/6,2/6,1]) #moving averaged skywave
plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 90 km h iono
plt.title("Event UF 15-42, 4th Return Stroke")
plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min-t_start,x_max-t_start)
plt.ylim(-0.1,0.82)

#UF 15-43, RS#4
#Plot channel-base current
suffix26=5
seg=3
lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+ \
                        str(suffix26)+".trc"
lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
IIHI_time = lecroy_IIHI.get_seg_time()
IIHI = lecroy_IIHI.get_segments()
plt.subplot(325)
plt.plot((IIHI_time-2.4e-3)*1e6,IIHI[seg]*calfactor/1000,color=[0.3, 0.3, 0.3],linewidth=2)
plt.xlabel("Time ($\mu$s)")
plt.ylabel("Channel-base Current (kA)")
plt.xlim(0,500)
plt.ylim(-1,21.5)
plt.grid()
plt.title("UF 15-43, RS#4, Peak Current = 20.5 kA")

#Plot DBY Data
moving_avg_gw=Skywave(43,4,23.293418545,13,x_max,10)   
moving_avg_ir=Skywave(43,4,23.293418545,13,x_max,50) 

temp=apply_two_filters(moving_avg_gw,moving_avg_ir)
time_gw=temp[0]
data_gw=temp[1]
time_ir=temp[2]
data_ir=temp[3]
raw_time_list=temp[4]
raw_data_list=temp[5]
t_start=temp[6]

plt.subplot(326)
plt.plot(time_gw,data_gw,linewidth=2.0,color=[1,1/6,1],label="UF 15-43, RS#4") #moving averaged skywave
plt.plot(time_ir, data_ir,linewidth=2.0,color=[1,1/6,1]) #moving averaged skywave
plt.plot([0,0],[-1,1.5],'--',linewidth=2.0) #time when skywave raises 3 std dev from mean noise
plt.plot([(dt_70km)*1e6,(dt_70km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 70 km h iono
plt.plot([(dt_80km)*1e6,(dt_80km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 80 km h iono
plt.plot([(dt_90km)*1e6,(dt_90km)*1e6],[-1,1.5],'--',linewidth=2.0) #time for 90 km h iono
plt.title("Event UF 15-43, 4th Return Stroke")
plt.xlabel("UTC time in $\mu$s after %s"%moving_avg_gw[2])
plt.ylabel("E-field (arb. units) \n measured 209 km SE of ICLRT")
plt.grid()
plt.xlim(x_min-t_start,x_max-t_start)
plt.ylim(-.13,0.78)


plt.show()
