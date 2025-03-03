import asyncio
import json
import random
import logging
from aiocoap import Context, Message, POST

# Configure logging
logging.basicConfig(level=logging.INFO)

async def simulate_sensor_data():
    # Create client context
    print("Starting sensor simulation...")
    
    # Retry mechanism
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Create a client context
            context = await Context.create_client_context()
            print("Client context created successfully")
            
            # Main loop for sending data
            while True:
                # Generate random sensor data
                temperature = round(random.uniform(20.0, 25.0), 1)
                humidity = round(random.uniform(30.0, 50.0), 1)
                
                # Create payload
                data = {"temperature": temperature, "humidity": humidity}
                payload = json.dumps(data).encode('utf-8')
                
                # Create request
                request = Message(code=POST, payload=payload)
                request.set_request_uri('coap://127.0.0.1:5683/sensor/data')
                
                # Send request
                print(f"Sending data: {data}")
                try:
                    response = await context.request(request).response
                    print(f"Response: {response.code} - {response.payload.decode('utf-8')}")
                    # Reset retry count on success
                    retry_count = 0
                except Exception as e:
                    print(f"Error sending data: {e}")
                    # Only increment retry count if we can't reach the server
                    retry_count += 1
                    if retry_count >= max_retries:
                        print(f"Maximum retries ({max_retries}) reached. Exiting.")
                        return
                
                # Wait before sending next data point
                await asyncio.sleep(2)
                
        except Exception as e:
            print(f"Error creating client context: {e}")
            retry_count += 1
            print(f"Retry {retry_count}/{max_retries}...")
            await asyncio.sleep(5)  # Wait longer between retries

if __name__ == "__main__":
    asyncio.run(simulate_sensor_data())