# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:20:29 2016

@author: lenz
"""
from read_DBY import read_DBY
from remove_60Hz_slope import remove_60Hz_slope
from chop_gw_ir import chop_gw_ir
import numpy as np
from lowpass import lowpass
import matplotlib.pyplot as plt
x_max=450e-6

read_DBY_output=read_DBY(38,1,26.522908895,8,x_max,1) #UF 15-38, RS1
#read_DBY_output=read_DBY(39,1,66.583436840,9,x_max,1) #UF 15-39, RS1
#read_DBY_output=read_DBY(40,3,20.767465080,10,x_max,1) #UF 15-40, RS3
#read_DBY_output=read_DBY(41,1,57.298446790,11,x_max,1) #UF 15-41, RS1
#read_DBY_output=read_DBY(42,4,43.058185590,12,x_max,1) #UF 15-42, RS4
#read_DBY_output=read_DBY(43,4,23.293418545,13,x_max,1) #UF 15-43, RS4
remove_60Hz_slope_output=remove_60Hz_slope(read_DBY_output,x_max)
print('UTC reference time: %s' %remove_60Hz_slope_output[2])
gw_time,gw_data,ir_time,ir_data=chop_gw_ir(remove_60Hz_slope_output)

gw_time=gw_time
gw=gw_data
ir_time=ir_time
ir=ir_data

gw_peak=gw_time[np.argmax(gw)]
print(gw_peak)
#plt.plot(gw_time-gw_peak,gw,ir_time-gw_peak,ir)
#plt.show()

lpf_gw_data=lowpass(gw,100e3)
lpf_ir_data=lowpass(ir,100e3)

lpf_gw_peak=gw_time[np.argmax(lpf_gw_data)]
print(lpf_gw_peak)

Dt=(lpf_gw_peak-gw_peak)
print("Time difference between LPF peak and raw peak=%r"%Dt)
plt.plot((gw_time-gw_peak)*1e6,lpf_gw_data,(ir_time-gw_peak)*1e6,lpf_ir_data)
plt.xlabel("Time in ($\mu s$)")
plt.show()