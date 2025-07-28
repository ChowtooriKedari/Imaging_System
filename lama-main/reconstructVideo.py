import cv2
import os

# Path to your frames (assuming images are stored in a folder)
frames_folder = "Frames/"  # Replace with the path where your frames are stored

# Sort the files correctly by filename (taking into account the padded numbers)
frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.png')],
                     key=lambda x: int(x.split('_')[1].split('.')[0]))[:1000]  # Sort by the number in the filename
if not frame_files:
    print("No frame images found in", frames_folder)
    exit(1)

# Video settings
output_video = "output_video_original.avi"  # Output video file name
frame_rate = 100  # Desired frame rate of the video

# Get the width and height of the images (assuming all frames have the same dimensions)
frame_example = cv2.imread(os.path.join(frames_folder, frame_files[0]))  # Read the first frame
height, width, _ = frame_example.shape  # Get the dimensions of the frame

# Initialize the video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

# Write each frame to the video
for frame_file in frame_files:
    frame_path = os.path.join(frames_folder, frame_file)
    frame = cv2.imread(frame_path)
    video_writer.write(frame)  # Add the frame to the video

# Release the video writer and finish
video_writer.release()
print(f"Video saved as {output_video}")
