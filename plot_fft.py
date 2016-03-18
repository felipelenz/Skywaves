# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:55:08 2016

@author: lenz
"""
import matplotlib.pyplot as plt
import numpy as np
from take_fft import take_fft
import csv

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