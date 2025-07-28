#import matplotlib.pyplot as plt
from re import X
import numpy as np
from math import *
import nidaqmx
from nidaqmx import *
from nidaqmx.constants import *
import time

X_PIN = "Dev1/AO0"
Y_PIN = "Dev1/AO1"


X_MIN, X_MAX = 0.4, 0.8
Y_MIN, Y_MAX = -0.2, 0.8
pos = [-1,1]
# pos = [-2.5, -0.5]
# pos = [0.273, 0.1]
# pos = [4.54, 3.0]
# pos = [4.8, 1.68]


with nidaqmx.Task() as task:
    chan = task.ao_channels.add_ao_voltage_chan("Dev1/AO0")
    print(f"Min Voltage: {chan.ao_min}, Max Voltage: {chan.ao_max}")
    
XYScan = nidaqmx.Task('XYScan')
# XYScan.timing.cfg_samp_clk_timing(20000,active_edge=Edge.RISING, sample_mode=AcquisitionType.CONTINUOUS)

XYScan.ao_channels.add_ao_voltage_chan(Y_PIN)
XYScan.ao_channels.add_ao_voltage_chan(X_PIN)

XYScan.output_buf_size = 5
XYScan.output_onbrd_buf_size = 5

XYScan.write(pos, auto_start=True)
XYScan.wait_until_done()
XYScan.stop()
XYScan.close()

