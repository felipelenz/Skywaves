# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 16:13:52 2016
This code does the following:

1) Removes 60 Hz noise of data
2) Applies a moving average filter
3) Chops the data array into two datasets: One containing the groundwave and
one containing the skywave
4) Zero pads data before and after 
5) Evaluates the FFT of the signal
6) Plots the mag^2 of the FFT + the -3dB frequency cutoff

inputs: The same as for read_DBY
event_number: int (number of the event, e.g. in UF 15-38, 38 is event_number)
RS_number: int (number of the return stroke)
RS_time: float (Xli timestamp %11.9f)
filename_suffix: int (last two digits of the filename, e.g. in C1DBY00008.trc, 08 is filename_suffix)
x_max: float (Time window of the data to be analyzed, e.g. 450e-6)
window_size: int (how many points you are averaging during the movavg filter, e.g. 10)


read_DBY is an updated version of Skywaves_plot_with_IRIG_LPF, but the
UTC time reference output was done much more carefully. 
@author: lenz
"""

from read_DBY import read_DBY
import matplotlib.pyplot as plt
from numpy import fft
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

#########################
# Moving Average Filter #
#########################
def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, mode='valid') 

#############################
# Break data into GW and IR #
#############################
def chop_gw_ir(remove_60Hz_slope_output):
    gw_ir_ref=2500 #we define this sample number to be the point where groundwave 
               #becomes skywave. This point doesn't need to be very well defined
               #we just put it here to make the code cleaner
    gw_time=remove_60Hz_slope_output[0][1:gw_ir_ref]
    gw_data=remove_60Hz_slope_output[1][1:gw_ir_ref]
    ir_time=remove_60Hz_slope_output[0][gw_ir_ref:-1]
    ir_data=remove_60Hz_slope_output[1][gw_ir_ref:-1]
    return gw_time,gw_data,ir_time,ir_data
    
##############
# FFT method #
##############
def take_fft(data,N,Ts):
    Fk=fft.fft(data)/N #Fourier coefficients
    nu=fft.fftfreq(N,Ts) #Natural frequencies
    Fk=fft.fftshift(Fk) #Shift zero frequency to center
    nu=fft.fftshift(nu) #Shift zero freq to center
    return nu, Fk
    
####################
# Plot FFT routine #
####################
def plot_fft(time,data,title_string):
    
    #plot original data
    plt.plot(time,data)
    plt.xlabel('Time in ($\mu s$)')
    plt.ylabel('Filtered E-field')
    plt.show()
    
    #zero pad data to increase frequency resolution
    N=len(data)
    window=np.ones(N)
    pad=np.zeros(N*1e3)
    data=np.append(pad,data)
    data=np.append(data,pad)
    
    window=np.append(pad,window)
    window=np.append(window,pad)
    #plot zero padded data
    plt.plot(data)
    plt.show()
    
    #call fft function
    N=len(data)
    fs=10e6
    Ts=1/fs
    data_FFT=take_fft(data,N,Ts)
    window_FFT=take_fft(window,N,Ts)
    nu=data_FFT[0]
    Fk=data_FFT[1]
    Window_Fk=window_FFT[1]
    
    #plot magnitude squared of fft
    plt.plot(nu*1e-3,np.absolute(Fk)**2/np.max(np.absolute(Fk)**2),label='data')
    plt.plot(nu*1e-3,np.absolute(Window_Fk)**2/np.max(np.absolute(Window_Fk)**2),label='window') #Window spectra
    plt.legend()
    
    max_ampl=np.max(np.absolute(Fk)**2) #find max 
    ampl=np.ones(len(nu))*max_ampl #create an array 
    plt.plot(nu*1e-3,ampl) #Max
    plt.plot(nu*1e-3,ampl/1.995) #3dB drop
    
    index=np.argmax(1/((np.absolute(Fk)**2)-ampl/1.995)) #find closest point to -3dB (half power)
    fc=float(nu[index])*1e-3
    print("3dB frequency cutoff = %3.2f kHz" %np.abs(fc))
    
    #plot 3dB frequency lines
    plt.plot([nu[index]*1e-3,nu[index]*1e-3],[-0.2,1])#[-np.min(np.absolute(Fk)**2),np.max(np.absolute(Fk)**2)])
    plt.plot([-nu[index]*1e-3,-nu[index]*1e-3],[-0.2,1])#[-np.min(np.absolute(Fk)**2),np.max(np.absolute(Fk)**2)]) 
    
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('$|fft|^2/max(|fft|^2)$')
    plt.title(title_string)
    plt.grid()
    plt.xlim(-100,100)
    
    plt.show()
    return
    
##############
# Start Code #
##############
x_max=450e-6

read_DBY_output=read_DBY(38,1,26.522908895,8,x_max,10) #UF 15-38, RS1
#read_DBY_output=read_DBY(38,2,26.579535265,8,x_max,10) #UF 15-38, RS2
#read_DBY_output=read_DBY(38,3,26.691097980,8,x_max,10) #UF 15-38, RS3
#read_DBY_output=read_DBY(43,1,22.706011205,13,x_max,10) #UF 15-43, RS1

remove_60Hz_slope_output=remove_60Hz_slope(read_DBY_output,x_max)
gw_time,gw_data,ir_time,ir_data=chop_gw_ir(remove_60Hz_slope_output)

gw_time=gw_time
gw=gw_data
ir_time=ir_time
ir=ir_data

ir_time=movingaverage(ir_time,50)
ir=movingaverage(ir,50)

plot_fft(gw_time,gw,'UF 15-38, RS#1 Groundwave Spectrum')
plot_fft(ir_time,ir,'UF 15-38, RS#1 Skywave Spectrum')