# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 13:19:42 2016

@author: lenz
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy import fft

I0=13e3
eta=0.73
tau1=0.15e-6
tau2=3e-6
n=2
pad1=np.zeros(1000)
tf=50e-6
N=10e3
pad1=np.zeros(N)
Ts=tf/N
fs=1/Ts

t=Ts*np.arange(0,N)
I=(I0/eta)*(((t/tau1)**n)/((t/tau1)**n+1))*np.exp(-t/tau2)
#I=np.sin(2*np.pi*f0*t)
I=np.append(pad1,I)
I=np.append(I,pad1)
N=len(I)
t=np.linspace(0,N*Ts,N)

def take_fft(data,N,Ts):
    Fk=fft.fft(data)/n #Fourier coefficients
    nu=fft.fftfreq(N,Ts) #Natural frequencies
    Fk=fft.fftshift(Fk) #Shift zero frequency to center
    nu=fft.fftshift(nu) #Shift zero freq to center
    return nu, Fk
    
I_fft=take_fft(I,N,Ts)
dI=np.diff(I)


plt.subplot(311)
dI=np.diff(I)
dI=np.append(dI,0.0)
plt.plot(t*1e6,dI/1000)
plt.xlabel('Time ($\mu s$)')
plt.ylabel('$dIdt$ $(kA/\mu s)$')
plt.grid()


dI_fft=take_fft(dI,N,Ts)
nu=dI_fft[0]
Fk=dI_fft[1]

#
plt.subplot(312)
plt.plot(nu*1e-6,np.absolute(Fk)**2)
max_ampl=np.max(np.absolute(Fk)**2)
ampl=np.ones(len(nu))*max_ampl
plt.plot(nu*1e-6,ampl)
plt.plot(nu*1e-6,ampl/1.995)

index=np.argmax(1/(np.absolute(Fk)**2-ampl/1.995)) #find closest point to -3dB
fc=float(nu[index])*1e-3
print("3dB frequency cutoff = %3.2f MHz" %fc)

plt.plot([nu[index]*1e-6,nu[index]*1e-6],[-np.min(np.absolute(Fk)**2),np.max(np.absolute(Fk)**2)])
plt.plot([-nu[index]*1e-6,-nu[index]*1e-6],[-np.min(np.absolute(Fk)**2),np.max(np.absolute(Fk)**2)])
plt.title("3dB frequency cutoff = %3.2f kHz" %fc)
plt.ylabel('$|fft(I)|^2$  ')
plt.xlabel('Frequency (MHz)')
plt.xlim(-5,5)
plt.grid()

plt.subplot(313)
phase=np.unwrap(np.angle(Fk))
plt.plot(nu*1e-6,phase)
plt.xlabel('Frequency (MHz)')
plt.ylabel('Phase (rad)')
plt.xlim(-5,5)
plt.grid()

plt.show()