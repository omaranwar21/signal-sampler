from audioop import add
from os import remove
from signal import signal
import streamlit as st
import matplotlib.pyplot as plt
from utils import samplingRate
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="Signal Sampler",
    layout="wide"
)

def add_simulated_signal():
    if st.session_state.signal_name =="":
        st.session_state.signal_name="Signal_"+str(len(st.session_state.simulated_signal)+1)
    st.session_state.simulated_signal[st.session_state.signal_name]={
        "freq_value":st.session_state.freq_value,
        "freq_scale":st.session_state.add_signal_freq_scale,
        "mag_value":st.session_state.mag_value
    }
def remove_simulated_signal():
    pass
    

if "simulated_signal" not in st.session_state:
    st.session_state.simulated_signal= {}
st.title("Signal Sampler")

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   The *Signal Sampler* app is an easy-to-use interface built in Streamlit for sampling singals and simulate it
	    """
    )

    st.markdown("")

c1,_ = st.columns([2,5])
with c1:
    file=st.file_uploader(label="Upload Signal File")

ce, c1, ce, c2, ce, c4,ce = st.columns([0.07, 1, 0.07, 3.5, 0.07,1,0.07])
with c1:
    sampling_rate_scale= st.selectbox("Scale of freq.",("10Hz","100Hz","1KHz","10KHz","100KHz","F(max)Hz"))
    maxV, step, format= samplingRate(sampling_rate_scale)
    sampling_rate = st.slider(
            "sampling rate",
            min_value=0.0,
            max_value=maxV,
            step=step,
            format=format,
            key="sampling_rate"
        )
    noise_checkbox=st.checkbox("Add Noise",key="noise_checkbox")
    if noise_checkbox:
        noise=st.slider("SNR",key="noise_slider")

    with st.expander("More Options"):
        st.write("")

with c4: 
    choose_signal= st.radio("Choose Signal",options=("Uploading Signal","Simulating"),horizontal=True)
    if choose_signal=="Simulating":
        
        add_signal=st.button("Add Signal")
        if add_signal:
            with st.form("add_signal_form"):
                signal_name= st.text_input("Enter Signal Name", key="signal_name")
                sampling_rate_scale= st.selectbox("Scale of freq.",("10Hz","100Hz","1KHz","10KHz","100KHz"),key="add_signal_freq_scale")
                maxV, step, format= samplingRate(sampling_rate_scale)
                signal_freq = st.slider(
                        "Choose Signal freqency",
                        min_value=0.0,
                        max_value=maxV,
                        step=step,
                        format=format,
                        key="freq_value"
                    )
                signal_mag= st.slider("Choose Signal magnitude",key="mag_value")
                add_button=st.form_submit_button("Add Signal",on_click=add_simulated_signal)


        if st.session_state.simulated_signal:
            remove_box= st.selectbox("choose a signal", st.session_state.simulated_signal.keys())
            remove_button=st.button("remove")
            if remove_button:
                del st.session_state.simulated_signal[remove_box]
    selected_graphs= st.selectbox("Select type of graph",("Signal with Samples","Samples Only","Signal Only","Reconstructed Signal"))        
        
                



with c2:
    
    st.line_chart()
