import nidaqmx
import time

# NI-DAQ Channels for Galvos
X_GALVO = "Dev1/ao0"  # X-Galvo Output
Y_GALVO = "Dev1/ao1"  # Y-Galvo Output

# Example X and Y values to move to
# x_value = -0.5  # Set your desired X value
# y_value = -1  # Set your desired Y value

x_value = 0.0  # Set your desired X value
y_value = 0.8  # Set your desired Y value

# Initialize DAQ session
daq_session = nidaqmx.Task()
daq_session.ao_channels.add_ao_voltage_chan(X_GALVO)
daq_session.ao_channels.add_ao_voltage_chan(Y_GALVO)

print(f"Moving Galvos to: X={x_value:.3f}, Y={y_value:.3f}")

# Move Galvos to the specified (x, y) point
daq_session.write([x_value, y_value])
time.sleep(0.01)  # Optional: Add a small delay if needed

print("Galvo movement complete!")
daq_session.stop()
daq_session.close()
