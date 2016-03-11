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
import pandas
from read_DBY import read_DBY
import matplotlib.pyplot as plt
from numpy import fft
import numpy as np
from scipy import signal
import csv

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
#    window=np.ones(int(window_size))/float(window_size)
#    return pandas.rolling_mean(interval, window)
#def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    filter_delay=((window_size-1)/2)*1/10e6
    return np.convolve(interval, window, mode='valid') ,filter_delay

###################
# Low Pass Filter #
###################
def lowpass(interval,cutoff):
    fs=10e6
    order=5
    
    nyq=0.5*fs #Hz
    normal_cutoff=cutoff/nyq 
    b,a=signal.butter(order,normal_cutoff,'low',analog=False)
    
    w,h=signal.freqz(b,a)
#    plt.semilogx(w*fs/(2*np.pi),np.abs(h))
#    plt.axvline(cutoff)
#    plt.show()
    w,mag,phase=signal.bode((b,a))
    filter_delay=-np.diff(phase)/(2*np.pi)
    plt.plot(w[1:]*fs/(2*np.pi),filter_delay)
    return signal.lfilter(b,a,interval)

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
###########################
# Tukey Window Definition #
###########################
def tukeywin(window_length, alpha=0.5):
    '''The Tukey window, also known as the tapered cosine window, can be regarded as a cosine lobe of width \alpha * N / 2
    that is convolved with a rectangle window of width (1 - \alpha / 2). At \alpha = 1 it becomes rectangular, and
    at \alpha = 0 it becomes a Hann window.
 
    We use the same reference as MATLAB to provide the same results in case users compare a MATLAB output to this function
    output
 
    Reference
    ---------
    http://www.mathworks.com/access/helpdesk/help/toolbox/signal/tukeywin.html
 
    '''
    # Special cases
    if alpha <= 0:
        return np.ones(window_length) #rectangular window
    elif alpha >= 1:
        return np.hanning(window_length)
 
    # Normal case
    x = np.linspace(0, 1, window_length)
    w = np.ones(x.shape)
 
    # first condition 0 <= x < alpha/2
    first_condition = x<alpha/2
    w[first_condition] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[first_condition] - alpha/2) ))
 
    # second condition already taken care of
 
    # third condition 1 - alpha / 2 <= x <= 1
    third_condition = x>=(1 - alpha/2)
    w[third_condition] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[third_condition] - 1 + alpha/2))) 
 
    return w
    
####################
# Plot FFT routine #
####################
def plot_fft(time1,data1,time2,data2,title_string):
    
    #plot original data
    plt.plot(time1,data1,label='data1')
    plt.plot(time2,data2,label='data1')
    plt.legend()
    plt.xlabel('Time in ($\mu s$)')
    plt.ylabel('Filtered E-field')
    plt.show()
    
    def zeropad(data):
    #zero pad data to increase frequency resolution
        N=len(data)
        window=np.ones(N)
#        window=tukeywin(N)
        pad=np.zeros(N*1e3)
        data=np.append(pad,data)
        data=np.append(data,pad)
    
        window=np.append(pad,window)
        window=np.append(window,pad)
        #plot zero padded data
        plt.plot(data)
        plt.show()
        return data,window
        
    padded_data1,padded_window1=zeropad(data1)
    padded_data2,padded_window2=zeropad(data2)
    
    #call fft function
    def callfft(data,window):
        N=len(data)
        fs=10e6
        Ts=1/fs    
        data_FFT=take_fft(data,N,Ts)
        window_FFT=take_fft(window,N,Ts)
        nu=data_FFT[0]
        Fk=data_FFT[1]
#        Window_Fk=window_FFT[1]
        return nu,Fk
    
    nu1, Fk1=callfft(padded_data1*padded_window1,padded_window1)
    nu2, Fk2=callfft(padded_data2*padded_window1,padded_window2)
    
    TF=Fk2/Fk1
    
    Mag=np.absolute(TF)**2 #linear
    Mag_dB=20*np.log10(np.abs(TF)) #dB
    Phase=np.unwrap(np.angle(TF)) #rad/s
    
    
    #plot magnitude squared of fft
    plt.subplot(311)
    plt.plot(nu1*1e-3,Mag,label='Trans. Func. Magnitude (linear)')
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Trans. Func. Magnitude (linear)')
    plt.grid()
#    plt.xlim(-50,50)
    
    plt.subplot(312)
    plt.plot(nu1*1e-3,Mag_dB,label='Trans. Func. Magnitude (dB)')
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Trans. Func. Magnitude (dB)')
    plt.grid()
#    plt.xlim(-50,50)
    
    plt.subplot(313)
    plt.plot(nu1*1e-3,Phase)   
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Trans. Func. Phase (rad/s)')
    plt.grid()
#    plt.xlim(-50,50)
    

    #Save to an .csv file
    ofile=open('UF_15_381_to_434_TF_tukey.csv','w')
    
    mywriter=csv.writer(ofile)
    mywriter.writerow(['Time','Mag_dB','Phase']) #Each columns title
    for i in range (0,len(nu1)):
        
        mywriter.writerow([nu1[i],Mag_dB[i],Phase[i]])
    
    ofile.close()
    
#    max_ampl=np.max(np.absolute(Fk)**2) #find max 
#    ampl=np.ones(len(nu))*max_ampl #create an array 
#    plt.plot(nu*1e-3,ampl) #Max
#    plt.plot(nu*1e-3,ampl/1.995) #3dB drop
#    
#    index=np.argmax(1/((np.absolute(Fk)**2)-ampl/1.995)) #find closest point to -3dB (half power)
#    fc=float(nu[index])*1e-3
#    print("3dB frequency cutoff = %3.2f kHz" %np.abs(fc))
#    
#    #plot 3dB frequency lines
#    plt.axvline(nu[index]*1e-3)
#    plt.axvline(-nu[index]*1e-3)
#    
#    plt.subplot(312)
#    plt.plot(nu*1e-3,20*np.log10(np.absolute(Window_Fk)),label='Window')
#    plt.plot(nu*1e-3,20*np.log10(np.absolute(Fk)),label='Data')
#   
#    #plot 3dB frequency lines
#    plt.axvline(nu[index]*1e-3)
#    plt.axvline(-nu[index]*1e-3)
##    plt.plot(nu*1e-3,np.absolute(Window_Fk)**2/np.max(np.absolute(Window_Fk)**2),label='window') #Window spectra
#    plt.legend()      
#    plt.xlabel('Frequency (kHz)')
#    plt.grid()
#    
##    plt.xlim(-100,100)
#    
#     #Calculate and Plot Phase and Group Delay
#    plt.subplot(313)
#    phase=np.unwrap(np.angle(TF))
#    delay=-(1/(2*np.pi))*np.diff(phase)
##    
##    plt.plot(nu*1e-3,phase,label='phase')
#    plt.plot(nu1[1:]*1e-3,delay,label='group delay')
#    plt.plot(nu2[1:]*1e-3,delay,label='group delay')
#    plt.xlabel('Frequency (kHz)')
#    plt.ylabel('Phase (rad)')
#    plt.ylabel('Group Delay (seconds)')
#    plt.grid()

    plt.title(title_string)
    plt.show()
    return
    
##############
# Start Code #
##############
x_max=450e-6

read_DBY_output=read_DBY(38,1,26.522908895,8,x_max,1) #UF 15-38, RS1
#read_DBY_output=read_DBY(38,2,26.579535265,8,x_max,10) #UF 15-38, RS2
#read_DBY_output=read_DBY(38,3,26.691097980,8,x_max,10) #UF 15-38, RS3
#read_DBY_output=read_DBY(38,4,26.734557870,8,x_max,10) #UF 15-38, RS4
#read_DBY_output=read_DBY(38,5,26.764446000,8,x_max,10) #UF 15-38, RS5
#read_DBY_output=read_DBY(39,1,66.583436840,9,x_max,10) #UF 15-39, RS1
#read_DBY_output=read_DBY(39,2,66.586552840,9,x_max,10) #UF 15-39, RS2
#read_DBY_output=read_DBY(39,3,66.633136315,9,x_max,10) #UF 15-39, RS3
#read_DBY_output=read_DBY(39,5,66.671758785,9,x_max,10) #UF 15-39, RS5
#read_DBY_output=read_DBY(40,2,20.746971600,10,x_max,10) #UF 15-40, RS2
#read_DBY_output=read_DBY(40,3,20.767465080,10,x_max,10) #UF 15-40, RS3
#read_DBY_output=read_DBY(41,1,57.298446790,11,x_max,10) #UF 15-41, RS1
#read_DBY_output=read_DBY(41,2,57.373669615,11,x_max,10) #UF 15-41, RS2
#read_DBY_output=read_DBY(41,3,57.405116910,11,x_max,10) #UF 15-41, RS3
#read_DBY_output=read_DBY(41,4,57.555913445,11,x_max,10) #UF 15-41, RS4
#read_DBY_output=read_DBY(41,5,57.575066540,11,x_max,10) #UF 15-41, RS5
#read_DBY_output=read_DBY(42,1,42.712899355,12,x_max,10) #UF 15-42, RS1
#read_DBY_output=read_DBY(42,3,42.862766400,12,x_max,10) #UF 15-42, RS3
#read_DBY_output=read_DBY(42,4,43.058185590,12,x_max,10) #UF 15-42, RS4
#read_DBY_output=read_DBY(42,5,43.338093110,12,x_max,10) #UF 15-42, RS5
#read_DBY_output=read_DBY(42,6,43.366312590,12,x_max,10) #UF 15-42, RS6
#read_DBY_output=read_DBY(43,1,22.706011205,13,x_max,10) #UF 15-43, RS1
#read_DBY_output=read_DBY(43,2,22.934697575,13,x_max,10) #UF 15-43, RS2
#read_DBY_output=read_DBY(43,3,23.157666725,13,x_max,10) #UF 15-43, RS3
#read_DBY_output=read_DBY(43,4,23.293418545,13,x_max,10) #UF 15-43, RS4
#read_DBY_output=read_DBY(43,5,23.389957810,13,x_max,10) #UF 15-43, RS5

remove_60Hz_slope_output=remove_60Hz_slope(read_DBY_output,x_max)
print('UTC reference time: %s' %remove_60Hz_slope_output[2])
gw_time,gw_data,ir_time,ir_data=chop_gw_ir(remove_60Hz_slope_output)

gw_time=gw_time
gw=gw_data
ir_time=ir_time
ir=ir_data

UF_15_38_time=ir_time
UF_15_38_data=lowpass(ir,900e3)
UF_15_38_data=ir

#Save to an .csv file
#ofile=open('UF_15_43_RS1_GW_DBY.csv','w')
#
#mywriter=csv.writer(ofile)
#mywriter.writerow(['Time','Uncalibrated, filtered, processed E-field']) #Each columns title
#for i in range (0,len(gw_time)):
#    
#    mywriter.writerow([gw_time[i],gw[i]])
#
#ofile.close()
#
#ofile=open('UF_15_43_RS1_IR_DBY.csv','w')
#
#mywriter=csv.writer(ofile)
#mywriter.writerow(['Time','Uncalibrated, filtered, processed E-field']) #Each columns title
#for i in range (0,len(ir_time)):
#    
#    mywriter.writerow([ir_time[i],ir[i]])
#
#ofile.close()

read_DBY_output=read_DBY(43,4,23.293418545,13,x_max,1) #UF 15-43, RS4
remove_60Hz_slope_output=remove_60Hz_slope(read_DBY_output,x_max)
print('UTC reference time: %s' %remove_60Hz_slope_output[2])
gw_time,gw_data,ir_time,ir_data=chop_gw_ir(remove_60Hz_slope_output)

gw_time=gw_time
gw=gw_data
ir_time=ir_time
ir=ir_data

UF_15_43_time=ir_time
UF_15_43_data=lowpass(ir,900e3)
UF_15_43_data=ir

plot_fft(UF_15_38_time,UF_15_38_data,UF_15_43_time,UF_15_43_data,'raw')

#XCORR CODE:
xcorr=np.correlate(UF_15_38_data,UF_15_43_data,'full')
xcorr_delay=np.argmax(xcorr)-(xcorr.size-1)/2 #this delay is how much one skywave is shifted relative to another. It must, however, be referenced to the same feature of the groundwave, i.e. GW peak
xcorr_delay=xcorr_delay*(1/10e6)
print(xcorr_delay)

plt.plot(UF_15_38_time,UF_15_38_data,label='UF 15-38, RS1')
plt.plot(UF_15_43_time,UF_15_43_data,label='UF 15-38, RS4')
plt.show()
plt.legend()
plt.grid()

plt.plot(xcorr)
plt.show()
plt.grid()