import threading
import signal
import sys
import adafruit_integration as adafruit_integration
import blynk_tst as blynk_tst
import email_notifier as email_notifier
import ultrasonic_servo as ultrasonic_servo
import data_generate as data_generate  # Add this import
from gpio_config import gpio_manager
import time
import ai_integration

def signal_handler(sig, frame):
    print("\nCleaning up...")
    gpio_manager.cleanup()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start threads
    threads = [
        threading.Thread(target=ultrasonic_servo.main, daemon=True),
        threading.Thread(target=blynk_tst.blynk_thread, daemon=True),
        threading.Thread(target=email_notifier.notify_via_email, daemon=True),
        threading.Thread(target=adafruit_integration.main, daemon=True),
        threading.Thread(target=data_generate.generate_dummy_data, daemon=True)
    ]
    
    for thread in threads:
        thread.start()

    print("All systems initialized and running...")

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()