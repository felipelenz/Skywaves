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
import numpy as np
from filter_DBY import filter_DBY
from filter_VE import filter_VE

import matplotlib.pyplot as plt
plt.figure(figsize=(15.8,10.9))

x_max=800e-6
       
#station="VE"
#station="DBY"
station="GL"
year=2016

if station == "VE":
    distance=302.5e3
elif station == "DBY":
    distance=209e3
elif station == "GL":
    distance=50e3

#read_skywaves_output=read_skywaves_2016(station,year,71516,4,1,34.694603515,2,x_max,1) #UF 16-04, RS1 VE
#read_skywaves_output=read_skywaves_2016(station,year,71516,4,1,34.694603515,81,x_max,1) #UF 16-04, RS1 DBY
#read_skywaves_output=read_skywaves_2016(station,year,71516,4,1,34.694603515,1,x_max,1) #UF 16-04, RS1 GL
#read_skywaves_output=read_skywaves_2016(station,year,73016,5,1,69.8246060,0,x_max,1) #UF 16-05, RS1 DBY
#read_skywaves_output=read_skywaves_2016(station,year,73016,5,1,09.8246060,0,x_max,1) #UF 16-05, RS1 GL
#read_skywaves_output=read_skywaves_2016(station,year,73016,5,2,09.9115729,2,x_max,1) #UF 16-05, RS2 VE
#read_skywaves_output=read_skywaves_2016(station,year,73016,5,2,09.9115729,0,x_max,1) #UF 16-05, RS2 GL
#read_skywaves_output=read_skywaves_2016(station,year,73016,5,2,69.9115729,0,x_max,1) #UF 16-05, RS2 DBY
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,1,59.0799352,3,x_max,1) #UF 16-06, RS1 VE
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,1,59.0799352,1,x_max,1) #UF 16-06, RS1 GL
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,2,59.1343666,3,x_max,1) #UF 16-06, RS2 VE
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,2,59.1343666,1,x_max,1) #UF 16-06, RS2 GL
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,3,59.2290428,3,x_max,1) #UF 16-06, RS3 VE
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,3,59.2290428,1,x_max,1) #UF 16-06, RS3 GL
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,4,59.3138698,3,x_max,1) #UF 16-06, RS4 VE
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,4,59.3138698,1,x_max,1) #UF 16-06, RS4 GL
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,3,09.9115729,1,x_max,1) #UF 16-05, RS2 DBY
#read_skywaves_output=read_skywaves_2016(station,year,73016,6,3,59.0799352,2,x_max,1) #UF 16-06, RS1 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,1,38.1069916,2,x_max,1) #UF 16-07, RS1 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,1,38.1069916,3,x_max,1) #UF 16-07, RS1 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,2,38.1429186,2,x_max,1) #UF 16-07, RS2 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,2,38.1106948,3,x_max,1) #UF 16-07, RS2 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,3,38.1429186,3,x_max,1) #UF 16-07, RS3 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,3,38.2151927,2,x_max,1) #UF 16-07, RS3 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,4,38.2355570,2,x_max,1) #UF 16-07, RS4 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,4,38.2151927,3,x_max,1) #UF 16-07, RS4 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,5,38.2421506,2,x_max,1) #UF 16-07, RS5 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,5,38.2355570,3,x_max,1) #UF 16-07, RS5 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,6,38.2421506,2,x_max,1) #UF 16-07, RS6 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,7,6,38.2421506,3,x_max,1) #UF 16-07, RS6 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,9,1,46.8819368,4,x_max,1) #UF 16-09, RS1 GL
##read_skywaves_output=read_skywaves_2016(station,year,80116,9,1,46.8819368,5,x_max,1) #UF 16-09, RS1 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,9,2,47.0016806,4,x_max,1) #UF 16-09, RS2 GL
##read_skywaves_output=read_skywaves_2016(station,year,80116,9,2,47.0016806,5,x_max,1) #UF 16-09, RS2 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,10,1,45.7826377,5,x_max,1) #UF 16-10, RS1 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,10,1,45.7826377,6,x_max,1) #UF 16-10, RS1 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,10,2,45.8240586,5,x_max,1) #UF 16-10, RS2 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,10,2,45.8240586,6,x_max,1) #UF 16-10, RS2 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,10,3,45.8502498,5,x_max,1) #UF 16-10, RS3 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,10,3,45.8502498,6,x_max,1) #UF 16-10, RS3 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,11,1,69.0580374,7,x_max,1) #UF 16-11, RS1 DBY
#read_skywaves_output=read_skywaves_2016(station,year,80116,11,1,69.0580374,6,x_max,1) #UF 16-11, RS1 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,12,1,27.8170084,7,x_max,1) #UF 16-12, RS1 GL
#read_skywaves_output=read_skywaves_2016(station,year,80116,12,1,27.8170084,8,x_max,1) #UF 16-12, RS1 DBY
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,1,27.286644730,437,x_max,1) #UF 16-23, RS1 DBY
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,1,27.286644730,2,x_max,1) #UF 16-23, RS1 VE
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,1,27.286644730,291,x_max,1) #UF 16-23, RS1 GL
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,2,27.333111390,437,x_max,1) #UF 16-23, RS2 DBY
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,2,27.333111390,2,x_max,1) #UF 16-23, RS2 VE
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,2,27.333111390,291,x_max,1) #UF 16-23, RS2 GL
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,3,27.436680310,437,x_max,1) #UF 16-23, RS3 DBY
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,3,27.436680310,2,x_max,1) #UF 16-23, RS3 VE
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,3,27.436680310,291,x_max,1) #UF 16-23, RS3 GL
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,4,27.565600070,437,x_max,1) #UF 16-23, RS4 DBY
#read_skywaves_output=read_skywaves_2016(station,year,81316,23,4,27.565600070,2,x_max,1) #UF 16-23, RS4 VE
read_skywaves_output=read_skywaves_2016(station,year,81316,23,4,27.565600070,291,x_max,1) #UF 16-23, RS4 GL
#read_skywaves_output=read_skywaves_2016(station,year,80316,0,0,45.694707,290,x_max,1) #UF Natural GL

if station == "DBY":
    remove_60Hz_slope_output=remove_60Hz_slope(read_skywaves_output,x_max)
    filtered=filter_DBY(remove_60Hz_slope_output[1])
    
#    plt.plot(read_skywaves_output[0]*1e6,read_skywaves_output[10])
#    plt.plot(remove_60Hz_slope_output[0],remove_60Hz_slope_output[1])
    plt.plot(remove_60Hz_slope_output[0][1510:-1]*1e6-150,filtered[1510:-1])
    plt.title('UF 16-'+str(read_skywaves_output[14])+', RS '+str(read_skywaves_output[15])+' from UF '+station+' ('+str(distance/1000)+' km) station')
    plt.xlabel('Time ($\mu s$) after '+str(read_skywaves_output[2]))
    plt.ylabel('Uncalibrated Ez')
    plt.grid()
    plt.show()

elif station == "VE":
    remove_60Hz_slope_output=remove_60Hz_slope(read_skywaves_output,x_max)
    filtered=filter_VE(remove_60Hz_slope_output[1])
    
#    plt.plot(read_skywaves_output[0]*1e6,read_skywaves_output[10])
#    plt.plot(remove_60Hz_slope_output[0],remove_60Hz_slope_output[1])
    plt.plot(remove_60Hz_slope_output[0][1510:-1]*1e6-150,filtered[1510:-1])
    plt.title('UF 16-'+str(read_skywaves_output[14])+', RS '+str(read_skywaves_output[15])+' from UF '+station+' ('+str(distance/1000)+' km) station')
    plt.xlabel('Time ($\mu s$) after '+str(read_skywaves_output[2]))
    plt.ylabel('Uncalibrated Ez')
    plt.grid()
    plt.show()
    
elif station == "GL":
    remove_60Hz_slope_output=remove_60Hz_slope(read_skywaves_output,x_max)
    
    plt.plot(read_skywaves_output[0]*1e6,read_skywaves_output[10])
    plt.title('UF 16-'+str(read_skywaves_output[14])+', RS '+str(read_skywaves_output[15])+' from UF '+station+' ('+str(distance/1000)+' km) station')
    plt.xlabel('Time ($\mu s$) after '+str(read_skywaves_output[2]))
    plt.ylabel('Uncalibrated Ez')
    plt.grid()
    plt.show()