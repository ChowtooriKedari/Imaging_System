import numpy as np
import nidaqmx
import pyvisa
import time
import csv            
import matplotlib.pyplot as plt

# NI-DAQ Channels
X_GALVO = "Dev1/ao0"  # X-Galvo Output
Y_GALVO = "Dev1/ao1"  # Y-Galvo Output

# Connect to the oscilloscope using VISA
rm = pyvisa.ResourceManager()
oscilloscope = rm.open_resource("USB0::0x5345::0x1235::2318021::0::INSTR")
oscilloscope.timeout = 12000  # 60 seconds timeout
oscilloscope.write("*IDN?")
print(f"Connected to oscilloscope: {oscilloscope.read()}")

oscilloscope.write("*RST")
waveform_header = oscilloscope.query(":WAVEFORM:PREAMBLE?")
print(f"Waveform Header: {waveform_header}")

oscilloscope.write(":HORIZONTAL:SCALE 500us")
oscilloscope.write(":HORIZONTAL:OFFSET 0")

oscilloscope.write(":CH1:SCALE 50mv")
oscilloscope.write(":CH1:OFFSET -6")
oscilloscope.write(":CH1:COUP DC")

oscilloscope.write(":CH3:SCALE 10mv")
oscilloscope.write(":CH3:OFFSET -5")
oscilloscope.write(":CH3:COUP DC")

# oscilloscope.write(":TRIGGER:SINGLE:MODE EDGE")
# oscilloscope.write(":TRIGGER:SINGLE:EDGE:SOURCE CH1")
# oscilloscope.write(":TRIGGER:SINGLE:EDGE:COUPLING DC")
# oscilloscope.write(":TRIGGER:SINGLE:EDGE:SLOPE RISE")
# oscilloscope.write(":TRIGGER:SINGLE:EDGE:LEVEL 1")
# oscilloscope.write(":TRIGGER:SINGLE:SWEep NORM")

oscilloscope.write(":TRIGGER:SINGLE:MODE EDGE")
oscilloscope.write(":TRIGGER:SINGLE:EDGE:SOURCE CH1")
oscilloscope.write(":TRIGGER:SINGLE:EDGE:COUPLING DC")
oscilloscope.write(":TRIGGER:SINGLE:EDGE:SLOPE RISE")
oscilloscope.write(":TRIGger:SINGle:EDGE:LEVEL 0.7")
oscilloscope.write(":TRIGGER:SINGLE:SWEep NORM")
# oscilloscope.write(":TRIG:SING:HOLD 5")
oscilloscope.write(":CH3:DISP ON")
oscilloscope.write(":CH1:DISP ON")

print("CH3 offset:", oscilloscope.query(":CH3:OFFSET?"))
print("CH1 offset:", oscilloscope.query(":CH1:OFFSET?"))

# Set acquisition parameters
oscilloscope.write(":ACQ:MODE SAMPLE")
oscilloscope.write(":ACQ:DEPMEM 100K")

# Oscilloscope settings
VOLTAGE_SCALE_STATIC = 0.05
VOLTAGE_SCALE_MOVING = 0.01

# Convert offsets from divisions to volts
VERTICAL_OFFSET_STATIC = -6
VERTICAL_OFFSET_MOVING = -5

SAMPLE_RATE = 10E6
TIME_PER_SAMPLE = 1 / SAMPLE_RATE

# Scan Parameters
grid_size=10  # 50x100 grid
X_MIN, X_MAX = -1.0, 0.8
Y_MIN, Y_MAX = -1.5, 0.8
X_STEPS = np.linspace(X_MIN, X_MAX, grid_size)
Y_STEPS = np.linspace(Y_MIN, Y_MAX, grid_size)
DWELL_TIME = 0.01  # 1 ms dwell time per point

# Initialize NI-DAQ for Galvo control
daq_session = nidaqmx.Task()
daq_session.ao_channels.add_ao_voltage_chan(X_GALVO)
daq_session.ao_channels.add_ao_voltage_chan(Y_GALVO)


oscilloscope.write(":WAVEFORM:BEGIN CH3")
oscilloscope.write(":WAVEFORM:RANGE 0,40000")
rawData_CH3 = oscilloscope.query_binary_values(":WAVEFORM:FETCH?", datatype='h')

oscilloscope.write(":WAVEFORM:BEGIN CH1")
oscilloscope.write(":WAVEFORM:RANGE 0,40000")
rawData_CH1 = oscilloscope.query_binary_values(":WAVEFORM:FETCH?", datatype='h')
oscilloscope.write(":WAVEFORM:END")

print(f"Pixel {0} Length of rawData_CH3: {len(rawData_CH3)} rawData_CH1: {len(rawData_CH1)}")
csv_file_static = f"pixel_static_PD_{0}.csv"
csv_file_moving = f"pixel_moving_PD_{0}.csv"

voltage_data_CH3=[]
for i in range(40000):
    d = rawData_CH3[i]
    voltage_data_CH3.append((float(d) / 6400-VERTICAL_OFFSET_MOVING) * VOLTAGE_SCALE_MOVING)

voltage_data_CH1 = []
timeData = []
for i in range(40000):
    d = rawData_CH1[i]
    timeData.append(float(i)/SAMPLE_RATE)
    voltage_data_CH1.append((float(d) / 6400 - VERTICAL_OFFSET_STATIC) * VOLTAGE_SCALE_STATIC)

print("Starting Galvo-based scanning with oscilloscope polling for synchronization...")
print("Current trigger settings:")
print("Trigger mode:", oscilloscope.query(":TRIGGER:SINGLE:MODE?"))
print("Trigger source:", oscilloscope.query(":TRIGGER:SINGLE:EDGE:SOURCE?"))
print("Trigger status:", oscilloscope.query(":TRIGGER:STATUS?"))
print("Current trigger level:", oscilloscope.query(":TRIGGER:SINGLE:EDGE:LEVEL?"))
print("Current CH1 scale:", oscilloscope.query(":CH1:SCALE?"))

# Query and print oscilloscope settings
print("Horizontal scale:", oscilloscope.query(":HORIZONTAL:SCALE?"))
print("Horizontal offset:", oscilloscope.query(":HORIZONTAL:OFFSET?"))

print("CH3 scale:", oscilloscope.query(":CH3:SCALE?"))
print("CH3 offset:", oscilloscope.query(":CH3:OFFSET?"))
print("CH3 coupling:", oscilloscope.query(":CH3:COUPLING?"))
print("CH3 display:", oscilloscope.query(":CH3:DISP?"))

print("CH2 scale:", oscilloscope.query(":CH1:SCALE?"))
print("CH2 coupling:", oscilloscope.query(":CH1:COUPLING?"))
print("CH2 display:", oscilloscope.query(":CH1:DISP?"))

print("Trigger source:", oscilloscope.query(":TRIGGER:SINGLE:EDGE:SOURCE?"))
print("Trigger mode:", oscilloscope.query(":TRIGGER:SINGLE:MODE?"))
print("Trigger coupling:", oscilloscope.query(":TRIGGER:SINGLE:EDGE:COUPLING?"))
print("Trigger slope:", oscilloscope.query(":TRIGGER:SINGLE:EDGE:SLOPE?"))
print("Trigger level:", oscilloscope.query(":TRIGGER:SINGLE:EDGE:LEVEL?"))
print("Trigger sweep:", oscilloscope.query(":TRIGGER:SINGLE:SWEep?"))

print("Acquisition mode:", oscilloscope.query(":ACQ:MODE?"))
print("Acquisition depth memory:", oscilloscope.query(":ACQ:DEPMEM?"))
print("Acquisition precision:", oscilloscope.query(":ACQ:PRECISION?"))

print("CH3 bandwidth limit:", oscilloscope.query(":CH3:BAND?"))
print("CH2 bandwidth limit:", oscilloscope.query(":CH1:BAND?"))
# Raster Scan with Software Synchronization
missing_pixels=[]
count = 1
for y in Y_STEPS:
    for x in X_STEPS:
        # Move Galvos to the scan position
        daq_session.write([x, y])
        time.sleep(DWELL_TIME)  # Allow Galvos to stabilize
        
        # oscilloscope.write(":TRIGGER:FORCE")
        # Reset trigger system

        # oscilloscope.write(":TRIGGER:SINGLE:STATE READY")  # Ensure trigger is armed
        oscilloscope.write(":TRIGGER:SINGLE:SWEep NORM")  # Ensure Normal Sweep mode
        oscilloscope.write(":TRIGger:SINGle:EDGE:LEVEL 0.7")
        oscilloscope.write(":TRIGGER:FORCE")

        print("Trigger status : "+ oscilloscope.query(":TRIGGER:SINGLE:EDGE:SOURCE?") +""+ oscilloscope.query(":TRIGGER:STATUS?"))

        # Force trigger (only works in Normal mode)

        oscilloscope.write(":WAVEFORM:BEGIN CH3")
        time.sleep(0.05)
        oscilloscope.write(":WAVEFORM:RANGE 0,40000")
        rawData_CH3 = oscilloscope.query_binary_values(":WAVEFORM:FETCH?", datatype='h')

        oscilloscope.write(":WAVEFORM:BEGIN CH1")
        time.sleep(0.05)
        oscilloscope.write(":WAVEFORM:RANGE 0,40000")
        rawData_CH1 = oscilloscope.query_binary_values(":WAVEFORM:FETCH?", datatype='h')
        oscilloscope.write(":WAVEFORM:END")

        print(f"Pixel {count} Length of rawData_CH3: {len(rawData_CH3)} rawData_CH1: {len(rawData_CH1)}")
        csv_file_static = f"pixel_static_PD_{count}.csv"
        csv_file_moving = f"pixel_moving_PD_{count}.csv"

        # if len(rawData_CH3) < 40000 or len(rawData_CH1) < 40000:
        #     count += 1
        #     missing_pixels.append(count)
        #     print(f"Incomplete data for pixel {count}. Skipping...")
        #     zero_timeData = np.linspace(0, (40000-1)/SAMPLE_RATE, 40000)  # Simulating timestamps
        #     zero_voltage = np.zeros(40000)  # All zero voltages

        #     # Combine into arrays
        #     data_static = np.column_stack((zero_timeData, zero_voltage))
        #     data_moving = np.column_stack((zero_timeData, zero_voltage))

        #     # Save zero-filled data
        #     np.savetxt(csv_file_static, data_static, delimiter=",", header="Time (s),Voltage (V)", comments="")
        #     np.savetxt(csv_file_moving, data_moving, delimiter=",", header="Time (s),Voltage (V)", comments="")
        #     continue

        voltage_data_CH3=[]
        for i in range(40000):
            d = rawData_CH3[i]
            voltage_data_CH3.append((float(d) / 6400-VERTICAL_OFFSET_MOVING) * VOLTAGE_SCALE_MOVING)

        voltage_data_CH1 = []
        timeData = []
        for i in range(40000):
            d = rawData_CH1[i]
            timeData.append(float(i)/SAMPLE_RATE)
            voltage_data_CH1.append((float(d) / 6400 - VERTICAL_OFFSET_STATIC) * VOLTAGE_SCALE_STATIC)

        plt.figure(figsize=(10, 5))
        plt.plot(timeData, voltage_data_CH1)
        plt.plot(timeData, voltage_data_CH3)
        # plt.xlabel('Time (s)')
        # plt.ylabel('Voltage (V)')
        # plt.title(f'Pixel {count} - Static and Moving PD')
        # plt.legend()
        plt.grid(True)
        plt.savefig(f"pixel_{count}_plot.png")
        plt.close()

    # # Convert data to NumPy arrays for faster writing
    #     data_static = np.column_stack((timeData, voltage_data_CH1))
    #     data_moving = np.column_stack((timeData, voltage_data_CH3))

    #     # # Write to CSV using NumPy (MUCH faster)
    #     np.savetxt(csv_file_static, data_static, delimiter=",", header="Time (s),Voltage (V)", comments="")
    #     np.savetxt(csv_file_moving, data_moving, delimiter=",", header="Time (s),Voltage (V)", comments="")

        # Update counter
        print(f"Saved pixel {count}: X={x:.3f} Y={y:.3f}")
        count += 1
        rawData_CH3 = []
        rawData_CH1 = []

        print(f"Missing pixels count: {len(missing_pixels)}")
        oscilloscope.write(":TRIGger:SINGle:EDGE:LEVEL -1")
        oscilloscope.write(":TRIGGER:FORCE")
        print("Trigger Level : " + oscilloscope.query(":TRIGger:SINGle:EDGE:LEVEL?"))
        print("Rearm Trigger status : "+ oscilloscope.query(":TRIGGER:SINGLE:EDGE:SOURCE?") +""+ oscilloscope.query(":TRIGGER:STATUS?"))


    #  # Set trigger to waiting state
       
    #     oscilloscope.write(":TRIGger:SINGle:STATE READY") 
    #     oscilloscope.write(":TRIGGER:SINGLE:SWEep AUTO")
    #     # oscilloscope.write(":TRIGGER:SINGLE:SWEep AUTO")
    # time.sleep(0.5)


print("Scan complete! Data saved.")
# Save missing pixel numbers to a CSV file
missing_pixels_file = "missing_pixels.csv"
np.savetxt(missing_pixels_file, np.array(missing_pixels, dtype=int), delimiter=",", fmt="%d", header="Missing Pixel Number", comments="")
print(f"Number of missing pixels: {len(missing_pixels)}")
print(f"Missing pixel numbers saved to {missing_pixels_file}")

# Cleanup
oscilloscope.close()
daq_session.close()
