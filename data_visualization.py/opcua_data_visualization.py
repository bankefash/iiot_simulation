from opcua import Client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

# OPC UA Client Setup
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()

# Data storage
data = []

try:
    plt.ion()
    plt.figure()

    while True:
        temperature_node = client.get_node("ns=2;i=2")  # Adjust Node ID accordingly
        humidity_node = client.get_node("ns=2;i=3")  # Adjust Node ID accordingly

        temperature = temperature_node.get_value()
        humidity = humidity_node.get_value()

        data.append((datetime.now(), temperature, humidity))

        # Keep only the last 100 records
        if len(data) > 100:
            data.pop(0)

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=["timestamp", "temperature", "humidity"])

        # Plot data
        plt.clf()
        plt.plot(df["timestamp"], df["temperature"], label="Temperature", color="r")
        plt.plot(df["timestamp"], df["humidity"], label="Humidity", color="b")
        plt.xlabel("Time")
        plt.ylabel("Values")
        plt.title("OPC UA Sensor Data Visualization")
        plt.legend()
        plt.draw()
        plt.pause(1)

        time.sleep(5)  # Fetch data every 5 seconds

except KeyboardInterrupt:
    print("Stopping visualization...")
    client.disconnect()
    plt.ioff()
    plt.show()
