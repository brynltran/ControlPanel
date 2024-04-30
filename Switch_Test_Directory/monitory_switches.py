import RPi.GPIO as GPIO
import time

class GPIO_Switch:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        if pin != 4:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    def get_state(self):
        return GPIO.input(self.pin) == GPIO.LOW

def monitor_switches(switches):
    try:
        while True:
            for switch in switches:
                if switch.get_state():
                    print(f"Switch {switch.pin} is ON (open)")
                else:
                    print(f"Switch {switch.pin} is OFF (closed)")
            time.sleep(0.5)  # Debounce time to avoid flickering effects
    except KeyboardInterrupt:
        print("Stopped monitoring.")
    finally:
        GPIO.cleanup()  # Clean up GPIO on normal exit

if __name__ == '__main__':
    # Initialize switches
    burn_wire_switch = GPIO_Switch(4)
    linear_actuator_switch = GPIO_Switch(11)
    solenoid_switch = GPIO_Switch(14)

    # List of switches
    switches = [burn_wire_switch, linear_actuator_switch, solenoid_switch]

    print("Monitoring switches... Press CTRL+C to exit.")
    monitor_switches(switches)

