import numpy as np
import pandas as pd
from scipy.signal import correlate
import matplotlib.pyplot as plt

# ------------------------------
# Step 1: Load Data
# ------------------------------
# Replace the file names with your actual CSV file names.
data1 = pd.read_csv('reference_1.csv')  # Signal 1 (Reference)
data2 = pd.read_csv('reference_2.csv')  # Signal 2 (to be shifted)

time1 = data1['Time (s)'].values
voltage1 = data1['Voltage (V)'].values

time2 = data2['Time (s)'].values
voltage2 = data2['Voltage (V)'].values

# ------------------------------
# Step 2: Determine Sampling Interval
# ------------------------------
# We assume that both signals share the same sampling rate.
dt = time1[1] - time1[0]

# ------------------------------
# Step 3: Compute Cross-Correlation to Find the Optimal Time Shift
# ------------------------------
# Compute full cross-correlation between Signal 2 and Signal 1.
corr = correlate(voltage2, voltage1, mode='full')
# Create an array of lag indices (in sample counts).
lags = np.arange(-len(voltage1) + 1, len(voltage2))
# The lag corresponding to the maximum correlation:
lag_index = lags[np.argmax(corr)]
# Convert the lag to a time shift.
time_shift = lag_index * dt
print(f"Computed time shift: {time_shift} seconds")

# ------------------------------
# Step 4: Shift Signal 2
# ------------------------------
# Shift Signal 2 by subtracting the computed time shift from its time vector.
shifted_time2 = time2 - time_shift

# ------------------------------
# Step 5: Plot the Results
# ------------------------------
plt.figure(figsize=(10, 6))

# Plot Signal 1 (the reference) as is.
plt.plot(time1, voltage1, label="Signal 1 (Reference)")

# Plot Signal 2 after applying the time shift.
plt.plot(shifted_time2, voltage2, label=f"Signal 2 (Shifted by {time_shift:.3f} s)", linestyle='--', color='red')

plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Signal 1 and Shifted Signal 2")
plt.legend()
plt.tight_layout()
plt.show()
