import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SWITCH_PIN = 14 
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(SWITCH_PIN) == GPIO.LOW:
            print("Switch is closed (connected to Ground)")
        else:
            print("Switch is open (no connection)")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Stopped monitoring.")
finally:
    GPIO.cleanup()

