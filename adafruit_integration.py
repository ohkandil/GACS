import zmq
from Adafruit_IO import Client, RequestError
import time
import json

# Load credentials
with open("/home/iot/Documents/adafruitio_key.txt", "r") as file:
    ADAFRUIT_IO_KEY = file.readline().strip()
    ADAFRUIT_IO_USERNAME = file.readline().strip()

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

SENSOR_FEEDS = {
    "sensor_1": "iot-ultrasonic-feed-1",
    "sensor_2": "iot-ultrasonic-feed-2"
}

def initialize_feeds():
    print("Initializing Adafruit IO feeds...")
    for sensor_id, feed_name in SENSOR_FEEDS.items():
        try:
            aio.feeds(feed_name)
            print(f"Feed {feed_name} is ready.")
        except RequestError:
            try:
                aio.create_feed(feed_name)
                print(f"Created new feed: {feed_name}")
            except RequestError as e:
                print(f"Error creating feed {feed_name}: {e}")

def send_to_adafruit(sensor_id, value):
    feed_name = SENSOR_FEEDS.get(sensor_id)
    if feed_name:
        try:
            aio.send_data(feed_name, value)
            print(f"Sent value {value} to feed {feed_name}")
        except RequestError as e:
            print(f"Error sending to Adafruit IO: {e}")

def main():
    # Set up ZMQ subscriber
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    
    initialize_feeds()
    print("Adafruit IO integration ready")
    
    while True:
        try:
            # Receive JSON data from ZMQ
            message = socket.recv_string()
            data = json.loads(message)
            
            # Send each sensor reading to its feed
            for sensor_id, value in data.items():
                send_to_adafruit(sensor_id, value)
            
            time.sleep(1)  # Rate limiting for Adafruit IO
            
        except Exception as e:
            print(f"Error in Adafruit IO integration: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()