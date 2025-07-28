import numpy as np
import pandas as pd

waveform_files = [f'circular/pixel_moving_PD_{i}.csv' for i in range(1,101)]
reference_files = [f'circular/reference_{i}_best_match.csv' for i in range(1,101)]
TARGET_SIZE = 20000
file_lengths = []
output_files = []

for i, (waveform_file, reference_file) in enumerate(zip(waveform_files, reference_files)):
    # Load waveform and reference data
    waveform_data = pd.read_csv(waveform_file)
    reference_data = pd.read_csv(reference_file)

    # Get the first timestamp from the reference file
    first_time_value = reference_data['Time (s)'].iloc[0]

    # Find the closest index in the waveform data
    start_index = waveform_data['Time (s)'].sub(first_time_value).abs().idxmin()

    # Extract the next 20,000 rows (or as many as available)
    matched_data = waveform_data.iloc[start_index:start_index + TARGET_SIZE]

    # Track the number of rows extracted
    file_lengths.append(len(matched_data))

    # Ensure uniform size by padding if necessary
    if len(matched_data) < TARGET_SIZE:
        padding_rows = TARGET_SIZE - len(matched_data)
        padding_data = pd.DataFrame({
            'Time (s)': [np.nan] * padding_rows,  # Use NaN for unknown times
            'Voltage (V)': [0] * padding_rows    # Fill voltage with zeros
        })
        matched_data = pd.concat([matched_data, padding_data], ignore_index=True)

    # Save the processed data
    output_file = f"circular/matched_waveform_{i + 1}.csv"
    matched_data.to_csv(output_file, index=False)
    
    print(f"{output_file} - {len(matched_data)} rows")
    output_files.append(output_file)

# Print min/max lengths for verification
print(f"Min file length: {min(file_lengths)}")
print(f"Max file length: {max(file_lengths)}")
print("Matched waveform files have been saved.")
