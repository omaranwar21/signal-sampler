from audioop import add
from signal import signal
import streamlit as st
import matplotlib.pyplot as plt
from utils import samplingRate
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="Signal Sampler",
    layout="wide"
)

simulated_signal=[]
st.title("Signal Sampler")

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   The *BERT Keyword Extractor* app is an easy-to-use interface built in Streamlit for the amazing [KeyBERT](https://github.com/MaartenGr/KeyBERT) library from Maarten Grootendorst!
-   It uses a minimal keyword extraction technique that leverages multiple NLP embeddings and relies on [Transformers] (https://huggingface.co/transformers/) 🤗 to create keywords/keyphrases that are most similar to a document.
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

with c4: 
    choose_signal= st.radio("Choose Signal",options=("Uploading Signal","Simulating"),horizontal=True)
    if choose_signal=="Simulating":
        
        add_signal=st.button("Add Signal")
        if add_signal:
            with st.form("Signal Info"):
                siganl_name= st.text_input("Enter Signal Name")
                signal_freq= st.slider("Choose Signal freqency",key="freq_value")
                signal_mag= st.slider("Choose Signal magnitude",key="mag_value")
                def add_data():
                    data= [siganl_name, signal_freq,signal_mag]
                    simulated_signal.append(data)
                    print(simulated_signal)
                add_button=st.form_submit_button(on_click=lambda: add_data())
                
                    
        if(simulated_signal):
            st.select_slider("Select a Signal", simulated_signal)          

with c2:
    
    st.line_chart()
