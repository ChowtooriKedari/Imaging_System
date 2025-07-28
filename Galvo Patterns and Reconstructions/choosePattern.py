import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'circular/reference_new.csv'
data = pd.read_csv(file_path)

start_row = 7800
num_rows = 20000
# Slice the data based on user input
subset_data = data.iloc[start_row:start_row + num_rows]

# Save the selected data to a new CSV file
output_file_path = 'circular/referencePattern.csv'
subset_data.to_csv(output_file_path, index=False)
print(f"Subset data saved to {output_file_path}")

# Extract the data for plotting
time = subset_data['Time (s)']
voltage = subset_data['Voltage (V)']

# Plot the graph
plt.figure(figsize=(10, 6))
plt.plot(time, voltage, label='Voltage vs Time')
plt.title(f'Voltage vs Time (Rows {start_row} to {start_row + num_rows - 1})')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True)
plt.show()