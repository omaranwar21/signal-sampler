import streamlit as st
from utils import download_signal, read_csv, read_wav, reconstructor, render_svg, sampled_signal_maxf, samplingRate, signal_sum, sampled_signal, add_noise
import numpy as np
import pandas as pd
import plotly.graph_objects as go



st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(
    page_title="Signal Sampler",
    page_icon="📈",
    layout="wide"
)
render_svg("svg.svg")

with open("style.css") as design:
    st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)

# Initialization of Session State attributes (time,uploaded_signal,maxf)
if 'time' not in st.session_state:
    st.session_state.time =np.linspace(0,5,2000)
if 'uploaded_signal' not in st.session_state:
    st.session_state.uploaded_signal = np.zeros(st.session_state.time.shape)
if 'maxf' not in st.session_state:
    st.session_state.maxf = 1


def add_simulated_signal():
    if st.session_state.signal_name =="":
        st.session_state.signal_name="Signal_"+str(len(st.session_state.simulated_signal)+1)
    st.session_state.simulated_signal[st.session_state.signal_name]={
        "freq_value":st.session_state.freq_value,
        "freq_scale":st.session_state.add_signal_freq_scale,
        "mag_value":st.session_state.mag_value
    }    

# Initialization of Session State attribute (simulated_signal)
if "simulated_signal" not in st.session_state:
    st.session_state.simulated_signal= {}


# c1,_ = st.columns([2,5])
# with c1:
#     file=st.file_uploader(label="Upload Signal File", key="uploaded_file")
#     if file:
#         signal, time, maxF=read_wav(file)
#         st.session_state.uploaded_signal=signal
#         st.session_state.time= time
#         st.session_state.maxf= maxF
    
ce, c4,  c2, c1, ce = st.columns([0.07, 1,  3.5, 1, 0.07])
#column 1 responsible for sampling rate slider and adding noise
with c1:
    
    sampling_options=("10Hz","100Hz","1KHz","10KHz","100KHz")
    # if st.session_state.uploaded_file:
    #     sampling_options=("10Hz","100Hz","1KHz","10KHz","100KHz","F(max)Hz")
    #sampling_rate_scale variable to store scale of frequency from selectbox
    sampling_rate_scale= st.selectbox("Scale of freq.",sampling_options,key="sampling_rate_scale")
    #getting maxV, minV,step,format values from samplingRate() function
    maxV, minV,step, format= samplingRate(sampling_rate_scale)
    #adding sampling rate slider to get sampling rate from user
    sampling_rate = st.slider(
            "sampling rate",
            min_value=minV,
            max_value=maxV,
            step=step,
            format=format,
            key="sampling_rate"
        )
    noise_checkbox=st.checkbox("Add Noise",key="noise_checkbox")
    if noise_checkbox:
        noise=st.slider("SNR",min_value=1.0,step=0.5,max_value=100.0,key="noise_slider")

#column 4 responsible for uploading and simulating signals
with c4: 
    #radio buttons to select to upload or simulate signal
    choose_signal= st.radio("Choose Signal",options=("Uploaded Signal","Simulating"),horizontal=True, key="choose_signal")
    if choose_signal=="Simulating":
        #slider to select signal period
        signal_period= st.slider("Signal Period",min_value=0.1,max_value=10.0,step=0.1,value=1.0,format="%fsec",key="signal_period")
        #button to add signal
        add_signal=st.button("Add Signal")
        if add_signal:
            #form to take added signal values(Signal Name, Signal Frequency, Signal Magnitude) from user
            with st.form("add_signal_form"):
                signal_name= st.text_input("Enter Signal Name", key="signal_name")
                sampling_rate_scale= st.selectbox("Scale of freq.",("100Hz","100KHz"),key="add_signal_freq_scale")
                signal_freq = st.slider(
                        "Choose Signal freqency",
                        min_value=0.0,
                        max_value=100.0,
                        step=0.5,
                        value=1.0,
                        key="freq_value"
                    )
                signal_mag= st.slider("Choose Signal magnitude",value=1.0,min_value=0.0,max_value=100.0,step=0.5,key="mag_value")
                add_button=st.form_submit_button("Add Signal",on_click=add_simulated_signal)
    elif choose_signal=="Uploaded Signal":
        file=st.file_uploader(label="Upload Signal File", key="uploaded_file",type=["csv","wav"])
        if file:
            if file.name.split(".")[-1]=="wav":
                signal, time=read_wav(file)
                st.session_state.uploaded_signal=signal
                st.session_state.time= time
            elif file.name.split(".")[-1]=="csv":
                signal, time=read_csv(file)
                st.session_state.uploaded_signal=signal
                st.session_state.time= time
    selected_graphs= st.selectbox("Select type of graph",("Signal with Samples","Samples Only","Signal Only","Reconstructed Signal"),key="graph_type")        
with c1:
    if st.session_state.simulated_signal:
        df=st.session_state.simulated_signal.values()
        # frquency=st.session_state.simulated_signal[st.session_state.signal_name]["freq_value"]
        # st.write(st.session_state.signal_name)
        # st.write(st.session_state.simulated_signal[st.session_state.signal_name])
        
        # st.table(df)
        with st.expander("Edit Signal"):
            remove_box= st.selectbox("choose a signal", st.session_state.simulated_signal.keys())
            # st.write(remove_box)
            frquency=st.session_state.simulated_signal[remove_box]["freq_value"]
            magnitude=st.session_state.simulated_signal[remove_box]["mag_value"]
            st.write('Frequency = ',frquency,'Hz')
            st.write('Amplitude = ',magnitude)

            remove_button=st.button("remove")
            if remove_button:
                del st.session_state.simulated_signal[remove_box]

        with st.expander("View Signals Table"):
            st.dataframe(df,use_container_width=True, height=178)

        
                



with c2:
    signal_flag=False
    sample_flag=False
    reconstruction_flag=False
    if(st.session_state.graph_type=="Signal with Samples"):
        signal_flag=True
        sample_flag=True
        reconstruction_flag=False
    elif(st.session_state.graph_type=="Samples Only"):
        sample_flag=True
        signal_flag=False
        reconstruction_flag=False
    elif(st.session_state.graph_type=="Signal Only"):
        signal_flag=True
        sample_flag=False
        reconstruction_flag=False
    elif(st.session_state.graph_type=="Reconstructed Signal"):
        signal_flag=True
        sample_flag=True
        reconstruction_flag=True

    time=np.linspace(0,5,2000)
    full_signals=np.zeros(time.shape)
    if st.session_state.choose_signal =="Uploaded Signal":
        full_signals, time= st.session_state.uploaded_signal, st.session_state.time
    
    else:
        time= np.linspace(0, st.session_state.signal_period, int(st.session_state.signal_period*500))
    
        full_signals=signal_sum(st.session_state.simulated_signal,time)

    if st.session_state.noise_checkbox:
        full_signals=add_noise(full_signals,st.session_state.noise_slider)
    fig = go.Figure()
    fig2=go.Figure()
    if signal_flag:
        fig.add_trace(go.Scatter(x=time,
                                 y=full_signals,
                                 mode='lines',
                                 name='lines'))
    if sample_flag:
        if st.session_state.sampling_rate_scale=="F(max)Hz":
            sampled_x, sampled_time=sampled_signal_maxf(full_signals,time, st.session_state.sampling_rate, st.session_state.maxf)
        else:
            sampled_x, sampled_time=sampled_signal(full_signals,time, st.session_state.sampling_rate, st.session_state.sampling_rate_scale)
        fig.add_trace(go.Scatter(x=sampled_time,
                                 y=sampled_x,
                                 mode='markers',
                                 name='markers'))
    if reconstruction_flag:
        if st.session_state.sampling_rate_scale=="F(max)Hz":
            sampled_x, sampled_time=sampled_signal_maxf(full_signals,time, st.session_state.sampling_rate, st.session_state.maxf)
        else:
            sampled_x, sampled_time=sampled_signal(full_signals,time, st.session_state.sampling_rate, st.session_state.sampling_rate_scale)
        if len(sampled_time) != 1:
            recon_signal=reconstructor(time, sampled_time,sampled_x)
            fig2.add_trace(go.Scatter(x=time, y=recon_signal,
                    mode='lines',
                    name='lines'))
            fig2.update_xaxes(showgrid=False)
            fig2.update_yaxes(showgrid=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
        title="Original Signal",
        xaxis_title="Time",
        yaxis_title="Amplitude",
        margin=dict(l=0,r=0,b=5,t=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

    fig.update_yaxes(automargin=True)
    st.plotly_chart(fig,use_container_width=True)


    if reconstruction_flag:
        fig2.update_layout(
            # title="Reconstructed Signal",
            xaxis_title="Time",
            yaxis_title="Amplitude",
            margin=dict(l=0,r=0,b=0,t=3.5),
        )
        fig2.update_xaxes(showgrid=False)
        fig2.update_yaxes(
            showgrid=False,
            automargin=True,
        )
        st.plotly_chart(fig2, use_container_width=True)

with c1:
    st.download_button(label="Download data as CSV", data=download_signal(full_signals,time),file_name="signal_data.csv",mime='text/csv')