#!/usr/bin/python

# Program to read and process LeCroy ".trc" files
#
# This program was originally written by Brian Hare and was modified by Jaime
# Caicedo to extend its functionality.
#
# Author: Jaime Caicedo, PhD Student, ILCRT
# Last Updated: 07/20/2014

import struct
import numpy as np
from datetime import datetime

class lecroy_data(object):
    def __init__(self, f_name):
        with open(f_name,'rb') as fin:
            ##header_data=fin.read(357)

            self.dummy=fin.read(11)
            self.descriptor_name=fin.read(16)
            self.template_name=fin.read(16)

            self.comm_type=struct.unpack('h',fin.read(2))[0] ## byte or word
            
            self.comm_order=struct.unpack('h',fin.read(2))[0]## HiFirst or LoFirst
            self.endianness = '<' if self.comm_order else '>'
            
            self.wave_descriptor=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.user_text=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.res_desc1=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.trig_time_array=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.ris_time_array=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.res_array1=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.wave_array_1=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.wave_array_2=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.res_array2=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.res_array3=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.instrament_array=fin.read(16)
            self.instrament_number=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.trace_label=fin.read(16)
            self.reserved1=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.reserved2=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.wave_array_count=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.pnts_per_screen=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.first_valid_pnt=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.last_valid_point=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.first_point=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.sparsing_factor=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.segment_index=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.subarray_count=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.sweeps_per_acq=struct.unpack(self.endianness + 'l',fin.read(4))[0]
            self.points_per_pair=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.pair_offset=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.vertical_gain=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.vertical_offset=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.max_value=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.min_value=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.nominal_bits=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.nom_subarray_count=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.horiz_interval=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.horiz_offset=struct.unpack(self.endianness + 'd',fin.read(8))[0]
            self.pixel_offset=struct.unpack(self.endianness + 'd',fin.read(8))[0]
            self.vert_unit=fin.read(48)
            self.hor_unit=fin.read(48)
            self.horiz_uncertanty=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.time_stamp_seconds=struct.unpack(self.endianness + 'd',fin.read(8))[0]
            self.time_stamp_minutes=struct.unpack(self.endianness + 'B',fin.read(1))[0]
            self.time_stamp_hours=struct.unpack(self.endianness + 'B',fin.read(1))[0]
            self.time_stamp_days=struct.unpack(self.endianness + 'B',fin.read(1))[0]
            self.time_stamp_months=struct.unpack(self.endianness + 'B',fin.read(1))[0]
            self.time_stamp_year=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.time_stamp_unused=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.acq_duration=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.lecroy_record_type=struct.unpack(self.endianness + 'h',fin.read(2))[0]
                ## singlesweep
                ##interleaved
                ##histogram
                ##graph
                ##filter coefficient
                ##complex
                ##extrema
                ##sequence obsolete
                ##centered RIS
                ##peak detect
            self.processing_done=struct.unpack(self.endianness + 'h',fin.read(2))[0]
                ##no processing
                ##fir filter
                ##interpolated
                ##sparsed
                ##autoscaled
                ##no_result
                ##rolling
                ##cumulative
            self.reserved5=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.RIS_sweeps=struct.unpack(self.endianness + 'h',fin.read(2))[0]
            self.timebase=struct.unpack(self.endianness + 'h',fin.read(2))[0]
##                                        tb1_ps
##                                      tb2_ps,
##                                      tb5_ps,
##                                      tb10_ps,
##                                      tb20_ps,
##                                      tb50_ps,
##                                      tb100_ps,
##                                      tb200_ps,
##                                      tb500_ps,
##                                      tb1_ns,
##                                      tb2_ns,
##                                      tb5_ns,
##                                      tb10_ns,
##                                      tb20_ns,
##                                      tb50_ns,
##                                      tb100_ns,
##                                      tb200_ns,
##                                      tb500_ns,
##                                      tb1_us,
##                                      tb2_us,
##                                      tb5_us,
##                                      tb10_us,
##                                      tb20_us,
##                                      tb50_us,
##                                      tb100_us,
##                                      tb200_us,
##                                      tb500_us,
##                                      tb1_ms,
##                                      tb2_ms,
##                                      tb5_ms,
##                                      tb10_ms,
##                                      tb20_ms,
##                                      tb50_ms,
##                                      tb100_ms,
##                                      tb200_ms,
##                                      tb500_ms,
##                                      tb1_s,
##                                      tb2_s,
##                                      tb5_s,
##                                      tb10_s,
##                                      tb20_s,
##                                      tb50_s,
##                                      tb100_s,
##                                      tb200_s,
##                                      tb500_s,
##                                      tb1_ks,
##                                      tb2_ks,
##                                      tb5_ks,
##                                      External=100

            self.vert_coupling=struct.unpack(self.endianness + 'h',fin.read(2))[0]
##                                      DC_50_Ohms,
##                                      DC_ground,
##                                      DC_1MOhm,
##                                      AC_ground,
##                                      AC_1MOhm

            self.probe_att=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.fixed_vert_gain=struct.unpack(self.endianness + 'h',fin.read(2))[0]
##                                      g1_uV_Per_Div,
##                                      g2_uV_Per_Div,
##                                      g5_uV_Per_Div,
##                                      g10_uV_Per_Div,
##                                      g20_uV_Per_Div,
##                                      g50_uV_Per_Div,
##                                      g100_uV_Per_Div,
##                                      g200_uV_Per_Div,
##                                      g500_uV_Per_Div,
##                                      g1_mV_Per_Div,
##                                      g2_mV_Per_Div,
##                                      g5_mV_Per_Div,
##                                      g10_mV_Per_Div,
##                                      g20_mV_Per_Div,
##                                      g50_mV_Per_Div,
##                                      g100_mV_Per_Div,
##                                      g200_mV_Per_Div,
##                                      g500_mV_Per_Div,
##                                      g1_V_Per_Div,
##                                      g2_V_Per_Div,
##                                      g5_V_Per_Div,
##                                      g10_V_Per_Div,
##                                      g20_V_Per_Div,
##                                      g50_V_Per_Div,
##                                      g100_V_Per_Div,
##                                      g200_V_Per_Div,
##                                      g500_V_Per_Div,
##                                      g1_kV_Per_Div

            self.bandwidth_limit=struct.unpack(self.endianness + 'h',fin.read(2))[0] ## on or off
            self.vertical_vernier=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.acq_vertical_offset=struct.unpack(self.endianness + 'f',fin.read(4))[0]
            self.wave_source=struct.unpack(self.endianness + 'h',fin.read(2))[0]
##                                        Channel_1,
##                                      Channel_2,
##                                      Channel_3,
##                                      Channel_4,
##                                      unknown=9

            self.user_text_data = fin.read(self.user_text)
            self.trig_time_array_data = fin.read(self.trig_time_array)
            self.ris_time_array_data = fin.read(self.ris_time_array)           
     
            original_data_string=fin.read()

            self.data_type = 'i2' if self.comm_type else 'i1'           
            
            self.Data=np.fromstring(original_data_string,dtype=self.endianness + self.data_type)
            
            self.Data = self.Data * self.vertical_gain - self.vertical_offset
            
    def get_trig_time_array_data(self):
        return np.fromstring(self.trig_time_array_data, dtype=self.endianness + 'f8')   
        
    def get_ris_time_array_data(self):
        return np.fromstring(self.ris_time_array_data, dtype=self.endianness + 'f8')
        
    def get_segments(self):
        segments = []
        pts_segment = len(self.Data) / self.subarray_count
        
        for i in range(self.subarray_count):
           segment = self.Data[i*pts_segment:(i+1)*pts_segment]
           
           segments.append(segment)
           
        return segments
        
    def get_segment(self, num=1, calFactor=1):
        seg = self.get_segments()
        
        self.data = seg[num - 1] * calFactor
        
    def get_seg_time(self):
        self.dataTime = np.arange(0, len(self.Data) / self.subarray_count) * \
                        self.horiz_interval

        return self.dataTime
        #~ return np.arange(0,len(self.Data) / self.subarray_count)*self.horiz_interval #- self.horiz_offset    
        
    def get_time(self):
        return np.arange(0,len(self.Data))*self.horiz_interval  #- self.horiz_offset

    def repack_header(self):
        ret=self.dummy+self.descriptor_name+self.template_name
        ret += struct.pack(self.endianness + 'h',self.comm_type)
        ret += struct.pack(self.endianness + 'h',self.comm_order)
        ret += struct.pack(self.endianness + 'l',self.wave_descriptor)
        ret += struct.pack(self.endianness + 'l',self.user_text)
        ret += struct.pack(self.endianness + 'l',self.res_desc1)
        ret += struct.pack(self.endianness + 'l',self.trig_time_array)
        ret += struct.pack(self.endianness + 'l',self.ris_time_array)
        ret += struct.pack(self.endianness + 'l',self.res_array1)
        ret += struct.pack(self.endianness + 'l',self.wave_array_1)
        ret += struct.pack(self.endianness + 'l',self.wave_array_2)
        ret += struct.pack(self.endianness + 'l',self.res_array2)
        ret += struct.pack(self.endianness + 'l',self.res_array3)
        ret += self.instrament_array
        ret += struct.pack(self.endianness + 'l',self.instrament_number)
        ret += self.trace_label
        ret += struct.pack(self.endianness + 'h',self.reserved1)
        ret += struct.pack(self.endianness + 'h',self.reserved2)
        ret += struct.pack(self.endianness + 'l',self.wave_array_count)  #this one
        ret += struct.pack(self.endianness + 'l',self.pnts_per_screen)  #this one
        ret += struct.pack(self.endianness + 'l',self.first_valid_pnt)
        ret += struct.pack(self.endianness + 'l',self.last_valid_point)
        ret += struct.pack(self.endianness + 'l',self.first_point)
        ret += struct.pack(self.endianness + 'l',self.sparsing_factor)
        ret += struct.pack(self.endianness + 'l',self.segment_index)
        ret += struct.pack(self.endianness + 'l',self.subarray_count)
        ret += struct.pack(self.endianness + 'l',self.sweeps_per_acq)
        ret += struct.pack(self.endianness + 'h',self.points_per_pair)
        ret += struct.pack(self.endianness + 'h',self.pair_offset)
        ret += struct.pack(self.endianness + 'f',self.vertical_gain)
        ret += struct.pack(self.endianness + 'f',self.vertical_offset)
        ret += struct.pack(self.endianness + 'f',self.max_value)  #this one
        ret += struct.pack(self.endianness + 'f',self.min_value)  #this one
        ret += struct.pack(self.endianness + 'h',self.nominal_bits)
        ret += struct.pack(self.endianness + 'h',self.nom_subarray_count)
        ret += struct.pack(self.endianness + 'f',self.horiz_interval)
        ret += struct.pack(self.endianness + 'd',self.horiz_offset)
        ret += struct.pack(self.endianness + 'd',self.pixel_offset)
        ret += self.vert_unit
        ret += self.hor_unit
        ret += struct.pack(self.endianness + 'f',self.horiz_uncertanty)
        ret += struct.pack(self.endianness + 'd',self.time_stamp_seconds)
        ret += struct.pack(self.endianness + 'B',self.time_stamp_minutes)
        ret += struct.pack(self.endianness + 'B',self.time_stamp_hours)
        ret += struct.pack(self.endianness + 'B',self.time_stamp_days)
        ret += struct.pack(self.endianness + 'B',self.time_stamp_months)
        ret += struct.pack(self.endianness + 'h',self.time_stamp_year)
        ret += struct.pack(self.endianness + 'h',self.time_stamp_unused)
        ret += struct.pack(self.endianness + 'f',self.acq_duration)
        ret += struct.pack(self.endianness + 'h',self.lecroy_record_type)
        ret += struct.pack(self.endianness + 'h',self.processing_done)
        ret += struct.pack(self.endianness + 'h',self.reserved5)
        ret += struct.pack(self.endianness + 'h',self.RIS_sweeps)
        ret += struct.pack(self.endianness + 'h',self.timebase)
        ret += struct.pack(self.endianness + 'h',self.vert_coupling)
        ret += struct.pack(self.endianness + 'f',self.probe_att)
        ret += struct.pack(self.endianness + 'h',self.fixed_vert_gain)
        ret += struct.pack(self.endianness + 'h',self.bandwidth_limit)
        ret += struct.pack(self.endianness + 'f',self.vertical_vernier)
        ret += struct.pack(self.endianness + 'f',self.acq_vertical_offset)
        ret += struct.pack(self.endianness + 'h',self.wave_source)

        return ret

    def repack_data(self):
        return self.Data.tostring()

    def get_timestamp(self):
            
        sec = self.time_stamp_seconds
        min = self.time_stamp_minutes
        hour_ = self.time_stamp_hours
        day_ = self.time_stamp_days
        month_ = self.time_stamp_months
        year_ = self.time_stamp_year
        micro = (sec-int(sec))*1000000

        return datetime(year=year_, month=month_, day=day_, hour=hour_,
                        minute=min, second=int(sec), microsecond=int(micro))
