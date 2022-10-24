from turtle import position
import streamlit as st
from utils import download_signal, read_csv, read_wav, reconstructor, render_svg, sampled_signal_maxf, samplingRate, signal_sum, sampled_signal, add_noise
import numpy as np
import pandas as pd
import plotly.graph_objects as go



st.set_page_config(
    page_title="Signal Sampler",
    page_icon="📈",
    layout="wide"
)
render_svg("svg.svg")

with open("style.css") as design:
    st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)

# Initialization of Session State attributes (time,uploaded_signal)
if 'time' not in st.session_state:
    st.session_state.time =np.linspace(0,5,2000)
if 'uploaded_signal' not in st.session_state:
    st.session_state.uploaded_signal = np.sin(2*np.pi*st.session_state.time)


#function to add new signal
def add_simulated_signal():
    if st.session_state.signal_name =="":
        st.session_state.signal_name="Signal_"+str(len(st.session_state.simulated_signal)+1)
    if st.session_state.signal_name in st.session_state.simulated_signal.keys():
        left_column.error("duplicated Name")
        return 
    st.session_state.simulated_signal[st.session_state.signal_name]={
        "freq_value":st.session_state.freq_value,
        "mag_value":st.session_state.mag_value
    }
    st.session_state.signal_name=""
#function to edit selected signal
def edit_simulated_signal(signal_name,freq,mag):
    st.session_state.simulated_signal[signal_name]={
        "freq_value": freq,
        "mag_value": mag
    }

# Initialization of Session State attribute (simulated_signal)
if "simulated_signal" not in st.session_state:
    st.session_state.simulated_signal= {"signal_1":{"mag_value":1,"freq_value":1}}

ce, left_column,  middle_column, right_column, ce = st.columns([0.07, 1,  3.5, 1, 0.07])
#right_column responsible for : sampling rate slider , adding noise ,editing and removing signals , Downloading Signal
with right_column:
    st.header(" ")
    sampling_options=("10Hz","100Hz","1KHz")
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
            value=2.0,
            format=format,
            key="sampling_rate"
        )
    noise_checkbox=st.checkbox("Add Noise",key="noise_checkbox")
    if noise_checkbox:
        noise=st.slider("SNR db",min_value=0,step=1,max_value=50,value=50,key="noise_slider")
    st.write("Graph")
    signal_flag = st.checkbox('Signal', value= True)  
    sample_flag = st.checkbox('Samples',value=True)  
    reconstruction_flag = st.checkbox('Reconstructed')  

    
        
#End of right_column

#left_column responsible for : uploading ot simulating signals , selecting seginal period , add signals ,selecting type of graph 
with left_column:
        #Editing Expander
    file=st.file_uploader(label="Upload Signal File", key="uploaded_file",type=["csv","wav"])
    browseButton_style = f"""
    <style>
        .css-1plt86z .css-186ux35{{
        display: none !important;
    }}

    .css-1plt86z{{
        cursor: pointer !important;
        user-select: none;
    }}

    .css-u8hs99{{
        flex-direction: column !important;
        text-align: center;
        margin-right: AUTO;
        margin-left: auto;
    }}

    .css-1m59kx1{{
        margin-right: 0rem !important;
    }}
    </style>
    """  
    st.markdown(browseButton_style, unsafe_allow_html=True)
    if file:
        if file.name.split(".")[-1]=="wav":
            signal, time=read_wav(file)
            st.session_state.uploaded_signal=signal
            st.session_state.time= time
        elif file.name.split(".")[-1]=="csv":
            try:
                signal, time=read_csv(file)
                st.session_state.uploaded_signal=signal
                st.session_state.time= time
            except:
                st.error("Import a file with X as time and Y as amplitude")
    edit_option_radio_button= st.radio("Edit option",options=("Add","Remove"),horizontal=True, key="edit_option_radio_button")
    

    if edit_option_radio_button == "Remove":
        selected_name= st.selectbox("choose a signal", st.session_state.simulated_signal.keys())
        disable_remove=True
        if selected_name!=None:
            disable_remove=False
            frquency=st.session_state.simulated_signal[selected_name]["freq_value"]
            magnitude=st.session_state.simulated_signal[selected_name]["mag_value"]
            st.write('Frequency = ',frquency,'Hz')
            st.write('Amplitude = ',magnitude)
        remove_button=st.button("Remove",disabled=disable_remove)
        if remove_button:
            if selected_name!=None:
                del st.session_state.simulated_signal[selected_name]
    elif edit_option_radio_button=="Add":
        signal_name= st.text_input("Enter Signal Name",key="signal_name")
        signal_freq = st.slider(
                "Freqency",
                min_value=1,
                max_value=100,
                step=1,
                value=1,
                key="freq_value",
                format=format
            )
        signal_mag= st.slider("Amplitude",value=1,min_value=1,max_value=100,step=1,key="mag_value")
        add_button=st.button("Add Signal",on_click=add_simulated_signal)
        
    # selected_graphs= st.selectbox("Select type of graph",("Signal with Samples","Samples Only","Signal Only","Reconstructed Signal","Display All"),key="graph_type")
    


#End of left_column

#middle_column responsible for viewing signals graphs(Original and Reconstructed)
with middle_column:

    time=np.linspace(0,5,2000)
    full_signals=np.zeros(time.shape)
    if file:
        full_signals, time= st.session_state.uploaded_signal, st.session_state.time
        full_signals=signal_sum(st.session_state.simulated_signal,time,full_signals)
    
    else:
        time= np.linspace(0, 4, 2000)
    
        full_signals=signal_sum(st.session_state.simulated_signal,time, np.zeros(len(time)))

    if st.session_state.noise_checkbox:
        full_signals=add_noise(full_signals,st.session_state.noise_slider)
    fig = go.Figure()
    if signal_flag:
        fig.add_trace(go.Scatter(x=time,
                                y=full_signals,
                                mode='lines',
                                name='Signal'))
    
    if reconstruction_flag:
        sampled_x, sampled_time=sampled_signal(full_signals,time, st.session_state.sampling_rate, st.session_state.sampling_rate_scale)
        if len(sampled_time) != 1:
            recon_signal=reconstructor(time, sampled_time,sampled_x)
            fig.add_trace(go.Scatter(x=time, y=recon_signal,
                    mode='lines',
                    name='reconstruct', line={"color":"orange"}))
    if sample_flag:
        sampled_x, sampled_time=sampled_signal(full_signals,time, st.session_state.sampling_rate, st.session_state.sampling_rate_scale)
        fig.add_trace(go.Scatter(x=sampled_time,
                                y=sampled_x,
                                mode='markers',
                                name='Samples', marker=dict(color="black",size=10)))
            
    fig.update_xaxes(showgrid=True, zerolinecolor='black', gridcolor='lightblue', range = (-0.1,time[-1]))
    fig.update_yaxes(showgrid=True, zerolinecolor='black', gridcolor='lightblue', range = (-1*(max(full_signals)+0.1*max(full_signals)),(max(full_signals)+0.1*max(full_signals))))
    fig.update_layout(
            font = dict(size = 20),
            xaxis_title="Time (sec)",
            yaxis_title="Amplitude",
            height = 600,
            margin=dict(l=0,r=0,b=5,t=0),
            legend=dict(orientation="h",
                        yanchor="bottom",
                        y=0.92,
                        xanchor="right",
                        x=0.99,
                        font=dict(size= 18, color = 'black'),
                        bgcolor="LightSteelBlue"
                        ),
            paper_bgcolor='rgb(4, 3, 26)',
            plot_bgcolor='rgba(255,255,255)'
        )
    fig.update_yaxes(automargin=True)
    st.plotly_chart(fig,use_container_width=True)

    

    
#End of middle_column

with right_column:
    st.download_button(label="Download data as CSV", data=download_signal(full_signals,time),file_name="signal_data.csv",mime='text/csv')
