import csv
import random
from datetime import datetime
import time

# CSV file configuration
SENSOR_LOG_FILE = "sensor_readings.csv"
CSV_HEADERS = ["timestamp", "sensor_id", "distance"]

def initialize_csv():
    """Create CSV file with headers"""
    try:
        with open(SENSOR_LOG_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)
            print(f"Created new log file: {SENSOR_LOG_FILE}")
    except Exception as e:
        print(f"Error creating CSV file: {e}")

def log_sensor_data(sensor_id, distance):
    """Log sensor readings to CSV file only if distance <= 10cm"""
    if distance <= 10:  # Only log if distance is 10cm or less
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(SENSOR_LOG_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, sensor_id, distance])
                print(f"Logged: Sensor {sensor_id} - {distance}cm at {timestamp}")
        except Exception as e:
            print(f"Error logging data: {e}")

def generate_dummy_data():
    """Generate and log dummy sensor data"""
    initialize_csv()
    print("Starting sensor data logging (only logging distances <= 10cm)...")
    
    try:
        while True:
            # Generate dummy readings for both sensors
            for sensor_id in [1, 2]:
                distance = round(random.uniform(0, 20), 2)  # Generate distances between 0-20cm
                if distance <= 10:  # Only log if distance is 10cm or less
                    log_sensor_data(sensor_id, distance)
            time.sleep(1)  # Log every second
            
    except KeyboardInterrupt:
        print("\nData generation stopped by user")

if __name__ == "__main__":
    generate_dummy_data()