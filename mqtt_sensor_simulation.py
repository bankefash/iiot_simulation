import paho.mqtt.client as mqtt
import random
import time

# MQTT Broker Configuration
broker = "localhost"
port = 1883
topic = "sensor/data"

# Initialize MQTT Client
client = mqtt.Client()
client.connect(broker, port)

def simulate_sensor_data():
    try:
        while True:
            temperature = random.uniform(20.0, 25.0)
            humidity = random.uniform(30.0, 50.0)
            payload = f'{{"temperature": {temperature:.2f}, "humidity": {humidity:.2f}}}'
            client.publish(topic, payload)
            print(f"Published: {payload}")  # Optional for debugging
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    simulate_sensor_data()
