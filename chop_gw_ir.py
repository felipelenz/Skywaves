# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:43:51 2016

@author: lenz
This function breaks electric field data into two parts: The Ground wave and 
the Sky wave at the sample point=2500. Everything before 2500 is the ground wave
and everything after sample 2500 is skywave
"""

#############################
# Break data into GW and IR #
#############################
def chop_gw_ir(remove_60Hz_slope_output):
    gw_ir_ref=2500 #we define this sample number to be the point where groundwave 
               #becomes skywave. This point doesn't need to be very well defined
               #we just put it here to make the code cleaner
    gw_time=remove_60Hz_slope_output[0][1:gw_ir_ref]
    gw_data=remove_60Hz_slope_output[1][1:gw_ir_ref]
    ir_time=remove_60Hz_slope_output[0][gw_ir_ref:-1]
    ir_data=remove_60Hz_slope_output[1][gw_ir_ref:-1]
    return gw_time,gw_data,ir_time,ir_data