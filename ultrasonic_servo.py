import time
import zmq
from gpio_config import gpio_manager

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

def main():
    # Set up ZMQ publisher
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    try:
        # Initial servo positions
        set_servo_angle(gpio_manager.servo_1, 0)
        set_servo_angle(gpio_manager.servo_2, 0)
        time.sleep(1)

        while True:
            dist_1 = distance(gpio_manager.GPIO_TRIGGER_1, gpio_manager.GPIO_ECHO_1)
            if dist_1 <= 10:
                print(f"Object detected by Sensor 1: {dist_1:.1f} cm")
                set_servo_angle(gpio_manager.servo_1, 90)
                gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, gpio_manager.GPIO.HIGH)
            else:
                set_servo_angle(gpio_manager.servo_1, 0)
                gpio_manager.GPIO.output(gpio_manager.GPIO_LED_1, gpio_manager.GPIO.LOW)

            dist_2 = distance(gpio_manager.GPIO_TRIGGER_2, gpio_manager.GPIO_ECHO_2)
            if dist_2 <= 10:
                print(f"Object detected by Sensor 2: {dist_2:.1f} cm")
                set_servo_angle(gpio_manager.servo_2, 90)
                gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, gpio_manager.GPIO.HIGH)
            else:
                set_servo_angle(gpio_manager.servo_2, 0)
                gpio_manager.GPIO.output(gpio_manager.GPIO_LED_2, gpio_manager.GPIO.LOW)

            # Publish sensor data
            # Publish sensor data
            data = {}
            if dist_1 <= 10:
                data["sensor_1"] = round(dist_1, 2)
            if dist_2 <= 10:
                data["sensor_2"] = round(dist_2, 2)

            if data:  # Only send if we have triggered sensors
                socket.send_json(data)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")

if __name__ == '__main__':
    main()