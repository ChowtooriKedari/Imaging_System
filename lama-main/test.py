import os
import shutil
import numpy as np
import cv2
import matplotlib.pyplot as plt
import subprocess

# ==== Function to generate Lissajous mask ====
def generate_lissajous_mask(shape, a=15, b=14, num_points=5000, thickness=2):
    height, width = shape
    t = np.linspace(0, 2 * np.pi, num_points)
    x = (width // 2) * (1 + np.cos(a * t))
    y = (height // 2) * (1 + np.sin(b * t))
    mask = np.zeros((height, width), dtype=np.uint8)
    for i in range(num_points):
        xi, yi = int(x[i]), int(y[i])
        if 0 <= xi < width and 0 <= yi < height:
            cv2.circle(mask, (xi, yi), thickness, 255, -1)
    return mask

# ==== Set up folder paths====
frames_dir = 'Frames'
output_dir = 'data_for_prediction'
shutil.rmtree(output_dir, ignore_errors=True)
os.makedirs(output_dir, exist_ok=True)

# ==== Process each frame in the frames folder ====
frame_files = sorted([f for f in os.listdir(frames_dir) if f.startswith('frame_')])[:10000]
for frame_file in frame_files:
    frame_path = os.path.join(frames_dir, frame_file)
    print(f"Processing {frame_path}...")
    # Load image (assumes image contains three channels)
    img = np.array(plt.imread(frame_path))
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    # Generate Lissajous mask and apply it
    mask = generate_lissajous_mask((img.shape[0], img.shape[1]), a=15, b=14, num_points=5000, thickness=2)
    masked_img = np.zeros_like(img)
    masked_img[mask == 255] = img[mask == 255]
    
    # Save masked image and inverted mask for inpainting (using frame_file name)
    input_filename = os.path.join(output_dir, frame_file)
    mask_filename = os.path.join(output_dir, f"{os.path.splitext(frame_file)[0]}_mask.png")
    
    cv2.imwrite(input_filename, masked_img)
    lama_mask = cv2.bitwise_not(mask)
    cv2.imwrite(mask_filename, lama_mask)
    plt.figure(figsize=(10, 5))
    
    def run_inpainting(img_suffix):
        model_path = os.path.join(os.getcwd(), 'big-lama')
        indir = os.path.join(os.getcwd(), 'data_for_prediction')
        outdir = os.path.join(os.getcwd(), 'output')
        
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        command = [
            'python3', 'bin/predict.py'
            # add further parameters as required by your Big-LAMA inpainting script
        ]
        subprocess.run(command)
    
    # Run inpainting on the current frame with png extension.
    run_inpainting(".png")
    
    # Delete the processed frame before processing the next one.
    os.remove(input_filename)
    os.remove(mask_filename)
    print(f"Processed and deleted {frame_file}")

# ===== Optional: Running inpainting with Big-LAMA =====


print("All frames have been processed.")
