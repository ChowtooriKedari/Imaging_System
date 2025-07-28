import os
import subprocess
import cv2

data_dir = 'data_for_prediction'
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to run inpainting (reconstruction) on a given image and mask file.
def run_inpainting(image_file, mask_file):
    model_path = os.path.join(os.getcwd(), 'big-lama')
    # Update these parameters as required by your Big-LAMA inpainting script.
    command = [
        'python3', 'bin/predict.py',
    ]
    subprocess.run(command)

# Process each image in the data_for_prediction folder (ignoring mask files).
all_files = os.listdir(data_dir)
input_images = [f for f in all_files if f.endswith('.png') and not f.endswith('_mask.png')]

for image_file in input_images:
    base_name = os.path.splitext(image_file)[0]
    mask_file = f"{base_name}_mask.png"
    if mask_file in all_files:
        print(f"Processing {image_file} with mask {mask_file}...")
        run_inpainting(image_file, mask_file)
    else:
        print(f"Mask file {mask_file} not found for image {image_file}.")

print("Reconstruction completed.")
