from aiocoap import Context, Message, Code
import asyncio
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json

# Data storage
data = []

async def fetch_data():
    protocol = await Context.create_client_context()
    request = Message(code=Code.GET, uri="coap://127.0.0.1:5683/sensor/data")

    try:
        response = await protocol.request(request).response
        payload = response.payload.decode("utf-8")

        sensor_data = json.loads(payload)
        timestamp = datetime.now()
        
        # Append new data
        data.append((timestamp, sensor_data["temperature"], sensor_data["humidity"]))

        # Keep only the last 100 records
        if len(data) > 100:
            data.pop(0)

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=["timestamp", "temperature", "humidity"])
        df = df.sort_values(by="timestamp")  # Ensure proper order

        # Plot data
        plt.clf()
        plt.plot(df["timestamp"], df["temperature"], label="Temperature", color="r")
        plt.plot(df["timestamp"], df["humidity"], label="Humidity", color="b")
        plt.xlabel("Time")
        plt.ylabel("Values")
        plt.title("CoAP Sensor Data Visualization")
        plt.legend()
        plt.draw()
        plt.pause(0.1)

    except Exception as e:
        print(f"CoAP Request Failed: {e}")

async def main():
    plt.ion()
    plt.figure()
    while True:
        await fetch_data()
        await asyncio.sleep(5)  # Fetch data every 5 seconds

asyncio.run(main())
