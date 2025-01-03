import time
import logging
import BlynkLib
import RPi.GPIO as GPIO
from gpio_config import gpio_manager

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Read Blynk auth token
with open("/home/iot/Documents/blynk_key.txt", "r") as file:
    BLYNK_AUTH = file.readline().strip()

# Initialize Blynk
BLYNK_SERVER = "blynk.cloud"
BLYNK_PORT = 80
blynk = BlynkLib.Blynk(BLYNK_AUTH, server=BLYNK_SERVER, port=BLYNK_PORT, heartbeat=30)

# State tracking
is_connected = False
manual_control_1 = False
manual_control_2 = False
servo1_position = 0
servo2_position = 0

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

@blynk.VIRTUAL_WRITE(1)
def v1_write_handler(value):
    global manual_control_1, servo1_position
    
    if value[0] == '1':  # ON pressed
        if not manual_control_1:
            manual_control_1 = True
            servo1_position = 90
            set_servo_angle(gpio_manager.servo_1, 90)
            gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, GPIO.HIGH)
            logging.info("Servo1 moved to 90 degrees")
    elif value[0] == '0':  # OFF pressed
        if manual_control_1:
            manual_control_1 = False
            servo1_position = 0
            set_servo_angle(gpio_manager.servo_1, 0)
            gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, GPIO.LOW)
            logging.info("Servo1 moved to 0 degrees")

@blynk.VIRTUAL_WRITE(2)
def v2_write_handler(value):
    global manual_control_2, servo2_position
    
    if value[0] == '1':  # ON pressed
        if not manual_control_2:
            manual_control_2 = True
            servo2_position = 90
            set_servo_angle(gpio_manager.servo_2, 90)
            gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, GPIO.HIGH)
            logging.info("Servo2 moved to 90 degrees")
    elif value[0] == '0':  # OFF pressed
        if manual_control_2:
            manual_control_2 = False
            servo2_position = 0
            set_servo_angle(gpio_manager.servo_2, 0)
            gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, GPIO.LOW)
            logging.info("Servo2 moved to 0 degrees")

def set_servo_angle(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)
    # Removed servo.ChangeDutyCycle(0) to maintain servo position
    # If needed, consider keeping the duty cycle active to hold position

def blynk_thread():
    while True:
        try:
            blynk.run()
            time.sleep(0.1)
        except Exception as e:
            logging.error(f"Blynk error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        logging.info('Starting Blynk client...')
        blynk_thread()
    except KeyboardInterrupt:
        logging.info('Stopping Blynk client...')
    finally:
        gpio_manager.cleanup()