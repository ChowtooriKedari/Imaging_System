import pandas as pd
from scipy.signal import correlate
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def find_best_match(reference, target):
    correlation = correlate(target, reference, mode='valid')
    best_match_index = correlation.argmax()
    best_match_segment = target[best_match_index:best_match_index + len(reference)]
    return {
        "index": best_match_index,
        "segment": best_match_segment
    }

reference_pattern = pd.read_csv('circular/referencePattern.csv')
reference_voltages = reference_pattern['Voltage (V)']
files = [f'circular/pixel_static_PD_{i}.csv' for i in range(1, 101)]
best_matches = {}
for i, file_path in enumerate(files, start=1):
    target_data = pd.read_csv(file_path)
    target_voltages = target_data['Voltage (V)']
    best_matches[f'reference_{i}'] = find_best_match(reference_voltages, target_voltages)

output_paths = {}

for i, (key, match) in enumerate(best_matches.items(), start=1):
    target_data = pd.read_csv(files[i - 1])
    best_match_index = match["index"]
    best_match_segment = target_data.iloc[best_match_index:best_match_index + len(reference_voltages)]
    output_path = f'circular/{key}_best_match.csv'
    print(output_path+" "+str(len(best_match_segment)))
    best_match_segment.to_csv(output_path, index=False)
    output_paths[key] = output_path

print("Best matching segments saved to the following files:")
for key, path in output_paths.items():
    print(f"{key}: {path}")

# Visualize the best matches for all files in a 3x100 grid
# output_pdf_path = "1K_500mV_500us/Best_Matching_Segments_3x100.pdf"
# n_rows, n_cols = 10, 1000  # Adjusted for 1000 files

# with PdfPages(output_pdf_path) as pdf:
#     # Create a large figure for the 3x100 grid
#     fig, axes = plt.subplots(n_rows, n_cols, figsize=(200, 15), constrained_layout=True)
#     fig.suptitle('Best Matching Segments Across All Files', fontsize=24)

#     for i, (key, match) in enumerate(best_matches.items()):
#         row = i // n_cols  # Determine row index
#         col = i % n_cols  # Determine column index
#         ax = axes[row, col]  # Access the specific subplot

#         best_match_segment = match["segment"]
#         best_match_index = match["index"]

#         # Plot the reference pattern
#         ax.plot(reference_voltages.values, label='Reference Pattern', color='blue', linewidth=1)
#         # Plot the best matching segment from the target
#         ax.plot(range(best_match_index, best_match_index + len(reference_voltages)),
#                 best_match_segment.values, label='Best Match', color='orange', linewidth=1)

#         ax.set_title(key, fontsize=6)
#         ax.set_xticks([])  # Remove x-ticks for compactness
#         ax.set_yticks([])  # Remove y-ticks for compactness
#         ax.grid(True)

#     # Save the figure to the PDF
#     pdf.savefig(fig)
#     plt.close(fig)

# print(f"Saved the 3x100 grid plot to {output_pdf_path}")
