# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:56:12 2015

@author: lenz
This code plots the skywaves from natural lightning NLDN data
Skywave_plot_general returns: time, skywave,UTC_time,t0 

It also removes the 60 Hz slope
"""
from Skywaves_plot_general import Natural_Skywaves
import csv

x_min=0*1e6
x_max=0.3

suffix=200
ofile=open('022316_Trace_number_to_IRIG.csv','w')

mywriter=csv.writer(ofile)
mywriter.writerow(['trace# ','IRIG initial time stamp']) #Each columns title
for suffix in range (100,110):
    
    time,skywave,UTC_time,t0,initial_timestamp=Natural_Skywaves(2016,1,22316,10e6,suffix,0,x_max)
    print('suffix: %r, IRIG initial time stamp: %r' %(suffix, initial_timestamp))
    mywriter.writerow([suffix,initial_timestamp])

ofile.close()