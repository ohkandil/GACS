import time
import zmq
import blynklib
from gpio_config import gpio_manager

# Read Blynk auth token
with open("/home/iot/Documents/blynk_key.txt", "r") as file:
    BLYNK_AUTH = file.readline().strip()

blynk = blynklib.Blynk(BLYNK_AUTH)

# Virtual Pins for Blynk buttons
VIRTUAL_PIN_SERVO_1 = 1
VIRTUAL_PIN_SERVO_2 = 2

# Flags to control manual override
manual_control_1 = False
manual_control_2 = False

# Set up ZeroMQ
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.subscribe("")

def distance(trigger, echo, num_samples=3):
    distances = []
    for _ in range(num_samples):
        gpio_manager.GPIO.output(trigger, True)
        time.sleep(0.00001)
        gpio_manager.GPIO.output(trigger, False)

        StartTime = time.time()
        StopTime = time.time()

        while gpio_manager.GPIO.input(echo) == 0:
            StartTime = time.time()

        while gpio_manager.GPIO.input(echo) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        distances.append(distance)
        time.sleep(0.005)

    return sum(distances) / len(distances)

def set_servo_angle(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo.ChangeDutyCycle(0)

@blynk.handle_event(f'write V{VIRTUAL_PIN_SERVO_1}')
def control_servo_1(pin, value):
    global manual_control_1
    try:
        if int(value[0]) == 1:
            manual_control_1 = True
            set_servo_angle(gpio_manager.servo_1, 90)
            gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, gpio_manager.GPIO.HIGH)
            print("Manual control ON for Servo 1")
        else:
            manual_control_1 = False
            set_servo_angle(gpio_manager.servo_1, 0)
            gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, gpio_manager.GPIO.LOW)
            print("Manual control OFF for Servo 1")
    except Exception as e:
        print(f"Error in control_servo_1: {e}")

@blynk.handle_event(f'write V{VIRTUAL_PIN_SERVO_2}')
def control_servo_2(pin, value):
    global manual_control_2
    try:
        if int(value[0]) == 1:
            manual_control_2 = True
            set_servo_angle(gpio_manager.servo_2, 90)
            gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, gpio_manager.GPIO.HIGH)
            print("Manual control ON for Servo 2")
        else:
            manual_control_2 = False
            set_servo_angle(gpio_manager.servo_2, 0)
            gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, gpio_manager.GPIO.LOW)
            print("Manual control OFF for Servo 2")
    except Exception as e:
        print(f"Error in control_servo_2: {e}")

def blynk_thread():
    try:
        while True:
            blynk.run()
            if not manual_control_1:
                dist_1 = distance(gpio_manager.GPIO_TRIGGER_1, gpio_manager.GPIO_ECHO_1)
                if dist_1 <= 10:
                    set_servo_angle(gpio_manager.servo_1, 90)
                    gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, gpio_manager.GPIO.HIGH)
                else:
                    set_servo_angle(gpio_manager.servo_1, 0)
                    gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, gpio_manager.GPIO.LOW)

            if not manual_control_2:
                dist_2 = distance(gpio_manager.GPIO_TRIGGER_2, gpio_manager.GPIO_ECHO_2)
                if dist_2 <= 10:
                    set_servo_angle(gpio_manager.servo_2, 90)
                    gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, gpio_manager.GPIO.HIGH)
                else:
                    set_servo_angle(gpio_manager.servo_2, 0)
                    gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, gpio_manager.GPIO.LOW)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Blynk thread stopped by User")