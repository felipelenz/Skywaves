import numpy as np
from datetime import timedelta,datetime
import matplotlib.pyplot as plt
#### for sample code, see read_DAQ.DAQ_time
##def to_seconds(time_delta):
##    ## this is o that we can convert arrays of timedelta objects to arrays of seconds
##    return time_delta.total_seconds()
##to_seconds=np.vectorize(to_seconds) ## so that we can apply this function to arrays

def BCD(data):
    """ given a list of o's and 1's, convert to a binary coded decimal, where the Least significant digit is FIRST. length of data must be divisiable by 4 """
    if len(data)%4 !=0:
        print("ERROR!, length of data must be divisible by 4 in BCD")
        exit()

    N_digits=len(data)/4
    num=0*data[0] ## data may be a list of floats, or list of arrays of floats
    for i in range(int(N_digits)):
        num+=sum( [ (10**i)*(2**ind)*b for ind,b in enumerate(data[4*i:4*(i+1)])]  )
    return num

IRIGA_rate=1000
time_frame=0.1

sampling_rate=10e6
def IRIGA_signal(signal, sampling_rate, year=2000):
    """for a IRIG_A signal that is sampled for sampling_rate (sampling rate is assumed to be perfect)
    this function returns a datetime object and an array of floats that is time in seconds relative to the datetime object
    sampling_rate should be a number, and signal should be a numpy array """
    
    sampling_rate=float(sampling_rate)

    signal=signal>(np.max(signal) + np.min(signal))*0.5 ## seperate signal into "high" and "low"
    ## this signal is a stream of bits. Each bit is when the signal is high. The kind of bit is detemined by the width.
    ## there are exactly 1000 bits per second

    bit_pos=np.where( signal[1:]>signal[:-1] )[0] ## positions of the begining of each bit
    bit_end_pos=np.where( signal[1:]<signal[:-1] )[0]## positions of the ends of each bit

    if signal[0]: ## make sure that there are the same number of endings as begenings of bits. This can be disrupted if the signal starts or ends on high
        bit_end_pos=bit_end_pos[1:]
    if signal[-1]:
        bit_pos=bit_pos[:-1]

    ## there are three kinds of bits. A low bit, which has a time width of 0.0002 seconds. A high bit, which has a width of 0.0005 seconds.  And a position bit which has a width of 0.0008 seconds
    bit_width=bit_end_pos-bit_pos
    bit_type=np.ones(len(bit_width))*-1  ## initialize bit times to -1. Which will mean "unknown bit type"

    bit_type[ np.logical_and(bit_width>=0.0002*sampling_rate-1, bit_width<=0.0002*sampling_rate+1) ] = 0 ## 0 will mean a low bit ## sometimes there is a sampling error, and the width is one point too short or too long
    bit_type[ np.logical_and(bit_width>=0.0005*sampling_rate-1, bit_width<=0.0005*sampling_rate+1) ] = 1  ## 1 will mean a high bit

    ## now all the bit_types that are position bits have the value -1
    ## there are two kinds of position bits: the first kind occurs 10 times in a 0.1 second, this kind counts from 0 to 9. The second kind of position bit is a position referance bit. It happens once in a 0.1 second, and allways happens after a 0 position bit.
    ## thus, if there are two bits in a rwo, the first is a 0 position bit, the second is a position referance bit
    ## we will identify the position referance bit with a 2, and a normal position bit will be identified with a -1
    bit_type[1:][ np.logical_and( bit_type[:-1]==-1, bit_type[1:]==-1) ]=2

    referance_bit_indeces=np.where(bit_type==2)[0] ## the position referance bit (a bit type of 2), always happens at exactly the tenth of a second time
    last_referance_bit=referance_bit_indeces[-1]
    referance_bit_indeces=referance_bit_indeces[:-1] ## the last timeframe will not be complete. So we will ignore it.
    N_time_frames=len(referance_bit_indeces)
    time_frame_signal_pos=bit_pos[referance_bit_indeces]
    ZEROS=np.zeros(N_time_frames)
    
    
    
    
#    BAD= np.where(referance_bit_indeces[:-1]-referance_bit_indeces[1:] + 100 !=0)[0]
#    
#    print referance_bit_indeces[BAD], referance_bit_indeces[BAD+1], referance_bit_indeces[BAD+2]
#    B=0
#
#    print bit_type[referance_bit_indeces[BAD[B]]:referance_bit_indeces[BAD[B]+2]]
#    
#    for RB in xrange(referance_bit_indeces[BAD[B]]-1, referance_bit_indeces[BAD[B]+2]+1):
#        if bit_type[RB]==-1:
#            t='g'
#        elif bit_type[RB]==2:
#            t='b'
#        else:
#            t='r'
#        
#        plt.plot( np.arange(bit_pos[RB],bit_pos[RB+1]), signal[bit_pos[RB]:bit_pos[RB+1]],t)
#    plt.show()
     

    ## now we use the information encoded after each referance bit to find the time information
    ## I don't even know how to document this next bit so that it makes sence. Just trust me.
    seconds=BCD([bit_type[referance_bit_indeces+1],bit_type[referance_bit_indeces+2],bit_type[referance_bit_indeces+3],bit_type[referance_bit_indeces+4],   bit_type[referance_bit_indeces+6],bit_type[referance_bit_indeces+7],bit_type[referance_bit_indeces+8], ZEROS])

    minutes=BCD([bit_type[referance_bit_indeces+10],bit_type[referance_bit_indeces+11],bit_type[referance_bit_indeces+12],bit_type[referance_bit_indeces+13],   bit_type[referance_bit_indeces+15],bit_type[referance_bit_indeces+16],bit_type[referance_bit_indeces+17],ZEROS])

    hours=BCD([bit_type[referance_bit_indeces+20],bit_type[referance_bit_indeces+21],bit_type[referance_bit_indeces+22],bit_type[referance_bit_indeces+23],   bit_type[referance_bit_indeces+25],bit_type[referance_bit_indeces+26],ZEROS,ZEROS])

    days=BCD([bit_type[referance_bit_indeces+30],bit_type[referance_bit_indeces+31],bit_type[referance_bit_indeces+32],bit_type[referance_bit_indeces+33],   bit_type[referance_bit_indeces+35],bit_type[referance_bit_indeces+36],bit_type[referance_bit_indeces+37],bit_type[referance_bit_indeces+38],   bit_type[referance_bit_indeces+40],bit_type[referance_bit_indeces+41],ZEROS,ZEROS ])

    tenths_seconds=BCD([bit_type[referance_bit_indeces+45],bit_type[referance_bit_indeces+46],bit_type[referance_bit_indeces+47],bit_type[referance_bit_indeces+48]])

    ## now we can generate the time objects based on the info in the next frame
    ##time_info=np.empty(N_time_frames, dtype=timedelta)
    initial_timedelta=timedelta(days=days[0], hours=hours[0], minutes=minutes[0], seconds=seconds[0]+tenths_seconds[0]/10.0) - timedelta(seconds=time_frame_signal_pos[0]/float(sampling_rate))
    initial_timestamp=datetime(year=year, month=1, day=1)+initial_timedelta

    time=np.empty(len(signal), dtype=np.double)
    time_indeces=np.arange(len(signal))
    
    start_signal_index=0
    for i in range(N_time_frames):
        
        signal_i=time_frame_signal_pos[i]        
        
        ##check that the frame is good
        if (i!=N_time_frames-1 and referance_bit_indeces[i+1]-referance_bit_indeces[i]!=100) or (i==N_time_frames-1 and last_referance_bit-referance_bit_indeces[i]!=100): 
            ##the frame is bad if there is not exactly 100 bits to the next frame
            seconds_from_timestamp=time[start_signal_index-1]+1.0/sampling_rate ## this may not work. Assumes that seconds from timestamp is at begenning of frame. Is this true?
            print("This IRIG has T1 issues, sugest 'retiming'")
            
        else:
            seconds_from_timestamp=(timedelta(days=days[i], hours=hours[i], minutes=minutes[i], seconds=seconds[i]+tenths_seconds[i]/10.0)-initial_timedelta).total_seconds()
            
        if seconds_from_timestamp<0: ## some other issue I haven't tracked down
            seconds_from_timestamp=time[start_signal_index-1]+1.0/sampling_rate
            print("This IRIG has T2 issues, sugest 'retiming'")
            
        ## there are still more issues I have yet to track down.
            
        time[start_signal_index:signal_i]=seconds_from_timestamp+(time_indeces[start_signal_index:signal_i]-signal_i)/sampling_rate
        
        start_signal_index=signal_i

    ## get the last bit
    time[start_signal_index:]=seconds_from_timestamp+(time_indeces[start_signal_index:]-time_frame_signal_pos[i])/sampling_rate


    ## and I processed a IRIG-A signal in python with only one explit loop.  WOOT!
    return initial_timestamp, time
