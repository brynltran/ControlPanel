import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
SWITCH_PIN = 4  # Connected to the switch and to Ground through the switch

GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def monitor_switch():
    try:
        while True:
            if GPIO.input(SWITCH_PIN) == GPIO.LOW:
                print("Switch is OFF (closed)")
            else:
                print("Switch is ON (open)")
            time.sleep(0.5)  # Debounce time to avoid flickering effects
    except KeyboardInterrupt:
        print("Stopped monitoring.")
    finally:
        GPIO.cleanup()  # Clean up GPIO on normal exit

if __name__ == '__main__':
    print("Monitoring switch... Press CTRL+C to exit.")
    monitor_switch()

