# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 09:55:02 2016

@author: felipelenz
"""
import csv
import numpy as np
import matplotlib.pyplot as plt

filename="/Users/felipelenz/Google Drive/8-7-2015 skywaves .csv files/Final Version of GW and IR/UF_15_38_RS1_GW_DBY.csv"
filename2="/Users/felipelenz/Google Drive/8-7-2015 skywaves .csv files/Final Version of GW and IR/UF_15_38_RS1_IR_DBY.csv"
filename3="/Users/felipelenz/Google Drive/8-7-2015 skywaves .csv files/Final Version of GW and IR/UF_15_43_RS4_GW_DBY.csv"
filename4="/Users/felipelenz/Google Drive/8-7-2015 skywaves .csv files/Final Version of GW and IR/UF_15_43_RS4_IR_DBY.csv"

def read_csv(filename):
    f=open(filename)
    csv_f=csv.reader(f)
    time=[]
    data=[]
    UTC_ref_time=[]
    for column in csv_f:
        time.append(column[0])
        data.append(column[1])
        UTC_ref_time.append(column[2])
        
    data=np.asarray(data)
    time=np.asarray(time)
    
    time=time.astype(np.float) #this time comes from read_DBY and is calculated
    data=data.astype(np.float)
    return time, data#,UTC_ref_time[0]

#UF 15-38, RS1
gw1_time, gw1_data=read_csv(filename)
gw1_max_time=np.argmax(gw1_data)*(1/10e6)
plt.plot((gw1_time-gw1_max_time-gw1_time[0])*1e6,gw1_data)
plt.plot([0,0],[-0.2,1])

ir1_time, ir1_data=read_csv(filename2)
plt.plot((ir1_time-gw1_max_time-gw1_time[0])*1e6,ir1_data)

#UF 15-43, RS4
gw2_time, gw2_data=read_csv(filename3)
gw2_max_time=np.argmax(gw2_data)*(1/10e6)
plt.plot((gw2_time-gw2_max_time-gw2_time[0])*1e6,gw2_data)

ir2_time, ir2_data=read_csv(filename4)
plt.plot((ir2_time-gw2_max_time-gw2_time[0])*1e6,ir2_data)
plt.show()

#Xcorr
xcorr=np.correlate(ir1_data, ir2_data,'full') #calculate xcorr between two skywaves
plt.plot(ir1_data/np.max(ir1_data))
plt.plot(ir2_data/np.max(ir2_data))
plt.plot(xcorr/np.max(xcorr))
#
xcorr_delay=np.argmax(xcorr)-(xcorr.size-1)/2 #this delay is how much one skywave is shifted relative to another. It must, however, be referenced to the same feature of the groundwave, i.e. GW peak
xcorr_delay=xcorr_delay*(1/10e6)
xcorr_delay=xcorr_delay-(gw1_max_time-gw2_max_time) #here is the bit of code that references the xcorr lag delay to the gw peak
print(xcorr_delay)
plt.show()