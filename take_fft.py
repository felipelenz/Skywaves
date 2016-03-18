# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:45:52 2016

@author: lenz
This function take the fft of a signal and returns the zero centered frequency
array (nu), and the Fourier complex coeficcients (Fk)
"""
from numpy import fft

##############
# FFT method #
##############
def take_fft(data,N,Ts):
    Fk=fft.fft(data)/N #Fourier coefficients
    nu=fft.fftfreq(N,Ts) #Natural frequencies
    Fk=fft.fftshift(Fk) #Shift zero frequency to center
    nu=fft.fftshift(nu) #Shift zero freq to center
    return nu, Fk