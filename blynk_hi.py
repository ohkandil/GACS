import time
import requests
import RPi.GPIO as GPIO
from gpio_config import gpio_manager  # Import our GPIO manager

# Use BCM mode as defined in gpio_config
GPIO.setmode(GPIO.BCM)

# Use pins from gpio_config
TRIG = gpio_manager.GPIO_TRIGGER_1  # 18
ECHO = gpio_manager.GPIO_ECHO_1     # 24
LED = gpio_manager.GPIO_LED_1       # 23

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(TRIG, False)

with open("/home/iot/Documents/blynk_key.txt", "r") as file:
    token = file.readline().strip()

def writeVirtualPin(token,pin,value):
    api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
    response = requests.get(api_url)
    if "200" in str(response):
        print("Value successfully updated")
    else:
        print("Could not find the device token or wrong pin format")
   

print("Starting.....")
time.sleep(2)

try:
   while True:
      GPIO.output(TRIG, True)
      time.sleep(0.00001)
      GPIO.output(TRIG, False)
      
      while GPIO.input(ECHO)==0:
         pulse_start = time.time()

      while GPIO.input(ECHO)==1:
         pulse_stop = time.time()

      pulse_time = pulse_stop - pulse_start

      distance = pulse_time * 17150
      rounded_distance = round(distance, 2)
      print(rounded_distance)
      writeVirtualPin(token,"V1", str(rounded_distance))

      time.sleep(1)
      
finally:
   GPIO.cleanup() # this ensures a clean exit