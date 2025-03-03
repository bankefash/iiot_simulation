import asyncio
import logging
from aiocoap import resource, Context, Message, Code

# Configure logging
logging.basicConfig(level=logging.INFO)

class SensorResource(resource.Resource):
    """Resource that handles sensor data."""
    
    def __init__(self):
        super().__init__()
        self.latest_data = None  # Store the last received sensor data

    async def render_post(self, request):
        """Handles POST requests from sensors sending data."""
        self.latest_data = request.payload.decode('utf-8')
        print(f"Received sensor data: {self.latest_data}")
        return Message(code=Code.CREATED, payload=b"Data received successfully")

    async def render_get(self, request):
        """Handles GET requests from visualization script to fetch latest data."""
        if self.latest_data:
            return Message(code=Code.CONTENT, payload=self.latest_data.encode('utf-8'))
        else:
            return Message(code=Code.NO_CONTENT, payload=b"No data available")

# Create a resource tree
def create_resource_tree():
    root = resource.Site()
    root.add_resource(['sensor', 'data'], SensorResource())  # Maps /sensor/data
    return root

async def main():
    """Starts the CoAP server."""
    root = create_resource_tree()
    
    print("Starting CoAP server on 127.0.0.1:5683...")
    
    # Create server context with the resource tree
    context = await Context.create_server_context(root, bind=('127.0.0.1', 5683))
    
    print("Server successfully started on 127.0.0.1:5683")
    print("CoAP server is now running and waiting for requests...")

    # Keep the server running until Ctrl+C is pressed
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Server shutdown requested")
    finally:
        await context.shutdown()
        print("Server shut down")

if __name__ == "__main__":
    asyncio.run(main())
