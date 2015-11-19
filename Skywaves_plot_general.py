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
        lecroy_fileName_DBY_IRIG="/Volumes/DBY Skywaves/C2DBY0"+str(suffix)+".trc"
        lecroy_DBY_IRIG= lc.lecroy_data(lecroy_fileName_DBY_IRIG)
#        seg_time_DBY_IRIG = lecroy_DBY_IRIG.get_seg_time()
        segments_DBY_IRIG = lecroy_DBY_IRIG.get_segments()
    else:
        lecroy_fileName_DBY_IRIG="/Volumes/DBY Skywaves/C2DBY00"+str(suffix)+".trc"
        lecroy_DBY_IRIG= lc.lecroy_data(lecroy_fileName_DBY_IRIG)
#        seg_time_DBY_IRIG = lecroy_DBY_IRIG.get_seg_time()
        segments_DBY_IRIG = lecroy_DBY_IRIG.get_segments()
    
    #read IRIG file and print time stamp
    timestamp,t = IRIGA.IRIGA_signal(segments_DBY_IRIG[0], fs, year=2015)
    print(timestamp)
    
    #import skywaves data
    if suffix>999:
        lecroy_fileName_DBY = "/Volumes/DBY Skywaves/C1DBY0"+str(suffix)+".trc"
        lecroy_DBY= lc.lecroy_data(lecroy_fileName_DBY)
#        seg_time_DBY = lecroy_DBY.get_seg_time()
        segments_DBY = lecroy_DBY.get_segments()
    else:
        lecroy_fileName_DBY="/Volumes/DBY Skywaves/C1DBY00"+str(suffix)+".trc"
        lecroy_DBY= lc.lecroy_data(lecroy_fileName_DBY)
#        seg_time_DBY = lecroy_DBY.get_seg_time()
        segments_DBY = lecroy_DBY.get_segments()
    
    # This is the time reported by NLDN that we are trying to find 
    # in the data file
    NLDN_time=RS_time-(timestamp.second+timestamp.microsecond/1e6)
    
    # The time below should coincide with the rising edge of the ground
    # wave reported by NLDN. However, the NLDN time resolution is in the 
    # order of 100s of ms, so the ground wave might actually be 100 ms
    # to the right or to the left of the GW_time_at_antenna
    GW_time_at_antenna=NLDN_time+Horizontal_distance/2.99e8
    
    plt.plot(t,segments_DBY[0],'r')    
    plt.plot([NLDN_time,NLDN_time],[-1,1])
    plt.plot([GW_time_at_antenna,GW_time_at_antenna],[-1,1])
    plt.plot([GW_time_at_antenna+100e-3,GW_time_at_antenna+100e-3],[-1,1],'--')
    plt.plot([GW_time_at_antenna-100e-3,GW_time_at_antenna-100e-3],[-1,1],'--')
    UTC_time= "%r:%r:%r" %(timestamp.hour,timestamp.minute,\
                           timestamp.second+timestamp.microsecond/1e6)
    plt.xlabel("Time in seconds after "+str(UTC_time))
    plt.title('Complete 200 ms file the ground wave \n'
               'should be around the solid line')
    plt.show()

    t0=GW_time_at_antenna
              
    # Rename variables to filter nmore easily
    skywave=segments_DBY[0];
    time=t;

    return time,skywave,UTC_time,t0,timestamp