"""
Author: author
Date: [Date]
Description:
    EEG-VB data parsing, optional resampling/harmonization, and waveform visualization.

Notes:
    - This script is used for blink-interaction EEG data in the EEG-VB dataset.
    - The dataset release is standardized to 512 Hz. If legacy files are at 256 Hz,
      set FS_ORIGINAL accordingly before calling save_data_to_file.
"""

import os
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Sampling-rate configuration used for optional harmonization.
FS_ORIGINAL = 512  # Source sampling rate of the current input file.
FS_TARGET = 512  # Target sampling rate used by the released EEG-VB data.


def save_data_to_file(data, filename):
    """
    Save a 1D EEG sequence after optional resampling.

    Parameters:
    data (array): Raw EEG samples (single-channel sequence)
    filename (str): Output path for serialized values
    """
    try:
        data = np.array(data)
        # Compute target length from source/target sampling rates.
        num_original = data.shape[0]
        num_target = int(num_original * FS_TARGET / FS_ORIGINAL)

        # Apply Fourier-method resampling for sampling-rate harmonization.
        data = signal.resample(data, num_target, axis=0)

        with open(filename, "w") as file:
            file.write(" ".join(map(str, data)))
        print(f"\nData successfully saved to {filename}!")
    except IOError:
        print("Error: Unable to open file for writing!")


def save_data_to_file2(data_big, filename):
    """
    Save packet-level parsed values to a text file (row-wise).

    Parameters:
    data_big (2D array): Parsed packet matrix
    filename (str): Output path
    """
    try:
        with open(filename, "w") as file:
            for row in data_big:
                file.write(" ".join(map(str, row)) + "\n")
        print(f"\nData successfully saved to {filename}!")
    except IOError:
        print("Error: Unable to open file for writing!")


def main(file_name):
    """
    Parse a raw hexadecimal EEG stream file and export parsed outputs.

    The parser supports both:
    - 36-byte packet structure (stored in data_big)
    - 8-byte single-channel packet structure (stored in data)

    Parameters:
    file_name (str): Path to raw input file
    """
    flag = 1
    try:
        with open(file_name, "r") as file:
            line = file.readline().strip()

            if not line:
                print("File is empty!")
                return None

            data = []  # Single-channel EEG sequence used for downstream analysis.
            data_big = []  # Packet-level parsed matrix for protocol inspection.
            hex_vec = []

            # Tokenize the hexadecimal stream and parse packet-by-packet.
            for hex_str in line.split():
                hex_vec.append(hex_str)

                # Early malformed header handling for stream alignment.
                if flag == 1 and len(hex_vec) == 4 and hex_vec[0] != "AA":
                    print(hex_vec)
                    flag = 0
                    hex_vec.clear()

                # Parse 36-byte packet format.
                if len(hex_vec) == 36 and hex_vec[2] == "20":
                    print(hex_vec)
                    try:
                        # Convert selected hexadecimal fields and validate checksum.
                        values = [int(hex_vec[i], 16) for i in
                                  [4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                                   28, 29, 30, 32, 34, 35]]
                        checksum = (sum([0x02, 0x83, 0x18, 0x04, 0x05] + values[:-1]) & 0xFF) ^ 0xFF

                        if checksum == values[-1]:
                            row = [values[0]] + [(values[i] << 16 | values[i + 1] << 8 | values[i + 2]) for i in
                                                 range(1, len(values) - 4, 3)]
                            row.append(values[-3])
                            row.append(values[-2])
                            data_big.append(row)
                            print("Valid packet", row)
                        else:
                            print("Invalid packet")
                    except IndexError:
                        print("Error parsing multi-channel packet")

                    hex_vec.clear()

                # Parse 8-byte single-channel packet format.
                elif len(hex_vec) == 8 and hex_vec[2] == "04":
                    print(hex_vec)
                    try:
                        num1, num2, num3 = [int(hex_vec[i], 16) for i in [5, 6, 7]]
                        checksum = ((0x80 + 0x02 + num1 + num2) ^ 0xFFFFFFFF) & 0xFF

                        if checksum == num3:
                            rawdata = (num1 << 8) | num2
                            if rawdata > 32768:
                                rawdata -= 65536
                            data.append(rawdata)
                            print(f"Valid packet. Rawdata: {rawdata}")
                        else:
                            print("Invalid packet. Checksum does not match.")
                    except IndexError:
                        print("Error parsing single-channel packet")

                    hex_vec.clear()

            if hex_vec:
                print("Unprocessed data found!")

            # Print a brief summary of parsed samples.
            print(f"Data processing complete! Total {len(data)} data points")
            print("Raw single-channel data:")
            for i, rawdata in enumerate(data, start=1):
                print(rawdata, end=" ")
                if i % 20 == 0:
                    print()

            # Persist both packet-level and single-channel outputs.
            # Default output directory is the same folder as the input file.
            output_dir = os.path.dirname(file_name) or os.getcwd()
            os.makedirs(output_dir, exist_ok=True)
            data_big_path = os.path.join(output_dir, "data_big.txt")
            data_small_path = os.path.join(output_dir, "data_small.txt")
            save_data_to_file2(data_big, data_big_path)
            save_data_to_file(data, data_small_path)
            return data_small_path

    except IOError:
        print("Error: Unable to open file!")
        return None


def read_data(filename):
    """
    Read a whitespace-separated numeric EEG sequence.

    Parameters:
    filename (str): Input file path

    Returns:
    list: Floating-point EEG values
    """
    with open(filename, 'r') as file:
        data_str = file.read().split()
        integer_data = [float(num) for num in data_str]
    return integer_data


def plot_waveform_in_window(data, sample_rate=512):
    """
    Plot EEG waveform in a standalone high-resolution Tkinter window.

    Parameters:
    data (list): EEG sequence to plot
    sample_rate (int): Sampling rate in Hz
    """
    # Create host window.
    root = tk.Tk()
    root.title("High-Resolution Waveform Plot")

    # Build time axis from the provided sampling rate.
    time = [i / sample_rate for i in range(len(data))]

    # Create a high-resolution figure for detailed inspection.
    fig, ax = plt.subplots(figsize=(20, 4), dpi=150)
    ax.plot(time, data, linewidth=1.0)
    ax.set_xlabel('Time (s)', fontsize=8)
    ax.set_ylabel('Data Value', fontsize=8)
    ax.set_title('Waveform Plot at {} Hz Sampling Rate'.format(sample_rate), fontsize=12)
    ax.grid(True)

    # Embed Matplotlib figure in the Tkinter window.
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Launch UI event loop.
    root.mainloop()


if __name__ == "__main__":
    file_path = r"XXX.TXT"
    output_file = main(file_path)
    # Read and visualize the parsed single-channel output if available.
    if output_file and os.path.exists(output_file):
        data = read_data(output_file)
        plot_waveform_in_window(data, sample_rate=512)
    else:
        print("No output file available for plotting.")