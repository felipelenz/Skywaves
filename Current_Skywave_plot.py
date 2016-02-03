# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 09:31:37 2015

@author: lenz
"""

import Yoko750 as yk
import matplotlib
import matplotlib.pyplot as plt
import lecroy as lc
matplotlib.rcParams.update({'font.size': 22})
from noise_analysis import noise_analysis

suffix26=3 #lecroy last digit og the .trc file name

date=82715
fs=500e6

dt1=1
dt2=1

#Yoko
yoko_fileName = "/Volumes/2015 Data/082715/Scope24/UF1538_IIHI"

f = yk.Yoko750File(yoko_fileName)
header = f.get_header()

IIHI=f.get_trace_data(header,1,8.56601119e-001,(8.56601119e-001+100e-6),19.90050)
plt.xlabel('Time ($\mu$s)')
plt.ylabel('Channel-Base Current (kA)')
plt.ylim(-1,22)
plt.grid()
plt.plot((IIHI.dataTime[::dt1]-8.56601119e-001)*1e6,IIHI.data[::dt1],color=[1,0,0],linewidth=2)
plt.show()

a=noise_analysis((IIHI.dataTime[::dt1]-8.56601119e-001),IIHI.data[::dt1],100e6,0)

plt.plot((IIHI.dataTime[::dt1]-8.56601119e-001)*1e6,IIHI.data[::dt1],color=[1,0,0],linewidth=2)
plt.plot([0,100],[0.5*a[5],0.5*a[5]],'b--',linewidth=2.0)
plt.xlabel('Time ($\mu$s)')
plt.ylabel('Channel-Base Current (kA)')
plt.ylim(-1,22)
plt.grid()
plt.show()
print(a)
#event=39
##Yoko
#yoko_fileName = "/Volumes/2015 Data/0"+str(date)+"/Scope24/UF15"+str(event)+"_IIHI"
#
#f = yk.Yoko750File(yoko_fileName)
#header = f.get_header()
#
#IIHI=f.get_trace_data(header,1,7.99957275e-001,(7.99957275e-001+100e-6),19.90050)
#
#plt.plot((IIHI.dataTime[::dt1]-7.99957275e-001)*1e6,IIHI.data[::dt1],color=[1,0,0],linewidth=2)
#plt.xlabel('Time ($\mu$s)')
#plt.ylabel('Channel-Base Current (kA)')
#plt.grid()
#plt.show()
#
#event=40
##Yoko
#yoko_fileName = "/Volumes/2015 Data/0"+str(date)+"/Scope24/UF15"+str(event)+"_IIHI"
#
#f = yk.Yoko750File(yoko_fileName)
#header = f.get_header()
#
#IIHI=f.get_trace_data(header,1,8.20478380e-001,(8.20478380e-001+100e-6),19.90050)
#
#plt.plot((IIHI.dataTime[::dt1]-8.20478380e-001)*1e6,IIHI.data[::dt1],color=[1,0,0],linewidth=2)
#plt.xlabel('Time ($\mu$s)')
#plt.ylabel('Channel-Base Current (kA)')
#plt.grid()
#plt.show()

#Current (from scope 26)
#lecroy_fileName_IIHI = "/Volumes/2015 Data/0"+str(date)+"/Scope26/C1AC0000"+str(suffix26)+".trc"
#lecroy_IIHI = lc.lecroy_data(lecroy_fileName_IIHI)
#seg_time_IIHI = lecroy_IIHI.get_seg_time()
#segments_IIHI = lecroy_IIHI.get_segments()
#seg=0
#plt.plot((seg_time_IIHI[::dt2])*1e6-2463, segments_IIHI[seg][::dt2]*19.90050,color=[1,0,0],linewidth=2)
#plt.xlim(0,100)
#plt.xlabel('Time ($\mu$s)')
#plt.ylabel('Channel-Base Current (kA)')
#plt.grid()
#plt.show()
#event=42
##Yoko
#yoko_fileName = "/Volumes/2015 Data/0"+str(date)+"/Scope24/UF15"+str(event)+"_IIHI"
#
#f = yk.Yoko750File(yoko_fileName)
#header = f.get_header()
#
#IIHI=f.get_trace_data(header,1,1.14526355e+000,(1.14526355e+000+100e-6),19.90050)
#
#plt.plot((IIHI.dataTime[::dt1]-1.14526355e+000)*1e6,IIHI.data[::dt1],color=[1,0,0],linewidth=2)
#plt.xlabel('Time ($\mu$s)')
#plt.ylabel('Channel-Base Current (kA)')
#plt.grid()
#plt.show()

#event=43
##Yoko
#yoko_fileName = "/Volumes/2015 Data/0"+str(date)+"/Scope24/UF15"+str(event)+"_IIHI"
#
#f = yk.Yoko750File(yoko_fileName)
#header = f.get_header()
#
#IIHI=f.get_trace_data(header,1,1.38738370e+000,(1.38738370e+000+100e-6),19.90050)
#
#plt.plot((IIHI.dataTime[::dt1]-1.38738370e+000)*1e6,IIHI.data[::dt1],color=[1,0,0],linewidth=2)
#plt.xlabel('Time ($\mu$s)')
#plt.ylabel('Channel-Base Current (kA)')
#plt.grid()
#plt.show()