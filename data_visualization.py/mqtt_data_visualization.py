import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
import threading
from datetime import datetime
import json

# Data storage
data = []

# Callback function when message is received
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    try:
        sensor_data = json.loads(payload)
        data.append((datetime.now(), sensor_data["temperature"], sensor_data["humidity"]))

        # Keep only the last 100 records
        if len(data) > 100:
            data.pop(0)

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=["timestamp", "temperature", "humidity"])

        # Update the plot
        ax.clear()
        ax.plot(df["timestamp"], df["temperature"], label="Temperature", color="r")
        ax.plot(df["timestamp"], df["humidity"], label="Humidity", color="b")
        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.set_title("MQTT Sensor Data Visualization")
        ax.legend()
        plt.draw()
        
    except json.JSONDecodeError:
        print("Error decoding JSON")

# MQTT Client Setup (ensuring no deprecation warning)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

# Connect to MQTT broker
client.connect("localhost", 1883)
client.subscribe("sensor/data")

# Start MQTT loop in a separate thread
def mqtt_loop():
    client.loop_forever()

mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
mqtt_thread.start()

# Setup Matplotlib figure
fig, ax = plt.subplots()
plt.ion()
plt.show()

# Keep the plot responsive
try:
    while True:
        plt.pause(1)  # Allow updates every second
except KeyboardInterrupt:
    print("Stopping visualization...")
    client.loop_stop()
    plt.close()
