import RPi.GPIO as GPIO
import time

class GPIOManager:
    def __init__(self):
        self.GPIO = GPIO
        GPIO.setmode(GPIO.BCM)
        
        # Pin definitions
        self.GPIO_TRIGGER_1 = 18
        self.GPIO_ECHO_1 = 24
        self.GPIO_SERVO_1 = 25
        self.GPIO_LED_1 = 23

        self.GPIO_TRIGGER_2 = 22
        self.GPIO_ECHO_2 = 27
        self.GPIO_SERVO_2 = 17
        self.GPIO_LED_2 = 4

        # Setup GPIO
        self._setup_gpio()
        
        # Initialize servos
        self.servo_1 = None
        self.servo_2 = None
        self._setup_servos()

    def _setup_gpio(self):
        GPIO.setup(self.GPIO_TRIGGER_1, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_1, GPIO.IN)
        GPIO.setup(self.GPIO_SERVO_1, GPIO.OUT)
        GPIO.setup(self.GPIO_LED_1, GPIO.OUT)

        GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)
        GPIO.setup(self.GPIO_SERVO_2, GPIO.OUT)
        GPIO.setup(self.GPIO_LED_2, GPIO.OUT)

    def _setup_servos(self):
        self.servo_1 = GPIO.PWM(self.GPIO_SERVO_1, 50)
        self.servo_2 = GPIO.PWM(self.GPIO_SERVO_2, 50)
        self.servo_1.start(0)
        self.servo_2.start(0)

    def cleanup(self):
        if self.servo_1:
            self.servo_1.stop()
        if self.servo_2:
            self.servo_2.stop()
        GPIO.cleanup()

# Create singleton instance
gpio_manager = GPIOManager()