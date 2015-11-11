# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:48:47 2015

@author: lenz
This code finds skywaves that happened at a specified (input) UTC time

###########
# Inputs: #
###########

RS_time=seconds of the XLI time stamp (for trigger lightning) this time can 
be found in the triggered lightning reports (e.g. 26.579535265) or from NLDN
data (for naturals)
date=date
fs=sampling frequency
suffix=file identifier
Horizontal_distance=distance between DBY and RS (calculated from their lat and long)
x_max=time limit

############
# Outputs: #
############
time=time list 
skywave= skywave list
UTC_Time=UTC_time string
t0=reference time (see below for specifics)

"""
from __future__ import division
import lecroy as lc
import matplotlib.pyplot as plt
import IRIGA

#def Skywave(RS_time,suffix,x_max): 
 


####################
# Input Parameters #
####################

def Natural_Skywaves(RS_time,date,fs,suffix,Horizontal_distance,x_max):
    ##############
    # Read Files #
    ##############
    #import IRIG file
    if suffix>999:
        lecroy_fileName_DBY_IRIG = "/Volumes/DBY Skywaves/C2DBY0"+str(suffix)+".trc"
        lecroy_DBY_IRIG= lc.lecroy_data(lecroy_fileName_DBY_IRIG)
        seg_time_DBY_IRIG = lecroy_DBY_IRIG.get_seg_time()
        segments_DBY_IRIG = lecroy_DBY_IRIG.get_segments()
    else:
        lecroy_fileName_DBY_IRIG = "/Volumes/DBY Skywaves/C2DBY00"+str(suffix)+".trc"
        lecroy_DBY_IRIG= lc.lecroy_data(lecroy_fileName_DBY_IRIG)
        seg_time_DBY_IRIG = lecroy_DBY_IRIG.get_seg_time()
        segments_DBY_IRIG = lecroy_DBY_IRIG.get_segments()
    
    #read IRIG file and print time stamp
    timestamp,t =IRIGA.IRIGA_signal(segments_DBY_IRIG[0], fs, year=2015)
    print(timestamp)
    
    #import skywaves data
    if suffix>999:
        lecroy_fileName_DBY = "/Volumes/DBY Skywaves/C1DBY0"+str(suffix)+".trc"
        lecroy_DBY= lc.lecroy_data(lecroy_fileName_DBY)
        seg_time_DBY = lecroy_DBY.get_seg_time()
        segments_DBY = lecroy_DBY.get_segments()
    else:
        lecroy_fileName_DBY = "/Volumes/DBY Skywaves/C1DBY00"+str(suffix)+".trc"
        lecroy_DBY= lc.lecroy_data(lecroy_fileName_DBY)
        seg_time_DBY = lecroy_DBY.get_seg_time()
        segments_DBY = lecroy_DBY.get_segments()
    
    print("From irig",(timestamp.second+timestamp.microsecond/1e6))
    # t0 is the zero reference point, it accounts for the input UTC time minus the 
    # beginning of the IRIG file plus the propagation delay from the lightning to 
    # the DBY station (this comes from NLDN)
    t0=RS_time-(timestamp.second+timestamp.microsecond/1e6)+Horizontal_distance/2.99e8
    
    # round it to the nearest nanosecond
    t0=round(t0*1e9)/1e9
    
    # This is the end of the skywave (500 us after t0)
    tf=t0+x_max
    n0=int(t0*fs)
    nf=int(tf*fs)
        
    #plt.plot([0,0],[-1,1],t[n0:nf]-t0,segments_DBY[0][n0:nf])
    #plt.xlabel('UTC Time in seconds after '+str(timestamp.hour)+':'+str(timestamp.minute)+':'+str(round((timestamp.second+timestamp.microsecond/1e6+t0)*1e9)/1e9))
    #plt.xlim(0,x_max)
    #plt.title("Date: "+str(date) )
    #plt.grid()
    #plt.show()
        
    seconds=(round((timestamp.second+timestamp.microsecond/1e6+t0)*1e9)/1e9)
    UTC_time= "%r:%r:%r" %(timestamp.hour,timestamp.minute,seconds)
    
    # Rename variables to filter nmore easily
    skywave=segments_DBY[0][n0:nf];
    time=t[n0:nf]-t0;
     
    ##chop lists
    #time=time[0:int((x_max)*fs)]
    #skywave=skywave[0:int((x_max)*fs)]
    
#    plt.plot(time,skywave)
#    plt.xlim(0,x_max)
#    plt.show()

    return time, skywave,UTC_time,t0