# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:53:14 2016

@author: lenz
This code applies a forward and reverse low-pass filter to a signal. inputs are
the data to be filtered and the cutoff frequency in Hz. The output of this function
is the low pass filtered data.
"""
from scipy import signal

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
#    w,mag,phase=signal.bode((b,a))
#    filter_delay=-np.diff(phase)/(2*np.pi)
#    plt.plot(w[1:]*fs/(2*np.pi),filter_delay)
#    plt.show()
   
    lpfiltered=signal.filtfilt(b,a,interval)
#    plt.plot(lpfiltered)
#    plt.show()
    return lpfiltered