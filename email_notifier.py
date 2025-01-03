from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os
import zmq
import smtplib

with open('/home/iot/Documents/email_cred.txt', 'r') as file:
    EMAIL = file.readline().strip()
    PASSWORD = file.readline().strip()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
last_event_times = {}  # Dictionary to store last event time per sensor

print(f"Process ID: {os.getpid()}")

def send_email_notification(sensor_id, distance):
    global last_event_times
    
    current_time = datetime.now()
    if (sensor_id in last_event_times and 
        (current_time - last_event_times[sensor_id]) < timedelta(seconds = 5)):
        print(f"Duplicate event detected for sensor {sensor_id} within 5 seconds, skipping email.")
        return

    last_event_times[sensor_id] = current_time

    msg = MIMEText(f"Motion detected on sensor {sensor_id} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}. Distance: {distance:.1f} cm")
    msg['Subject'] = "Motion Alert"
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)

    print(f"Email sent: Motion detected on sensor {sensor_id} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}. Distance: {distance:.1f} cm")

def notify_via_email():
    # ...existing code...
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.subscribe("")

    print("Email notifier running...")

    while True:
        event = socket.recv_json()
        print(f"Received event: {event}")
        
        if 'sensor_1' in event:
            send_email_notification(18, event['sensor_1'])
        if 'sensor_2' in event:
            send_email_notification(22, event['sensor_2'])

if __name__ == "__main__":
    notify_via_email()