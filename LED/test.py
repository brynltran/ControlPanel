import RPi.GPIO as GPIO
import time

class SwitchWithLED:
    def __init__(self, position_pins, led_pins):
        self.position_pins = position_pins  # GPIO pins for Load A, Neutral, Load B
        self.led_pins = led_pins  # Red, Blue, Green LEDs
        GPIO.setmode(GPIO.BCM)
        
        for pin in self.position_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def update_leds_based_on_switch(self):
        load_a_active = GPIO.input(self.position_pins[0]) == GPIO.LOW
        load_b_active = GPIO.input(self.position_pins[2]) == GPIO.LOW
        neutral_active = not load_a_active and not load_b_active

        # Debug outputs for switch positions
        print(f"Load A active: {load_a_active}")
        print(f"Neutral active: {neutral_active}")
        print(f"Load B active: {load_b_active}")

        # Update Red LED for Load A
        if load_a_active:
            GPIO.output(self.led_pins[0], GPIO.HIGH)
            print("Red LED on")
        else:
            GPIO.output(self.led_pins[0], GPIO.LOW)
            print("Red LED off")

        # Update Green LED for Load B
        if load_b_active:
            GPIO.output(self.led_pins[2], GPIO.HIGH)
            print("Green LED on")
        else:
            GPIO.output(self.led_pins[2], GPIO.LOW)
            print("Green LED off")

        # Update Blue LED for Neutral
        if neutral_active:
            GPIO.output(self.led_pins[1], GPIO.HIGH)
            print("Blue LED on")
        else:
            GPIO.output(self.led_pins[1], GPIO.LOW)
            print("Blue LED off")

    def clean_up(self):
        GPIO.cleanup()

class limitswitch():
    def __init__(self, initial_state, red, green):
        self.state = initial_state
        self.red = red
        self.green = green

        # Setup the GPIO pins for the LEDs
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        self.update()  # Update the LEDs based on the initial state

    def set_state(self, state):
        self.state = state
        self.update()

    def update(self):
        if self.state:
            GPIO.output(self.red, GPIO.HIGH)
            GPIO.output(self.green, GPIO.LOW)
        else:
            GPIO.output(self.green, GPIO.HIGH)
            GPIO.output(self.red, GPIO.LOW)
 
def monitor_switch_and_leds(switch):
    launchConfirm = limitswitch(False, 24, 23)
    DampConfirm  = limitswitch(False, 14, 15)
    try:
        while True:
            switch.update_leds_based_on_switch()
            time.sleep(0.1)  # Reduce CPU usage with a small sleep
    except KeyboardInterrupt:
        print("Stopped monitoring.")
        switch.clean_up()

if __name__ == '__main__':
    switch = SwitchWithLED(
        position_pins=[8, 7, 1],  # Pins for Load A, Neutral, Load B
        led_pins=[21, 20, 16]     # Red, Blue, Green LEDs
    )
    print("Monitoring switch and controlling LEDs... Press CTRL+C to exit.")
    monitor_switch_and_leds(switch)

