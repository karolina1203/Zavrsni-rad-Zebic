PLOT_drugi

import matplotlib
matplotlib.use('TkAgg')
from rosbags.highlevel import AnyReader
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

bag_path = Path('/home/karolina-z/ros2_ws/src/rosbag2_2025_07_08-16_23_57')

try:
    with AnyReader([bag_path]) as reader:
        times = []
        pressures = []

        for conn, timestamp, rawdata in reader.messages():
            if conn.topic == '/bmp280/pressure':
                try:
                    msg = reader.deserialize(rawdata, conn.msgtype)
                    times.append(timestamp / 1e9)
                    pressures.append(msg.data)
                except Exception as e:
                    print(f"Error deserializing message: {e}")
                    continue

    if times:
        times = [t - times[0] for t in times]  # Normalize time
        
        plt.figure(figsize=(10, 6))
        plt.plot(times, pressures, 'b-')
        plt.xlabel('Vrijeme (s)')
        plt.ylabel('Tlak (hPa)')
        plt.title('Promjena tlaka kroz vrijeme')
        plt.grid(True)
        
        # Set y-axis to start at 900 while keeping x-axis at 0
        plt.ylim(bottom=970)  # Y-axis starts at 900
        plt.xlim(left=0)      # X-axis starts at 0 (y-axis crosses here)
        
        plt.show(block=True)
        plt.savefig('pressure_plot.png')
        print("Plot saved to pressure_plot.png")
        
    else:
        print("No pressure data found")

except Exception as e:
    print(f"Error: {e}")
