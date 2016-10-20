# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 13:20:51 2016

@author: lenz
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:40:55 2016

@author: lenz
"""
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.rcParams.update({'font.size': 22})

x=np.asarray([0,460.5,1014.3,1170.8,1396.6,1736.8])
#Localtime=(["19:24:26.0","19:32:07.0","19:41:20.8","19:43:57.3","19:47:43.1","19:53:23.3"])
Localtime=(["19:24:26.5","19:32:06.6",\
"19:41:20.7","19:43:57.3",\
"19:47:42.7","19:53:22.7"])


dh_UF_xcorr_UF_gaussianfit=np.array([0.00,656.2682,851.39,1552.00,1612.30,1636.20])
dh_error_gaussianfit=np.array([36.91,51.667,273.23,49.13,45.63,58.37])

dh_FIT_xcorr_FIT_gaussianfit=np.array([114.82,447.2007,1.96E+03,1.88E+03,1.97E+03,1.81E+03])
dh_FIT_error_gaussianfit=np.array([6.99,8.1373,38.9902,11.999,10.5587,34.247])


##All REFERRED TO UF 15-38, RS1
plt.subplot(121)
plt.xticks(rotation=90)

plt.xticks(x, Localtime)
plt.plot(x,dh_UF_xcorr_UF_gaussianfit,'D-',label='UF $E_z$',linewidth=2)
for i in range(0,6):
    plt.plot([x[i],x[i]],[dh_UF_xcorr_UF_gaussianfit[i]+dh_error_gaussianfit[i]+130,dh_UF_xcorr_UF_gaussianfit[i]-dh_error_gaussianfit[i]-130],'b+-', markeredgewidth=2,markersize=10,linewidth=2)
plt.plot(x,dh_FIT_xcorr_FIT_gaussianfit,'D-',label='FIT $B_\phi$',linewidth=2)
for i in range(0,6):
    plt.plot([x[i],x[i]],[dh_FIT_xcorr_FIT_gaussianfit[i]+dh_FIT_error_gaussianfit[i]+130,dh_FIT_xcorr_FIT_gaussianfit[i]-dh_FIT_error_gaussianfit[i]-130],'g+-', markeredgewidth=2,markersize=10,linewidth=2)


plt.xlim(-100,1836.8)
plt.ylim(-400,2300)
plt.grid()
plt.ylabel("Effective reflection height \n variation $\Delta h'$ (meters)")
plt.title('All-to-first cross-correlation (best return strokes from each flash)')
plt.xlabel('Local time (hh:mm:ss.s)')
plt.legend(loc=4)


## All to UF 15-38, RS1
dh_38=np.asarray([0.00,143.6538,696.0683,684.5863])
dh_38_error=np.asarray([36.91,88.5014,22.2785,15.6712])
dh_39=np.asarray([656.2682])
dh_39_error=np.asarray([51.667])
dh_40=np.asarray([851.39])
dh_40_error=np.asarray([273.23])
dh_41=np.asarray([881.72,1.05E+03])
dh_41_error=np.asarray([35.32,38.4822])
dh_42=np.asarray([1.36E+03,1.17E+03,1612.30,1201.50])
dh_42_error=np.asarray([34.54,36.4099,45.63,36.58])
dh_43=np.asarray([1750.10,1630.40,1636.20])
dh_43_error=np.asarray([54.39,76.74,58.37])


#dh_best_rs=np.array([0,547,854,1303,1459,1711])
#
x=np.asarray([0,1,2,3,4,5])
time_best_rs=[0,4,5,6,10,14]
time_38=[0,1,2,3]
time_39=[4]
time_40=[5]
time_41=[6,7]
time_42=[8,9,10,11]
time_43=[12,13,14]

plt.subplot(122)

plt.xticks(rotation=90)

plt.xticks(time_best_rs, Localtime)

plt.plot(time_38,dh_38,'Db',label='UF $E_z$',linewidth=2)
for i in range(0,4):
    plt.plot([time_38[i],time_38[i]],[dh_38[i]+dh_38_error[i]+130,dh_38[i]-dh_38_error[i]-130],'b+-', markeredgewidth=2,markersize=10,linewidth=2)

plt.plot(time_39,dh_39,'Dg',label='UF $E_z$',linewidth=2)
for i in range(0,1):
    plt.plot([time_39[i],time_39[i]],[dh_39[i]+dh_39_error[i]+130,dh_39[i]-dh_39_error[i]-130],'g+-', markeredgewidth=2,markersize=10,linewidth=2)

plt.plot(time_40,dh_40,'Dr',label='UF $E_z$',linewidth=2)
for i in range(0,1):
    plt.plot([time_40[i],time_40[i]],[dh_40[i]+dh_40_error[i]+130,dh_40[i]-dh_40_error[i]-130],'r+-', markeredgewidth=2,markersize=10,linewidth=2)

plt.plot(time_41,dh_41,'Dc',label='UF $E_z$',linewidth=2)
for i in range(0,2):
    plt.plot([time_41[i],time_41[i]],[dh_41[i]+dh_41_error[i]+130,dh_41[i]-dh_41_error[i]-130],'c+-', markeredgewidth=2,markersize=10,linewidth=2)

plt.plot(time_42,dh_42,'Dy',label='UF $E_z$',linewidth=2)
for i in range(0,4):
    plt.plot([time_42[i],time_42[i]],[dh_42[i]+dh_42_error[i]+130,dh_42[i]-dh_42_error[i]-130],'y+-', markeredgewidth=2,markersize=10,linewidth=2)

plt.plot(time_43,dh_43,'Dm',label='UF $E_z$',linewidth=2)
for i in range(0,3):
    plt.plot([time_43[i],time_43[i]],[dh_43[i]+dh_43_error[i]+130,dh_43[i]-dh_43_error[i]-130],'m+-', markeredgewidth=2,markersize=10,linewidth=2)

plt.xlim(-1,15)
plt.ylim(-400,2300)
plt.grid()


##
##plt.subplot(122)
#plt.xticks(time_best_rs, Localtime)
##plt.plot(time_best_rs,dh_best_rs,'d-')
#plt.plot(time_38[0],dh_38[0],'Db',markersize=8)
#plt.plot(time_38[1:],dh_38[1:],'ob',label='UF 15-38',markersize=8)
#plt.plot(time_39[0],dh_39[0],'Dg',markersize=8)
#plt.plot(time_39[1:],dh_39[1:],'og',label='UF 15-39',markersize=8)
#plt.plot(time_40[1],dh_40[1],'Dr',markersize=8)
#plt.plot(time_40[0],dh_40[0],'or',label='UF 15-40',markersize=8)
#plt.plot(time_41[0],dh_41[0],'Dc',markersize=8)
#plt.plot(time_41[1:],dh_41[1:],'oc',label='UF 15-41',markersize=8)
#plt.plot(time_42,dh_42,'oy',label='UF 15-42',markersize=8)
#plt.plot(time_42[2],dh_42[2],'Dy',markersize=8)
#plt.plot(time_43[3],dh_43[3],'Dm',markersize=8)
#plt.plot(time_43[0:3],dh_43[0:3],'om',label='UF 15-42',markersize=8)

#plt.xlim(-1,21)
#plt.ylim(-750,2600)
#plt.grid()
plt.ylabel("Effective reflection height \n variation $\Delta h'$ (meters)")
plt.title('All-to-first cross-correlation all return strokes')
plt.xlabel('Local time (hh:mm:ss.s) not to scale')
#plt.legend(loc=2)
#plt.show()
#
#plt.subplot(121)
#x=np.asarray([0,460.5,1014.3,1170.8,1396.6,1736.8])
#plt.xticks(x, Localtime)
#slow_bpoint_Duke=np.asarray([80.2281,81.7677,82.0404,82.3126,82.3126,82.5841])
#slow_bpoint_UF_movavg=np.asarray([82.0289,82.2707,84.2851,83.9753,84.0707,83.9037])
#slow_bpoint_UF_100=np.asarray([82.8974,82.8493,83.3536,83.6170,83.8560,83.4494])
#slow_bpoint_UF_300=np.asarray([81.9804,82.2224,82.9936,82.4156,82.4880,82.1740])
#
#fast_bpoint_Duke=np.asarray([84.2,83.93,85.53,85.0,85.0,85.0])
#fast_bpoint_UF_movavg=np.asarray([84.0880,83.3710,84.1360,84.2790,84.8020,84.2550])
#fast_bpoint_UF_100=np.asarray([84.5200,84.2800,84.9440,85.0600,85.2760,85.2520])
#fast_bpoint_UF_300=np.asarray([83.8900,83.9450,84.4790,84.5050,84.7260,84.9890])
#
#plt.plot(x,slow_bpoint_Duke,'bD-',linewidth=2,label='Duke $B_\phi$')
#plt.plot(x,slow_bpoint_UF_movavg,'rD-',linewidth=2,label='UF $E_z$ (mov. avg.)')
#plt.plot(x,slow_bpoint_UF_100,'gD-',linewidth=2,label='UF $E_z$ (100 kHz LPF)')
#plt.plot(x,slow_bpoint_UF_300,'cD-',linewidth=2,label='UF $E_z$ (300 kHz LPF)')
#
#plt.grid()
#plt.xlim(-100,1836.8)
#plt.ylim(80,86)
#plt.legend(loc=4)
#plt.title('Absolute reflecting height from "slow-break down point"')
#plt.xlabel('Local time (hh:mm:ss.s)')
#plt.ylabel('Absolute reflecting height (km)')
#
#plt.subplot(122)
#plt.xticks(x, Localtime)
#plt.plot(x,fast_bpoint_Duke,'bD--',linewidth=2,label='Duke $B_\phi$')
#plt.plot(x,fast_bpoint_UF_movavg,'rD--',linewidth=2,label='UF $E_z$ (mov. avg.)')
#plt.plot(x,fast_bpoint_UF_100,'gD--',linewidth=2,label='UF $E_z$ (100 kHz LPF)')
#plt.plot(x,fast_bpoint_UF_300,'cD--',linewidth=2,label='UF $E_z$ (300 kHz LPF)')
#plt.grid()
#plt.xlim(-100,1836.8)
#plt.legend(loc=4)
#plt.title('Absolute reflecting height from "fast-break down point"')
#plt.xlabel('Local time (hh:mm:ss.s)')
#plt.ylabel('Absolute reflecting height (km)')
#plt.ylim(80,86)
#plt.show()
#
#x=np.asarray([0,460.5,1014.3,1170.8,1396.6,1736.8])
#plt.xticks(x, Localtime)
#upsampling_Duke=np.asarray([83178.20,83612.95,81005.49,81439.94,83395.56,80788.26])
#downsampling_UF=np.asarray([84917.89,87096.02,82743.54,82743.54,84917.89,82743.54])
#plt.plot(x,downsampling_UF/1000,'bD-',linewidth=2,label='Downsampling $E_z$ to $B_\phi$')
#plt.plot(x,upsampling_Duke/1000,'rD-',linewidth=2,label='Upsampling $B_\phi$ to $E_z$')
#plt.ylabel('Effective reflecting height (km)')
#plt.title('Effective reflecting height from dual-station cross-correlation technique')
#plt.legend()
#plt.xlim(-100,1836.8)
#plt.grid()
plt.show()