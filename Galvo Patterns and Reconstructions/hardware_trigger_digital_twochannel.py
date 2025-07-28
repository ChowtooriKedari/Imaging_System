import numpy as np
from math import *
import nidaqmx
from nidaqmx import *
from nidaqmx.constants import *
import matplotlib.pyplot as plt
import time
# import cv2q
import keyboard

X_PIN = "Dev1/AO0"
Y_PIN = "Dev1/AO1"

xmin = 0.0 
xmax = 2 * np.pi

ymin = xmin + 0.5 * np.pi 
ymax = xmax + 0.5 * np.pi 

hz = 0.2
scans = 1000
amplitude = 0.5

y = np.linspace(ymin, ymax, num=scans, endpoint=False)
x = np.linspace(xmin, xmax, num=scans, endpoint=False)
wave=np.vstack((amplitude * np.sin(3*x), amplitude * np.sin(7*y)))
print(wave.shape)

# plt.figure(figsize=(10, 5))

# # plt.subplot(1, 3, 1)
# # plt.plot(wave[0], label='wave_y (cos(y))')
# # plt.title('Wave Y')
# # plt.xlabel('Sample')
# # plt.ylabel('Amplitude')
# # plt.legend()

# # plt.subplot(1, 3, 2)
# # plt.plot(wave[1], label='wave_x (sin(x))')
# # plt.title('Wave X')
# # plt.xlabel('Sample')
# # plt.ylabel('Amplitude')
# # plt.legend()

# plt.plot(wave[0], wave[1])

# plt.tight_layout()
# plt.show()


with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan(Y_PIN)
    task.ao_channels.add_ao_voltage_chan(X_PIN)
    task.timing.cfg_samp_clk_timing(hz * scans, sample_mode=AcquisitionType.CONTINUOUS)
    task.write(wave, auto_start=True)
    print("Press 'q' to stop the task.")
    while True:
        if keyboard.is_pressed('q'):
            print("Stopping the task...")
            task.stop()
            break