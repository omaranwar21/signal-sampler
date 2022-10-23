# Signal Sampler

> Signal sampler is a digital signal processing website to see the effect of changing the sampling rate of any signal, how some points can affect you signal.

## Getting Started

### Dependencies

- python 3.9
- streamlit 1.13
- plotly

### installing

1. first you need to install
   [Python](https://www.python.org/downloads/).
2. clone the Repo

```
git clone https://github.com/youssef-shaban/DSP_Task1_4.git
```

3. and then run this in terminal

```
$ pip install -r requirements.txt
```

### Excuting program

```
$ streamlit run app.py
```

## Features

- Open CSV or WAV signal

![Screenshot 2022-10-23 091419](https://user-images.githubusercontent.com/85808789/197392085-44e394e9-4089-423a-bbc3-c740c7a4acf2.jpg)



- Mix sin waves toghter to generate a new signal

![Signal Mixer](img\Screenshot 2022-10-23 141305.jpg)

- Sample Signal with any frequncy

![Sampling Signal](img\Screenshot 2022-10-23 141528.jpg)

- Reconstruct Sampled signal to see the affect of sampling

![Signal Reconstruction](img\Screenshot 2022-10-23 141822.jpg)

- Noise to Signal

![Add Noise](img\Screenshot 2022-10-23 142045.jpg)

- with more features like downloading Signal and edit signals in Signal mixer
