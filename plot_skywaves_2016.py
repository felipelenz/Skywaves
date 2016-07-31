# -*- coding: utf-8 -*-
"""
Created on Mon May 23 10:04:42 2016
inputs: (station,year,date,event,RS_number,RS_time,suffix,x_max,filterwindow)
@author: lenz
"""
from read_skywaves_2016 import read_skywaves_2016
from remove_60Hz_slope import remove_60Hz_slope
from chop_gw_ir_2016 import chop_gw_ir_2016
from lowpass import lowpass
import matplotlib.pyplot as plt
plt.figure(figsize=(15.8,10.9))

x_max=400e-6
       
station="VE"
#station="DBY"
#station="GL"
year=2016

if station == "VE":
    distance=302.5e3
elif station == "DBY":
    distance=209e3
elif station == "GL":
    distance=50e3

#read_skywaves_output=read_skywaves_2016(station,year,71516,4,1,34.694603515,81,x_max,1) #UF 16-04, RS1
#read_skywaves_output=read_skywaves_2016(station,year,73016,5,1,09.8246060,2,x_max,1) #UF 16-05, RS1
read_skywaves_output=read_skywaves_2016(station,year,73016,5,2,09.9115729,2,x_max,1) #UF 16-05, RS2
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,1,59.0799352,3,x_max,1) #UF 16-06, RS1
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,2,59.1343666,3,x_max,1) #UF 16-06, RS2
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,3,59.2290428,3,x_max,1) #UF 16-06, RS3
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,3,59.3138698,3,x_max,1) #UF 16-06, RS4

remove_60Hz_slope_output=remove_60Hz_slope(read_skywaves_output,x_max)
print('UTC reference time: %s' %remove_60Hz_slope_output[2])
gw_time,gw_data,ir_time,ir_data=chop_gw_ir_2016(station,remove_60Hz_slope_output)

#plt.plot(gw_time*1e6,gw_data,ir_time*1e6,ir_data)
#plt.show()

#Uncomment for LPF 
GW_five_percent=read_skywaves_output[13]
print("5-pk")
print(GW_five_percent)
gw_time=gw_time
gw=gw_data
ir_time=ir_time
ir=ir_data

lpf_ir_data=lowpass(ir,300e3)
lpf_gw_data=lowpass(gw,700e3)

plt.plot((gw_time[:-100])*1e6,lpf_gw_data[:-100],(ir_time)*1e6,lpf_ir_data,linewidth=2)
plt.title('UF 16-05, RS 2')
plt.xlabel('Time ($\mu s$)')
plt.grid()
plt.ylabel('Uncalibrated Ez from UF '+station+' ('+str(distance/1000)+' km) station')
plt.show()