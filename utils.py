import numpy as np
from scipy.io import wavfile
from scipy import signal, fft
import base64
import streamlit as st
import pandas as pd


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
        step=0.01
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
        maxV= 5.0
        minV=0.1
        step=0.1
        format="%fF(max)Hz"
    return maxV,minV, step, format

def signal_sum(Signals,time):
    keys= Signals.keys()
    Sum=np.zeros(len(time))
    for i in keys:
        signal= Signals[i]["mag_value"]*np.sin(2*np.pi*Signals[i]["freq_value"]*time)
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

def sampled_signal_maxf(signal, time,sample_freq,maxf):
    sample_rate= int((len(time)/time[-1])/(sample_freq*maxf))
    if sample_rate==0:
        sample_rate=1
    sampled_time= time[::sample_rate]
    sampled_signal= signal[::sample_rate]
    return sampled_signal, sampled_time

def add_noise(signal, SNR):
    signal_avg_power= np.mean(signal**2)
    signal_avg_power_db= 10*np.log(signal_avg_power)
    noise_db= signal_avg_power_db-SNR
    noise_power= 10**(noise_db/10)
    noise= np.random.normal(0,np.sqrt(noise_power),len(signal))
    noisy_signal=signal+noise
    return noisy_signal

def read_wav(file):
    try:
        sample_rate, samples = wavfile.read(file)
        time= np.linspace(0,samples.shape[0]/sample_rate,samples.shape[0] )
        return samples, time
    except:
        time=np.linspace(0,5,2000)
        full_signals=np.zeros(time.shape)
        return full_signals, time


def reconstructor(recon_signal_points, sampled_time, sampled_signal):
    
    u = np.resize(recon_signal_points, (len(sampled_time), len(recon_signal_points)))
    v = (u.T-sampled_time) / (sampled_time[1] - sampled_time[0])
    m = sampled_signal * np.sinc(v)
    recon_signal = np.sum(m, axis = 1)
    return recon_signal



def render_svg(svg):
    """Renders the given svg string."""
    svg=open(svg).read()
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

@st.cache
def download_signal(signal,time):
    df= pd.DataFrame({"Y":signal,"X":time})
    return df.to_csv().encode("utf-8")
def read_csv(file):
    try:
        df= pd.read_csv(file)
        signal= np.array(df['Y'])
        time= np.array(df["X"])
        return signal,time
    except:
        return ValueError("Import a file with X as time and Y as amplitude")