import numpy as np
def samplingRate(rate):
    if rate=="10Hz":
        maxV= 10.0
        minV=1.0
        step=0.5
        format="%fHz"
    elif rate=="100Hz":
        maxV= 100.0
        minV=1.0
        step=1.0
        format="%dHz"
    elif rate=="1KHz":
        maxV=1.0
        minV=0.1
        step=0.1
        format="%fKHz"
    elif rate=="10KHz":
        maxV= 10.0
        minV=1.0
        step=0.5
        format="%fKHz"
    elif rate== "100KHz":
        maxV= 100.0
        minV=1.0
        step=1.0
        format="%dKHz"
    elif rate=="F(max)Hz":
        maxV= 100.0
        minV=1.0
        step=1.0
        format="%dKHz"
    return maxV,minV, step, format

def signal_sum(Signals,t):
    keys= Signals.keys()
    Sum=np.zeros(len(t))
    for i in keys:
        factor=1
        if Signals[i]["freq_scale"]=="100KHz":
            factor=1000
        signal= Signals[i]["mag_value"]*np.sin(2*np.pi*Signals[i]["freq_value"]*t*factor)
        Sum+=signal
    return Sum

def sampled_signal(signal, time,sample_freq,scale):
    factor=1
    if scale in ["1KHz","10KHz","100KHz"]:
        factor=1000
    sample_rate= int((len(time)/time[-1])/(sample_freq*factor))
    if sample_rate==0:
        sample_rate=1
    sampled_time= time[::sample_rate]
    sampled_signal= signal[::sample_rate]
    return sampled_signal, sampled_time

def add_noise(signal, SNR):
    noise= np.random.randn(len(signal))
    Es= np.sum(signal**2)
    En= np.sum(noise**2)
    alpha= np.sqrt(Es/(SNR*En))
    d= signal+noise*alpha
    return d