# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:53:06 2016

@author: lenz
"""

from read_DBY import read_DBY
from remove_60Hz_slope import remove_60Hz_slope
from chop_gw_ir import chop_gw_ir
import numpy as np
from lowpass import lowpass
import matplotlib.pyplot as plt
plt.figure(figsize=(15.8,10.9))
x_max=450e-6
from xcorr import xcorr

#read_DBY_output=read_DBY(38,1,26.522908895,8,x_max,1) #UF 15-38, RS1
#read_DBY_output=read_DBY(38,2,26.579535265,8,x_max,1) #UF 15-38, RS2
#read_DBY_output=read_DBY(38,3,26.691097980,8,x_max,1) #UF 15-38, RS3
#read_DBY_output=read_DBY(38,4,26.734557870,8,x_max,1) #UF 15-38, RS4
#read_DBY_output=read_DBY(38,5,26.764446000,8,x_max,1) #UF 15-38, RS5
#read_DBY_output=read_DBY(39,1,66.583436840,9,x_max,1) #UF 15-39, RS1
#read_DBY_output=read_DBY(39,2,66.586552840,9,x_max,1) #UF 15-39, RS2
#read_DBY_output=read_DBY(39,3,66.633136315,9,x_max,1) #UF 15-39, RS3
#read_DBY_output=read_DBY(39,5,66.671758785,9,x_max,1) #UF 15-39, RS5
#read_DBY_output=read_DBY(40,2,20.746971600,10,x_max,1) #UF 15-40, RS2
#read_DBY_output=read_DBY(40,3,20.767465080,10,x_max,1) #UF 15-40, RS3
#read_DBY_output=read_DBY(41,1,57.298446790,11,x_max,1) #UF 15-41, RS1
#read_DBY_output=read_DBY(41,2,57.373669615,11,x_max,1) #UF 15-41, RS2
#read_DBY_output=read_DBY(41,3,57.405116910,11,x_max,1) #UF 15-41, RS3
#read_DBY_output=read_DBY(41,4,57.555913445,11,x_max,1) #UF 15-41, RS4
#read_DBY_output=read_DBY(41,5,57.575066540,11,x_max,1) #UF 15-41, RS5
#read_DBY_output=read_DBY(42,1,42.712899355,12,x_max,1) #UF 15-42, RS1
#read_DBY_output=read_DBY(42,3,42.862766400,12,x_max,1) #UF 15-42, RS3
#read_DBY_output=read_DBY(42,4,43.058185590,12,x_max,1) #UF 15-42, RS4
#read_DBY_output=read_DBY(42,5,43.338093110,12,x_max,1) #UF 15-42, RS5
#read_DBY_output=read_DBY(42,6,43.366312590,12,x_max,1) #UF 15-42, RS6
read_DBY_output=read_DBY(43,1,22.706011205,13,x_max,1) #UF 15-43, RS1
#read_DBY_output=read_DBY(43,2,22.934697575,13,x_max,1) #UF 15-43, RS2
#read_DBY_output=read_DBY(43,3,23.157666725,13,x_max,1) #UF 15-43, RS3
#read_DBY_output=read_DBY(43,4,23.293418545,13,x_max,1) #UF 15-43, RS4
#read_DBY_output=read_DBY(43,5,23.389957810,13,x_max,1) #UF 15-43, RS5
remove_60Hz_slope_output=remove_60Hz_slope(read_DBY_output,x_max)
print('UTC reference time: %s' %remove_60Hz_slope_output[2])
gw_time,gw_data,ir_time,ir_data=chop_gw_ir(remove_60Hz_slope_output)

##Uncomment for moving average filter
#n=len(remove_60Hz_slope_output[0])
#gw_time=remove_60Hz_slope_output[0][:n/2]
#gw=remove_60Hz_slope_output[1][:n/2]
#ir_time=remove_60Hz_slope_output[0][n/2:]
#ir=remove_60Hz_slope_output[1][n/2:]
#plt.plot(gw_time*1e6,gw,ir_time*1e6,ir)
#plt.show()

#Uncomment for LPF 
GW_five_percent=read_DBY_output[13]
print("5-pk")
print(GW_five_percent)
gw_time=gw_time
gw=gw_data
ir_time=ir_time
ir=ir_data


lpf_ir_data=lowpass(ir,300e3)
lpf_gw_data=lowpass(gw,700e3)
plt.plot(gw_time*1e6,lpf_gw_data,ir_time[50:]*1e6,lpf_ir_data[50:])
plt.plot([gw_time[0]*1e6,gw_time[-1]*1e6],[0.05*np.max(lpf_gw_data),0.05*np.max(lpf_gw_data)],'r-')
plt.xlabel('Time ($\mu s$)')
plt.ylabel('data 1 Uncalibrated Ez from DBY station')
plt.show()

#read_DBY_output=read_DBY(38,1,26.522908895,8,x_max,1) #UF 15-38, RS1
#read_DBY_output=read_DBY(38,2,26.579535265,8,x_max,1) #UF 15-38, RS2
#read_DBY_output=read_DBY(38,3,26.691097980,8,x_max,1) #UF 15-38, RS3
#read_DBY_output=read_DBY(38,4,26.734557870,8,x_max,1) #UF 15-38, RS4
#read_DBY_output=read_DBY(38,5,26.764446000,8,x_max,1) #UF 15-38, RS5
#read_DBY_output=read_DBY(39,1,66.583436840,9,x_max,1) #UF 15-39, RS1
#read_DBY_output=read_DBY(39,2,66.586552840,9,x_max,1) #UF 15-39, RS2
#read_DBY_output=read_DBY(39,3,66.633136315,9,x_max,1) #UF 15-39, RS3
#read_DBY_output=read_DBY(39,5,66.671758785,9,x_max,1) #UF 15-39, RS5
#read_DBY_output=read_DBY(40,2,20.746971600,10,x_max,1) #UF 15-40, RS2
#read_DBY_output=read_DBY(40,3,20.767465080,10,x_max,1) #UF 15-40, RS3
#read_DBY_output=read_DBY(41,1,57.298446790,11,x_max,1) #UF 15-41, RS1
#read_DBY_output=read_DBY(41,2,57.373669615,11,x_max,1) #UF 15-41, RS2
#read_DBY_output=read_DBY(41,3,57.405116910,11,x_max,1) #UF 15-41, RS3
#read_DBY_output=read_DBY(41,4,57.555913445,11,x_max,1) #UF 15-41, RS4
#read_DBY_output=read_DBY(41,5,57.575066540,11,x_max,1) #UF 15-41, RS5
#read_DBY_output=read_DBY(42,1,42.712899355,12,x_max,1) #UF 15-42, RS1
#read_DBY_output=read_DBY(42,3,42.862766400,12,x_max,1) #UF 15-42, RS3
#read_DBY_output=read_DBY(42,4,43.058185590,12,x_max,1) #UF 15-42, RS4
#read_DBY_output=read_DBY(42,5,43.338093110,12,x_max,1) #UF 15-42, RS5
#read_DBY_output=read_DBY(42,6,43.366312590,12,x_max,1) #UF 15-42, RS6
#read_DBY_output=read_DBY(43,1,22.706011205,13,x_max,1) #UF 15-43, RS1
#read_DBY_output=read_DBY(43,2,22.934697575,13,x_max,1) #UF 15-43, RS2
read_DBY_output=read_DBY(43,3,23.157666725,13,x_max,1) #UF 15-43, RS3
#read_DBY_output=read_DBY(43,4,23.293418545,13,x_max,1) #UF 15-43, RS4
#read_DBY_output=read_DBY(43,5,23.389957810,13,x_max,1) #UF 15-43, RS5
remove_60Hz_slope_output=remove_60Hz_slope(read_DBY_output,x_max)
print('UTC reference time: %s' %remove_60Hz_slope_output[2])
gw_time,gw_data,ir_time,ir_data=chop_gw_ir(remove_60Hz_slope_output)

##Uncomment for moving average filter
#n=len(remove_60Hz_slope_output[0])
#gw_time2=remove_60Hz_slope_output[0][:n/2]
#gw2=remove_60Hz_slope_output[1][:n/2]
#ir_time2=remove_60Hz_slope_output[0][n/2:]
#ir2=remove_60Hz_slope_output[1][n/2:]
#plt.plot(gw_time2*1e6,gw2,ir_time2*1e6,ir2)
#plt.show()
#
#delay=xcorr(ir_time,ir_time2,ir,ir2)

#Uncomment for LPF
GW_five_percent2=read_DBY_output[13]
print("5-pk")
print(GW_five_percent2)
gw_time=gw_time
gw=gw_data
ir_time2=ir_time
ir=ir_data

lpf_ir_data2=lowpass(ir,300e3)
lpf_gw_data=lowpass(gw,700e3)
plt.plot(gw_time*1e6,lpf_gw_data,ir_time[50:]*1e6,lpf_ir_data[50:])
plt.plot([gw_time[0]*1e6,gw_time[-1]*1e6],[0.05*np.max(lpf_gw_data),0.05*np.max(lpf_gw_data)],'r-')
plt.xlabel('Time ($\mu s$)')
plt.ylabel('data 2 Uncalibrated Ez from DBY station')
plt.show()

delay=xcorr(ir_time[50:],ir_time2[50:],lpf_ir_data[50:],lpf_ir_data2[50:])



#This part of the code accounts for the xcorr from 5% of GW peak
if GW_five_percent2>GW_five_percent:
    xcorr=np.abs(delay)+(np.abs(GW_five_percent2-GW_five_percent))
    if delay<0:
        xcorr=xcorr*-1
    else:
        xcorr=xcorr
    print("xcorr_delay")
    print(xcorr)
else:
    xcorr=np.abs(delay)-(np.abs(GW_five_percent2-GW_five_percent))
    if delay<0:
        xcorr=xcorr*-1
    else:
        xcorr=xcorr
    print("xcorr_delay")
    print(xcorr)