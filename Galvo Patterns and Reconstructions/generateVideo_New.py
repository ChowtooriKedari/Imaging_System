import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import PIL
# Function to map voltage to intensity (0-255 range)
def map_voltage_to_intensity(voltage, min_voltage, max_voltage):
    return np.clip(((voltage - min_voltage) / (max_voltage - min_voltage)) * 255, 0, 255)

file_paths = [f'Repeats/matched_waveform_{i}.csv' for i in range(1,2501)]

# Specify the number of rows to use
num_rows_to_use = 20000
data_frames = [pd.read_csv(file).iloc[:num_rows_to_use] for file in file_paths]

num_rows = num_rows_to_use
all_voltages = np.concatenate([df['Voltage (V)'].values for df in data_frames])
min_voltage = all_voltages.min()
max_voltage = all_voltages.max()

grid_size = (50,50)

# Function to update the frame for animation
def update_frame(frame):
    # Extract voltage values from each photodetector at current time
    voltages = np.array([df['Voltage (V)'].iloc[frame] for df in data_frames])
    # Map voltages to intensities
    intensities = map_voltage_to_intensity(voltages, min_voltage, max_voltage)
    # Reshape intensities to 3x100 grid
    intensity_grid = intensities.reshape(grid_size)
    # Update the image
    im.set_array(intensity_grid)
    return [im]

# Initialize the plot with larger Y-axis
fig, ax = plt.subplots(figsize=(10, 10))  # Increased Y-axis size
im = ax.imshow(np.zeros(grid_size), cmap='gray', vmin=0, vmax=255)

# Adjust spacing between columns and rows
ax.set_xticks([])
ax.set_yticks([])

# Add color bar and labels
# plt.colorbar(im, label="Intensity", orientation='vertical')
plt.title("Pixel Intensity Visualization from Grid Over Time", color='white')
plt.xlabel("Grid Columns", color='white')
plt.ylabel("Grid Rows", color='white')

# Adjust plot aesthetics for black background
ax.set_facecolor("black")
ax.spines[:].set_color("white")
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.tick_params(axis='both', colors='white')

# Create the animation
ani = animation.FuncAnimation(fig, update_frame, frames=num_rows, interval=200, blit=True)

# Save the animation as a video
video_filename = "Repeats/TEST_5000FPS.mp4"
ani.save(video_filename, writer='ffmpeg', fps=5000)  # Save as .mp4 video with 24 fps

plt.show()

# Return the video filename for downloading
video_filename
