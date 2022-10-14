def samplingRate(rate):
    if rate=="10Hz":
        maxV= 10.0
        step=0.5
        format="%fHz"
    elif rate=="100Hz":
        maxV= 100.0
        step=1.0
        format="%dHz"
    elif rate=="1KHz":
        maxV=1.0
        step=0.1
        format="%fKHz"
    elif rate=="10KHz":
        maxV= 10.0
        step=0.5
        format="%fKHz"
    elif rate== "100KHz":
        maxV= 100.0
        step=1.0
        format="%dKHz"
    elif rate=="F(max)Hz":
        maxV= 100.0
        step=1.0
        format="%dKHz"
    return maxV, step, format