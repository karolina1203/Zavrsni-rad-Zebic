from rosbags.highlevel import AnyReader
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

bag_path = Path('/home/karolina-z/ros2_ws/src/rosbag2_2025_06_04-13_51_06')

try:
    with AnyReader([bag_path]) as reader:
        # Print connection info for debugging
        print("Available topics and types:")
        for conn in reader.connections:
            print(f"- {conn.topic}: {conn.msgtype}")
        
        times = []
        pressures = []

        for conn, timestamp, rawdata in reader.messages():
            if conn.topic == '/bmp280/pressure':
                try:
                    msg = reader.deserialize(rawdata, conn.msgtype)
                    time_sec = timestamp / 1e9
                    times.append(time_sec)
                    # Adjust based on actual message structure
                    # For sensor_msgs/FluidPressure it would be msg.fluid_pressure
                    # For custom messages, check your message definition
                    pressures.append(msg.data)  # This might need adjustment
                except Exception as e:
                    print(f"Error deserializing message: {e}")
                    continue

    if times:
        start_time = times[0]
        times = [t - start_time for t in times]

        df = pd.DataFrame({'Vrijeme (s)': times, 'Tlak (hPa)': pressures})

        plt.figure(figsize=(10, 5))
        plt.plot(df['Vrijeme (s)'], df['Tlak (hPa)'], marker='o', color='tab:blue')
        plt.xlabel('Vrijeme (s)')
        plt.ylabel('Tlak (hPa)')
        plt.title('Promjena tlaka kroz vrijeme')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('graf_tlaka.png')
        plt.show()
    else:
        print("Nema poruka na topicu '/bmp280/pressure' u datoteci.")

except Exception as e:
    print(f"Error processing bag file: {e}")
