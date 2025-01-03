import time
import zmq
import BlynkLib
import logging
import RPi.GPIO as GPIO
from gpio_config import gpio_manager

# Disable GPIO warnings
GPIO.setwarnings(False)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Read Blynk auth token
with open("/home/iot/Documents/blynk_key.txt", "r") as file:
    BLYNK_AUTH = file.readline().strip()

# Initialize Blynk
BLYNK_SERVER = "blynk.cloud"
BLYNK_PORT = 80
blynk = BlynkLib.Blynk(BLYNK_AUTH, server=BLYNK_SERVER, port=BLYNK_PORT, heartbeat=30)

# Connection status
is_connected = False
manual_control_1 = False
manual_control_2 = False

@blynk.ON("connected")
def blynk_connected(ping):
    global is_connected
    is_connected = True
    logging.info('Blynk connected with ping: %d ms' % ping)

@blynk.ON("disconnected") 
def blynk_disconnected():
    global is_connected
    is_connected = False
    logging.warning('Blynk disconnected')

# Add position tracking
servo1_position = 0  # Track current angle
servo2_position = 0

@blynk.VIRTUAL_WRITE(1)
def v1_write_handler(value):
    global manual_control_1, servo1_position
    if value[0] == '1' and servo1_position != 90:  # Only move if not already at 90
        manual_control_1 = True
        servo1_position = 90
        set_servo_angle(gpio_manager.servo_1, 90)
        gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, gpio_manager.GPIO.HIGH)
    elif value[0] == '0' and servo1_position != 0:  # Only move if not already at 0
        manual_control_1 = False
        servo1_position = 0
        set_servo_angle(gpio_manager.servo_1, 0)
        gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, gpio_manager.GPIO.LOW)

@blynk.VIRTUAL_WRITE(2)
def v2_write_handler(value):
    global manual_control_2, servo2_position
    if value[0] == '1' and servo2_position != 90:
        manual_control_2 = True
        servo2_position = 90
        set_servo_angle(gpio_manager.servo_2, 90)
        gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, gpio_manager.GPIO.HIGH)
    elif value[0] == '0' and servo2_position != 0:
        manual_control_2 = False
        servo2_position = 0
        set_servo_angle(gpio_manager.servo_2, 0)
        gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, gpio_manager.GPIO.LOW)

def set_servo_angle(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo.ChangeDutyCycle(0)  # Prevents jitter

def blynk_thread():
    while True:
        try:
            blynk.run()
            if not is_connected:
                # Run automatic control
                pass
            time.sleep(0.1)
        except Exception as e:
            logging.error(f"Blynk error: {e}")
            time.sleep(1)  # Wait before retry

if __name__ == "__main__":
    try:
        logging.info('Starting Blynk client...')
        blynk_thread()
    except KeyboardInterrupt:
        logging.info('Stopping Blynk client...')
    finally:
        gpio_manager.cleanup()