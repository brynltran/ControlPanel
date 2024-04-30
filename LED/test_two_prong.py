import RPi.GPIO as GPIO
import time

class SwitchWithLED:
    def __init__(self, switch_pin, green_led_pin, red_led_pin):
        self.switch_pin = switch_pin
        self.green_led_pin = green_led_pin
        self.red_led_pin = red_led_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.green_led_pin, GPIO.OUT)
        GPIO.setup(self.red_led_pin, GPIO.OUT)

        GPIO.output(self.green_led_pin, GPIO.LOW)
        GPIO.output(self.red_led_pin, GPIO.LOW)

    def update_leds_based_on_switch(self):
        if GPIO.input(self.switch_pin) == GPIO.LOW:
            GPIO.output(self.green_led_pin, GPIO.HIGH)  # Switch closed, turn green LED on
            GPIO.output(self.red_led_pin, GPIO.LOW)
        else:
            GPIO.output(self.green_led_pin, GPIO.LOW)
            GPIO.output(self.red_led_pin, GPIO.HIGH)  # Switch open, turn red LED on

    def clean_up(self):
        GPIO.cleanup()  # Clean up GPIO on normal exit

def monitor_switch_and_leds(switches):
    try:
        while True:
            for sw in switches:
                sw.update_leds_based_on_switch()
            time.sleep(0.1)  # Short sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Stopped monitoring.")
        for sw in switches:
            sw.clean_up()

if __name__ == '__main__':
    # Initialize switches and LEDs
    switches = [
        SwitchWithLED(4, 5, 6),   # Burn wire switch with green LED on GPIO 5, red on 6
        SwitchWithLED(11, 17, 27), # Linear actuator switch
        SwitchWithLED(14, 19, 26)  # Solenoid switch with green LED on GPIO 22, red on 23
    ]
    
    print("Monitoring switches and controlling LEDs... Press CTRL+C to exit.")
    monitor_switch_and_leds(switches)

